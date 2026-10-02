from pathlib import Path
from datetime import datetime
from collections import Counter
import json, re, hashlib, shutil, statistics

ROOT = Path(r'D:\drive\Investment')
OUT = Path(__file__).parent
def read_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def clean(s):
    return re.sub(r'[*`]', '', s).replace('<br>','; ').strip()
def cells(line):
    return [clean(c) for c in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
def tables(lines):
    out=[]; block=[]; start=0
    for i,line in enumerate(lines+['']):
        if line.lstrip().startswith('|'):
            if not block:start=i+1
            block.append(line)
        elif block:
            out.append({'line':start,'rows':[cells(x) for x in block if not re.fullmatch(r'[\s|:\-]+',x)],'raw':'\n'.join(block)})
            block=[]
    return out
def sha(data):return hashlib.sha256(data).hexdigest().upper()

if __name__=='__main__':
    active=read_jsonl(ROOT/'tools/queue.jsonl')
    done=read_jsonl(ROOT/'tools/queue.done.jsonl')
    selected=[x for x in done if x.get('domain')=='company-investment-decision' and x.get('finishedAt','')>='2026-09-08 18:50:00']
    latest={}
    for x in sorted(selected,key=lambda x:x['finishedAt']):latest[x['subject']]=x
    batch=[x for x in active+done if x.get('domain')=='company-investment-decision' and x.get('createdAt','').startswith('2026-09-08T22:52')]
    snapshot=OUT/'报告快照';snapshot.mkdir(exist_ok=True)
    plan=(ROOT/'分析报告/公司情景投资决策/研究方案.md').read_text(encoding='utf-8-sig').strip()
    (OUT/'研究方案快照.md').write_text(plan+'\n',encoding='utf-8')
    session_files=[]
    for day in ['08','09']:
        p=Path(r'C:\Users\cheny\.codex\sessions\2026\09')/day
        if p.exists():session_files.extend(p.glob('*.jsonl'))
    by_id={p.stem[-36:]:p for p in session_files}
    reports=[]
    for x in sorted(latest.values(),key=lambda x:x['finishedAt']):
        p=ROOT/x['outputFile']; data=p.read_bytes() if p.exists() else b''
        raw=data.decode('utf-8-sig'); lines=raw.splitlines(); ts=tables(lines)
        mats=[]
        for t in ts:
            if len(t['rows'])==5 and len(t['rows'][0])==4 and all(any(k in r[0] for r in t['rows'][1:]) for k in ['悲观','基准','乐观','突破']) and sum(bool(re.search('投资|不投|谨慎|中性|建议|等待|回避',c)) for row in t['rows'][1:] for c in row[1:])==12:mats.append(t)
        details=[t for t in ts if len(t['rows'])>=13 and any('建议' in h or '评级' in h for h in t['rows'][0]) and any('情景' in h for h in t['rows'][0])]
        action=[t for t in ts if t['line']<130 and any('判断' in h or '选择' in h or '建议' in h for h in t['rows'][0])]
        top=raw[:raw.find('\n## 2.')] if '\n## 2.' in raw else '\n'.join(lines[:100])
        top=top[:9500]
        paragraphs=[p.strip() for p in top.split('\n\n') if ('当前' in p or '现价' in p or '结论' in p or '建议' in p or '期限' in p) and not p.lstrip().startswith(('#','|'))]
        digest='\n'.join(paragraphs)[:1400]
        if not digest:digest='\n'.join(lines[:25])[:1400]
        a=x.get('tokenUsage',{}).get('attempts',[])
        formal=a[-1].get('formal',{}) if a else {}
        thread=formal.get('threadId'); session=by_id.get(thread)
        prompt_match=None
        if session:
            expected=plan.replace('【公司股票代号】',x['subject']).replace('<公司股票代号>',x['subject'])
            with session.open(encoding='utf-8') as fh:
                for i,line in enumerate(fh):
                    if i>70:break
                    if '单家公司经营情景' not in line:continue
                    rec=json.loads(line); payload=rec.get('payload',{})
                    if payload.get('role')=='user':
                        texts='\n'.join(c.get('text','') for c in payload.get('content',[]) if isinstance(c,dict))
                        if '单家公司经营情景' in texts:
                            prompt_match=expected.replace('\r\n','\n') in texts.replace('\r\n','\n');break
        secs=(datetime.fromisoformat(x['finishedAt'])-datetime.fromisoformat(x['startedAt'])).total_seconds()
        record={**{k:x.get(k) for k in ['id','subject','displayName','category','createdAt','startedAt','finishedAt','attempts','outputFile']},'cohort':'22:52批次' if x in batch else '19点十家公司','bytes':len(data),'characters':len(raw),'lines':len(lines),'sha256':sha(data),'minutes':round(secs/60,2),'model':formal.get('model'),'effort':formal.get('reasoningEffort'),'threadId':thread,'sessionFile':str(session) if session else None,'latestPlanInSession':prompt_match,'usage':x.get('tokenUsage',{}).get('total',{}),'matrices':mats,'detailTables':details,'actionTables':action,'opening':top,'digest':digest,'headings':[{'line':i+1,'text':v} for i,v in enumerate(lines) if v.startswith('#')],'replacementCharacters':raw.count('\ufffd')}
        if data:(snapshot/f"{x['subject']}.md").write_bytes(data)
        reports.append(record)
    summary={'cutoff':datetime.now().astimezone().isoformat(),'count':len(reports),'cohorts':dict(Counter(x['cohort'] for x in reports)),'batchTotal':len(batch),'batchStatus':dict(Counter(x['status'] for x in batch)),'nonPendingUnfinished':[{k:x.get(k) for k in ['subject','status','startedAt','finishedAt','note']} for x in batch if x['status'] not in ['done','pending']],'planSha256':sha((ROOT/'分析报告/公司情景投资决策/研究方案.md').read_bytes()),'modelEffort':dict(Counter(str((r['model'],r['effort'])) for r in reports)),'planMatches':dict(Counter(str(r['latestPlanInSession']) for r in reports)),'bytes':{'min':min(r['bytes'] for r in reports),'median':statistics.median(r['bytes'] for r in reports),'max':max(r['bytes'] for r in reports),'total':sum(r['bytes'] for r in reports)},'minutes':{'min':min(r['minutes'] for r in reports),'median':statistics.median(r['minutes'] for r in reports),'max':max(r['minutes'] for r in reports),'total':sum(r['minutes'] for r in reports)},'matrixCounts':dict(Counter(len(r['matrices']) for r in reports)),'nonempty':sum(r['bytes']>0 for r in reports),'replacementCharacterFiles':[r['subject'] for r in reports if r['replacementCharacters']]}
    (OUT/'提取数据.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'运行与文件核对.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'活动队列快照.json').write_text(json.dumps(active,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 已完成报告：原文条件矩阵','',f"固定审查时点：{summary['cutoff']}；共{len(reports)}家公司。每格是报告原文的条件价值判断，不是当前实际投资建议。",'']
    for r in reports:
        lines += [f"## {r['subject']} — {r['displayName']}",'',f"[{r['cohort']}；完成于{r['finishedAt']}]({(ROOT/r['outputFile']).as_posix()})",'']
        for m in r['matrices']:lines += [m['raw'],'']
        if not r['matrices']:lines += ['自动提取未识别唯一标准矩阵，须人工查看原报告。','']
    (OUT/'全部公司原文条件矩阵.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('MATRIX_EXCEPTIONS',[(r['subject'],len(r['matrices'])) for r in reports if len(r['matrices'])!=1])
    print('TIME_EXTREMES',[(r['subject'],r['minutes']) for r in sorted(reports,key=lambda r:r['minutes'])[:3]+sorted(reports,key=lambda r:r['minutes'])[-3:]])
