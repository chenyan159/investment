from pathlib import Path
import json,collections
P=Path(__file__).parent
# Manual transcription of the opening current-choice paragraphs/tables, not the base scenario row.
# N = not recommended; W = neutral/wait; C = cautiously recommended; P = recommended.
mapping='''
AAOI NNN
ADI WWN
AEP NWW
AJNMY WWN
ALAB NNN
AMD NWN
AMPX NNN
ANET NNN
APD NWW
APH WWN
ARM NNN
ASGLY NWW
AVGO NWW
AXTI NNN
BDC WCW
BE NNN
BELFB WNN
BWXT WNN
CBRS NNN
CC WCW
CDNS NNN
CEG NWN
CIEN NWN
CLS WCN
CMI WWN
COHR WNN
CRDO NNN
CSCO NNN
DD WWN
DELL WWN
DHR WNN
DKILY WWC
DTE WCC
ECL NNW
ENPH NNN
ENS WNN
ENTG NNN
ET WCC
ETR NWW
FCEL WNN
FLEX NWN
FLNC WWW
FN WWN
GEV NNN
GLW NNN
GNRC WWN
HOCPY WWN
HPE WWW
HTHIY WCN
INTC NNN
JBL NWN
LIN WWN
LITE NNN
LWLG NNN
MCHP WWN
MMM NNN
MRAM NNN
MRVL NNN
MTRN NNN
MTSI NWN
MU WWN
MXL NNW
NDSN WWN
NOK WCN
NTAP NNW
NVDA WWN
OKLO NNN
ON WWN
P WNW
PENG WNW
POET WNN
PSIX CCW
Q NNN
QCOM NNN
RMBS WNN
ROG NWN
RYCEY NNN
SANM WCN
SHECY WCC
SIMO WWN
SITM NNW
SKHY WWN
SMCI WCW
SMR WNN
SMTC NNN
SMTOY WWW
SNDK WWN
SNPS WNN
SOMMY WCP
STM NWW
STX NNN
TEL WWW
TXN WWN
VIAV WWN
VISN WWN
VST WWN
WDC NNN
'''
labels={'N':'不建议投资','W':'中性／等待','C':'谨慎建议投资','P':'建议投资'}
m=dict(line.split() for line in mapping.strip().split('\n'))
manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
assert set(m)=={x['subject'] for x in manifest['reports']}
source={x['subject']:x['lines'] for x in json.loads((P/'current_summary_raw.json').read_text(encoding='utf-8'))}
special={'AXTI':8,'BE':7,'CDNS':8,'GEV':7,'LITE':6,'MTRN':6,'NTAP':13,'OKLO':7,'Q':11,'STX':5,'WDC':7}
out=['# 97份报告的当前实际主判断', '',
     '按报告开头的当前判断人工转录；不以基准条件格替代。高风险或其他理念的条件分歧保留在原文，本表不是个人化投资建议，也不是概率排序。PSIX短期正面限六个月，三个月为等待。', '',
     '| 公司 | 短期6个月 | 中期12个月 | 长期36个月 | 开头判断来源 |','| --- | --- | --- | --- | --- |']
rows=[]
for t,code in m.items():
    line=special.get(t,source[t][0][0] if source[t] else 1)
    url=f'{P.as_posix()}/报告快照/{t}.md:{line}'
    out.append('| '+t+' | '+' | '.join(labels[c] for c in code)+' | [原文](<'+url+'>) |')
    rows.append(dict(subject=t,ratings=[labels[c] for c in code],line=line))
stats=[]
for i in range(3):
    counts=dict(collections.Counter(labels[c[i]] for c in m.values()))
    positives=[t for t,c in m.items() if c[i] in 'CP']
    stats.append(dict(time=i,counts=counts,positive=positives))
print(json.dumps(stats,ensure_ascii=False,indent=2))
(P/'97家公司当前实际建议.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
(P/'current_choices.json').write_text(json.dumps(dict(rows=rows,stats=stats),ensure_ascii=False,indent=2),encoding='utf-8')
