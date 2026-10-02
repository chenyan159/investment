from pathlib import Path
import json,hashlib,re,collections,sys,subprocess
sys.stdout.reconfigure(encoding='utf-8')
out=Path(__file__).parent
data=json.loads((out/'analysis_data.json').read_text(encoding='utf-8'))
changed=[d['ticker'] for d in data if hashlib.sha256(Path(d['file']).read_bytes()).hexdigest()!=d['sha256']]
assert not changed,changed
assert len({d['ticker'] for d in data})==193
assert all(len({(c['scenario'],c['months']) for c in d['cells']})==12 for d in data)
assert all(d.get('anchor_price',0)>0 for d in data)
assert sum(any('rebased_low' in c for c in d['cells']) for d in data)==191
vis=Path(r'C:\Users\cheny\.codex\visualizations\2026\09\09\01a08863-4bd3-72f1-9e37-058d18265914\scenario-opportunity-map.html').read_text(encoding='utf-8')
v=json.loads(re.search(r'id="scenario-data-193">(.*?)</script>',vis,re.S)[1])
assert len(v)==193 and '__SCENARIO_DATA__' not in vis
work=out/'tmp';work.mkdir(exist_ok=True)
script=work/'visual-script-check.js'
script.write_text('\n'.join(re.findall(r'<script>(.*?)</script>',vis,re.S)),encoding='utf-8')
subprocess.run(['node','--check',str(script)],check=True)
bad=[]
for f in out.glob('*.md'):
    for path in re.findall(r'\]\(<([A-Z]:/[^>]+)>\)',f.read_text(encoding='utf-8')):
        if not Path(re.sub(r':\d+$','',path)).exists(): bad.append((f.name,path))
assert not bad,bad
r={'companies':193,'cells':2316,'source_hash_mismatches':changed,'anchors_verified':193,'rebased_companies':191,'missing_same_day_quotes':['MICLF','SPACEX'],'visual_points':len(v),'javascript_syntax':'passed','local_broken_links':bad,'confidence_counts':dict(collections.Counter(c['text'].split('｜')[-1] for d in data for c in d['cells']))}
(out/'verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=False))
print('FILES',[(f.name,f.stat().st_size) for f in out.glob('*.md')])
