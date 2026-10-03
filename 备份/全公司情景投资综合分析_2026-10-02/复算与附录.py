from pathlib import Path
from datetime import date
import json, csv, hashlib, statistics, collections, re

ROOT = Path(r'D:\investment')
OUT = Path(__file__).parent
CACHE = ROOT / '备份/全公司情景投资横评_2026-10-02/analysis.json'
obj = json.loads(CACHE.read_text(encoding='utf-8'))
rows = obj['companies']
keys = ['悲观', '基准', '乐观', '突破']
issues = []
for r in rows:
    source = ROOT / r['path']
    if hashlib.sha256(source.read_bytes()).hexdigest() != r['sha256']:
        raise ValueError('Source changed: ' + r['ticker'])
    lines = source.read_text(encoding='utf-8-sig').splitlines()
    for k, sc in r['scenarios'].items():
        if sc['raw'].strip() != lines[sc['line'] - 1].strip():
            raise ValueError('Line changed: ' + r['ticker'])
        text = re.sub(r'\*\*|`', '', sc['evidence_text'] or '').strip()
        match = re.match(r'^(?:证据(?:支撑度)?\s*[:：]?\s*)?(强|中|弱|不足)', text)
        if not match:
            match = re.search(r'[；;]\s*(强|中|弱|不足)(?=[：:；;，,（(]|$)', text)
        sc['evidence_corrected'] = match.group(1) if match else None
        if r['ticker'] == 'CSCO' and k == '基准':
            sc['evidence_corrected'] = '中'
        if r['ticker'] == 'TDY' and k == '基准':
            sc['evidence_corrected'] = '中'
        if r['ticker'] == 'MMM' and k == '悲观':
            sc['evidence_corrected'] = '中'
        if sc['evidence_corrected'] is None:
            issues.append([r['ticker'], k, 'evidence label needs review', text])
        calculated = [(p / r['quote'] - 1) * 100 for p in sc['price']]
        if max(abs(a-b) for a,b in zip(calculated, sc['return_calculated'])) > 1e-7:
            raise ValueError('Return mismatch: ' + r['ticker'])
    r['eligible'] = r['ticker'] not in ['ATKR', 'TOELY']
    r['exclusion'] = '现金并购对价约束，独立经营目标价不代表实际持股路径' if r['ticker'] == 'ATKR' else '报告为JPY东京8035拆股后普通股，快照为旧USD ADR，不能复算' if r['ticker'] == 'TOELY' else ''
    y = r['years']
    p = r['snapshot_price']
    mid = sum(r['scenarios']['基准']['price']) / 2
    if r['eligible']:
        r['delay_annual_snapshot'] = ((mid/p)**(1/(y+1))-1)*100
        r['cut20_annual_snapshot'] = ((mid*.8/p)**(1/y)-1)*100
        r['joint_annual_snapshot'] = ((mid*.8/p)**(1/(y+1))-1)*100
        r['price_for_10pct_base_floor'] = r['scenarios']['基准']['price'][0]/(1.1**y)
        lo,hi = r['scenarios']['基准']['return_snapshot']
        ann_lo = r['scenarios']['基准']['annual_snapshot'][0]
        r['current_bucket'] = ('基准区间全负' if hi < 0 else '基准跨零' if lo < 0 else '基准年化下沿不足8%' if ann_lo < 8 else '基准年化下沿至少8%')
    else:
        r['current_bucket'] = '特殊证券'

eligible = [r for r in rows if r['eligible']]
def med(values):
    return round(statistics.median(values), 4)
stats = {
    'research_date': '2026-10-02', 'company_count':len(rows), 'scenario_count':sum(len(r['scenarios']) for r in rows),
    'comparable_count':len(eligible), 'special_securities':{r['ticker']:r['exclusion'] for r in rows if not r['eligible']},
    'current_buckets':dict(collections.Counter(r['current_bucket'] for r in eligible)),
    'median_current_base_mid_annual':med(r['base_mid_annual_snapshot'] for r in eligible),
    'median_current_base_mid_total':med(statistics.mean(r['scenarios']['基准']['return_snapshot']) for r in eligible),
    'median_current_pess_low':med(r['scenarios']['悲观']['return_snapshot'][0] for r in eligible),
    'current_pess_below_minus50':sum(r['scenarios']['悲观']['return_snapshot'][0] <= -50 for r in eligible),
    'current_base_mid_annual_gt10':sum(r['base_mid_annual_snapshot'] >= 10 for r in eligible),
    'cut20_mid_annual_gt10':sum(r['cut20_annual_snapshot'] >= 10 for r in eligible),
    'joint_mid_annual_gt10':sum(r['joint_annual_snapshot'] >= 10 for r in eligible),
    'median_delay_annual':med(r['delay_annual_snapshot'] for r in eligible),
    'median_cut20_annual':med(r['cut20_annual_snapshot'] for r in eligible),
    'median_joint_annual':med(r['joint_annual_snapshot'] for r in eligible),
    'evidence_corrected':{k:dict(collections.Counter(r['scenarios'][k]['evidence_corrected'] for r in rows)) for k in keys},
    'label_issues':issues, 'categories':[],
    'report_quote_stats':{k:v for k,v in obj['stats'].items() if k != 'evidence'},
    'provenance':'All original report hashes and scenario table lines independently matched. Existing cache only used for table extraction; source reports govern interpretation.',
}
for cat in sorted(set(r['category'] for r in rows)):
    allcat=[r for r in rows if r['category']==cat]
    group=[r for r in allcat if r['eligible']]
    stats['categories'].append({'category':cat,'count':len(allcat),'comparable':len(group),
        'base_mid_annual':med(r['base_mid_annual_snapshot'] for r in group),
        'pess_low':med(r['scenarios']['悲观']['return_snapshot'][0] for r in group),
        'base_low_gt8':sum(r['scenarios']['基准']['annual_snapshot'][0]>=8 for r in group),
        'base_full_negative':sum(r['scenarios']['基准']['return_snapshot'][1]<0 for r in group)})
(OUT/'复算数据.json').write_text(json.dumps({'stats':stats,'companies':rows},ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'全公司四情景复算.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['公司代码','公司名称','分类','纳入当前横比','报告买价','快照买价','快照报价日期','目标日','期限年','情景','目标价下沿','目标价上沿','报告回报下沿pct','报告回报上沿pct','快照回报下沿pct','快照回报上沿pct','快照年化下沿pct','快照年化上沿pct','证据标签','固定倍数原文','来源','来源行号','来源sha256','特殊口径说明']
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in rows:
        for k in keys:
            s=r['scenarios'][k]
            compatible = r['ticker'] != 'TOELY'
            vals=[r['ticker'],r['name'],r['category'],r['eligible'],r['quote'],r['snapshot_price'] if compatible else None,r['snapshot'].get('价格日期'),r['target'],r['years'],k,*s['price'],*s['return_calculated'],*(s['return_snapshot'] or [None,None]),*(s['annual_snapshot'] or [None,None]),s['evidence_corrected'],s['fixed_text'],r['path'],s['line'],r['sha256'],r['exclusion']]
            w.writerow(dict(zip(fields,[round(v,4) if isinstance(v,float) else v for v in vals])))

def pct(xs):
    return '～'.join(f'{x:+.1f}%' for x in xs) if xs else '不可换算'
parts=['# 全部221家公司四情景对照\n\n研究日2026年10月2日。按报告条件目标价与10月2日日度快照复算，均为价格回报，未统一加入未来股息或本币汇率收益。年化从研究日至各公司目标日，悲观回报为目标期情景结果，不代表持有期间最大回撤。ATKR经营目标价是收购失败后独立情景参考；TOELY用日元普通股原报告口径，均不计入219家当前报价横比。\n\n证据栏依次为悲观、基准、乐观、突破；源报告链接可定位到四情景表。各分类第二表比较目标期、买价和额外时间/估值压力。终点价减20%及延后一年仅为统一敏感性测试，没有重做经营或资本模型；10%条件买价仅表示原基准下沿对应的数学门槛，不是内在价值或买入指令。未调整新增资本、稀释、股息和融资条件。原文摘要保留原报告判断，不能视作本次独立评级。\n']
for cat in sorted(set(r['category'] for r in rows)):
    parts += [f'\n## {cat.replace("_", " ")}\n\n', '| 公司及原报告 | 当前分组 | 悲观价格回报 | 基准价格回报 | 基准年化 | 乐观价格回报 | 突破价格回报 | 四情景证据 |\n|---|---|---:|---:|---:|---:|---:|---|\n']
    for r in [r for r in rows if r['category']==cat]:
        sc=r['scenarios'];use='return_calculated' if r['ticker']=='TOELY' else 'return_snapshot'
        annual=sc['基准']['annual_report'] if r['ticker']=='TOELY' else sc['基准']['annual_snapshot']
        source='/'+(ROOT/r['path']).as_posix()
        parts.append(f'| [{r["ticker"]}]({source}:{r["table_line"]}) {r["name"]} | {r["current_bucket"]} | {pct(sc["悲观"][use])} | {pct(sc["基准"][use])} | {pct(annual)} | {pct(sc["乐观"][use])} | {pct(sc["突破"][use])} | {" / ".join(sc[k]["evidence_corrected"] or "待核" for k in keys)} |\n')
    parts.append('\n### 目标期、买价和敏感性\n\n| 公司 | 快照买价 | 目标日 / 期限年 | 基准中点年化 | 延后一年 | 终点价减20% | 两者叠加 | 基准下沿年化10%的条件买价 |\n|---|---:|---|---:|---:|---:|---:|---:|\n')
    for r in [r for r in rows if r['category']==cat]:
        if r['eligible']:
            vals=[r['base_mid_annual_snapshot'],r['delay_annual_snapshot'],r['cut20_annual_snapshot'],r['joint_annual_snapshot']]
            parts.append(f'| {r["ticker"]} | {r["snapshot_price"]:.2f} | {r["target"]} / {r["years"]:.2f} | '+' | '.join(f'{v:+.1f}%' for v in vals)+f' | {r["price_for_10pct_base_floor"]:.2f} |\n')
        else:
            parts.append(f'| {r["ticker"]} | 单列 | {r["target"]} / {r["years"]:.2f} | — | — | — | — | — |\n')
    parts.append('\n')
    for r in [r for r in rows if r['category']==cat]:
        text = re.sub(r'\*\*|`', '', ' '.join(r['summary']))
        first = re.split(r'(?<=[。])\s*', text)[0]
        if len(first)>330:first=first[:330]+'…'
        parts.append(f'- **{r["ticker"]} 原报告判断：**{first}\n')
(OUT/'全部221家公司对照.md').write_text(''.join(parts),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
