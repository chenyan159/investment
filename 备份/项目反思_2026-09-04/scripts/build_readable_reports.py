from pathlib import Path
import pandas as pd,json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';PROJ=ROOT.parents[1]
c=pd.read_csv(D/'company_returns.csv');d=pd.read_csv(D/'decisions_historical.csv');r=pd.read_csv(D/'historical_rankings.csv',dtype={'list_id':str,'method_id':str});m=pd.read_csv(D/'method_metrics.csv',dtype={'list_id':str,'method_id':str});comp=pd.read_csv(D/'company_comparison_historical.csv');cm=pd.read_csv(D/'company_comparison_forward_metrics.csv');el=pd.read_csv(D/'ranking_top20_eligibility.csv',dtype={'method_id':str});reg=pd.read_csv(PROJ/'分析报告/公司排序/00_运行与榜单注册表.csv',dtype={'list_id':str,'method_id':str})
c=c.merge(d,on='ticker',validate='one_to_one').merge(comp[['ticker','overall_rank','source_path']],on='ticker',validate='one_to_one')
def link(label,path,line=None):return f'[{label}](<{str(path).replace(chr(92),"/")}{":"+str(int(line)) if line is not None and pd.notna(line) else ""}>)'
def pct(x):return f'{x:+.2%}' if pd.notna(x) else 'NA'
def num(x):return f'{x:.2f}' if pd.notna(x) else 'NA'
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(y).replace('|','／').replace('\n',' ') for y in x)+' |' for x in rows])
main=ROOT/'00_项目反思与问题诊断.md';t=main.read_text(encoding='utf-8')
b=pd.read_csv(D/'all_returns_and_benchmarks.csv').set_index('ticker');metric=m.set_index('list_id')
performance=[['审计重建七家族共识20','7/13收盘',pct(metric.loc['ACTIVE_CONSENSUS','top20_mean']),'7家亏损；捕捉实际赢家20中的5家'],['192家公司池等权','7/13收盘',pct(c.ret_0713.mean()),'130家下跌、62家上涨']]
for sym in ['SPY','QQQ','SOXX','IGV','XLE']:performance.append([sym,'7/13收盘',pct(b.loc[sym,'ret_0713']),'同一观察窗口'])
performance.extend([['审计重建七家族共识20','7/14开盘','+2.5741%','保守执行时点敏感性'],['SPY','7/14开盘','+2.5676%','与上一行同起点；超额约0.66bp']])
t=t.replace('{{PERFORMANCE_TABLE}}',table(['对象','起点','截至9/4收益','解释'],performance))
focus=pd.read_csv(D/'decisions_focus_verified.csv');fr=[]
for sym in ['SMCI','DELL','MSFT','PENG','MOD','WDC','VST','P','AEHR','AXTI','ATKR','PSIX','ORCL','ATEYY','SOMMY']:
    x=c[c.ticker==sym].iloc[0];fx=focus[focus.ticker==sym].iloc[0]
    fr.append([sym,int(x.consensus_rank),pct(x.ret_0713),pct(x.ret_0715),link(fx.scenario_rating_manual,fx.scenario_path,fx.scenario_line)])
t=t.replace('{{FOCUS_TABLE}}',table(['公司','审计共识名次','7/13以来','7/15情景日以来','7/15主条件意见及原文'],fr))
t=t.replace('科技增长多为重述共识','六例基准与公开预期接近').replace('runner.mjs:475','runner.mjs:490')
marker='### 3.4 AEHR：只差两天'
pnotes=[]
for lid in ['06F','02','05','03']:
    q=r[(r.ticker=='P')&(r.list_id==lid)].iloc[0];pnotes.append(link(lid+'原文',q.source_path,q.source_line))
para='更具体的排名证据排除了单一归因：06F基本面性价比实际上将P排第6；02第147的理由包括第二客户未披露、桥梁未到订单级；05第129包含20日价格缺口及Top30禁入，03第104也标记价格历史不足。因此P存在一个角度明确选中、其他角度因证据和数据门槛降级、汇总后排名低的多重机制，不能归咎于单一的“没有近期收入”。'+ '、'.join(pnotes)+'。\n\n'
if para not in t:t=t.replace(marker,para+marker)
main.write_text(t,encoding='utf-8')

lines=['# 192家公司逐股复盘表','', '观察截止2026-09-04；MICLF有效末价2026-09-03。三种收益均为各层报告日收盘起算的复权价格比率，不是长期目标到期命中率。共识为本次审计重建，06三视图先平均后与01–07家族等权；并非历史真实持仓。','', '同一家公司可能在不同层被看好、看空或中性。下表只将文本意见与已发生结果并列，不凭涨跌重写原文。除15个重点样本及部分复合/状态修正条目外，其余意见为摘要规则抽取，人工核验范围见CSV的rating_review_note；全表原文都可直接点击。','', '价格列为Yahoo已拆股调整的历史Close；收益列进一步使用Adjusted Close处理分红。海外ADR与本地估值主锚不同的SOMMY/MICLF另标记，不直接评价本地股价目标。','',link('完整768条分来源日期观察，含每个起点价及次日开盘敏感性',D/'company_observations_by_source_date.csv'),'',link('全192家行情、28榜名次、基准和回撤',D/'company_returns.csv'),'']
for category,grp in c.groupby('category',sort=True):
    lines+=['## '+category.rstrip('/'),'',f'分类{len(grp)}家；7/13起等权均值{pct(grp.ret_0713.mean())}。','']
    rr=[]
    for _,x in grp.sort_values('ticker').iterrows():
        note=''
        if x.ticker=='SOMMY':note='；19个零量日；本地股估值锚'
        if x.ticker=='MICLF':note='；末价9/3；38个零量日；本地股估值锚'
        if x.ticker=='VISN':note='；含5美元特别分派调整'
        rr.append([x.ticker,x.company,int(x.consensus_rank),num(x.close_0713),num(x.close_0715),num(x.end_close),pct(x.ret_0713),pct(x.ret_0714),pct(x.ret_0715),link(x.current_condition_rating_reviewed,x.scenario_path,x.summary_line)+note])
    lines+=[table(['代码','公司','审计共识名次','7/13价','7/15价','期末价','排序7/13起','对比7/14起','情景7/15起','情景意见与历史原文'],rr),'']
(ROOT/'01_192家公司逐股复盘表.md').write_text('\n'.join(lines),encoding='utf-8')

lines=['# 全部排序、公司对比与原方法资格','', '所有28榜均为2026-07-13运行，观察至2026-09-04；这里的Top20首先表示连续名次前20的机械等权篮子。排名不是统一买入评级；右尾、五倍、门控、收入台阶等方法有不同资格与期限。未经资格区分，不得把所有机械篮子当成原方法正式投资建议。','', 'Rank IC = 负名次与实现收益名次的Pearson相关（等价于相应的秩相关）；正数表示前排表现较好。所有相关仅为39个交易日收益间隔后的单个横截面，不表示已证明跨期有效。平均个股MDD不是组合MDD。','', '## 28榜完整结果','']
rr=[]
for _,g in reg.iterrows():
    x=metric.loc[g.list_id];e=el[el.method_id==g.method_id].iloc[0]
    rr.append([g.list_id,g.list_name,g.lifecycle,pct(x.top20_mean),pct(x.top20_excess_universe),pct(x.top20_excess_SPY),f'{x.rank_ic:+.3f}',int(x.top20_negative),int(x.winner20_captured),link('资格/期限',e.source_path,e.source_line)])
lines+=[table(['榜','名称','历史状态','机械Top20收益','超公司池','超SPY','Rank IC','下跌数/20','赢家20捕捉数','原文'],rr),'','## 特殊资格和期限','']
rr=[]
for _,x in el.iterrows():
    if x.method_id in ['07','08','12','16','17','N03','N04','N05','N06','E03']:
        rr.append([x.method_id,x.method_name,x.stated_thesis_qualified_selected_count,x.qualification_note,x.horizon])
lines+=[table(['方法','名称','原命题合格席位','资格说明','期限/含义'],rr),'', 'N03严格合格8家为MU/PENG/TSLA/TT/ASX/APLD/BWXT/BDC，不能按连续名次取前8（UMC连续第7不合格）；八家等权收益-6.08%，6家下跌。12与16控制组不代表其已找到五倍机会。','', '## 公司对比六维及总体：使用自身7/14报告日','']
names={'near':'近端兑现','long':'长期复利','odds':'风险调整赔率','defense':'压力防守','explosion':'爆发突破','mispricing':'认知错价','overall':'总体'}
rr=[]
for dim in names:
    a=cm[(cm.dimension==dim)&(cm.variant=='all_directions')].iloc[0];bb=cm[(cm.dimension==dim)&(cm.variant=='same_winner_only')].iloc[0]
    rr.append([names[dim],pct(a.top20_return),f'{a.rank_ic:+.3f}',pct(bb.top20_return),f'{bb.rank_ic:+.3f}',a.top20_tickers])
lines+=[table(['维度','双向汇总Top20','Rank IC','仅同胜方Top20','仅同胜方IC','原始Top20名单'],rr),'', '这些维度同样有期限差异；长期复利和爆发路径的短窗表现不等于原期限命题到期失败。公司对比总体+5.08%不能与7/13起的排序收益无条件作精细差值，日期不同。','', '## 共识20的收益分布','']
rr=[]
for _,x in c.nsmallest(20,'consensus_rank').iterrows():rr.append([int(x.consensus_rank),x.ticker,pct(x.ret_0713),pct(x.mdd_0713),x.current_condition_rating_reviewed])
lines+=[table(['审计共识名次','代码','7/13起收益','个股过程MDD','7/15情景主意见'],rr),'', '共识组合MDD为-14.01%；这里逐股MDD不能直接平均代替组合MDD。单家公司未达长期目标尚不能判其长期情景失败。','',link('完整原始名次与行号',D/'historical_rankings.csv'),'、',link('比较方向冲突及分类',D/'company_comparison_reciprocal_summary.csv'),'、',link('所有指标CSV',D/'method_metrics.csv')]
(ROOT/'02_全部排序与对比结果.md').write_text('\n'.join(lines),encoding='utf-8')

joined=c[['ticker','company','category','consensus_rank','overall_rank','close_0713','close_0714','close_0715','end_date','end_close','ret_0713','ret_0714','ret_0715','mdd_0713','zero_volume_0713','scenario_report_date','current_condition_rating_reviewed','rating_review_note','scenario_path','summary_line','evaluation_path','source_path']]
joined.to_csv(D/'company_review_joined.csv',index=False,encoding='utf-8-sig')
print('BUILT main + 192-company appendix + method appendix;',len(c),'companies',len(reg),'lists')
