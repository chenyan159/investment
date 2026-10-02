from pathlib import Path
from urllib.parse import unquote
import csv,re,json,collections
ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
reports=list(csv.DictReader((OUT/'data/company_industry_inventory.csv').open(encoding='utf-8-sig')))
rows=[]
for r in reports:
    if not r['path']: continue
    p=Path(r['path']); txt=p.read_text(encoding='utf-8-sig')
    for m in re.finditer(r'\]\((<[^>\n]+>|[^)\n]+)\)',txt):
        raw=m.group(1).strip().strip('<>')
        if re.match(r'^(?:https?://|#|mailto:)',raw,re.I):continue
        target=unquote(raw.split('#',1)[0])
        target=re.sub(r':\d+$','',target)
        if not target.lower().endswith('.md'):continue
        dst=Path(target.replace('/','\\'))
        if not dst.is_absolute():dst=p.parent/dst
        dst=dst.resolve()
        # Only plain Markdown file targets without a Markdown title; no inference about unsupported links.
        rows.append(dict(domain=r['domain'],subject=r['subject'],report_path=str(p),line=txt[:m.start()].count('\n')+1,target_raw=raw,resolved_path=str(dst),exists=dst.is_file()))
with (OUT/'data/company_industry_local_links.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
stats={}
for domain in ['company','industry']:
    rr=[r for r in rows if r['domain']==domain]; bad=[r for r in rr if not r['exists']]
    stats[domain]={'reports_indexed':sum(r['domain']==domain for r in reports),'reports_with_parsed_local_md_links':len(set(r['report_path'] for r in rr)),'parsed_local_md_link_occurrences':len(rr),'nonresolving_occurrences':len(bad),'reports_with_nonresolving_links':len(set(r['report_path'] for r in bad)),'unique_nonresolving_targets':len(set(r['resolved_path'] for r in bad))}
stats['scope']='Markdown inline links with local .md target (optional fragment or :line suffix), unquoted title unsupported; repeated occurrences counted; existence checked 2026-09-05. Broken link is retrieval failure, not proof cited facts wrong or files absent from backups.'
(OUT/'data/company_industry_local_links_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
archive_index=collections.defaultdict(list)
for p in (ROOT/'基本面/行业调研').rglob('*.md'):
    if '备份' in p.parts: archive_index[p.name].append(str(p))
targets=collections.Counter(r['resolved_path'] for r in rows if not r['exists'])
backup_rows=[dict(target=k,occurrences=v,backup_matches=len(archive_index[Path(k).name]),backup_path=';'.join(archive_index[Path(k).name])) for k,v in targets.items()]
with (OUT/'data/company_industry_broken_target_backups.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['target','occurrences','backup_matches','backup_path']);w.writeheader();w.writerows(backup_rows)
print(json.dumps(stats,ensure_ascii=False,indent=2))
