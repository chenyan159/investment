from pathlib import Path
import json,re,collections
P=Path(__file__).parent
raw=json.loads((P/'parsed_matrices_raw.json').read_text(encoding='utf-8'))
rm={r['subject']:r['matrix'] for r in raw}
def norm(s):return re.sub(r'\s|\*','',s).replace('／','/')
def nums(s):
    return [float(n.replace('−','-')) for n in re.findall(r'[+\-−]?\d+(?:\.\d+)?',s.replace(',',''))]
details={}
for f in sorted((P/'报告快照').glob('*.md')):
    rows=[]
    for i,l in enumerate(f.read_text(encoding='utf-8-sig').split('\n'),1):
        if not l.startswith('|'):continue
        c=[z.strip() for z in re.split(r'(?<!\\)\|',l.strip().strip('|'))]
        if len(c)==11 and re.search('建议投资|中性.?[／/]?.?等待',c[7]):c=c[:6]+c[7:]
        if len(c)==10 and re.search('建议投资|中性.?[／/]?.?等待',c[6]):rows.append({'line':i,'cells':c})
    details[f.stem]=rows
assert all(len(a)==12 for a in details.values())
mismatches=[]
for t,rows in details.items():
    for i,r in enumerate(rows):
        c=r['cells'];s,h=divmod(i,3)
        matrix=rm[t][s]['cells'][h].split('｜')
        problems=[]
        if norm(matrix[0])!=norm(c[6]):problems.append('rating')
        nr,nd=nums(matrix[1])[:2],nums(c[5])[:2]
        if len(nr)==2 and len(nd)==2 and max(abs(a-b) for a,b in zip(nr,nd))>0.15:problems.append('return')
        if norm(matrix[2])!=norm(c[9]):problems.append('confidence')
        if problems:mismatches.append(dict(subject=t,line=r['line'],problems=problems,matrix=matrix,detail=c))

# No ordinary dividend subsample; LWLG's hypothetical Y3 liquidation distributions are included separately.
prices={'AAOI':105.53,'AMD':477.57,'AMPX':9.89,'BE':252.87,'CRDO':170.57,'FN':407.40,
        'GNRC':187.35,'LWLG':5.35,'MRAM':16.37,'OKLO':41.27,'POET':7.92,'SMR':9.70,'SNDK':1740.0,'PSIX':40.49}
arithmetic=[];arithmetic_issues=[]
for t,p0 in prices.items():
    for i,r in enumerate(details[t]):
        c=r['cells'];v,ret=nums(c[4])[:2],nums(c[5])[:2]
        if len(v)!=2 or len(ret)!=2:continue
        distribution=[0.1372,0.0556,0.0155,0.0059][i//3] if t=='LWLG' and i%3==2 else 0
        calculated=[((q+distribution)/p0-1)*100 for q in v]
        error=max(abs(a-b) for a,b in zip(calculated,ret))
        # Public tables round prices to cents, or whole dollars for large share prices.
        target_tokens=re.findall(r'\d+(?:\.\d+)?',c[4].replace(',',''))[:2]
        quantum=max(10**(-len(n.partition('.')[2])) for n in target_tokens)
        tolerance=max(0.15,(quantum/2)/p0*100+0.06)
        x=dict(subject=t,line=r['line'],price=p0,target=v,distribution=distribution,reported=ret,calculated=calculated,max_error_pp=error,tolerance_pp=tolerance)
        arithmetic.append(x)
        if error>tolerance:arithmetic_issues.append(x)

# Manual method classification from all 97 detail tables; a separate early-project NPV does not make a multiple-based core into DCF.
switched='ADI AJNMY ALAB AMD APH ASGLY AVGO BDC CC CIEN CLS CMI DD DELL FLEX FN GEV GLW GNRC HOCPY HPE HTHIY JBL LIN LITE MCHP MMM MRVL MTSI MU MXL NDSN NOK NTAP NVDA ON PENG PSIX QCOM ROG SANM SIMO SKHY SMCI SMTOY SNDK SNPS STM TEL TXN VIAV VST'.split()
cells=json.loads((P/'all_cells.json').read_text(encoding='utf-8'))
base={t:sorted([c for c in cells if c['subject']==t and c['si']==1],key=lambda c:c['ti']) for t in details}
lower=[t for t,c in base.items() if c[2]['rank']<c[1]['rank']]
switch_lower=[t for t in switched if t in lower]
result=dict(report_count=len(details),detail_count=sum(len(a) for a in details.values()),matrix_detail_mismatches=mismatches,
            arithmetic_companies=list(prices),arithmetic_cells=len(arithmetic),arithmetic_issues=arithmetic_issues,
            method_switch_companies=switched,method_switch_count=len(switched),long_lower_count=len(lower),
            method_switch_and_long_lower=switch_lower,method_switch_and_long_lower_count=len(switch_lower),arithmetic=arithmetic)
(P/'structure_numeric_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'details_normalized.json').write_text(json.dumps(details,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='arithmetic'},ensure_ascii=False,indent=2))
