import json, re, collections, statistics
from pathlib import Path

ROOT = Path(__file__).parent
manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
raw = json.loads((ROOT / 'parsed_matrices_raw.json').read_text(encoding='utf-8'))
RATINGS = ['强烈不建议投资', '不建议投资', '中性 / 等待', '谨慎建议投资', '建议投资', '强烈建议投资']
SHORT = ['强烈不建议', '不建议', '等待', '谨慎建议', '建议', '强烈建议']
TIMES = ['短期（6个月）', '中期（12个月）', '长期（36个月）']
SCENARIOS = ['悲观', '基准', '乐观', '突破']
all_cells = []
by_company = {}
for report in raw:
    t = report['subject']
    mat = []
    for si, row in enumerate(report['matrix']):
        cells = []
        for ti, cell in enumerate(row['cells']):
            parts = cell.split('｜')
            assert len(parts) == 3, (t, cell)
            rating, ret, conf = [p.strip() for p in parts]
            assert rating in RATINGS, (t, rating)
            nums = re.findall(r'[+\-−]?\d+(?:\.\d+)?', ret)
            rr = [float(n.replace('−', '-')) for n in nums]
            entry = dict(subject=t, scenario=SCENARIOS[si], time=TIMES[ti], si=si, ti=ti,
                         rating=rating, rank=RATINGS.index(rating), returns=ret, bounds=rr,
                         confidence=conf, line=row['line'])
            cells.append(entry)
            all_cells.append(entry)
        mat.append(cells)
    by_company[t] = mat

grid = []
for si, s in enumerate(SCENARIOS):
    for ti, h in enumerate(TIMES):
        v = [c for c in all_cells if c['si'] == si and c['ti'] == ti]
        cc = collections.Counter(c['rating'] for c in v)
        groups = {r: [c['subject'] for c in v if c['rating'] == r] for r in RATINGS}
        grid.append(dict(scenario=s, time=h, counts=dict(cc), positive=sum(c['rank']>=3 for c in v),
                         strong_positive=sum(c['rank']>=4 for c in v), negative=sum(c['rank']<=1 for c in v),
                         wait=cc[RATINGS[2]], groups=groups))
same_time = {}
for si, s in enumerate(SCENARIOS):
    same_time[s] = [t for t, m in by_company.items() if len({c['rank'] for c in m[si]}) == 1]

base_compare = collections.Counter()
for t, mat in by_company.items():
    x = mat[1]
    base_compare['long_lower_than_mid' if x[2]['rank'] < x[1]['rank'] else 'long_higher_than_mid' if x[2]['rank'] > x[1]['rank'] else 'same_long_mid'] += 1

stats = dict(sample_count=len(raw), cell_count=len(all_cells), ratings=RATINGS, grid=grid,
             same_rating_across_times=same_time, base_long_vs_mid=dict(base_compare),
             confidence=dict(collections.Counter(c['confidence'] for c in all_cells)),
             quantified=sum(len(c['bounds'])==2 for c in all_cells),
             categories=dict(collections.Counter(r['category'] for r in manifest['reports'])))
(ROOT / 'census.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'all_cells.json').write_text(json.dumps(all_cells, ensure_ascii=False, indent=2), encoding='utf-8')
out = ['# 97家公司四情景 × 三期限条件建议全表', '',
       '样本冻结：2026-09-07 18:29 PDT；仅本批成功任务。以下是条件建议，不能按正面格数排序或当作当前买入结论。', '',
       '| 经营情景 | 持有期限 | 强烈不建议 | 不建议 | 等待 | 谨慎建议 | 建议 | 强烈建议 |',
       '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for g in grid:
    out.append('| '+g['scenario']+' | '+g['time']+' | '+' | '.join(str(g['counts'].get(r,0)) for r in RATINGS)+' |')
for t, mat in by_company.items():
    out += ['', f'## {t}', '', '| 情景 | 短期（6个月） | 中期（12个月） | 长期（36个月） |', '| --- | --- | --- | --- |']
    for si, row in enumerate(mat):
        out.append('| '+SCENARIOS[si]+' | '+' | '.join(c['rating']+'；'+c['returns']+'；置信度'+c['confidence'] for c in row)+' |')
    out += ['', f'来源：[冻结报告](<{ROOT.as_posix()}/报告快照/{t}.md:{mat[0][0]["line"]}>)。']
(ROOT / '97家公司条件建议全表.md').write_text('\n'.join(out)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in stats.items() if k not in ['grid','same_rating_across_times']}, ensure_ascii=False, indent=2))
for g in grid:
    print(g['scenario'], g['time'], [g['counts'].get(r,0) for r in RATINGS], '正面',g['positive'])
    if g['scenario']=='基准':
        print('基准正面:', {SHORT[RATINGS.index(r)]: ts for r,ts in g['groups'].items() if RATINGS.index(r)>=3})
print('同评级三期限:', {s:len(ts) for s,ts in same_time.items()})
