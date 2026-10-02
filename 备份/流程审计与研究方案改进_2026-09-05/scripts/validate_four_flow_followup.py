from pathlib import Path
import json,re,hashlib,datetime
ROOT=Path('D:/drive/Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
data=OUT/'data'
prior={'validated_at':'2026-09-05T01:44:31.950777-07:00','documents':10,'markdown_links_checked':589,'invalid_links':0,'source_hash_checks':1169,'unique_source_paths':1141,'source_mismatches':0,'scope':'Prior completed delivery check; preserved from the verified tool result before the later user follow-up. Not a current-state claim.','errors':[]}
(data/'delivery_validation_summary_2026-09-05T014431.json').write_text(json.dumps(prior,ensure_ascii=False,indent=2),encoding='utf-8')
current=json.loads((data/'delivery_validation_summary.json').read_text(encoding='utf-8'))
(data/'delivery_validation_summary_followup_2026-09-05.json').write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf-8')
relocated=[]
for r in current['errors']:
    if r.get('type')!='source_changed' or r.get('current_sha256')!='':continue
    p=Path(r['path'])
    hits=list((p.parent/'备份').rglob(p.name))
    matching=[x for x in hits if hashlib.sha256(x.read_bytes()).hexdigest()==r['expected_sha256']]
    relocated.append({'old_path':p.as_posix(),'expected_sha256':r['expected_sha256'],'matching_backup_paths':[x.as_posix() for x in matching]})
doc=OUT/'05_四类流程修改与文件整理详细建议.md'
s=doc.read_text(encoding='utf-8')
links=[]
for m in re.finditer(r'\]\(<([^>]+)>\)',s):
    target=m.group(1); line=None
    hit=re.search(r':(\d+)$',target)
    if hit:line=int(hit.group(1));target=target[:hit.start()]
    p=Path(target);valid=p.exists()
    if valid and line:
        rows=p.read_text(encoding='utf-8-sig').splitlines()
        valid=0<line<=len(rows) and bool(rows[line-1].strip())
    links.append({'target':target,'line':line,'valid':valid})
out={'checked_at':datetime.datetime.now().astimezone().isoformat(),'document':doc.as_posix(),'links':links,'invalid_links':sum(not r['valid'] for r in links),'relocated_source_reports':relocated,'note':'The global audit check at 12:14 found source/queue changes since 01:44. Six missing company/industry report paths were resolved to identical archived bytes. This follow-up only writes audit artifacts; it does not modify running research, source reports, queue or historical report text. Original 01:44 validation summary preserved separately; current validation must not be described as all sources unchanged.'}
(data/'four_flow_followup_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_document_links':len(links),'invalid_links':out['invalid_links'],'relocated_reports':len(relocated),'all_relocated_hash_match':all(len(r['matching_backup_paths'])==1 for r in relocated)},ensure_ascii=False))
