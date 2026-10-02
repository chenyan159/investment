from pathlib import Path
import pandas as pd,numpy as np,re,json,hashlib
R=Path('D:/drive/Investment');O=R/'备份/company-comparison专项回测_2026-09-05';D=O/'data'
e=pd.read_csv(D/'comparison_pair_outcomes_next_open.csv',usecols=['cohort','ticker','opponent','dimension','status','winner','confidence','a_return','b_return','edge','correct']);e=e[(e.cohort=='original_0714')&(e.status=='winner')]
r=pd.read_csv(D/'derived_rankings.csv');r=r[(r.cohort=='original_0714')&(r.variant=='both')]
rows=[]
for d,q in e.groupby('dimension'):
 ranks=r[r.dimension==d].set_index('ticker')['rank'];ar=q.ticker.map(ranks);br=q.opponent.map(ranks)
 groups={'all':np.ones(len(q),bool),'both_top30':(ar<=30)&(br<=30),'top30_vs_outside':((ar<=30)&(br>30))|((ar>30)&(br<=30)),'both_top60':(ar<=60)&(br<=60),'boundary_15_60':ar.between(15,60)&br.between(15,60),'both_bottom96':(ar>96)&(br>96),'both_positive':(q.a_return>0)&(q.b_return>0),'both_negative':(q.a_return<0)&(q.b_return<0)}
 for name,mask in groups.items():
  g=q[mask];winnerret=np.where(g.winner==g.ticker,g.a_return,g.b_return)
  rows.append(dict(dimension=d,group=name,n=len(g),accuracy=g.correct.mean(),mean_edge=g.edge.mean(),winner_positive=np.mean(winnerret>0),winner_return=winnerret.mean()))
pd.DataFrame(rows).to_csv(D/'frontier_accuracy.csv',index=False,encoding='utf-8-sig')

# Only rows whose opponent is QCOM. This avoids conflating a net-cash claim about a different target.
src=pd.read_csv(D/'source_reports.csv');src=src[src.cohort=='original_0714'];qrows=[];excerpts=[];deltas=[]
for x in src.itertuples():
 p=Path(x.path);lines=p.read_text(encoding='utf-8-sig').splitlines()
 for i,l in enumerate(lines,1):
  if not re.match(r'^\|\s*\d+\s*\|',l):continue
  cs=[s.strip().replace('`','').replace('**','') for s in re.split(r'(?<!\\)\|',l.strip('|'))]
  if len(cs)!=12 or not re.match(r'^QCOM(?:\s|/|$)',cs[1]):continue
  for k,c in enumerate(cs[4:11]):
   # Screen only; humans must distinguish genuine stock-of-cash language from cash-flow ability.
   if c.startswith('QCOM') and re.search(r'净现金(?!流|创造|能力|式)',c):
    qrows.append(dict(report_ticker=x.ticker,source_path=p.as_posix(),source_line=i,dimension=['near','long','odds','defense','explosion','mispricing','overall'][k],text=c))
pd.DataFrame(qrows).to_csv(D/'qcom_net_cash_claim_screen.csv',index=False,encoding='utf-8-sig')
print(pd.DataFrame(rows).query("dimension in ['overall','odds','explosion']").to_string(index=False))
print('QCOM candidate net-cash claims:',len(qrows),'reports:',len(set(r['report_ticker'] for r in qrows)))
for x in qrows[:24]:print(x['report_ticker'],x['dimension'],x['text'])
