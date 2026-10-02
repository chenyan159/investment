from pathlib import Path
import json, re

B = Path(__file__).resolve().parent
data = json.loads((B/'提取数据.json').read_text(encoding='utf-8'))
checks = json.loads((B/'核验数据.json').read_text(encoding='utf-8'))
manifest = json.loads((B/'manifest.json').read_text(encoding='utf-8'))
tickers = [m['ticker'] for m in manifest]
prices = {'SOMMY':(20,20),'PSIX':(40.49,43.15),'ET':(21.50,21.51),
          'SPACEX':(147.95,153.47),'GOOGL':(338.46,338.36),'MU':(1016.59,1000.26),
          'CRWV':(102.86,99.83),'SNDK':(1740,1737.99),'AVGO':(369.35,368.56),
          'CRDO':(170.57,167.75)}
def rating(c):
    return c.split('｜')[0].strip().replace('／','/').replace(' ','')
def nums(s):
    return [float(x) for x in re.findall(r'[+-]?\d+(?:\.\d+)?',s.replace('−','-').replace(',',''))]
def link(t,v,line):
    return f'[原文](D:/drive/Investment/备份/{B.name}/{v}/{t}.md:{line})'
rows=[]; changes=[]; values=[]
for t in tickers:
    old = next(d for d in data if d['ticker']==t and d['version']=='旧报告')
    new = next(d for d in data if d['ticker']==t and d['version']=='新报告')
    for i,(o,n) in enumerate(zip(old['matrices'],new['matrices'])):
        for j in range(3):
            oc,nc=o['cells'][j+1],n['cells'][j+1]
            diff=rating(oc)!=rating(nc)
            change={'ticker':t,'scenario':['悲观','基准','乐观','突破'][i],
                    'months':[6,12,36][j],'old':oc,'new':nc,'ratingChanged':diff,
                    'oldLine':o['line'],'newLine':n['line']}
            changes.append(change)
            rows.append(f"| {t} | {change['scenario']} | {change['months']}个月 | {oc} | {nc} | {'改变' if diff else '相同'} | {link(t,'旧报告',o['line'])} / {link(t,'新报告',n['line'])} |")
    o,n=old['matrices'][1],new['matrices'][1]
    pold,pnew=prices[t]
    oo=nums(o['cells'][3].split('｜')[1]);nn=nums(n['cells'][3].split('｜')[1])
    sameoldprice=[(1+x/100)*pnew/pold*100-100 for x in nn]
    values.append({'ticker':t,'priceOld':pold,'priceNew':pnew,'priceChangePct':(pnew/pold-1)*100,
                   'base3yOldPct':oo,'base3yNewPct':nn,'newModelAtOldPricePct':sameoldprice})

arith=[]
for table in checks['tables']:
    t=table['ticker']
    if t not in ['PSIX','SPACEX','CRWV','SNDK','CRDO']: continue
    p=prices[t][1]
    for detail in table['details']:
        for v,r in zip(detail['prices'][:2],detail['returns'][:2]):
            calculated=(v/p-1)*100
            # Roundoff from displayed prices plus returns to one decimal percent.
            tolerance=.055+(.5 if t=='SNDK' else .05 if t=='CRDO' else .005)/p*100
            arith.append({'ticker':t,'line':detail['line'],'price':v,'reportedReturnPct':r,
                           'recalculatedReturnPct':calculated,'errorPp':calculated-r,
                           'tolerancePp':tolerance,'passes':abs(calculated-r)<=tolerance})

waiting=[]
for t,p,r,years,delay,cashrate,V,q,reported in [
    ('CRWV',99.83,.20,3,.5,.04,200,125,126.8),
    ('PSIX',43.15,.20,1,.25,.04,77.07,65,67.22),
    ('GOOGL',338.36,.12,3,.25,.039,565.5,414,414),
    ('CRDO',167.75,.15,.5,.25,.04,223,215,215),
]:
    cash=p*(1+cashrate)**delay
    target=p*(1+r)**years
    waiting.append({'ticker':t,'initial':p,'annualHurdle':r,'originalYears':years,'waitYears':delay,
                    'eventCash':cash,'exitValue':V,'assumedBuy':q,'reportedMaximumBuy':reported,
                    'maximumBuyAtOriginalWealthTarget':cash*V/target,
                    'maximumBuyAtRemainingExposureHurdle':V/(1+r)**(years-delay),
                    'finalWealthIfBuy':cash*V/q,'originalRequiredWealth':target,
                    'annualReturnFromOriginalStart':(cash*V/q/p)**(1/years)-1})

out={'ratingChanges':sum(c['ratingChanged'] for c in changes),
     'byTicker':{t:sum(c['ratingChanged'] for c in changes if c['ticker']==t) for t in tickers},
     'matrixDetailMatched':sum(d['matrixMatch'] for t in checks['tables'] for d in t['details']),
     'returnArithmetic':{'testedEndpoints':len(arith),'failures':[r for r in arith if not r['passes']],
                         'maxAbsoluteErrorPp':max(abs(r['errorPp']) for r in arith)},
     'priceAndBaseChanges':values,'waitingBenchmarkTests':waiting,
     'cells':changes,'returnArithmeticDetails':arith}
(B/'比较与复算.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'120格逐项对照.md').write_text('# 两轮120格逐项对照\n\n全部为报告在各自买价下的条件价值回报，非市场成交价预测。三年为累计，评级附带置信度。中性文字形式已归一后比较。\n\n| 公司 | 经营情景 | 期限 | 上轮评级/累计回报/置信度 | 本轮评级/累计回报/置信度 | 评级 | 证据 |\n|---|---|---|---|---|---|---|\n'+'\n'.join(rows)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['cells','returnArithmeticDetails']},ensure_ascii=False,indent=2))
