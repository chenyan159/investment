from pathlib import Path
import json, re, sys, hashlib
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('D:/drive/Investment')
OUT=Path(__file__).resolve().parent
PREV=ROOT/'备份/16份排序结果横评_2026-09-09'
symbols='ADBE MSFT MU ET PNR ST DOV ALLE EME TEL NTAP HUBB TSM NVDA AVGO BABA SMCI AEP DTE DKILY ASML FTV META HPE BDC ENS QCOM GFS PLAB VISN SNDK FN CLS AMZN ETN VST GOOGL ACLS'.split()
snapshot=ROOT/'金融资料/每日金融数据/每日金融数据_2026-09-09.md'
prices={}
for n,line in enumerate(snapshot.read_text(encoding='utf-8').splitlines(),1):
    if not line.startswith('|'): continue
    cells=[x.strip() for x in line.strip('|').split('|')]
    if cells[0]=='股票代号': headers=cells
    elif cells[0] in symbols:
        prices[cells[0]]=dict(zip(headers,cells))|{'line':n}
analysis=json.loads((PREV/'交集与选择及历史核验.json').read_text(encoding='utf-8'))
manifest=json.loads((PREV/'16份结果清单.json').read_text(encoding='utf-8'))
records={}
for sym in symbols:
    paths=sorted((ROOT/'分析报告/公司情景投资决策/结果').glob(sym+'_*.md'))
    if not paths: print('MISSING',sym); continue
    p=paths[-1]; raw=p.read_text(encoding='utf-8'); lines=raw.splitlines()
    one_year=[]
    for i,s in enumerate(lines,1):
        if s.startswith('|') and re.search(r'2027[-/.年]0?9|1年|一年|12\s*个月|1Y|1y',s):
            one_year.append({'line':i,'text':s})
    record={'ticker':sym,'report':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
        'snapshot':prices.get(sym), 'intro':[{'line':i,'text':s} for i,s in enumerate(lines[:19],1)],
        'one_year_lines':one_year,
        'focus_lists':[k for k,v in analysis['focus'].items() if sym in v],
        'support':{k:{f:v[f].index(sym)+1 for f in ['c3','c6','y3','y6','research3','research6'] if v.get(f) and sym in v[f]} for k,v in analysis['views'].items() if any(v.get(f) and sym in v[f] for f in ['c3','c6','y3','y6','research3','research6'])}}
    records[sym]=record
(OUT/'候选公司本地证据.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
mode=sys.argv[1:] or symbols
for sym in mode:
    x=records[sym]; s=x['snapshot']; print('\n###',sym,Path(x['report']).name)
    print('FIN', {k:s[k] for k in ['最新价格','TTM PE','Forward PE','Call IV','Put IV']})
    print('LISTS',','.join(x['support']))
    for row in x['intro']:
        if row['line']>4 and row['text'].startswith('**'):print(row['line'],row['text'][:350])
    for row in x['one_year_lines']:
        if re.search('基准|乐观|Base|Bull|正常|超预期',row['text']) and re.search('建议|中性|等待|选择',row['text']):print(row['line'],row['text'][:520])
