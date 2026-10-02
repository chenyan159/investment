from pathlib import Path
from collections import Counter, defaultdict
import ast, csv, hashlib, json, re
import pandas as pd
import numpy as np

ROOT=Path('D:/drive/Investment'); OUT=ROOT/'备份/项目反思_2026-09-04'
RR=ROOT/'分析报告/公司排序'; CR=ROOT/'分析报告/公司对比'
OLD=RR/'90_有效性评估/2026-07-13_26方案3月6月生成前历史回看'

def writecsv(name, rows):
    rows=list(rows)
    if not rows: return
    with (OUT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# Load only explicitly selected pure parsing functions/constants from the archived evaluator.
source=(OLD/'10_评估脚本快照.py').read_text(encoding='utf-8')
tree=ast.parse(source)
names={'split_md_row','norm_header','clean_cell','is_separator','selector_match','parse_rank_rows'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=='SELECTORS' or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='METHOD06_LISTS' for t in n.targets)]
env={'re':re,'pd':pd,'np':np,'Path':Path}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<selected read-only parsers>','exec'),env)
registry=pd.read_csv(RR/'00_运行与榜单注册表.csv',dtype=str).to_dict('records')
old=pd.read_csv(OLD/'02_28张榜全部名次.csv',dtype={'method_id':str,'list_id':str})
rankrows=[]; audit=[]; planextract=[]
for item in registry:
    method,lid=item['method_id'],item['list_id']; path=RR/item['result_path']
    selectors=[(env['METHOD06_LISTS'][lid],None)] if method=='06' else env['SELECTORS'][method]
    frame,notes=env['parse_rank_rows'](path,selectors)
    prev=old[old.list_id==lid].set_index('ticker')
    mismatch=sum(int(int(prev.loc[r.ticker,'rank'])!=r['rank']) for _,r in frame.iterrows())
    txt=path.read_text(encoding='utf-8'); lines=txt.splitlines()
    date_lines=[f'{i}: {l}' for i,l in enumerate(lines,1) if i<65 and re.search('截止|执行日|生成日|运行日|资料时点|研究时点',l)]
    audit.append(dict(method_id=method,list_id=lid,run_date=item['run_date'],rows=len(frame),unique_tickers=frame.ticker.nunique(),normalized_mismatches=mismatch,parse_notes=';'.join(notes),source_path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),date_evidence=' | '.join(date_lines)))
    for _,r in frame.iterrows():
        rankrows.append(dict(method_id=method,list_id=lid,method_name=item['method_name'],list_name=item['list_name'],run_date=item['run_date'],ticker=r.ticker,rank=int(r['rank']),score=r.score,source_path=str(path),source_line=int(r.line),lifecycle=item['lifecycle'],status=item['status'],plan_path=str(RR/item['plan_path'])))
    if method!='06' or lid=='06F':
        for typ,p in [('plan',RR/item['plan_path']),('result',path)]:
            for i,l in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
                if re.search(r'个月|季度|3年|5年|一年|未来|只能读取|不得读取|公司调研|行业调研|复权|全部.*中性|全样本.*0|均.*0|未确认|关键词|词频|词语|命中|映射|固定计分',l):
                    planextract.append(dict(method_id=method,kind=typ,source_path=str(p),source_line=i,text=l))
writecsv('historical_rankings.csv',rankrows); writecsv('historical_rankings_source_audit.csv',audit); writecsv('ranking_plan_evidence_extract.csv',planextract)

# Freeze comparison generation cohort at July 14, excluding July 18 updates.
pattern=re.compile(r'^([A-Z0-9.-]+)_逐家公司投资思路对比_(\d{4}-\d{2}-\d{2})\.md$')
candidates=defaultdict(list)
for path in (CR/'结果').rglob('*.md'):
    m=pattern.match(path.name)
    if m and m[2]<='2026-07-17': candidates[m[1]].append((m[2],path))
chosen={t:sorted(items,key=lambda x:(x[0], x[1].parent==CR/'结果', str(x[1].parent)),reverse=True)[0] for t,items in candidates.items()}
dimensions=['near','long','odds','defense','explosion','mispricing','overall']
directed=[]; manifest=[]; warnings=[]
def clean(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s)
    return re.sub(r'<br\s*/?>',' ',s).replace('**','').replace('`','').strip()
def outcome(raw,a,b):
    text=clean(raw)
    if re.match('接近|难分|大致平衡|基本平衡',text): return ('close','','',0)
    if re.match('资料不足|信息不足|无法判断|不可判断',text): return ('unavailable','','',0)
    m=re.match(r'^([A-Z0-9.-]+)\s*(?=明显更优|略优|更优|：|:|（|\(|$)',text)
    winner=m[1] if m else ''
    if winner=='A': winner=a
    if winner=='B': winner=b
    if winner=='PSTG': winner='P'
    conf=re.search(r'([高中低])置信',text)
    return ('winner' if winner in [a,b] else 'invalid',winner,conf[1] if conf else '',2 if '明显更优' in text else 1)
for ticker,(date,path) in sorted(chosen.items()):
    txt=path.read_text(encoding='utf-8'); parsed=[]
    datelines=[f'{i}: {l}' for i,l in enumerate(txt.splitlines(),1) if i<30 and re.search('研究截止|价格截止|生成日期',l)]
    for i,line in enumerate(txt.splitlines(),1):
        if not re.match(r'^\|\s*\d+\s*\|',line.strip()): continue
        cells=[x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
        if len(cells)!=12: continue
        m=re.match(r'^([A-Z][A-Z0-9.-]*)',clean(cells[1]))
        if not m: continue
        opponent='P' if m[1]=='PSTG' else m[1]
        row=dict(ticker=ticker,opponent=opponent,run_date=date,source_path=str(path),source_line=i,relation=clean(cells[3]),reason=clean(cells[11]))
        for k,raw in zip(dimensions,cells[4:11]):
            status,winner,conf,strength=outcome(raw,ticker,opponent)
            row[k+'_status']=status;row[k+'_winner']=winner;row[k+'_confidence']=conf;row[k+'_strength']=strength;row[k+'_text']=clean(raw)
            if status=='invalid': warnings.append(dict(ticker=ticker,opponent=opponent,dimension=k,text=raw,source_line=i,source_path=str(path)))
        parsed.append(row)
    assert len(parsed)==191,(ticker,len(parsed),path)
    assert len({r['opponent'] for r in parsed})==191,ticker
    directed+=parsed
    manifest.append(dict(ticker=ticker,run_date=date,price_date='2026-07-13',source_path=str(path),is_backup='备份' in path.parts,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),row_count=len(parsed),date_evidence=' | '.join(datelines),same_date_candidate_count=sum(d==date for d,p in candidates[ticker])))
assert len(chosen)==192,len(chosen)
writecsv('company_comparison_historical_sources.csv',manifest)
writecsv('company_comparison_historical_pairs.csv',directed)
if warnings: writecsv('company_comparison_parse_warnings.csv',warnings)
tickers=sorted(chosen); pairmap={(r['ticker'],r['opponent']):r for r in directed}
stats={d:{t:Counter(wins=0,losses=0,close=0,unavailable=0) for t in tickers} for d in dimensions}
recip={d:Counter(sameWinner=0,eachSelf=0,eachOther=0,bothClose=0,oneDecisiveOneClose=0,unavailable=0) for d in dimensions}
conflicts=[]
for row in directed:
    a,b=row['ticker'],row['opponent']
    for d in dimensions:
        status,w=row[d+'_status'],row[d+'_winner']
        if status=='winner': stats[d][w]['wins']+=1;stats[d][b if w==a else a]['losses']+=1
        else:
            for t in [a,b]: stats[d][t]['close' if status=='close' else 'unavailable']+=1
for i,a in enumerate(tickers):
    for b in tickers[i+1:]:
        x,y=pairmap[a,b],pairmap[b,a]
        for d in dimensions:
            sx,sy=x[d+'_status'],y[d+'_status'];wx,wy=x[d+'_winner'],y[d+'_winner']
            if 'unavailable' in [sx,sy] or 'invalid' in [sx,sy]: status='unavailable'
            elif sx==sy=='close': status='bothClose'
            elif 'close' in [sx,sy]: status='oneDecisiveOneClose'
            elif wx==wy: status='sameWinner'
            elif wx==a and wy==b: status='eachSelf'
            else: status='eachOther'
            recip[d][status]+=1
            if status in ['eachSelf','eachOther']:
                conflicts.append(dict(ticker_a=a,ticker_b=b,dimension=d,conflict=status,a_text=x[d+'_text'],b_text=y[d+'_text'],a_source=x['source_path'],a_line=x['source_line'],b_source=y['source_path'],b_line=y['source_line']))
ranks={}
for d in dimensions:
    for t,s in stats[d].items(): s['net']=s['wins']-s['losses']
    order=sorted(tickers,key=lambda t:(-stats[d][t]['net'],-stats[d][t]['wins'],stats[d][t]['losses'],t))
    ranks[d]={t:i+1 for i,t in enumerate(order)}
summary=[]
for t in tickers:
    row=dict(ticker=t,run_date=chosen[t][0],source_path=str(chosen[t][1]))
    for d in dimensions:
        row[d+'_rank']=ranks[d][t]
        for k,v in stats[d][t].items():row[d+'_'+k]=v
    summary.append(row)
writecsv('company_comparison_historical.csv',summary)
writecsv('company_comparison_reciprocal_conflicts.csv',conflicts)
writecsv('company_comparison_reciprocal_summary.csv',[dict(dimension=d,pairs=18336,**c) for d,c in recip.items()])
prior=pd.read_csv(ROOT/'备份/公司对比_排序_情景决策全量综合分析_2026-07-17/192家公司三类报告交叉指标明细_2026-07-17.csv').set_index('ticker')
diff=[]
for r in summary:
    for d in dimensions:
        p=int(prior.loc[r['ticker'],'comparison_'+d+'_rank'])
        if p!=r[d+'_rank']:diff.append(dict(ticker=r['ticker'],dimension=d,prior_rank=p,reconstructed_rank=r[d+'_rank']))
if diff:writecsv('company_comparison_july17_validation_diff.csv',diff)
frame=pd.DataFrame(summary)
correlation=frame[[d+'_rank' for d in dimensions]].corr(method='spearman')
correlation.to_csv(OUT/'data/company_comparison_dimension_correlation.csv',encoding='utf-8-sig')
result=dict(rank_lists=len(audit),rank_rows=len(rankrows),ranking_mismatches=sum(r['normalized_mismatches'] for r in audit),comparison_reports=len(chosen),comparison_directed_rows=len(directed),comparison_warnings=len(warnings),comparison_versus_july17_rank_differences=len(diff),comparison_dates=dict(Counter(d for d,p in chosen.values())),comparison_backup_count=sum(m['is_backup'] for m in manifest),reciprocal={d:dict(c) for d,c in recip.items()})
(OUT/'data/ranking_comparison_audit_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
