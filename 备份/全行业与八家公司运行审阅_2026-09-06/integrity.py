exec((__import__('pathlib').Path(__file__).parent/'audit.py').read_text(encoding='utf-8'))
from urllib.parse import unquote
checks={}; dirs=sorted({str((R/s['output']).parent) for s in stats}); extras=[]; empties=[]; localbroken=[]
for d in dirs:
 for p in Path(d).iterdir():
  if p.is_file() and p.suffix.lower() not in ['.md'] and p.name.lower()!='desktop.ini':extras.append(str(p))
  if p.is_file() and p.stat().st_size==0:empties.append(str(p))
for s in stats:
 p=R/s['output']; t=p.read_text(encoding='utf-8-sig')
 for target in re.findall(r'\]\(([^\n]+?)\)',t):
  target=unquote(target.strip('<>')).split('#')[0]
  if not target or target.startswith(('https:','http:','mailto:')):continue
  if '.md' in target and not (p.parent/target).exists():localbroken.append(dict(report=s['subject'],target=target))
industry_dirs={str((R/s['output']).parent) for s in stats if s['domain']=='industry'}
industry_files=[str(p.relative_to(R)).replace('\\','/') for d in industry_dirs for p in Path(d).glob('*.md') if p.name not in ['README.md','AGENTS.md']]
expected={s['output'] for s in stats if s['domain']=='industry'}
inputs=[R/'基本面/行业调研/研究方法/行业调研方案.md',R/'基本面/公司调研/研究方法/调研方案.md',R/'基本面/行业调研/行业索引.md',R/'基本面/公司调研/公司索引.md']
inputs+=list((R/'基本面/行业调研/产业背景').rglob('*.md'))
badinput=[]
for p in inputs:
 try:
  t=p.read_text(encoding='utf-8-sig')
  if len(t)<30 or '\0' in t or '\ufffd' in t:badinput.append(str(p))
 except Exception as e:badinput.append(str(p)+':'+str(e))
checks=dict(output_dirs=len(dirs),unexpected_nonmarkdown=extras,zero_files=empties,industry_formal_files=len(industry_files),industry_extra=sorted(set(industry_files)-expected),industry_missing=sorted(expected-set(industry_files)),local_broken_links=localbroken,inputs_checked=len(inputs),input_bad=badinput)
(OUT/'目录与输入完整性.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))
sessions={}
for day in ['05','06']:
 for p in (Path('C:/Users/cheny/.codex/sessions/2026/09')/day).glob('*.jsonl'):
  sessions[p.stem[-36:]]=p
session_summary=[]
for pair in pairs:
 p=sessions.get(pair['thread']); reads=[]; utext=[]; outputs=[]
 if not p:continue
 badlines=[]; records=[]
 for line_no,line in enumerate(p.read_text(encoding='utf-8-sig').split('\n'),1):
  if not line.strip():continue
  try:records.append(json.loads(line))
  except json.JSONDecodeError:badlines.append(dict(line=line_no,chars=len(line)))
 for x in records:
  pl=x.get('payload',{})
  if x.get('type')=='response_item' and pl.get('role')=='user':
   utext.extend(c.get('text','') for c in pl.get('content',[]) if isinstance(c,dict))
  if x.get('type')=='response_item' and pl.get('type') in ['function_call','custom_tool_call']:
   a=pl.get('arguments',pl.get('input','')); a=a if isinstance(a,str) else json.dumps(a,ensure_ascii=False)
   if ('Get-Content' in a or 'read_text' in a or 'rg ' in a) and not any(z in a for z in ['apply_patch','Add File:','Update File:']):reads.append(a)
 safe=re.sub(r'[/\\ ]','_',pair['subject']);(OUT/f'{safe}_实际读取调用.json').write_text(json.dumps(reads,ensure_ascii=False,indent=2),encoding='utf-8')
 session_summary.append(dict(subject=pair['subject'],session=str(p),read_calls=len(reads),unparseable_lines=badlines))
(OUT/'会话取证.json').write_text(json.dumps(session_summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('sessions',len(session_summary))
