"""Assemble source records without upgrading inherited/excerpt access to full reads."""
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '06_final'
OUT.mkdir(exist_ok=True)

def walk_records(value):
    if isinstance(value, list):
        for entry in value:
            yield from walk_records(entry)
    elif isinstance(value, dict):
        url = value.get('url') or value.get('source_url')
        if isinstance(url, str) and url.startswith('http'):
            yield value
        else:
            for entry in value.values():
                if isinstance(entry, (dict, list)):
                    yield from walk_records(entry)

records = []
for path in sorted((ROOT / '07_logs').glob('*sources.json')):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    for i, entry in enumerate(walk_records(data), 1):
        records.append({
            'record_id': f'{path.stem}:{entry.get("id", i)}',
            'role_log': path.relative_to(ROOT).as_posix(),
            'url': entry.get('url', entry.get('source_url')),
            'access_status_original': entry.get('access_status', entry.get('access', '未结构化标明，查原日志')),
            'original_record': entry,
        })

# Controller prose is preserved as prose: a URL citation alone is not an opened source.
controller_refs = []
for path in sorted((ROOT / '04_verification').glob('控制器*.md')):
    body = path.read_text(encoding='utf-8')
    urls = list(dict.fromkeys(re.findall(r'https?://[^\s\)\]>`]+', body)))
    for url in urls:
        controller_refs.append({'url': url, 'memo': path.relative_to(ROOT).as_posix(),
            'access_status': '详见原核验备忘录：引用本身不代表全文打开',
            'not_counted_as_new_independent_access': True})

by_url = {}
for rec in records:
    by_url.setdefault(rec['url'], []).append(rec['record_id'])
report = {
    'built_utc': datetime.now(timezone.utc).isoformat(),
    'source_record_count': len(records),
    'unique_logged_urls': len(by_url),
    'controller_memo_reference_count': len(controller_refs),
    'unique_controller_urls': len({x['url'] for x in controller_refs}),
    'unique_urls_all_references': len(set(by_url) | {x['url'] for x in controller_refs}),
    'interpretation': '记录数是角色访问/引用记录，不是独立事实数量，也不是全部读过全文。搜索片段、失败、继承、原始公告、外部意见分别保留原字段。同一事件多家转载不增加事件独立性。',
    'access_status_counts': dict(Counter(str(x['access_status_original']) for x in records)),
    'records': records,
    'controller_memo_references': controller_refs,
    'url_to_record_ids': by_url,
}
(OUT / '外部来源总索引.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
lines = ['# 外部来源总索引', '', report['interpretation'], '',
    f'角色日志记录 {len(records)} 条；去重URL {len(by_url)} 个。另保留控制器备忘录引用 {len(controller_refs)} 条；合并去重URL {report["unique_urls_all_references"]} 个。', '',
    '## 角色日志', '', '|记录|访问原始标记|链接|', '|---|---|---|']
for rec in records:
    status = str(rec['access_status_original']).replace('|','/').replace('\n',' ')
    lines.append(f'|{rec["record_id"]}|{status}|[来源]({rec["url"]})|')
lines += ['', '## 控制器补充备忘录', '', '以下只统计引用，不把它们自动计为新一次阅读全文。', '']
for path in sorted((ROOT / '04_verification').glob('控制器*.md')):
    lines.append(f'- [{path.stem}]({path.as_posix()})')
(OUT / '外部来源总索引.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ['source_record_count','unique_logged_urls','unique_urls_all_references']}, ensure_ascii=False))
