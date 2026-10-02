from pathlib import Path
import csv, hashlib, json, shutil

ROOT = Path('D:/drive/Investment')
OUT = Path(__file__).parent
SORT = ROOT / '分析报告/公司排序'
METHODS = ROOT / '基本面/行业调研/研究方法'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest = OUT / '实施前快照.json'
    if manifest.exists():
        raise SystemExit('Snapshot already exists; refusing to overwrite baseline')
    rows = list(csv.DictReader((SORT/'00_运行与榜单注册表.csv').open(encoding='utf-8-sig')))
    protected = set()
    for rel in {r['method_path'] for r in rows}:
        protected.update(p for p in (SORT/rel/'迭代版本').rglob('*') if p.is_file())
    for rel in ['备份/24家公司最新投资价值多情景评估_2026-08-19',
                '基本面/tmp/research-runner-prompts/2026-08-18',
                '基本面/行业调研/产业背景']:
        protected.update(p for p in (ROOT/rel).rglob('*') if p.is_file())
    for name in ['00_运行与榜单注册表.csv','00_当前评估.json','00_站点发布策略.csv',
                 '00_方案状态总表.csv','站点数据/current.json']:
        protected.add(SORT/name)
    editable = sorted(METHODS.glob('产业背景：*.md')) + [METHODS/'会议调研方案.md',
        SORT/'AGENTS.md',SORT/'00_总索引.md',SORT/'91_通用研究方案/README.md']
    for p in editable:
        dest = OUT/'原文件备份'/p.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    payload = {'date':'2026-09-07','protected':[{'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p)} for p in sorted(protected)],
        'editable':[{'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p)} for p in editable]}
    manifest.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print({'protected':len(protected),'backed_up':len(editable)})

if __name__ == '__main__':
    main()
