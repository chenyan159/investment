from pathlib import Path
import json,csv,re,hashlib,datetime
ROOT=Path('D:/drive/Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
errors=[];links=[];hashrows=[]
def load(name): return json.loads((OUT/'data'/name).read_text(encoding='utf-8-sig'))
def addrows(rows,pathkey='path',hashkey='sha256',origin=''):
    for r in rows:
        p=Path(r[pathkey])
        if not p.is_absolute(): p=ROOT/p
        h=r[hashkey].lower()
        actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ''
        row={'source':origin,'path':p.as_posix(),'expected_sha256':h,'current_sha256':actual,'match':h==actual}
        hashrows.append(row)
        if h!=actual: errors.append({'type':'source_changed',**row})
for name in ['source_plan_code_inventory.json','queue_snapshot_meta.json','nonranking_sources_snapshot.json']:
    addrows(load(name),origin=name)
addrows(load('feature_summary.json'),pathkey='report',origin='feature_summary.json')
addrows(load('peripheral_automation_config_snapshot.json')['automations'],pathkey='config_path',hashkey='config_sha256',origin='peripheral_config')
for name,pathkey,hkey in [('company_industry_inventory.csv','path','sha256'),('decisions_current_report_inventory.csv','source_path','sha256'),('sorting_current_inventory.csv','plan_path','plan_sha256')]:
    with (OUT/'data'/name).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    addrows(rows,pathkey=pathkey,hashkey=hkey,origin=name)

docs=sorted(OUT.glob('*.md'))+sorted((OUT/'evidence').glob('*.md'))
for doc in docs:
    s=doc.read_text(encoding='utf-8-sig')
    searchable=re.sub(r'(?ms)^```[^\n]*\n.*?^```[^\n]*(?:\n|$)',lambda m: re.sub(r'[^\n]',' ',m.group(0)),s)
    for m in re.finditer(r'\]\((?:<([^>]+)>|([^\)]+))\)',searchable):
        target=(m.group(1) or m.group(2)).strip()
        if re.match(r'^(https?://|#|mailto:)',target): continue
        if target.startswith('/D:') or target.startswith('/C:'): target=target[1:]
        line=None
        suffix=re.search(r':(\d+)$',target)
        if suffix:
            line=int(suffix.group(1));target=target[:suffix.start()]
        p=Path(target)
        if not p.is_absolute(): p=doc.parent/p
        ok=p.exists()
        why=''
        if ok and line:
            sl=p.read_text(encoding='utf-8-sig').splitlines()
            ok=0<line<=len(sl) and bool(sl[line-1].strip())
            if not ok:why='line absent or blank'
        if not ok and not why:why='target missing'
        row={'document':doc.relative_to(OUT).as_posix(),'document_line':s[:m.start()].count('\n')+1,'target':p.as_posix(),'target_line':line,'valid':ok,'reason':why}
        links.append(row)
        if not ok:errors.append({'type':'link',**row})

def savecsv(name,rows):
    with (OUT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
savecsv('delivery_source_hash_validation.csv',hashrows)
savecsv('delivery_link_validation.csv',links)
summary={'validated_at':datetime.datetime.now().astimezone().isoformat(),'documents':len(docs),'markdown_links_checked':len(links),'invalid_links':sum(not r['valid'] for r in links),'source_hash_checks':len(hashrows),'unique_source_paths':len(set(r['path'].lower() for r in hashrows)),'source_mismatches':sum(not r['match'] for r in hashrows),'scope':'Checks source snapshots and local citations; not all external facts, not runtime/new strategy validation. Only audit artifacts written.','errors':errors}
(OUT/'data/delivery_validation_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
