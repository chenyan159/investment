from pathlib import Path
import re,csv,json,hashlib,collections
ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/项目反思_2026-09-04'
for d in ['data','evidence']: (OUT/d).mkdir(parents=True,exist_ok=True)
index=(ROOT/'基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig')
entries=re.findall(r'^\| ([A-Z0-9.\-]+) \| (.*?) \| `([^`]+)/` \|',index,re.M)
cutoff='2026-07-15'
rows=[]
for ticker,name,category in entries:
    paths=[]
    for p in (ROOT/'基本面/公司调研'/category).rglob('*.md'):
        m=re.search(r'_公司调研_(\d{4}-\d{2}-\d{2})\.md$',p.name)
        if m and p.name.split('_')[0]==ticker:
            paths.append((m.group(1),p))
    eligible=sorted([(d,p) for d,p in paths if d<=cutoff],key=lambda x:(x[0],-len(str(x[1]))))
    if not eligible:
        rows.append(dict(ticker=ticker,name=name,category=category,status='no dated company source by cutoff'));continue
    date,p=eligible[-1]
    text=p.read_text(encoding='utf-8-sig')
    def match(pattern):
        hits=[(i,line) for i,line in enumerate(text.splitlines(),1) if re.search(pattern,line,re.I)]
        return hits
    row=dict(ticker=ticker,name=name,category=category,status='found',report_date=date,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),lines=len(text.splitlines()),chars=len(text),num_url=len(re.findall(r'https?://',text)))
    patterns={'three_upside_scenarios':r'基准.{0,15}乐观.{0,15}(?:极度|极)乐观','bear_terms':r'悲观|下行情景|压力情景','dilution_terms':r'稀释|摊薄|SBC|股权激励|每股','quarter_horizon_terms':r'0[—–\-～~至]3|3[—–\-～~至]6\s*个?月|未来三个月|未来六个月|未来3个月|未来6个月','order_unknown_terms':r'(?:取消率|backlog|积压|订单|产能).{0,40}(?:未披露|无法|不能|不披露|估算|假设)|(?:未披露|不披露|估算|假设).{0,40}(?:取消率|backlog|积压|订单|产能)','ai_skip_terms':r'跳过|不展开|略过|低相关|非AI|非 AI','expectation_terms':r'一致预期|预期差|consensus','macro_terms':r'通胀|战争|伊朗|联储|美联储|利率|油价|地缘|关税'}
    for k,v in patterns.items():
        hits=match(v);row[k+'_hits']=len(hits);row[k+'_lines']=';'.join(str(i) for i,_ in hits)
    rows.append(row)
with (OUT/'data/upstream_company_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
# Two companies per indexed category, alphabetically first and last: deterministic stratified diagnostic sample, not random population inference.
groups=collections.defaultdict(list)
for r in rows: groups[r['category']].append(r)
sample=[]
for category,rr in groups.items():
    rr.sort(key=lambda r:r['ticker']);sample += [rr[0],rr[-1]]
(OUT/'data/upstream_sample_design.json').write_text(json.dumps({'cutoff':cutoff,'rule':'For each of 10 index categories select alphabetically first and last ticker (20); purposive audit additions separate; nonrandom sample does not estimate population prevalence. Text-hit counters are discovery aids only and do not measure factual omission.','sample':sample},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'n':len(rows),'status':dict(collections.Counter(r['status'] for r in rows)),'dates':dict(collections.Counter(r.get('report_date','none') for r in rows)),'sample':[r['ticker'] for r in sample]},ensure_ascii=False))
