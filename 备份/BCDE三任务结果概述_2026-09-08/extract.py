from pathlib import Path
import re,json,csv,hashlib
ROOT=Path('D:/drive/Investment');OUT=Path(__file__).resolve().parent
rows=list(csv.DictReader((ROOT/'分析报告/公司排序/00_待运行研究方案注册表.csv').open(encoding='utf-8-sig',newline='')))
data={}
for eid in ['E04','E05','E06']:
 r=next(x for x in rows if x['method_id']==eid);p=ROOT/r['expected_output_file'];t=p.read_text(encoding='utf-8');lines=t.splitlines()
 pattern=r'^### 5\.\d+ ([A-Z0-9.]+) —' if eid=='E04' else (r'^### \d+\. ([A-Z0-9.]+) —' if eid=='E05' else r'^### \d+\. ([A-Z0-9.]+)｜')
 focused=re.findall(pattern,t,re.M);assert len(focused)==len(set(focused))==30,(eid,focused)
 start=next(i for i,l in enumerate(lines) if l.startswith('## ') and ('193行' in l or '193家公司完整覆盖' in l or '八、全样本覆盖清单' in l))
 end=next(i for i in range(start+1,len(lines)) if lines[i].startswith('## '))
 table=[l for l in lines[start:end] if l.startswith('|')]
 assert len(table)-2==193,(eid,len(table))
 data[eid]={'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'lines':len(lines),'focus30':focused,'coverage_rows':len(table)-2,'control_result_exists':(ROOT/r['control_expected_output_file']).exists(),'headings':[{'line':i+1,'heading':l} for i,l in enumerate(lines) if l.startswith('## ')]}
pairs=[]
for a,b in [('E04','E05'),('E04','E06'),('E05','E06')]:
 x=set(data[a]['focus30']);y=set(data[b]['focus30']);pairs.append({'a':a,'b':b,'overlap':len(x&y),'common':sorted(x&y),'a_only':sorted(x-y),'b_only':sorted(y-x)})
result={'reports':data,'focus_overlap':pairs,'focus_union':len(set().union(*(set(v['focus30']) for v in data.values())))}
(OUT/'结果结构与交集核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'coverage':{k:v['coverage_rows'] for k,v in data.items()},'controls_exist':{k:v['control_result_exists'] for k,v in data.items()},'focus':{k:v['focus30'] for k,v in data.items()},'pairs':pairs,'union':result['focus_union']},ensure_ascii=False,indent=2))
