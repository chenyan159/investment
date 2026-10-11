import hashlib
import json
import ntpath
import pathlib
import re
import shutil
import urllib.parse

root = pathlib.Path('D:/investment')
audit = root / '备份/结果目录同级备份迁移_2026-10-11'
manifest = json.loads((audit / 'manifest.json').read_text(encoding='utf-8-sig'))
normalize = lambda value: ntpath.normcase(ntpath.normpath(str(value).replace('/', '\\')))
moved = {normalize(root / item['From']): item['To'] for item in manifest['Moves']}
records = []
for item in manifest['FormalBefore']:
    file = root / item['Path']
    original = file.read_bytes()
    text = original.decode('utf-8')
    links = []

    def repair(match):
        literal = match.group(1)
        target = urllib.parse.unquote(literal.strip('<>')).replace('file:///', '')
        if target.startswith(('/D:', '/d:')):
            target = target[1:]
        if re.match(r'https?://', target):
            return match.group(0)
        target = target.split('#')[0]
        target = re.sub(r':\d+(?::\d+)?$', '', target)
        absolute = target if ntpath.isabs(target) else file.parent / target
        destination = moved.get(normalize(absolute))
        if not destination:
            return match.group(0)
        if not (root / destination).is_file():
            raise RuntimeError('Missing migrated reference: ' + destination)
        replacement = ntpath.relpath(str(root / destination), str(file.parent)).replace('\\', '/')
        links.append({'From': literal, 'To': replacement})
        return '](' + replacement + ')'

    updated = re.sub(r'\]\(([^\n]+?)\)', repair, text)
    if not links:
        continue
    before = hashlib.sha256(original).hexdigest().upper()
    if before != item['Sha256']:
        raise RuntimeError('Report changed since migration: ' + item['Path'])
    saved = file.parent.parent / '备份/引用修复前_2026-10-11' / file.name
    if saved.exists():
        raise RuntimeError('Original backup already exists: ' + str(saved))
    saved.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, saved)
    payload = updated.encode('utf-8')
    record = {'Path': item['Path'], 'OriginalBackup': saved.relative_to(root).as_posix(),
              'BeforeSha256': before, 'AfterSha256': hashlib.sha256(payload).hexdigest().upper(), 'Links': links}
    records.append(record)
    # Persist provenance before replacing references; original report bytes remain in the backup.
    (audit / 'link-repairs.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    file.write_bytes(payload)
    assert saved.read_bytes() == original
    assert file.read_bytes() == payload
shutil.copy2(__file__, audit / pathlib.Path(__file__).name)
print(json.dumps({'reports_repaired': len(records), 'links_repaired': sum(len(r['Links']) for r in records)}))
