"""Read-only integrity checks; output stays in this experiment."""
from pathlib import Path
import hashlib, json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = Path('D:/investment')
OLD = ROOT.parent / '2026-10-12_20家公司多角色实验'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def check(base, entries):
    bad = []
    for e in entries:
        p = base / e['path']
        if not p.is_file():
            bad.append({'path':e['path'], 'status':'missing'})
        else:
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if h != e['sha256']:
                bad.append({'path':e['path'], 'status':'hash_changed', 'actual_sha256':h})
    return {'checked':len(entries),'unchanged':len(entries)-len(bad),'differences':bad}

old = read(ROOT/'00_control/previous_experiment_preservation_manifest.json')
core = read(ROOT/'00_control/input_manifest.json')
extra = read(ROOT/'00_control/extra_inputs_manifest.json')
round1 = read(ROOT/'03_round2/首轮五角色汇总.json')['sealed_files']
result = {
    'checked_utc':datetime.now(timezone.utc).isoformat(),
    'previous_experiment':check(OLD,old),
    'frozen_core':check(ROOT/'01_inputs/frozen',core),
    'frozen_extra':check(ROOT/'01_inputs/frozen',extra),
    'upstream_core_current':check(UPSTREAM,core),
    'upstream_extra_current':check(UPSTREAM,extra),
    'sealed_round1':check(ROOT,round1),
    'note':'An upstream difference may be another writer; frozen hashes remain the research version. This audit itself writes only this JSON in the experiment.'
}
(ROOT/'00_control/preservation_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:{'checked':v['checked'],'differences':len(v['differences'])} for k,v in result.items() if isinstance(v,dict)},ensure_ascii=False))
