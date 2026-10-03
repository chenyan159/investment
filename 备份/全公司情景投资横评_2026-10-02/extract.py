from pathlib import Path
import re, json, hashlib, csv, math
from datetime import date

ROOT = Path(r'D:\investment')
OUT = Path(__file__).parent
BASE = ROOT / '分析报告/公司情景投资决策/结果'

def clean(s):
    return re.sub(r'\*\*|`', '', s).strip()

def cells(s):
    return [clean(x) for x in s.strip().strip('|').split('|')]

def norm(s):
    s=s.replace('−','-').replace('–','~').replace('—','~').replace('～','~').replace('，',',').replace('％','%')
    return re.sub(r'(?<=%)\s*-\s*(?=\d)','~',s)

def nums(s):
    return [float(x.replace(',','')) for x in re.findall(r'[+-]?\d[\d,]*(?:\.\d+)?',norm(s))]

def price_range(s):
    s=re.sub(r'\([^)]*\)|（[^）]*）','',s)
    vs=nums(s)
    vs=[abs(x) for x in vs]
    return vs[:2] if len(vs)>=2 else vs*2

index = (ROOT/'基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig')
companies={}
for l in index.splitlines():
    if not l.startswith('|'): continue
    cs=cells(l)
    if len(cs)>=3 and re.fullmatch(r'[A-Z][A-Z0-9.-]*',cs[0]):
        companies[cs[0]]={'name':cs[1],'category':cs[2].strip('/')}

rows=[]
for p in sorted(BASE.glob('*.md')):
    ticker=p.name.split('_')[0]
    s=p.read_text(encoding='utf-8-sig'); lines=s.splitlines()
    head=s[:11000]
    table=None; scens={}; headers=[]; tablelines=[]
    for i,l in enumerate(lines[:170]):
        if l.startswith('|') and ('情景' in l) and ('预计' in l or '交易' in l or '涨跌' in l or '变化' in l):
            hs=cells(l)
            if '情景' not in hs[0]:continue
            if not any(any(w in x for w in ['股价','交易','组合价值']) for x in hs): continue
            candidate=[]
            for j in range(i+1,min(i+18,len(lines))):
                if lines[j].startswith('|'): candidate.append((j,lines[j]))
                elif candidate: break
            scenarios={}
            for j,raw in candidate:
                cs=cells(raw)
                if not cs: continue
                key=next((k for k in ['悲观','基准','乐观','突破'] if cs[0].startswith(k)),None)
                if key: scenarios[key]={'cells':cs,'line':j+1,'raw':raw}
            if len(scenarios)==4:
                headers=hs;scens=scenarios;tablelines=[l]+[raw for _,raw in candidate];table=i+1;break
    # Quote candidates restricted to pre-table metadata, then verify returns independently.
    pre='\n'.join(lines[:table-1]) if table else head
    quoted=[]
    for l in pre.splitlines():
        if any(w in l for w in ['买价','股价','报价','价格锚','价格基准','现价','参考价','当前价格']):
            quoted.append(l)
    qtext='\n'.join(quoted)
    p0=None
    patterns=[r'(?:USD|US\$|\$)\s*((?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)',r'([\d,]+(?:\.\d+)?)\s*美元',r'(?:价格锚|买价|股价|报价)[^\n]{0,25}?([\d,]+\.\d+)']
    for pat in patterns:
        m=re.search(pat,qtext)
        if m: p0=float(m[1].replace(',',''));break
    hq=next((h for h in headers if re.match(r'^(?:相对|较|对)',h) and re.search(r'\d',h) and 'P0' not in h),None)
    if hq: p0=nums(hq)[0]
    # For headers without a numeric anchor, use explicitly labeled quote metadata.
    if not hq:
        explicit=[l for l in quoted if not l.startswith('#') and any(w in l[:65] for w in ['统一买价','统一当前买价','共同买价','价格基准','共同价格','价格锚','买价基准','当前买价','当前股价','买价锚','当前参考买价','当前价格与报价','测算买价','统一参考买价'])]
        for l in explicit:
            for pat in patterns:
                m=re.search(pat,clean(l))
                if m:p0=float(m[1].replace(',',''));break
            if m:break
    # Metadata phrases embedded in a paragraph need their local price rather than earlier DCF numbers.
    if ticker=='DCI':p0=89.53
    if ticker=='VSH':p0=38.18
    targetlines=[l for l in pre.splitlines() if ('目标' in l or '观察' in l or '主要定价' in l) and re.search(r'20[2-4]\d',l)]
    targetlines.sort(key=lambda l: 0 if re.search(r'共同主要|共同目标|主要目标|目标观察|观察日',l) else 1)
    target=None
    for l in targetlines:
        label=re.search(r'共同主要|共同目标|共同观察|主要目标|目标观察|观察日',l)
        if label:l=l[label.start():]
        ms=list(re.finditer(r'(20[2-4]\d)[-年/](\d{1,2})[-月/](\d{1,2})',l))
        for m in ms:
            try:
                dt=date(*map(int,m.groups()))
                if dt<=date(2026,10,2):continue
                target=dt.isoformat();break
            except ValueError:pass
        if target:break
    if not target:
        for l in targetlines:
            m=re.search(r'(20[2-4]\d)\s*年?\s*(?:末|财年末|年末)',l)
            if m:target=f'{m[1]}-12-31';break
    summary=[]
    for l in lines[:80]:
        if not l.strip() or l.startswith(('#','|','-')):continue
        summary.append(l)
        if sum(len(x) for x in summary)>1100:break
    row={'ticker':ticker,**companies.get(ticker,{}),'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chars':len(s),'lines':len(lines),'quote':p0,'quote_lines':quoted[:7],'target':target,'target_lines':targetlines,'summary':summary,'headers':headers,'table_line':table,'table':tablelines,'scenarios':scens}
    for key,rec in scens.items():
        cs=rec['cells']; rec['fields']={k:v for k,v in zip(headers,cs)}
        pi=next((i for i,h in enumerate(headers) if ('交易' in h or '预计组合价值' in h) and not any(x in h for x in ['变化','涨跌','回报'])),None)
        ri=next((i for i,h in enumerate(headers) if (re.match(r'^(相对|较|对\d)',h) or any(x in h for x in ['股价变化','价格变化','预计变化'])) and not any(w in h for w in ['固定','纯业务','纯基本面'])),None)
        fi=next((i for i,h in enumerate(headers) if '纯业务' in h or '纯基本面' in h or '固定' in h),None)
        ei=next((i for i,h in enumerate(headers) if '支撑' in h or '证据' in h),None)
        rec['price_text']=cs[pi] if pi is not None and pi<len(cs) else None
        rec['price']=price_range(rec['price_text']) if rec['price_text'] else []
        rec['return_text']=cs[ri] if ri is not None and ri<len(cs) else None
        rec['fixed_text']=cs[fi] if fi is not None and fi<len(cs) else None
        rec['evidence_text']=cs[ei] if ei is not None and ei<len(cs) else None
        rec['evidence']=next((v for v in ['不足','弱','中','强'] if rec['evidence_text'] and v in rec['evidence_text'][:35]),None)
        rec['return_calculated']=[(v/p0-1)*100 for v in rec['price']] if p0 else []
        rec['return_published']=nums(rec['return_text'])[:2] if rec['return_text'] else []
        if len(rec['return_published'])==1:rec['return_published']*=2
    rows.append(row)

missing=sorted(set(companies)-{x['ticker'] for x in rows})
extra=sorted({x['ticker'] for x in rows}-set(companies))
(OUT/'extracted.json').write_text(json.dumps({'index_count':len(companies),'report_count':len(rows),'missing':missing,'extra':extra,'companies':rows},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'summaries.txt').write_text('\n\n'.join(f"{r['ticker']} | {r.get('category')} | quote={r['quote']} target={r['target']}\n"+'\n'.join(r['summary'])+'\n'+'\n'.join(r['table']) for r in rows),encoding='utf-8')
print('INDEX',len(companies),'REPORTS',len(rows),'MISSING',missing,'EXTRA',extra)
print('MISSING TABLES',[r['ticker'] for r in rows if not r['table_line']])
print('MISSING QUOTE',[r['ticker'] for r in rows if r['quote'] is None])
print('MISSING TARGET',[r['ticker'] for r in rows if r['target'] is None])
for r in rows:
    if any(len(x['price'])!=2 for x in r['scenarios'].values()):print('PRICE PARSE',r['ticker'],r['headers'],[x['price_text'] for x in r['scenarios'].values()])
print('TOTAL_CHARS',sum(r['chars'] for r in rows))
