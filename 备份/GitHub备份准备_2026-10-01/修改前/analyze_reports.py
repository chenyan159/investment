from pathlib import Path
import json, re, statistics as st, collections, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent
ROOT=Path(r'D:\drive\Investment')
data=json.loads((OUT/'extracted_reports.json').read_text(encoding='utf-8'))
index={}
for line in (ROOT/'基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('|'):
        r=[s.strip(' `') for s in line.strip('|').split('|')]
        if len(r)==3 and re.fullmatch('[A-Z]+',r[0]): index[r[0]]={'name':r[1], 'sector':r[2].rstrip('/')}
snap={}
for line in (ROOT/'金融资料/每日金融数据/每日金融数据_2026-09-09.md').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('|'):
        r=[s.strip() for s in line.strip('|').split('|')]
        if len(r)==25 and re.fullmatch('[A-Z]+',r[0]):
            try: price=float(r[3].replace(',',''))
            except ValueError: price=None
            snap[r[0]]={'price':price,'price_date':r[2],'currency':r[13],'note':r[24]}
missing=set(index)-{d['ticker'] for d in data}
extra={d['ticker'] for d in data}-set(index)
assert len(data)==193 and len(index)==193 and not missing and not extra,(missing,extra)
positive={'强烈建议投资','建议投资','谨慎建议投资'}
for d in data:
    d.update(index[d['ticker']]); d['latest_quote']=snap.get(d['ticker'])
    for c in d['cells']:
        assert len(c['percent_values'])==2
        c['low'],c['high']=c['percent_values']
        assert -100<=c['low']<=c['high'],(d['ticker'],c)
        c['mid']=(c['low']+c['high'])/2
        c['annual_low']=((1+c['low']/100)**(12/c['months'])-1)*100
        c['annual_high']=((1+c['high']/100)**(12/c['months'])-1)*100
        c['positive']=c['label'] in positive
(OUT/'analysis_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def cell(d,s,m): return next(c for c in d['cells'] if c['scenario']==s and c['months']==m)
def fm(v): return f'{v:+.1f}%'
def rng(c): return fm(c['low'])+'～'+fm(c['high'])
stats={}
for m in [6,12,36]:
    stats[m]={}
    for s in ['悲观','基准','乐观','突破']:
        cs=[cell(d,s,m) for d in data]
        stats[m][s]={'n':len(cs),'positive':sum(c['positive'] for c in cs),'labels':dict(collections.Counter(c['label'] for c in cs)), 'median_low':st.median(c['low'] for c in cs),'median_high':st.median(c['high'] for c in cs),'median_interval_midpoint':st.median(c['mid'] for c in cs),'uniform_floor_pass':sum(c['low']>={6:8,12:15,36:40.4928}[m] for c in cs)}
print('UNIVERSE',len(data),'INDEX',len(index),'QUOTES',len(snap),'MISSING',missing,'EXTRA',extra)
print('STATS',json.dumps(stats,ensure_ascii=False))
print('BASE 12 DESC',[(d['ticker'],rng(cell(d,'基准',12))) for d in sorted(data,key=lambda d:cell(d,'基准',12)['low'],reverse=True)[:24]])
print('BASE 36 POS',[(d['ticker'],rng(cell(d,'基准',36))) for d in data if cell(d,'基准',36)['positive']])
print('OPT36 LOWER SORT',[(d['ticker'],rng(cell(d,'乐观',36)),cell(d,'乐观',36)['label']) for d in sorted(data,key=lambda d:cell(d,'乐观',36)['low'],reverse=True)[:30]])
print('BREAK36 LOWER SORT',[(d['ticker'],rng(cell(d,'突破',36)),cell(d,'突破',36)['label']) for d in sorted(data,key=lambda d:cell(d,'突破',36)['low'],reverse=True)[:25]])
print('STRONG OPT ALL',[(d['ticker'],rng(cell(d,'乐观',12))) for d in data if all(cell(d,'乐观',m)['label']=='强烈建议投资' for m in [6,12,36])])
print('NO POSITIVE ALL', [d['ticker'] for d in data if not any(c['positive'] for c in d['cells'])])
print('ONLY BREAK POS', len([d for d in data if any(c['positive'] for c in d['cells']) and all(not c['positive'] for c in d['cells'] if c['scenario']!='突破')]))
print('SECTORS')
for sector in dict.fromkeys(v['sector'] for v in index.values()):
    ds=[d for d in data if d['sector']==sector]
    print(sector,len(ds),'base12+',sum(cell(d,'基准',12)['positive'] for d in ds),'opt12+',sum(cell(d,'乐观',12)['positive'] for d in ds),'break12+',sum(cell(d,'突破',12)['positive'] for d in ds),'base12median',round(st.median(cell(d,'基准',12)['mid'] for d in ds),1))
(OUT/'statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
# Complete, directly traceable inventory. No probability or current-action inference from labels.
overview=['# 193家公司全量结果清单（2026-09-09）','','覆盖193/193家公司；147篇报告日期为9月9日，46篇为9月8日。数据直接取自最新正式Markdown，共2316格。以下评级是固定经营路径后的条件评级，不是当前买入评级，也不是胜率。数值为各报告原买价下税前累计条件价值回报，非未来成交价格预测；各报告要求回报并不完全相同。最新报价来自9月9日本地金融快照，未用它自动重评原报告。','', '三年12%年化要求对应累计40.5%；区间中点不是期望回报。每行链接至原报告矩阵所在行。']
for sector in dict.fromkeys(v['sector'] for v in index.values()):
    overview += ['', '## '+sector, '', '| 公司 | 9/9快照价格及日期 | 基准6个月 | 基准12个月 | 基准36个月 | 三年最先出现正面评级的经营行 |','|---|---|---|---|---|---|']
    for d in data:
        if d['sector']!=sector: continue
        q=d['latest_quote']; qt=f"{q['price']} {q['currency']}（{q['price_date']}）" if q else '缺失'
        link=f"[{d['ticker']} {d['name']}](<{d['file'].replace(chr(92),'/')}:{d['matrix']['line']}>)"
        cols=[cell(d,'基准',m)['label']+'；'+rng(cell(d,'基准',m)) for m in [6,12,36]]
        first=next((s for s in ['悲观','基准','乐观','突破'] if cell(d,s,36)['positive']),'四行均无')
        overview.append('| '+' | '.join([link,qt]+cols+[first])+' |')
(OUT/'193家公司全量清单.md').write_text('\n'.join(overview)+'\n',encoding='utf-8')
full=['# 全部公司当前判断摘录与2316格原始矩阵','','以下保留当前结论的原文上下文及完整条件矩阵。条件正面不等于当前买入，三年数字为累计回报。摘录仅覆盖报告开篇当前判断，不替代全文证据、资本模型及反证。来源SHA256见数据文件。']
for d in data:
    full += ['', '## '+d['ticker']+' — '+d['name'],'',f"[完整正式报告](<{d['file'].replace(chr(92),'/')}>)；报告日期 {d['date']}；SHA256 `{d['sha256']}`。",'', '### 当前判断原文摘录','']
    intro=d['intro']; cut=re.search(r'###\s*1\.[12].*(?:时点|时间|价格|证券|信息|日期|口径)',intro)
    if cut: intro=intro[:cut.start()]
    # Demote copied headings so each company remains a navigable section.
    intro=re.sub(r'^#+\s*(.*)$',r'**\1**',intro,flags=re.M)
    full += [intro.strip(),'', '### 四种经营情景与三个期限','', '| 情景 | 6个月条件建议及累计回报 | 12个月条件建议及累计回报 | 36个月条件建议及累计回报 |','|---|---|---|---|']
    for s in ['悲观','基准','乐观','突破']:
        full.append('| '+s+' | '+' | '.join(cell(d,s,m)['text'].replace('|','｜') for m in [6,12,36])+' |')
(OUT/'193家公司当前判断与完整矩阵.md').write_text('\n'.join(full)+'\n',encoding='utf-8')
