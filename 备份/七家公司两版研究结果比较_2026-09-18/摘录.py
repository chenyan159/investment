from pathlib import Path
import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
manifest=json.loads((Path(__file__).parent/'版本配对与哈希.json').read_text(encoding='utf-8'))
args=sys.argv[1:]
assert len(args)%5==0
for offset in range(0,len(args),5):
    ticker,kind,version,start,end=args[offset:offset+5]
    p=Path(manifest[ticker][kind][version]['path'])
    lines=p.read_text(encoding='utf-8-sig').splitlines()
    print('\n'+ticker+' '+kind+' '+version+' '+p.name)
    if start=='find':
        selected=((i,l) for i,l in enumerate(lines,1) if re.search(end,l))
    else:
        selected=((i+1,lines[i]) for i in range(int(start)-1,min(int(end),len(lines))))
    for i,line in selected: print(str(i)+': '+line)
