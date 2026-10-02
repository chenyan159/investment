from pathlib import Path
import tomllib,hashlib,json,csv,re
ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
CONFIG=Path(r'C:\Users\cheny\.codex\automations')
# Exact user-authorized configurations only; never enumerate or read other configuration contents.
ids=['automation','ai-news-collect','ai-news-produce','automation-2','runner','project-ananta']
schedule={'automation':'weekdays 13:30','ai-news-collect':'daily 05:00','ai-news-produce':'daily 05:30','automation-2':'Saturday 08:00 (paused)','runner':'every 12 hours (paused)','project-ananta':'daily 06:00'}
roles={'automation':'current price, valuation, TTM/forward fields and coverage','ai-news-collect':'high recall signals, delta evidence, editorial candidate queue','ai-news-produce':'editorial selection, public script, audio, broadcast ledger','automation-2':'weekly frontier-person speech discovery','runner':'queue runner launcher, not research evidence','project-ananta':'ETL/build/publication verification, not new investment research'}
rows=[]
for ident in ids:
    p=CONFIG/ident/'automation.toml'; raw=p.read_bytes();obj=tomllib.loads(raw.decode('utf-8-sig'))
    rows.append(dict(id=obj['id'],name=obj['name'],kind=obj.get('kind'),status=obj['status'],configured_schedule=schedule[ident],timezone='not specified in this TOML; scheduler timezone not independently verified',model=obj.get('model'),reasoning_effort=obj.get('reasoning_effort'),config_path=p.as_posix(),config_sha256=hashlib.sha256(raw).hexdigest(),prompt_sha256=hashlib.sha256(obj['prompt'].encode('utf-8')).hexdigest(),prompt_chars=len(obj['prompt']),role=roles[ident],prompt_line=5,status_line=6))
doc={'snapshot_date':'2026-09-05','scope':'Six exact automation.toml files only. No runs, secrets, credentials, memory files, queues, processes or automation state mutations. ACTIVE/PAUSED is configuration state, not runtime success. Only whitelisted nonsecret summary fields copied.','automations':rows}
(OUT/'data').mkdir(parents=True,exist_ok=True)
(OUT/'data/peripheral_automation_config_snapshot.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'data/peripheral_automation_config_snapshot.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
people=(ROOT/'金融资料/前沿访谈/AI每日新闻重点人物与产业链跟踪清单.md').read_text(encoding='utf-8-sig')
print(json.dumps({'states':{r['id']:r['status'] for r in rows},'seed_numbered_people_rows':len(re.findall(r'^\|\s*\d+\s*\|',people,re.M))},ensure_ascii=False))
