from pathlib import Path
from collections import Counter, defaultdict
import csv, hashlib, json, re

ROOT = Path('D:/drive/Investment')
OUT = ROOT/'备份/流程审计与研究方案改进_2026-09-05'
def writecsv(name, rows):
    rows=list(rows)
    if not rows: return
    with (OUT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def clean(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
    return re.sub(r'<br\s*/?>',' ',s).replace('**','').replace('`','').strip()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def linehits(lines, expression, limit=None):
    return ' | '.join(f'{i}: {l}' for i,l in enumerate(lines,1) if (limit is None or i<=limit) and re.search(expression,l))

inventory=[];selected={}
for domain,folder,part in [('decision','公司情景投资决策','经营情景市场状态投资决策'),('comparison','公司对比','逐家公司投资思路对比')]:
    candidates=defaultdict(list)
    for p in (ROOT/'分析报告'/folder/'结果').glob('*.md'):
        m=re.match(r'^([A-Z0-9.-]+)_'+part+r'_(\d{4}-\d{2}-\d{2})\.md$',p.name)
        if m: candidates[m[1]].append((m[2],p))
    selected[domain]={t:max(ps,key=lambda z:z[0]) for t,ps in candidates.items()}
    for ticker,(date,p) in sorted(selected[domain].items()):
        text=p.read_text(encoding='utf-8-sig');lines=text.splitlines()
        inventory.append(dict(domain=domain,ticker=ticker,report_date=date,source_path=str(p),sha256=digest(p),lines=len(lines),characters=len(text),mentions_old_evaluation='公司评估' in text,mentions_scenario='公司情景投资决策' in text,date_evidence=linehits(lines,r'研究截止|价格截止|生成日期|研究日期|资料截止|主投资期限|主分析期|研究时点|主判断期',70)))
writecsv('decisions_current_report_inventory.csv',inventory)

manifest=json.loads((ROOT/'tools/research-runner/company-investment-decision.batches.json').read_text(encoding='utf-8-sig'))
batchrows=[]
for batch in manifest['batches']:
    snap=ROOT/batch['snapshotFile'];snaptext=snap.read_text(encoding='utf-8-sig')
    snapid=re.search(r'\|\s*市场快照身份[^|]*\|\s*`?([^|`]+)',snaptext)
    if not snapid: snapid=re.search(r'\|\s*快照身份[^|]*\|\s*`?([^|`]+)',snaptext)
    # These are the actual identity strings of the sole live batch; exact text presence is audited, not semantic quality.
    knownid='US-EQ-USD-20260818-CLOSE-5B-v1.0'
    priceanchor='金融资料/每日金融数据/每日金融数据_2026-08-18.md'
    for ticker in batch['subjects']:
        date,p=selected['decision'][ticker];txt=p.read_text(encoding='utf-8-sig');lines=txt.splitlines()
        batchrows.append(dict(ticker=ticker,batch_id=batch['batchId'],source_date=batch['sourceDate'],report_date=date,snapshot_hash_ok=digest(snap).upper()==batch['sha256'].upper(),batch_id_echo=batch['batchId'] in txt,snapshot_path_echo=batch['snapshotFile'] in txt,sha256_echo=batch['sha256'].lower() in txt.lower(),snapshot_id_echo=knownid in txt,price_anchor_echo=priceanchor in txt,main_state_echo='宽基风险扩张' in txt,neighbor_echo=bool(re.search(r'震荡\s*[/／]\s*均值回归',txt)),source_path=str(p),identity_evidence=linehits(lines,r'批次|SHA|快照身份|快照 ID|snapshot|价格.*锚|锚定.*时|宽基风险扩张|唯一相邻|价格.*时间',80)))
writecsv('decisions_current_batch_echo.csv',batchrows)

dimensions=['near','long','odds','defense','explosion','mispricing','overall']
def outcome(raw,a,b):
    text=clean(raw)
    if re.match('接近|难分|大致平衡|基本平衡',text): return ('close','','')
    if re.match('资料不足|信息不足|无法判断|不可判断',text): return ('unavailable','','')
    m=re.match(r'^([A-Z0-9.-]+)\s*(?=明显更优|略优|更优|：|:|（|\(|$)',text)
    winner=m[1] if m else ''
    if winner=='A': winner=a
    if winner=='B': winner=b
    if winner=='PSTG': winner='P'
    if winner=='AGC': winner='ASGLY'  # Company name alias, verified in VIAV vs ASGLY source row.
    conf=re.search(r'([高中低])置信',text)
    return ('winner' if winner in [a,b] else 'invalid',winner,conf[1] if conf else '')
directed=[];rowcounts=[];warnings=[]
for ticker,(date,p) in sorted(selected['comparison'].items()):
    txt=p.read_text(encoding='utf-8-sig');parsed=[]
    for i,line in enumerate(txt.splitlines(),1):
        if not re.match(r'^\|\s*\d+\s*\|',line.strip()): continue
        cells=[x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
        if len(cells)!=12: continue
        m=re.match(r'^([A-Z][A-Z0-9.-]*)',clean(cells[1]))
        if not m: continue
        b='P' if m[1]=='PSTG' else m[1]
        row=dict(ticker=ticker,opponent=b,report_date=date,source_path=str(p),source_line=i,reason=clean(cells[11]))
        for k,raw in zip(dimensions,cells[4:11]):
            status,winner,conf=outcome(raw,ticker,b)
            row[k+'_status']=status;row[k+'_winner']=winner;row[k+'_confidence']=conf;row[k+'_text']=clean(raw)
            if status=='invalid':warnings.append(dict(ticker=ticker,opponent=b,dimension=k,text=raw,source_line=i,source_path=str(p)))
        parsed.append(row)
    directed+=parsed
    rowcounts.append(dict(ticker=ticker,report_date=date,rows=len(parsed),unique_opponents=len({r['opponent'] for r in parsed}),source_path=str(p)))
writecsv('decisions_current_comparison_rows.csv',directed)
writecsv('decisions_current_comparison_coverage.csv',rowcounts)
writecsv('decisions_current_comparison_warnings.csv',warnings)
pairmap={(r['ticker'],r['opponent']):r for r in directed}
recips=defaultdict(Counter);conflicts=[]
for i,a in enumerate(sorted(selected['comparison'])):
    for b in sorted(selected['comparison'])[i+1:]:
        x,y=pairmap.get((a,b)),pairmap.get((b,a))
        if not x or not y: continue
        cohort='same_date_'+x['report_date'] if x['report_date']==y['report_date'] else 'different_dates'
        for d in dimensions:
            sx,sy=x[d+'_status'],y[d+'_status'];wx,wy=x[d+'_winner'],y[d+'_winner']
            if 'unavailable' in [sx,sy] or 'invalid' in [sx,sy]: status='unavailable'
            elif sx==sy=='close':status='bothClose'
            elif 'close' in [sx,sy]:status='oneDecisiveOneClose'
            elif wx==wy:status='sameWinner'
            elif wx==a and wy==b:status='eachSelf'
            else:status='eachOther'
            recips[(cohort,d)][status]+=1;recips[('all',d)][status]+=1
            if status in ['eachSelf','eachOther']:
                conflicts.append(dict(cohort=cohort,ticker_a=a,ticker_b=b,dimension=d,status=status,a_text=x[d+'_text'],b_text=y[d+'_text'],a_source=x['source_path'],a_line=x['source_line'],b_source=y['source_path'],b_line=y['source_line']))
writecsv('decisions_current_reciprocal_summary.csv',[dict(cohort=c,dimension=d,pairs=sum(v.values()),**{k:v[k] for k in ['sameWinner','eachSelf','eachOther','bothClose','oneDecisiveOneClose','unavailable']}) for (c,d),v in sorted(recips.items())])
writecsv('decisions_current_reciprocal_conflicts.csv',conflicts)
summary=dict(
    report_counts={d:dict(Counter(r['report_date'] for r in inventory if r['domain']==d)) for d in selected},
    post_merger_reports={d:sum(r['report_date']>='2026-09-01' for r in inventory if r['domain']==d) for d in selected},
    old_evaluation_mentions={d:sum(r['mentions_old_evaluation'] for r in inventory if r['domain']==d) for d in selected},
    scenario_mentions={d:sum(r['mentions_scenario'] for r in inventory if r['domain']==d) for d in selected},
    batch_count=len(manifest['batches']),batch_subject_count=len(batchrows),
    batch_echo_counts={k:sum(r[k] for r in batchrows) for k in ['snapshot_hash_ok','batch_id_echo','snapshot_path_echo','sha256_echo','snapshot_id_echo','price_anchor_echo','main_state_echo','neighbor_echo']},
    comparison_rows=len(directed),comparison_parse_warnings=len(warnings),
    comparison_row_distribution=dict(Counter(r['rows'] for r in rowcounts)),
    comparison_confidence_distribution={d:dict(Counter(r[d+'_confidence'] for r in directed)) for d in dimensions},
    reciprocal=[dict(cohort=c,dimension=d,pairs=sum(v.values()),**dict(v)) for (c,d),v in sorted(recips.items())])
(OUT/'data/decisions_current_audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='reciprocal'},ensure_ascii=False,indent=2))
print(json.dumps([r for r in summary['reciprocal'] if r['dimension']=='overall'],ensure_ascii=False,indent=2))

