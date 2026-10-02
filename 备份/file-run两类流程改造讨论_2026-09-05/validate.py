from pathlib import Path
import json,csv,re,hashlib,statistics,datetime
from decimal import Decimal
R=Path('D:/drive/Investment');O=Path(__file__).parent;issues=[];links=[];hashchecks=[]
for d in O.glob('*.md'):
    s=d.read_text(encoding='utf-8');mask=re.sub(r'(?ms)^```[^\n]*\n.*?^```[^\n]*(?:\n|$)',lambda m:re.sub(r'[^\n]',' ',m[0]),s)
    for m in re.finditer(r'\]\((?:<([^>]+)>|([^\)]+))\)',mask):
        dest=m[1] or m[2]
        if dest.startswith(('http','#')):continue
        dest=re.sub(r'^/([CD]:)',r'\1',dest);q=re.search(r':(\d+)$',dest);n=int(q[1]) if q else None;p=Path(dest[:q.start()] if q else dest)
        ok=p.is_file()
        if ok and n:
            ls=p.read_text(encoding='utf-8-sig').splitlines();ok=0<n<=len(ls) and bool(ls[n-1].strip())
        row={'doc':d.name,'doc_line':s[:m.start()].count('\n')+1,'path':str(p),'target_line':n,'valid':ok};links.append(row)
        if not ok:issues.append(row)
for manifest in ['来源快照.json','讨论引用源快照.json']:
    for r in json.loads((O/'data'/manifest).read_text(encoding='utf-8')):
        p=Path(r['path'])
        # New discussion artifacts may be edited during proofreading, not protected upstream.
        if O in p.parents:continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest();ok=actual==r['sha256'];hashchecks.append({'path':str(p),'unchanged':ok})
        if not ok:issues.append({'changed_source':str(p)})
# Check registered July source plans still match the audited exact revisions.
with (R/'备份/流程审计与研究方案改进_2026-09-05/data/sorting_current_inventory.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        p=Path(r['plan_path']);ok=hashlib.sha256(p.read_bytes()).hexdigest()==r['plan_sha256'];hashchecks.append({'path':str(p),'matches_prior_revision':ok})
        if not ok:issues.append({'plan_changed_since_previous_audit':str(p)})
# Independent Decimal replay of the 24 next-open adjusted returns.
with (R/'备份/项目反思_2026-09-04/data/daily_prices.csv').open(encoding='utf-8-sig') as f:
    rows={(r['symbol'],r['date']):r for r in csv.DictReader(f) if r['date'] in ['2026-08-20','2026-09-04']}
with (O/'data/专项24公司逐股回测.csv').open(encoding='utf-8-sig') as f: test=list(csv.DictReader(f))
errs=[]
for r in test:
    a=rows[r['ticker'],'2026-08-20'];b=rows[r['ticker'],'2026-09-04'];start=Decimal(a['open'])*Decimal(a['adj_close'])/Decimal(a['close']);v=Decimal(b['adj_close'])/start-1
    errs.append(abs(float(v)-float(r['ret_0820_open'])))
assert max(errs)<1e-12
summary={'checked_at':datetime.datetime.now().astimezone().isoformat(),'local_links':len(links),'invalid_links':sum(not x['valid'] for x in links),'source_hash_checks':len(hashchecks),'special_return_independent_decimal_checks':len(errs),'max_return_difference':max(errs),'issues':issues,'scope':'Only referenced sources and fixed historical revisions checked; no claim that the entire live project stopped changing.'}
(O/'data/交付核验.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
