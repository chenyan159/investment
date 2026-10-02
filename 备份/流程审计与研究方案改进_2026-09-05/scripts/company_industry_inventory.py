from pathlib import Path
import re,csv,json,hashlib,collections,statistics
ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
(OUT/'data').mkdir(parents=True,exist_ok=True)
rows=[]
for domain,folder,indexfile,pattern in [('company','公司调研','公司索引.md',r'^\| ([A-Z0-9.\-]+) \| (.*?) \| `([^`]+)/` \|'),('industry','行业调研','行业索引.md',r'^\| (.*?) \| `([^`]+)/` \|')]:
    base=ROOT/'基本面'/folder
    idx=(base/indexfile).read_text(encoding='utf-8-sig')
    for m in re.finditer(pattern,idx,re.M):
        if domain=='company': subject,name,cat=m.groups()
        else: subject,cat=m.groups();name=subject
        candidates=[]
        for p in (base/cat).glob('*.md'):
            d=re.search(r'_(\d{4}-\d{2}-\d{2})\.md$',p.name)
            if not d: continue
            if domain=='company': matched=p.name.startswith(subject+'_') and '_公司调研_' in p.name
            else:
                canonical=lambda s: re.sub(r'[\s_\-—–、,，/／\\()（）]+','',s).lower()
                matched=canonical(re.sub(r'_\d{4}-\d{2}-\d{2}\.md$','',p.name).removeprefix('行业调研_'))==canonical(subject)
            if matched:candidates.append((d.group(1),p))
        candidates.sort(key=lambda x:(x[0],str(x[1])))
        date,p=candidates[-1] if candidates else ('',None)
        txt=p.read_text(encoding='utf-8-sig') if p else ''
        rows.append(dict(domain=domain,subject=subject,name=name,category=cat,index_line=idx[:m.start()].count('\n')+1,current_direct_files=len(candidates),report_date=date,path=str(p) if p else '',sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p else '',lines=len(txt.splitlines()),chars=len(txt),urls=len(re.findall(r'https?://',txt))))
with (OUT/'data/company_industry_inventory.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
stats={}
for domain in ['company','industry']:
    rr=[r for r in rows if r['domain']==domain]
    stats[domain]={'indexed':len(rr),'with_current_direct_file':sum(bool(r['path']) for r in rr),'categories':dict(collections.Counter(r['category'] for r in rr)),'dates':dict(sorted(collections.Counter(r['report_date'] for r in rr).items())),'chars_total':sum(r['chars'] for r in rr),'median_chars':statistics.median(r['chars'] for r in rr),'max_chars':max(r['chars'] for r in rr),'zero_or_multiple_file_subjects':[r['subject'] for r in rr if r['current_direct_files']!=1]}
stats['scope']='2026-09-05 snapshot; indexed subjects; category-direct dated formal .md only, exclude backup/tmp; report filename date is not evidence freshness; byte hashes recorded, no semantic prevalence inferred.'
(OUT/'data/company_industry_inventory_summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
