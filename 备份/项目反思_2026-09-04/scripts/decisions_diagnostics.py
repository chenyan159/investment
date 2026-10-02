from pathlib import Path
import csv,json,re,statistics
from collections import Counter
ROOT=Path(r'D:\drive\Investment'); OUT=ROOT/'备份/项目反思_2026-09-04'
def rd(n):return list(csv.DictReader((OUT/'data'/n).open(encoding='utf-8-sig')))
def wr(n,rows):
    with (OUT/'data'/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rs=rd('decisions_historical.csv'); cells=rd('decisions_matrix_cells.csv')
pat=r'宽基风险扩张|窄幅\s*[/／]?\s*主题主导上涨|窄幅主题上涨|震荡\s*[/／]\s*均值回归|有序风险收缩|流动性\s*[/／]\s*信用压力'
out=[];vix=[];lex=[]
for r in rs:
    s=r['summary_text'];sh=s[s.find('共享'):]
    states=[x[0] for x in re.finditer(pat,sh)]
    states=[re.sub(r'\s|[/／]','',x) for x in states]
    # First state after shared-snapshot introduction, anchored to original summary.
    main=states[0] if states else ''
    v=re.search(r'当前最弱传导环节.{0,8}(.*?)(?:[：:]|；|。)',s)
    weak=v[1] if v else ''
    snapshot=sh[:min([x for x in [sh.find('对应'),sh.find('当前主格'),sh.find('纯矩阵')] if x>=0] or [len(sh)])]
    market='US-explicit' if re.search(r'美国|US[-_]|US\|',snapshot) and not re.search(r'日本股票|欧洲|英国|瑞士|韩国|瑞典|日本市場|STOXX',snapshot) else 'Other-or-unclear'
    out.append({'ticker':r['ticker'],'path':r['scenario_path'],'summary_line':r['summary_line'],'main_market_state_first_mention':main,'main_market_scope_filter':market,'snapshot_text':snapshot,'base_in_current_position':bool(re.search(r'基准',s.split('共享')[0])),'composite_explicit':bool(re.search(r'复合定位\s*达到门槛',s.split('共享')[0])),'weakest_link_text':weak,'weakest_cash_or_capital':bool(re.search(r'现金|资本|稀释|利润|成本|单位经济|ROIC|融资',weak)),'weakest_capture_or_delivery':bool(re.search(r'捕获|份额|订单|交付|验收|认证|资格',weak)),'summary_text':s})
    txt=Path(r['scenario_path']).read_text(encoding='utf-8-sig')
    for i,line in enumerate(txt.splitlines(),1):
        if re.search(r'\bVIX\b',line) and re.search(r'15\.67|16\.54|16\.50|16\.5',line):
            vix.append({'ticker':r['ticker'],'path':r['scenario_path'],'line':i,'contains_15_67':'15.67' in line,'contains_16_54':'16.54' in line,'contains_16_5':bool(re.search(r'16\.5(?:0\b|\b)',line)),'text':line})
    for kind,path in [('scenario',r['scenario_path']),('evaluation',r['evaluation_path'])]:
        t=Path(path).read_text(encoding='utf-8-sig'); lines=t.splitlines()
        for label,regex in [('probability_na',r'概率层.{0,20}NA'),('consensus_unavailable',r'(?:没有|缺少|缺乏|未提供|无|未给出|不虚构).{0,65}(?:市场一致预期|一致预期数字|卖方一致|市场共识)'),('prohibit_technical_sentiment',r'(?:不|未|禁止|排除).{0,45}(?:技术面|情绪)'),('interval_envelope',r'包络|低端取.{0,30}低|高端取.{0,30}高|不做简单平均'),('nonmarket_current_expectation',r'当前预期.{0,65}(?:管理层|公司指引|run-rate|基准|本报告|本文)')]:
            hits=[(i,l) for i,l in enumerate(lines,1) if re.search(regex,l)]
            if hits:
                i,l=hits[0];lex.append({'ticker':r['ticker'],'kind':kind,'label':label,'path':path,'line':i,'matching_lines_count':len(hits),'first_evidence':l,'warning':'Lexical screening count, not a count of proven defects'})
wr('decisions_state_audit.csv',out);wr('decisions_vix_conflicts_evidence.csv',vix);wr('decisions_lexical_screen.csv',lex)
widths=[float(r['current_condition_return_high_pct'])-float(r['current_condition_return_low_pct']) for r in rs]
cross=[r for r in rs if float(r['current_condition_return_low_pct'])<0<float(r['current_condition_return_high_pct'])]
envelope=[]
for r in rs:
    cs=[c for c in cells if c['ticker']==r['ticker'] and c['return_low_pct']!='']
    lo=min(float(c['return_low_pct']) for c in cs);hi=max(float(c['return_high_pct']) for c in cs)
    envelope.append({'ticker':r['ticker'],'range_min_low_pct':lo,'range_max_high_pct':hi,'envelope_span_pp':hi-lo,'warning':'Unweighted union of conditional scenarios, not a forecast distribution'})
wr('decisions_full_envelope.csv',envelope)
stats={'n':len(rs),'probability_na':sum(r['probability_na_explicit']=='True' for r in rs),'all_current_position_mentions_base':sum(r['base_in_current_position'] for r in out),'composite_explicit_screen':sum(r['composite_explicit'] for r in out),'current_return_intervals':len(widths),'current_return_width_median_pp':statistics.median(widths),'current_return_width_mean_pp':statistics.mean(widths),'current_return_width_ge50_count':sum(x>=50 for x in widths),'current_return_width_ge100_count':sum(x>=100 for x in widths),'current_return_cross_zero_count':len(cross),'matrix_cells':len(cells),'matrix_cells_with_numeric_interval':sum(c['return_low_pct']!='' for c in cells),'full_envelope_median_span_pp':statistics.median(r['envelope_span_pp'] for r in envelope),'full_envelope_span_ge200':sum(r['envelope_span_pp']>=200 for r in envelope),'global_main_market_states':dict(Counter(r['main_market_state_first_mention'] for r in out)),'us_explicit_denominator':sum(r['main_market_scope_filter']=='US-explicit' for r in out),'us_explicit_main_market_states':dict(Counter(r['main_market_state_first_mention'] for r in out if r['main_market_scope_filter']=='US-explicit')),'cash_profit_capital_in_weakest_link':sum(r['weakest_cash_or_capital'] for r in out),'capture_delivery_in_weakest_link':sum(r['weakest_capture_or_delivery'] for r in out),'lexical_only_not_defects':dict(Counter((r['kind']+'/'+r['label']) for r in lex)),'vix_exact_value_lexical_company_counts':{str(v):len(set(r['ticker'] for r in vix if r[k])) for v,k in [('15.67','contains_15_67'),('16.54','contains_16_54'),('16.5','contains_16_5')]}}
(OUT/'data/decisions_diagnostic_stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(stats,ensure_ascii=False,indent=2))
