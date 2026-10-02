from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).parent; ROOT=Path(r'D:\drive\Investment')
data=json.loads((OUT/'analysis_data.json').read_text(encoding='utf-8'))
p8={}
for line in (ROOT/'金融资料/每日金融数据/每日金融数据_2026-09-08.md').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('|'):
        r=[s.strip() for s in line.strip('|').split('|')]
        if len(r)==25 and re.fullmatch('[A-Z]+',r[0]):
            try:p8[r[0]]=float(r[3].replace(',',''))
            except ValueError:pass
unmatched=[]
overrides={'ABBNY':99.57,'ASGLY':7.01,'ASMIY':971.37,'ASMVY':62.115,'ATEYY':220.09,'BESIY':225.56,'DKILY':13.21,'DSCSY':34.99,'HTHIY':33.82,'LITE':978.54,'MIELY':65.72,'SHECY':18.45,'SOMMY':20.00,'TOELY':177.27,'SPACEX':153.47}
for d in data:
    candidates=[]
    for dt,p in [('2026-09-08',p8.get(d['ticker'])),('2026-09-09',d['latest_quote']['price'])]:
        if p is None:continue
        # Match the exact quoted price in the report opening; retain the evidence.
        for form in {f'{p:.2f}',f'{p:,.2f}',str(p)}:
            for m in re.finditer(r'(?<![\d.])'+re.escape(form)+r'(?![\d.])',d['intro']):
                context=d['intro'][max(0,m.start()-55):m.end()+55]
                if any(w in context for w in ['买价','买入','现价','收盘','美元','参照价','参考价']):
                    candidates.append((m.start(),dt,p,context))
    candidates.sort(key=lambda r:r[0])
    if d['ticker'] in overrides:
        p=overrides[d['ticker']]
        evidence=next((line for line in d['intro'].splitlines() if (f'{p:.2f}' in line or str(p) in line) and any(w in line for w in ['买价','买入','收盘','美元','主矩阵'])), '')
        assert evidence,(d['ticker'],p)
        candidates=[(0,'原文人工核对',p,evidence)]
    if candidates:
        _,dt,p,evidence=candidates[0]
        if p==d['latest_quote']['price'] and '2026-09-09' in evidence and '2026-09-08' not in evidence:dt='2026-09-09'
        d['anchor_price']=p;d['anchor_price_match_date']=dt;d['anchor_evidence']=evidence
        latest=d['latest_quote']['price']
        d['price_change_percent']=(latest/p-1)*100 if latest else None
        for c in d['cells']:
            if latest and d['latest_quote']['price_date']=='2026-09-09':
                c['rebased_low']=(p/latest*(1+c['low']/100)-1)*100
                c['rebased_high']=(p/latest*(1+c['high']/100)-1)*100
    else:unmatched.append(d['ticker'])
print('UNMATCHED',unmatched)
for d in data:
    if abs(d.get('price_change_percent') or 0)>=5:
        print('MOVE',d['ticker'],d['anchor_price'],d['latest_quote']['price'],round(d['price_change_percent'],2),d['anchor_evidence'].replace('\n',' '))
for t in 'ADBE ET MU SMCI BABA PNR NVDA TSM'.split():
    d=next(d for d in data if d['ticker']==t)
    print('KEY',t,'ANCHOR',d.get('anchor_price'),'LATEST',d['latest_quote']['price'])
    for c in d['cells']:
        if c['scenario']=='基准' and c['months'] in [12,36]: print(c['months'],round(c.get('rebased_low',c['low']),1),round(c.get('rebased_high',c['high']),1))
(OUT/'analysis_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 9月9日报价下的机械重算：完整193家公司','','只改变买价，固定原报告的经营、现金分配和目标日价值，未更新9月9日新增经营信息，也不自动改变原评级。公式：新回报＝(1＋原回报)×原报告买价÷新报价−1。原回报已四舍五入，以下数值约到0.1个百分点；所有回报是税前累计条件价值回报，不是预测成交价。目标日继续采用原报告日期，三年重算的精确日数差异未年化。','','191家公司具备9月9日报价；MICLF报价停在9月8日，SPACEX研究标识未映射到行情证券，保留缺失。SOMMY原报告20美元为9月3日非零成交参考，ASGLY等OTC报价有流动性和价差限制。','','| 公司 | 原报告买价 | 9月9日报价 | 基准6个月 | 基准12个月 | 基准36个月 | 乐观36个月 | 突破36个月 |','|---|---:|---:|---|---|---|---|---|']
for d in data:
    values=[]
    for s,m in [('基准',6),('基准',12),('基准',36),('乐观',36),('突破',36)]:
        c=next(c for c in d['cells'] if c['scenario']==s and c['months']==m)
        values.append(f"{c['rebased_low']:+.1f}%～{c['rebased_high']:+.1f}%" if 'rebased_low' in c else '无9月9日报价，不重算')
    quote=d['latest_quote'];q=str(quote['price']) if quote['price_date']=='2026-09-09' else '缺失/滞后'
    md.append('| '+f"[{d['ticker']} {d['name']}](<{d['file'].replace(chr(92),'/')}>) | {d.get('anchor_price','未知')} | {q} | "+' | '.join(values)+' |')
(OUT/'9月9日报价机械重算_193家公司.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
