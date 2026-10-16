import csv, json, hashlib
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
FILES = ['X1_event', 'X2_ai', 'X3_clinical', 'X4_space_energy', 'X5_reverse']
universe = json.loads((ROOT / '01_inputs/universe.json').read_text(encoding='utf-8-sig'))
tickers = {x['ticker'] for x in universe}
records = {x['ticker']: {'ticker': x['ticker'], 'name': x['name'], 'category': x['category'],
                         'anchor': x['finance'].get('最新价格'), 'nominations': [], 'reserves': [],
                         'deep_read_roles': [], 'screen_roles': []} for x in universe}
seals, roles = [], []
for stem in FILES:
    p = ROOT / '02_round1' / (stem + '.json')
    if not p.exists():
        raise RuntimeError('All five independent first rounds must exist: ' + str(p))
    data = json.loads(p.read_text(encoding='utf-8-sig'))
    role = data.get('role', stem)
    noms = data['nominations']
    assert len(noms) == 20, (stem, len(noms))
    assert len({n['ticker'] for n in noms}) == 20
    for n in noms:
        assert n['ticker'] in tickers, n['ticker']
        records[n['ticker']]['nominations'].append({'role': role, 'rank': n.get('rank'), 'file': str(p.relative_to(ROOT))})
    for n in data.get('reserves', []):
        if isinstance(n, str):
            ticker = n.split(':')[0].split('：')[0].split(' ')[0]
        else:
            ticker = n.get('ticker', '')
        if ticker in tickers:
            records[ticker]['reserves'].append(role)
    for ticker in data.get('deep_read_tickers', []):
        if ticker in tickers:
            records[ticker]['deep_read_roles'].append(role)
    scan = next((ROOT / '07_logs').glob(stem.split('_')[0] + '_full245_screen.csv'))
    with scan.open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    actual = [r.get('ticker', r.get('代码', r.get('股票代号', ''))) for r in rows]
    assert len(actual) == 245 and set(actual) == tickers, (stem, len(actual), set(actual) ^ tickers)
    for t in actual:
        records[t]['screen_roles'].append(role)
    roles.append({'role': role, 'nominations': len(noms), 'deep_read_count': len(data.get('deep_read_tickers', [])),
                  'screen_rows': len(actual), 'scope': 'structured initial scan plus disclosed targeted deep reading; not 245 full manual research reports'})
    for q in [p, p.with_suffix('.md'), scan, *list((ROOT / '07_logs').glob(stem.split('_')[0] + '_sources.json')), *list((ROOT / '07_logs').glob(stem.split('_')[0] + '_reading_notes.md'))]:
        if q.exists():
            seals.append({'path': str(q.relative_to(ROOT)), 'sha256': hashlib.sha256(q.read_bytes()).hexdigest(), 'bytes': q.stat().st_size})
out = list(records.values())
selected = [r for r in out if r['nominations']]
selected.sort(key=lambda r: (-len(r['nominations']), r['ticker']))
result = {'sealed_utc': datetime.now(timezone.utc).isoformat(), 'roles': roles, 'nominated_unique': len(selected),
          'warning': 'Nomination counts are a search priority and disagreement map, not a vote-based final ranking.',
          'candidate_union': selected, 'all245': out, 'sealed_files': seals}
(ROOT / '03_round2/首轮五角色汇总.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
with (ROOT / '03_round2/首轮245家公司轨迹.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ticker','name','category','anchor','nominated_count','nomination_roles_ranks','reserves','deep_read_roles','screen_count'])
    for r in out:
        w.writerow([r['ticker'],r['name'],r['category'],r['anchor'],len(r['nominations']),'; '.join(str(n['role'])+':'+str(n['rank']) for n in r['nominations']),'; '.join(r['reserves']),'; '.join(r['deep_read_roles']),len(r['screen_roles'])])
md = ['# 五位独立研究者首轮汇总', '', '提名次数仅用于揭示共识、分歧与遗漏，不是最终名次。每位先做245家结构扫描，再作定向深读；不把自动扫描表述为逐家公司全文人工研究。', '', '|公司|价格锚|提名次数|角色及顺位|', '|---|---:|---:|---|']
for r in selected:
    md.append('|'+r['ticker']+'|'+str(r['anchor'])+'|'+str(len(r['nominations']))+'|'+', '.join(n['role']+':'+str(n['rank']) for n in r['nominations'])+'|')
md.extend(['', '五份首轮文件和扫描/来源/阅读日志已记录SHA-256。后续更新另存新轮文件，不覆盖首轮。', '', json.dumps(roles, ensure_ascii=False, indent=2)])
(ROOT / '03_round2/首轮五角色汇总.md').write_text('\n'.join(md), encoding='utf-8')
print(json.dumps({'roles': len(roles), 'universe': len(out), 'unique_nominations': len(selected), 'sealed_files': len(seals)}, ensure_ascii=False))
