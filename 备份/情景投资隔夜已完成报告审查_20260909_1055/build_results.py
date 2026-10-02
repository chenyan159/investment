from pathlib import Path
from collections import Counter
import json, re, math

OUT = Path(__file__).parent
ROOT = Path('D:/drive/Investment')
data = json.loads((OUT / '提取数据.json').read_text(encoding='utf-8'))
audit = json.loads((OUT / '运行与文件核对.json').read_text(encoding='utf-8'))
assert len(data) == len({r['subject'] for r in data}) == 85

# Manual reading of each report's opening/current decision, not inferred from its matrix.
# N = no current new position under the report's primary thesis; W = neutral/unidentified;
# P = cautious participation. Alternative philosophies remain in the verbatim excerpts.
decisions = {r['subject']: ['N', 'N', 'N'] for r in data}
decisions.update({
    'ET': ['W', 'P', 'P'], 'MU': ['W', 'P', 'P'],
    'SMCI': ['W', 'P', 'W'], 'SOMMY': ['N', 'W', 'W'],
    'SKHY': ['N', 'W', 'N'], 'APH': ['N', 'N', 'W'],
    'BDC': ['N', 'N', 'W'], 'ASGLY': ['W', 'W', 'W'],
    'VISN': ['W', 'W', 'N'],
})
notes = {
    'ET': '一年及三年谨慎参与；网络现金、分配和扩建，较弱持续性会翻转。',
    'MU': '一年及三年谨慎参与；存储利润持续、资本开支和稀释是关键。',
    'SMCI': '仅一年谨慎参与；经营/现金修复；长持及高风险尾部并未充分解决。',
    'SOMMY': 'ADR陈旧成交和日美非同步价格；长期高风险优势不可判定。',
    'SKHY': '一年中性；长期稳健不参与，较低要求的高风险理念保留条件分歧；ADS与韩股不同。',
    'APH': '长期持续性解释会翻转；保留复利理念分歧。',
    'BDC': '三年8%要求可容纳基准中枢，12%要求不足；普通偏差会削弱回报。',
    'ASGLY': '普通修复余量薄；高风险联合上行程度难识别。',
    'VISN': '短中期修复观察；长期稳健不参与、高风险暂不可判定。',
    'NVDA': '当前不参与，但更新平台持续解释三年年化14.6%–21.6%；主DCF并未裁决它。',
    'SNDK': '当前不参与；NBM较持久净价解释可使三年中枢年化约15.8%。',
    'GOOGL': '普通现金路径缺少现价优势；长期核心投入回报比单一远期项目更重要。',
    'ECL': '现金理念不参与；维持约30倍退出的长期复利理念仍有条件分歧。',
    'LIN': '现金理念不参与；高倍数随EPS增长的交易路径保留条件分歧。',
    'TXN': '8%–10%要求及更强平台持续性组合可改变判断；不等于只降门槛即可。',
    'HOCPY': '较低回报要求与较低资本成本的组合有不同结论；主标准不参与。',
    'LWLG': '当前不参与；规模采用、净收费、跨代存续及融资的联合程度难识别。',
    'FCEL': '当前主行动不参与；高风险理念保留难判定，单一碳捕集成功不足。',
    'POET': '当前不参与；突破条件上沿可获利，量产净贡献和资本路径仍关键。',
    'BE': '三年突破条件回报仍约−16%至+15%；已计入的增长要求很高。',
    'SPACEX': '主路径远低现价；更长期平台解释仍须同时承担巨大经营和资本要求。',
    'DELL': '增长与EPS不能代替股东现金；采用的最新10-Q公开晚于报告买价时点。',
}
names = {'P': '谨慎参与', 'W': '中性/难判定', 'N': '暂不参与'}
labels = ['强烈不建议投资', '不建议投资', '强烈建议投资', '谨慎建议投资', '建议投资', '中性', '等待']
positive = {'强烈建议投资', '谨慎建议投资', '建议投资'}
def label(cell):
    return next((x for x in labels if x in cell), '?')
def ret(cell):
    bits = cell.replace('**','').split('｜')
    assert len(bits) == 3, cell
    return bits[1].strip().replace('|', '／')
def frozen(r, line=None):
    return (OUT / '报告快照' / (r['subject'] + '.md')).as_posix() + (f':{line}' if line else '')
def link(text, path):
    return f'[{text}](<{path}>)'

stats = {
    'scope': audit['cutoff'],
    'current_decision_counts': {str(h): dict(Counter(decisions[r['subject']][i] for r in data)) for i,h in enumerate([6,12,36])},
    'current_same_three_horizons': sum(len(set(decisions[r['subject']])) == 1 for r in data),
    'conditional_same_three_horizons_rows': sum(len({label(c) for c in row[1:]}) == 1 for r in data for row in r['matrices'][0]['rows'][1:]),
    'conditional_same_all_four_rows_companies': sum(all(len({label(c) for c in row[1:]}) == 1 for row in r['matrices'][0]['rows'][1:]) for r in data),
    'confidence': dict(Counter(c.replace('**','').split('｜')[-1].strip() for r in data for row in r['matrices'][0]['rows'][1:] for c in row[1:])),
    'category': dict(Counter(r['category'] for r in data)),
    'conditional_positive': {scene: [sum(label(r['matrices'][0]['rows'][s+1][h+1]) in positive for r in data) for h in range(3)] for s,scene in enumerate(['悲观','基准','乐观','突破'])},
    'manual_current': decisions,
}
assert stats['current_same_three_horizons'] == 77
assert sum(stats['confidence'].values()) == 1020
(OUT / '结果与质量统计.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')

lines = ['# 已完成85家公司：结果总表与当前取舍原文', '',
    f"冻结时点：{audit['cutoff']}。昨夜22:52大批次完成75家；同晚19点先完成10家，单独注明。", '',
    '范围为成功归档的任务，不把已有文件但任务仍running/retry_pending的公司纳入。全部使用Astra high及相同最新方案。', '',
    '当前行动依据逐份阅读报告开头和当前权衡章节，归并为谨慎参与、中性/难判定、暂不参与。暂不参与仅对应报告主要理念下当前新增仓位；不表示看空、不表示所有风险偏好均应拒绝，也不代表等待策略已获证明。不同理念的条件分歧见备注及下方原文。', '',
    '百分比逐字摘自各报告条件矩阵，均为累计总回报，三年数值未年化。它们是给定经营路径下的合理价值回报，不是概率加权预期收益或实际股价预测；回报参照报告自身价格，多为9月8日收盘。报告间风险标准和估值参数未统一，不能按区间上沿直接跨公司排名。', '',
    link('全部1,020格原文矩阵', (OUT/'全部公司原文条件矩阵.md').as_posix()), '',
    '| 公司 | 批次 | 当前6月 / 12月 / 36月 | 基准6月 | 基准12月 | 基准36月 | 乐观36月 | 突破36月 | 主要限定 |',
    '|---|---|---|---|---|---|---|---|---|']
for r in data:
    m = r['matrices'][0]['rows']; t = r['subject']
    values = [ret(c) for c in m[2][1:]] + [ret(m[3][3]), ret(m[4][3])]
    lines.append('| '+ ' | '.join([link(t+' '+r['displayName'], frozen(r,r['matrices'][0]['line'])), '先前10家' if r['cohort']=='19点十家公司' else '22:52大批次', ' / '.join(names[x] for x in decisions[t]), *values, notes.get(t, '主行动暂不参与；具体理念及改变条件见下方原文。')])+' |')
lines += ['', '## 各公司当前取舍原文', '', '以下保留各报告开头的当前判断；后文的概率、估值和敏感性仍应与原文一起使用。报告中的F/M/E/U等标记分别依各报告定义，未来值不转述为已发生事实。', '']
for r in data:
    opening = r['opening'].split('\n### ')[0].strip()
    opening = re.sub(r'^# .+\n', '', opening, count=1).strip()
    lines += [f"### {r['subject']} — {r['displayName']}", '', link('冻结全文', frozen(r))+'；'+link('正式结果文件',(ROOT/r['outputFile']).as_posix()), '',
              f"完成：{r['finishedAt']}；本次成功尝试{r['minutes']}分钟；{r['bytes']:,}字节；SHA256 `{r['sha256']}`。", '', opening, '']
(OUT / '全部公司结果.md').write_text('\n'.join(lines), encoding='utf-8')

# Independent arithmetic checks of published model numbers, not a re-estimation of their inputs.
smci_values1 = [56,35,12,95,2]; smci_values3 = [69,43,17,130,2]
weights = {'working':[.50,.25,.12,.10,.03], 'weak':[.45,.30,.18,.05,.02], 'strong':[.55,.20,.08,.15,.02]}
checks = {'SMCI': {k: {'one_year_value': sum(a*b for a,b in zip(w,smci_values1)), 'three_year_value':sum(a*b for a,b in zip(w,smci_values3))} for k,w in weights.items()}}
checks['SMCI']['working']['one_year_return_at_report_price'] = 47.75/40.26-1
checks['SMCI']['working']['D_to_B_flip_percentage_points'] = (47.75-40.26*1.15)/(95-35)*100
checks['SMCI_wait'] = {'initial_funds':40.26,'five_month_cash':40.923,'future_value':56,
    'buy_ceiling_same_original_15pct_total_hurdle':40.923/40.26*56/1.15,
    'buy_ceiling_reset_seven_month_15pct_annual_hurdle':56/(1.15**(7/12))}
checks['SKHY_report_non_synchronous_price'] = {'adr_equivalent':1793000/10/1343.57,'premium':185.55/(1793000/10/1343.57)-1}
checks['SOMMY_report_non_synchronous_price'] = {'adr_equivalent':568.1*5/153.855,'premium_at_20':20/(568.1*5/153.855)-1}
checks['ASGLY'] = {'two_branch_weight_for_10pct_annual':(7.01*1.1**3-2.03)/(9.62-2.03)}
checks['disclaimer'] = '复算验证算术与口径；未证明条件价值、分支权重或未来报价真实。SMCI等待两个门槛对应不同策略标准，不是单纯除法算错。'
(OUT/'独立算术复核.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'stats':stats,'arithmetic':checks,'result_bytes':(OUT/'全部公司结果.md').stat().st_size},ensure_ascii=False,indent=2))
