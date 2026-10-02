from pathlib import Path
import csv,hashlib,json
ROOT=Path('D:/drive/Investment');OUT=Path(__file__).parent;SORT=ROOT/'分析报告/公司排序';BASE=ROOT/'基本面/行业调研/研究方法'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg=SORT/'00_待运行研究方案注册表.csv';rows=list(csv.DictReader(reg.open(encoding='utf-8-sig')))
for r in rows:
    if not r['prompt_file']:continue
    p=ROOT/r['prompt_file'];s=p.read_text(encoding='utf-8')
    s=s.replace('本方法的独特问题见下一节。','本方法的独特问题见“本方法”部分。')
    marker='前30家公司是重点研究对象，前20要优先深入核验，但不要求买足30只，也不要求两种期限的次序一致。'
    if '目标日按T之后3个、6个自然月计算' not in s:
        s=s.replace(marker,marker+'目标日按T之后3个、6个自然月计算并写明日期；回测目标日非交易日时使用其后首个有效交易日，资料截止与可执行入场时点另列。')
    p.write_text(s,encoding='utf-8');r['sha256']=sha(p)
with reg.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'排序新版本清单.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
reg=BASE/'会议/00_会议方案注册表.json';cs=json.loads(reg.read_text(encoding='utf-8'))
for r in cs:
    p=ROOT/r['prompt_file'];s=p.read_text(encoding='utf-8').replace('的专项研究重点','的专属研究重点')
    p.write_text(s,encoding='utf-8');r['sha256']=sha(p)
reg.write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'会议新版本清单.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding='utf-8')
cases=[{'runId':f'sorting-{r["method_id"]}-{r["version_id"]}','promptFile':r['prompt_file'],'expectedOutputDir':r['expected_output_dir'],'expectedOutputFile':r['expected_output_file']} for r in rows if r['prompt_file']]
cases += [{'runId':f'conference-{r["conference"]}-{r["version"]}','promptFile':r['prompt_file'],'expectedOutputDir':r['expected_output_dir']} for r in cs]
cases += [{'runId':f'background-{i}-2026-09-07','promptFile':p.relative_to(ROOT).as_posix(),'expectedOutputDir':'基本面/行业调研/产业背景'} for i,p in enumerate(sorted(BASE.glob('产业背景：*.md')),1)]
cases += [{'runId':'conference-generic-2026-09-07','promptFile':(BASE/'会议调研方案.md').relative_to(ROOT).as_posix(),'expectedOutputDir':'基本面/行业调研/产业背景/顶级会议信息'}]
(OUT/'入口预检用例.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
print({'sorting':len(rows),'conference':len(cs),'runtime_cases':len(cases)})
