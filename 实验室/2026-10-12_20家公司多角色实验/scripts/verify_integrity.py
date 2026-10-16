"""Read-only hash verification of frozen inputs and original source files."""
import datetime, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM=Path('D:/investment')
manifest=json.loads((ROOT/'00_control/input_manifest.json').read_text(encoding='utf-8-sig'))
def check(base):
    failures=[]
    for row in manifest:
        path=base/row['path']
        if not path.exists():failures.append({'path':row['path'],'status':'missing'});continue
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=row['sha256']:failures.append({'path':row['path'],'status':'hash_changed','expected':row['sha256'],'actual':actual})
    return failures
sealed=json.loads((ROOT/'03_round2/round1_union.json').read_text(encoding='utf-8-sig'))
blind=[]
for row in sealed['reports']:
    path=ROOT/'02_round1'/row['file']
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=row['sha256']:blind.append({'file':row['file'],'expected':row['sha256'],'actual':actual})
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_files':len(manifest),'frozen_copy_failures':check(ROOT/'01_inputs/frozen'),'upstream_changes_since_freeze':check(UPSTREAM),'sealed_blind_report_changes':blind,'scope_note':'Hashes prove the enumerated945 source files and five sealed blind reports stayed identical if all lists empty. This is not an OS-wide write audit; all task-controlled paths were restricted to the laboratory.'}
(ROOT/'00_control/integrity_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
