from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads((Path(__file__).parent/'16份结果清单.json').read_text(encoding='utf-8'))
for arg in sys.argv[1:]:
 parts=arg.split(':');k=parts[0];v=d[k];a=Path(v['report']).read_text(encoding='utf-8').splitlines()
 print('REPORT '+k)
 if len(parts)==1:
  for x in v['headings']:print(str(x['line'])+': '+x['text'])
 else:
  start=int(parts[1]);end=int(parts[2]) if len(parts)>2 else start+100
  for i in range(start-1,min(end,len(a))):print(f'{i+1}: {a[i]}')
