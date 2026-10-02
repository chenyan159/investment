from pathlib import Path
from collections import Counter
import json,re,sys
OUT=Path(__file__).parent
DATA=OUT/'提取数据.json'
reports=json.loads(DATA.read_text(encoding='utf-8'))
labels=['强烈不建议投资','不建议投资','强烈建议投资','谨慎建议投资','建议投资','中性 / 等待','中性／等待','中性/等待','中性','等待']
def label(c):
    for l in labels:
        if l in c:return l.replace('／','/').replace(' ','')
    return c.split('｜')[0]
def normalize():
    for r in reports:
        r['matrices']=[m for m in r['matrices'] if sum(bool(re.search('投资|不投|谨慎|中性|建议|等待|回避',c)) for row in m['rows'][1:] for c in row[1:])==12]
    DATA.write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
    s=json.loads((OUT/'运行与文件核对.json').read_text(encoding='utf-8'));s['matrixCounts']=dict(Counter(len(r['matrices']) for r in reports))
    (OUT/'运行与文件核对.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 已完成报告：原文条件矩阵','',f"固定审查时点：{s['cutoff']}；共{len(reports)}家公司。每格是报告原文的条件价值判断，不是当前实际投资建议。",'']
    for r in reports:
        lines += [f"## {r['subject']} — {r['displayName']}",'',f"[{r['cohort']}；完成于{r['finishedAt']}](D:/drive/Investment/{r['outputFile']})",'']
        for m in r['matrices']:lines += [m['raw'],'']
    (OUT/'全部公司原文条件矩阵.md').write_text('\n'.join(lines),encoding='utf-8')
    print('COUNTS',s['matrixCounts'])
def digest(lo,hi):
    for i,r in enumerate(reports[lo:hi],lo):
        print(f"\n[{i}] {r['subject']} {r['displayName']} ({r['category']})")
        # Narrative opening and the actual decision column preserve qualifications.
        print(r['digest'][:1050])
        if r['actionTables']:
            t=r['actionTables'][0]
            print('CURRENT_TABLE',t['line'],t['rows'][0])
            for row in t['rows'][1:]: print(' | '.join(row[:2])[:500])
        for m in r['matrices']:
            for row in m['rows'][1:]:print('MATRIX',' / '.join(row))
def selected(tickers):
    for r in reports:
        if r['subject'] in tickers:
            print('\n'+r['subject']+'\n'+r['opening'])
def scan(lo,hi):
    for i,r in enumerate(reports[lo:hi],lo):
        print(f"\n[{i}] {r['subject']} {r['displayName']}")
        paras=[p for p in r['opening'].split('\n\n') if p.startswith('**') and any(k in p for k in ['当前','建议','选择','现价'])]
        print((paras[0] if paras else r['digest'])[:650])
        if r['actionTables']:
            for row in r['actionTables'][0]['rows'][1:]:print('ACT',' | '.join(row[:2])[:340])
        m=r['matrices'][0]['rows']
        print('BASE',' / '.join(m[2][1:]))
        print('OPT',' / '.join(m[3][1:]))
        print('BREAK_3Y',m[4][3])
def stats():
    output={}
    for s in range(4):
        for h in range(3):
            vals=[(r['subject'],r['matrices'][0]['rows'][s+1][h+1]) for r in reports]
            output[f'{s}/{h}']={'counts':dict(Counter(label(c) for _,c in vals)),'positive':[t for t,c in vals if label(c) in ['强烈建议投资','建议投资','谨慎建议投资']]}
    (OUT/'矩阵统计.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='normalize':normalize()
    elif cmd=='digest':digest(int(sys.argv[2]),int(sys.argv[3]))
    elif cmd=='opening':selected(sys.argv[2:])
    elif cmd=='scan':scan(int(sys.argv[2]),int(sys.argv[3]))
    elif cmd=='stats':stats()
