from pathlib import Path
import csv, re, json, hashlib, statistics, datetime
from collections import Counter

ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/项目反思_2026-09-04'
CUTOFF='2026-07-15'
def clean(s):
    return re.sub(r'[*`]', '', s).strip()
def getrows(text):
    return [(i,clean(line)) for i,line in enumerate(text.splitlines(),1)]
def hit(lines,pat,limit=None):
    return next(((i,s) for i,s in lines[:limit] if re.search(pat,s,re.I)), (None,''))
def field(lines,pat):
    return next(((i,s) for i,s in lines[:100] if s.startswith('|') and re.search(pat,s.split('|')[1].strip())),(None,''))
def value(line):
    parts=line.split('|')
    return parts[2].strip() if len(parts)>2 else line
def writecsv(name,rows):
    with (OUT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def scan(kind,folder,marker):
    docs=[]
    for p in (ROOT/folder).rglob('*.md'):
        m=re.match(r'^([A-Z0-9.\-]+)_.*'+marker+r'.*_(\d{4}-\d{2}-\d{2})\.md$',p.name)
        if not m: continue
        t=p.read_text(encoding='utf-8-sig');lines=getrows(t)
        docs.append({'ticker':m[1],'kind':kind,'filename_date':m[2],'path':str(p),'is_backup':'备份' in p.relative_to(ROOT/folder).parts,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'line_count':len(lines),'_text':t,'_lines':lines})
    selected={}
    for d in docs:
        if d['filename_date']>CUTOFF: continue
        prev=selected.get(d['ticker'])
        # Latest report date; for same filename date prefer current direct file, then latest archival snapshot.
        key=lambda x:(x['filename_date'],not x['is_backup'],x['path'])
        if prev is None or key(d)>key(prev): selected[d['ticker']]=d
    return docs,selected
sd,ss=scan('scenario','分析报告/公司情景投资决策','经营情景市场状态投资决策')
ed,es=scan('evaluation','分析报告/公司评估_淘汰','收入传导估值评估')
legacy_evaluation_tickers=sorted(set(es)-set(ss))
es={k:v for k,v in es.items() if k in ss} # PSTG survives only as historical alias; P is the selected current-universe company.
index=[]
for d in sd+ed:
    row={k:v for k,v in d.items() if not k.startswith('_')}
    row['selected_midjuly']=(ss if d['kind']=='scenario' else es).get(d['ticker']) is d
    index.append(row)
writecsv('decisions_document_index.csv', sorted(index,key=lambda d:(d['ticker'],d['kind'],d['filename_date'],d['path'])))

results=[]; cellrows=[]
rating_pattern=r'强烈不建议投资|谨慎不建议投资|不建议投资|强烈建议投资|谨慎建议投资|建议投资|中性\s*[/／]\s*等待|无法(?:可靠)?估值|不适合投资'
range_pattern=r'([+\-−]?\d+(?:\.\d+)?)\s*%\s*(?:～|〜|~|—|–|至|到|−|-)\s*(?:约\s*)?([+\-−]?\d+(?:\.\d+)?)\s*%'
for ticker in sorted(ss):
    d=ss.get(ticker);e=es.get(ticker)
    row={'ticker':ticker,'historical_cutoff':CUTOFF}
    if d:
        lines=d['_lines'];txt=d['_text'];n,summary=hit(lines,r'^>\s*当前条件定位\s*[：:]|^>.*当前证据最接近',120)
        if not summary:
            n,_=hit(lines,r'当前条件定位',100)
            summary=' '.join(s for i,s in lines if n and n<i<=n+8)
        pn,price=None,''
        for i,s in lines[:60]:
            if not s.startswith('|'): continue
            parts=s.split('|');label=parts[1].strip();v=parts[2].strip() if len(parts)>2 else ''
            if not re.search(r'股价|价格|收盘|ADR.*报价|可交易|冻结报价|^报价$',label):continue
            if re.search(r'日期|截止|来源|要求|隐含|信息|股数|市值|换算|资金|状态|风险|发现|证券',label):continue
            if not re.search(r'\$\s*\d|\d[\d,.]*\s*美元|(?<!\d)\d{1,4}[,.]\d{1,3}',v): continue
            pn,price=i,s;break
        if not price: pn,price=hit(lines,r'(?:冻结|当前|收盘|股价).{0,25}(?:\$\s*\d|\d[\d,.]*\s*美元)',60)
        hn,horizon=hit(lines,r'^[>\-].*(?:主投资期限|主投资期|主目标期|主期限|主投资窗口|主投资和估值期限)',50)
        if not horizon:hn,horizon=field(lines,r'主投资期限|投资期限|主期限|主投资窗口|主估值期限|主研究期限')
        if not horizon: hn,horizon=field(lines,r'主.*(?:窗口|时点|目标)|目标.*(?:日期|日|期限|期)|投资.*(?:期限|窗口)')
        if not horizon: hn,horizon=hit(lines,r'(?:主投资期限|主期限|目标日|主投资窗口|主目标|主判断期限|主估值期).{0,160}',100)
        dn,dated=field(lines,r'运行日期|信息截止|研究日期|报告日期')
        _,prob=hit(lines,r'概率层.{0,30}(?:NA|不提供|不启用)|^\*?概率.{0,15}NA',None)
        pnums=re.findall(r'\$\s*([\d,]+(?:\.\d+)?)',value(price))
        if not pnums: pnums=re.findall(r'([\d,]+(?:\.\d+)?)\s*美元',value(price))
        if not pnums: pnums=re.findall(r'收盘价\s*([\d,]+(?:\.\d+)?)',value(price))
        retmatch=re.search(r'(?:总回报|回报)[^%]{0,22}?'+range_pattern,summary)
        if not retmatch: retmatch=re.search(range_pattern,summary)
        rating=re.search(rating_pattern,summary)
        dates=re.findall(r'20\d\d-\d\d-\d\d',value(horizon))
        targetdate=next((x for x in dates if x>CUTOFF),'')
        months=re.search(r'(\d+(?:\.\d+)?)\s*个月',value(horizon))
        pos=hit(lines,r'当前证据最接近|当前.*最接近',100)[1]
        op=re.search(r'当前证据最接近\s*([^；;。]+)',pos)
        row.update({'scenario_path':d['path'],'scenario_report_date':d['filename_date'],'scenario_from_backup':d['is_backup'],'scenario_sha256':d['sha256'],'information_cutoff_line':dn,'information_cutoff_text':value(dated),'price_line':pn,'price_text':value(price),'price_usd_first':pnums[0].replace(',','') if pnums else '', 'horizon_line':hn,'horizon_text':value(horizon),'target_date':targetdate,'horizon_months_explicit':months[1] if months else '', 'summary_line':n,'summary_text':summary,'current_condition_rating_heuristic':rating[0] if rating else '', 'current_operating_position':op[1].strip() if op else '', 'current_condition_return_low_pct':retmatch[1].replace('−','-') if retmatch else '', 'current_condition_return_high_pct':retmatch[2].replace('−','-') if retmatch else '', 'probability_na_explicit':bool(prob),'probability_evidence':prob,'three_to_six_month_price_forecast':'Not extracted: primary declared horizon governs; no substitution','mentions_3_to_6_month':bool(re.search(r'3\s*[—–\-～/]\s*6\s*个?月',txt)),'no_overall_rating_language':bool(re.search(r'不给出.*总体投资评级|不形成.*总体投资评级|不给.*单一总体投资评级|不.*总体投资评级|不提供.*总体投资评级',txt))})
        # Reviewed exceptions preserve source quotes and lines, without rewriting any report.
        price_review={'MICLF':(15,'32.50','OTC stale quote, latest actual trade 2026-07-09; scenario uses MYCR 345.60 SEK instead'), 'SOMMY':(18,'16.84','ADR reference only; scenario total returns use ordinary share JPY548.7')}
        if ticker in price_review:
            pl,pv,note=price_review[ticker];row.update(price_line=pl,price_text=lines[pl-1][1],price_usd_first=pv,price_review_note=note)
        else:row['price_review_note']='Automated snapshot extraction; raw line is authoritative'
        horizon_review={'DTE':27,'EME':37,'VICR':32}
        if ticker in horizon_review:
            hl=horizon_review[ticker];row['horizon_line']=hl;row['horizon_text']=lines[hl-1][1]
        if ticker=='PSIX':row['horizon_months_explicit']=''
        # Summary's first recommendation can describe the superseded pure scenario or a sector adjustment.
        rating_review={'BDC':'中性 / 等待','CC':'中性 / 等待','FLNC':'不建议投资','IREN':'不建议投资','SMCI':'中性 / 等待','BABA':'中性 / 等待','COHR':'不建议投资','SKHY':'不建议投资'}
        row['current_condition_rating_reviewed']=rating_review.get(ticker,row['current_condition_rating_heuristic'])
        row['rating_review_note']='Manual correction: composite or sector override in quoted summary' if ticker in rating_review else 'Summary first rating; inspect summary for scope'
        if ticker in ['P','AEHR','ATKR','AXTI','SOMMY','ATEYY','PSIX','ORCL','PENG','MOD','WDC','VST','SMCI','DELL','MSFT']:
            row['rating_review_note']='Manually checked current primary condition against original summary; focus sample'
        dates=re.findall(r'20\d\d-\d\d-\d\d',row['horizon_text']);row['target_date']=max((x for x in dates if x>CUTOFF),default='')
        row['target_months_from_date']=round((datetime.date.fromisoformat(row['target_date'])-datetime.date.fromisoformat(CUTOFF)).days/30.4375,2) if row['target_date'] else ''
        # Parse first compact matrix, with recommendation and return interval in a single cell.
        matrix=[]
        for ln, s in lines:
            if not s.startswith('|'): continue
            parts=[x.strip() for x in s.split('|')[1:-1]]
            if len(parts)!=6 or not re.match(r'悲观|基准|乐观|突破',parts[0]): continue
            if not all(re.search(rating_pattern,x) or x=='NA｜NA｜NA' for x in parts[1:]): continue
            for col,cell in enumerate(parts[1:]):
                rr=re.search(range_pattern,cell);rat=re.search(rating_pattern,cell)
                matrix.append({'ticker':ticker,'path':d['path'],'line':ln,'operating_row':parts[0],'market_col_index':col,'market_col':['宽基风险扩张','窄幅主题主导上涨','震荡均值回归','有序风险收缩','流动性信用压力'][col],'rating':rat[0] if rat else '', 'return_low_pct':rr[1].replace('−','-') if rr else '', 'return_high_pct':rr[2].replace('−','-') if rr else '', 'cell_text':cell})
            if len(matrix)==20: break
        cellrows+=matrix
        row['matrix_cells_parsed']=len(matrix)
        row['matrix_numeric_ranges_parsed']=sum(c['return_low_pct']!='' for c in matrix)
    if e:
        row.update({'evaluation_path':e['path'],'evaluation_report_date':e['filename_date'],'evaluation_from_backup':e['is_backup'],'evaluation_sha256':e['sha256']})
        en,scope=hit(e['_lines'],r'(?:不提供|不给|不判断|不涉及|不输出).{0,50}(?:投资评级|股价区间|目标价)',50)
        row['evaluation_scope_line']=en;row['evaluation_scope_text']=scope
        en,anchor=hit(e['_lines'],r'(?:基准.*(?:NTM.*)?收入|NTM.*收入.*基准)',60)
        row['evaluation_baseline_revenue_line']=en;row['evaluation_baseline_revenue_text']=anchor
    results.append(row)
allfields=list(dict.fromkeys(k for r in results for k in r))
results=[{k:r.get(k,'') for k in allfields} for r in results]
writecsv('decisions_historical.csv',results)
if cellrows:writecsv('decisions_matrix_cells.csv',cellrows)
stats={'cutoff':CUTOFF,'all_documents':len(index),'scenario_documents':len(sd),'evaluation_documents':len(ed),'scenario_selected':len(ss),'evaluation_selected':len(es),'scenario_backup_selected':sum(d['is_backup'] for d in ss.values()),'evaluation_backup_selected':sum(d['is_backup'] for d in es.values()),'scenario_dates':dict(Counter(d['filename_date'] for d in ss.values())),'evaluation_dates':dict(Counter(d['filename_date'] for d in es.values())),'primary_horizons_explicit':dict(Counter(r['horizon_months_explicit'] for r in results)),'horizon_missing':[r['ticker'] for r in results if not r['horizon_text']],'summary_missing':[r['ticker'] for r in results if not r['summary_text']],'price_missing':[r['ticker'] for r in results if not r['price_usd_first']],'rating_distribution_heuristic':dict(Counter(r['current_condition_rating_heuristic'] for r in results)),'probability_na_explicit':sum(r['probability_na_explicit'] for r in results),'no_overall_rating_language':sum(r['no_overall_rating_language'] for r in results),'evaluation_no_rating_scope':sum(bool(r['evaluation_scope_text']) for r in results),'matrix_cell_count':len(cellrows),'matrix_complete':sum(r['matrix_cells_parsed']==20 for r in results),'matrix_numeric_ranges':sum(c['return_low_pct']!='' for c in cellrows)}
(OUT/'data/decisions_extraction_stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
