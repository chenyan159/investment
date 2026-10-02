from pathlib import Path
import json, re, hashlib

ROOT = Path('D:/drive/Investment')
OUT = Path(__file__).parent
PAIRS = json.loads((ROOT / '备份/全行业与八家公司运行审阅_2026-09-06/对照清单.json').read_text(encoding='utf-8-sig'))
PAIRS = [p for p in PAIRS if p['domain'] == 'company']

def numbered(path):
    return list(enumerate(path.read_text(encoding='utf-8-sig').split('\n'), 1))

inventory = []
for p in PAIRS:
    ticker = p['subject']
    row = {'ticker': ticker, 'new': str(ROOT / p['output']), 'old': str(ROOT / p['old'])}
    for label, key in [('new','output'), ('old','old')]:
        path = ROOT / p[key]
        lines = numbered(path)
        content = '\n'.join(s for _,s in lines)
        headings = [(n,s) for n,s in lines if re.match(r'^#{1,4} ',s)]
        row[label+'_chars'] = len(content)
        row[label+'_headings'] = headings
        (OUT / f'{ticker}_{label}_带行号.txt').write_text('\n'.join(f'{n}: {s}' for n,s in lines), encoding='utf-8-sig')
    inventory.append(row)
(OUT / '报告对照索引.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8-sig')
protected = [ROOT/'基本面/公司调研/研究方法/调研方案.md', ROOT/'基本面/公司调研/公司索引.md', ROOT/'分析报告/公司情景投资决策/研究方案.md']
(OUT/'只读基线哈希.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},ensure_ascii=False,indent=2),encoding='utf-8-sig')
for row in inventory:
    print(row['ticker'], row['new'])
    for n,s in row['new_headings']:
        print(f'{n}: {s}')
