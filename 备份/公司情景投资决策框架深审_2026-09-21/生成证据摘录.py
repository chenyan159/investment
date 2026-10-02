from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
OLD=PROJECT/'备份/27家公司情景投资决策复审_2026-09-19'
manifest=json.loads((OLD/'报告清单.json').read_text(encoding='utf-8-sig'))
assert all(hashlib.sha256((PROJECT/x['path']).read_bytes()).hexdigest()==x['hash'] for x in manifest)
groups={
'A 时间网格与插值':[('NVDA',95,108),('AMZN',131,145),('TSLA',108,124),('CRWV',210,221),('SNDK',148,156)],
'B DCF滚动与目标价格识别':[('CRWV',225,246),('NBIS',255,287),('SPCX',275,294),('MSFT',229,247),('ADBE',272,276)],
'C 条件评级的重复与差异':[('ADBE',347,358),('MSFT',344,355),('NVDA',302,313),('SNDK',373,384),('TSM',245,256)],
'D 业务数量级检查与预测依据的距离':[('NVDA',110,138),('MSFT',87,126),('ADBE',77,111),('SNDK',118,146),('ANET',105,115)],
'E 有价值的业务研究与自然时间节点':[('OKLO',115,183),('RKLB',84,110),('TSLA',78,104),('NBIS',104,108),('NBIS',166,184)],
'F 概率对象与代表点偏差':[('MSFT',151,164),('NVDA',167,192),('ALAB',98,113),('NBIS',150,164),('SNDK',128,146),('RKLB',90,96),('CRWV',138,161)],
'G 远期主导与成熟阶段假设':[('CRWV',225,244),('NBIS',270,287),('AMZN',215,240),('MSFT',280,287),('ADBE',241,270)],
'H 资本市场条件进入业务成功':[('NBIS',221,253),('CRWV',179,210),('SPCX',248,269)],
'I 资本分配与每股结果':[('MSFT',215,227),('ADBE',208,229),('SNDK',211,221)],
'J 权益和风险覆盖差异':[('TSM',1,13),('NBIS',150,164),('CRWV',138,161),('SNDK',128,146)],
}
out=['# 多公司交叉证据摘录\n\n核验日：2026-09-21。27家公司最新正式报告仍均为2026-09-19，哈希与前轮复审全部相同。本次只读正式方案及报告。下面按问题分组，保留原始行号；同一报告可支持不同问题，但不把同一报告当多个独立样本。\n']
for title,items in groups.items():
 out.append('## '+title+'\n')
 for t,a,b in items:
  p=PROJECT/f'分析报告/公司情景投资决策/结果/{t}_经营情景市场状态投资决策_2026-09-19.md'
  ls=p.read_text(encoding='utf-8-sig').splitlines()
  out.append(f'### {t}，原报告第{a}—{b}行\n\n[打开原文](</{p.as_posix()}:{a}>)\n')
  out.append('\n'.join(f'{i+1}: {ls[i]}' for i in range(a-1,min(b,len(ls)))))
(ROOT/'多公司交叉证据摘录.md').write_text('\n\n'.join(out),encoding='utf-8')
roll=[]
for t,v,r,source in [('CRWV',17.56,.15,[20.19,26.71,46.71]),('NBIS',33.07,.14,[37.70,49,82.76]),('SPCX',6.18,.12,[6.92,8.68,13.66])]:
 for h,reported in zip([1,3,7],source):
  calc=v*(1+r)**h
  roll.append(dict(ticker=t,v0=v,ke=r,year=h,reported=reported,calculated=calc,error=calc-reported))
assert max(abs(x['error']) for x in roll)<.015
(ROOT/'期限滚动复算.json').write_text(json.dumps(roll,ensure_ascii=False,indent=2),encoding='utf-8')
print('reports_unchanged=27; excerpts='+str(sum(map(len,groups.values())))+'; rollforward_checks=9')
