import json,csv,pathlib,hashlib,datetime,re,sys
R=pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,d): (R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def link(label,p): return '['+label+']('+str((R/p).resolve()).replace('\\','/')+')'
def fmt(x): return f'{x:,.2f}'
def pct(x): return f'{x:+.1f}%'
def rows(d): return d if isinstance(d,list) else d.get('companies',[])
def clean(x): return str(x).replace('|','／').replace('\n',' ')
universe={c['ticker']:c for c in load('01_inputs/universe.json')}
models={c['ticker']:c for c in load('04_verification/V2_models.json')['companies']}
facts={c['ticker']:c for c in load('04_verification/V1_evidence.json')['companies']}
round1=load('03_round2/首轮五角色汇总.json')
trail={c['ticker']:c for c in round1['all245']}
rolefiles={'S1':'03_round2/S1_ai_deep.json','S2':'03_round2/S2_nonai_deep.json','B1':'03_round2/B1_business_rebuttal.json','B2':'03_round2/B2_valuation_rebuttal.json'}
roledata={k:{c['ticker']:c for c in rows(load(f))} for k,f in rolefiles.items()}
extra=R/'03_round2/B2_末轮补充反驳.json'
if extra.exists():
    x=json.loads(extra.read_text(encoding='utf-8-sig'))
    for c in rows(x): roledata['B2'][c['ticker']]=c
work=load('05_chair/主席条件卡工作稿.json')['candidates']
cp=R/'05_chair/主席裁决.json'
final=cp.exists() and '--draft' not in sys.argv
chair=load('05_chair/主席裁决.json') if final else {}
if final: assert 'DRAFT' not in chair.get('status','DRAFT'), 'chair not sealed'
selection=chair.get('final20',[{'rank':i+1,'ticker':t,'tier':'待最终裁决'} for i,t in enumerate('MU KYTX IREN SNDK AAOI SMCI AMPX PSIX UCTT VISN BNTX ENPH ACMR CRWV LEU ADBE AOSL CLS RDW MOD'.split())])
selection=[dict(rank=i+1,ticker=x) if isinstance(x,str) else x for i,x in enumerate(selection)]
selected=[c['ticker'] for c in selection]
assert len(selected)==20 and len(set(selected))==20
assert set(selected)<=set(universe) and set(selected)<=set(models) and set(selected)<=set(facts)
outdir='06_final' if final else 'tmp'
source_records=[]
def recurse_sources(obj,role):
    if isinstance(obj,list):
        for x in obj: recurse_sources(x,role)
    elif isinstance(obj,dict):
        if isinstance(obj.get('url'),str) and obj['url'].startswith('http'): source_records.append(dict(obj,_role=role))
        for k,v in obj.items():
            if isinstance(v,(list,dict)): recurse_sources(v,role)
for p in (R/'07_logs').glob('*sources.json'):
    try: recurse_sources(json.loads(p.read_text(encoding='utf-8-sig')),p.stem.split('_')[0])
    except (ValueError,UnicodeError): pass
def ticker_sources(t):
    found=[]; seen=set()
    ids={role:set(roledata[role].get(t,{}).get('source_ids',roledata[role].get(t,{}).get('sources',[]))) for role in roledata}
    for s in source_records:
        ts=s.get('tickers',s.get('ticker',[])); ts=[ts] if isinstance(ts,str) else ts
        if t in ts or s.get('id') in ids.get(s['_role'],set()):
            if s['url'] not in seen: found.append(s);seen.add(s['url'])
    return found
def source_links(t):
    fs=ticker_sources(t); pri=[]; outside=[]
    for s in fs:
        tp=str(s.get('type',s.get('source_type',''))).lower()
        (pri if 'primary' in tp else outside).append(s)
    chosen=[];seen=set()
    for u in facts[t]['source_urls'][:2]:
        chosen.append({'url':u,'title':'V1独开原始资料','access':'相关决定段，非全文'});seen.add(u)
    for s in outside[:4]+pri[:3]:
        if s['url'] not in seen: chosen.append(s);seen.add(s['url'])
    text=[]
    for s in chosen[:7]:
        date=s.get('published',s.get('publication_date',s.get('event_date',s.get('public_date','日期见日志')))) or '日期见日志'
        status=s.get('access_status',s.get('access','访问范围见日志'))
        title=s.get('title',s.get('id','外部证据'))
        text.append(f"- [{clean(title)}]({s['url']})；{clean(date)}；{clean(status)}。")
    return '\n'.join(text)
def model_explain(c):
    i=c['scenario_inputs'][2]['inputs']; typ=c['model_type']; n=i['shares_m']; inv=c['two_x_inverse']; details=[]
    if typ=='EV_NopAT':
        details=[f"前瞻完整年度收入 {fmt(i['revenue_m'])}M，毛利率 {i['gross_margin']:.1%}，经济费用率 {i['economic_opex_rate']:.1%}，税率 {i['tax_rate']:.1%}，税后经营利润倍数 {i['multiple']}，股数 {n:,.3f}M，净债 {fmt(i['net_debt_m'])}M，其他权益索取 {fmt(i.get('other_claims_m',0))}M",f"同成本/倍数/资本条件下，翻倍需收入 {fmt(inv['required_revenue_m'])}M、税后经营利润 {fmt(inv['required_NOPAT_m'])}M"]
    elif typ=='economic_parent_EPS_PE_plus_incremental_option':
        details=[f"收入 {fmt(i['revenue_m'])}M、毛利 {i['gross_margin']:.1%}、经济费用 {fmt(i['economic_opex_m'])}M、净利息成本 {fmt(i['net_interest_cost_m'])}M、税 {i['tax_rate']:.1%}、少数权益分成 {i['nci_fraction']:.1%}、股数 {n:,.3f}M、PE {i['PE']}；只另加增量业务期权 {fmt(i['incremental_option_value_m'])}M，不再加已有现金",f"同其他条件翻倍需归母经济EPS {inv['required_EPS']:.2f}，或前瞻收入 {fmt(inv['required_revenue_m'])}M"]
    elif typ=='EV_Sales_with_profit_crosscheck':
        details=[f"收入 {fmt(i['revenue_m'])}M、EV/收入 {i['sales_multiple']}倍、股数 {n:,.3f}M、净债 {fmt(i['net_debt_m'])}M；交叉检验毛利 {i['gross_margin']:.1%}、费用 {fmt(i['economic_opex_m'])}M、税 {i['tax_rate']:.1%}，对应税后经营利润 {fmt(c['scenario_inputs'][2]['result']['nopat_m'])}M",f"同条件翻倍需收入 {fmt(inv['required_revenue_m'])}M；若收入仍为成功分支，需收入倍数 {inv['required_sales_multiple_at_branch_revenue']:.2f}。收入倍数不能替代最终盈利检验"]
    elif typ=='EV_EBITDA_with_maintenance_FCF_crosscheck':
        details=[f"收入 {fmt(i['revenue_m'])}M、折旧前毛利 {i['gross_margin_before_DA']:.1%}、含股份费用等价成本的现金费用 {fmt(i['cash_opex_including_SBC_equivalent_m'])}M，EBITDA {fmt(c['scenario_inputs'][2]['result']['EBITDA_m'])}M×{i['multiple']}，净债 {fmt(i['net_debt_m'])}M、股数 {n:,.3f}M",f"同条件翻倍需EBITDA {fmt(inv['required_EBITDA_m'])}M；维护资本开支 {fmt(i['maintenance_capex_m'])}M，增长资本/营运资本还需另核"]
    elif typ.startswith('conditional_owned_asset_SOTP'):
        parts='、'.join(k+' '+fmt(v)+'M' for k,v in i['risk_adjusted_asset_values_m'].items())
        details=[f"归属公司并已打风险折价的业务/管线代理价值：{parts}；期末净现金 {fmt(i['net_cash_m'])}M、股数 {n:,.3f}M",f"翻倍需归属业务与管线价值合计 {fmt(inv['required_owned_pipeline_and_franchise_EV_m'])}M。这是临床/商业化条件估值，未完成逐药物、逐授权合同rNPV审计，也不是半年销售预测"]
        if 'cash_bridge_EUR' in i: details.append('现金以欧元财报为起点，扣消耗及回购后用研究汇率换成美元；ADS 1:1，详细汇率敏感性在模型。')
    elif typ=='EV_NOPAT_endogenous_convertibles_and_preferred':
        details=[f"收入 {fmt(i['revenue_m'])}M、毛利 {i['gross_margin']:.1%}、经济费用 {fmt(i['economic_opex_m'])}M、税 {i['tax_rate']:.1%}、EV/NOPAT {i['multiple']}；随价格解算转债与优先股，成功经济分母 {n:,.3f}M，尚余债 {fmt(c['scenario_inputs'][2]['result']['remaining_debt_m'])}M、优先分配现值 {i['preferred_dividends_PV_m']}M",f"在79.96目标价重新判断价内转换后，翻倍需收入 {fmt(inv['required_revenue_m'])}M；这不能单独证明现实可达，因为12.5%毛利和19倍也必须成立。股数不是声称2027年4月法律上已全部转股"]
    elif typ=='discounted_expansion_SOTP_endogenous_warrants':
        details=[f"存量贸易EV {fmt(i['existing_trade_EV_m'])}M；远期增量税后经营利润 {fmt(i['mature_incremental_NOPAT_m'])}M×{i['mature_multiple']}，折现 {i['years_to_mature']}年、折现率 {i['discount_rate']:.1%}、执行折扣 {i['conditional_execution_discount']:.0%}、再扣尚未出资资本现值 {fmt(i['remaining_unfunded_capital_PV_m'])}M；按四档行权价解算股数/现金",f"翻倍270.62只第一档价内；同条件需远期成熟增量NOPAT {fmt(inv['required_mature_incremental_NOPAT_m'])}M。3–6个月靠承购/融资去风险提前定价，新增产量2029，绝不作为半年利润"]
    else: details=['详细现金流及权益瀑布见独立模型。']
    return '。'.join(details)+'。'
notes={
'SMCI':'重大分歧：V2的“工作中枢”79.44已接近B2旧强成功81.60的假设强度，不能认定最可能值。85B成功收入高于FY27官方上限72B约18%，且CEO指出80B以上可能需要更多资金。4.5B净现金改善中有债务经济转股贡献，不等于4.5B经营现金。',
'ENPH':'1.55是近零盈利长期资本化的极端压力，不是完整清算估值，也非可比损失分位。净金融现金若烧损0/150/300M，独立压力约2.67/1.56/0.46每股，不能与含利息PE简单相加。成功核心EPS2.08×27=56.16；仅达到翻倍仍需约941M新增SST期权，强成功模型给予2.3B，均非订单价值认证。',
'CLS':'44B收入较FY26指引20.5B×公司2027增长>65%的最低起点33.825B高约30%；需要更远期增长提前反映。成功700.98略越翻倍，倍数降到24或经营利润率回到8%，即约601.90/591.47，均不足翻倍。',
'MOD':'成功经济EBIT率19.5%接近旧FY28调整EBITDA率约20.3%，折旧等空间很小，需要分拆后新证据。10月12日新买者不能另加已于10月1日分配给旧股东的THRM。',
'ADBE':'重点复活公司。FY26 GAAP EPS中点18.145；若PE23，翻倍所需EPS20.71比该起点高约14.1%，但当前约13.1倍到23倍的重估才是更大假设。独立外部373是12个月目标，不能拿来证明476的半年目标。MAX 11月10–12日及12月1日CEO交接已公告；财报12月/3月只是预计窗口。',
'AMPX':'强成功10倍收入对应税后经营利润倍数约114，增长确定性必须提高才有支撑。CAMINUS计划Q1/27美国代工量产；政府74.793M总额只有22.3M初始资金且按验收支付。Q2 bill-and-hold为零减弱旧短报告部分担忧，不能推导全部质量问题已消失。',
'IREN':'全公司资金桥仍未闭合。已指定微软GPU包融资加预付较设备资本开支约差220M，另有设施、其他GPU和利息。NVIDIA 30M股×70是购买权，翻倍价69.60还低于行权价。失望模型接近归零，故明确不属于下行有限组。',
'AAOI':'10月5日ATM净588M与5.694845M新增股只计一次。200M以上首笔1.6T订单是3月旧公告，不能称10月新获得。官方650k/月与媒体930k/月口径未完全统一；成功40%毛利、收入3.2B需要实物交付、良率和现金共同验证。',
'VISN':'现金与回购同时变化，不能既保留全额现金又用回购后低股数。160M退税预计2027H2，排除在4月现金桥之外；旧15美元特殊分配不计新买者收益。现金缓冲较有意义，但并非股价地板。',
'BNTX':'大额欧元现金使同类临床风险具有缓冲；需估值的仍是归属公司、扣合作方分成后的管线。强成功肿瘤权益31B为研究代理，未逐合同重建。数据为事件累积驱动，时间和结果都可能变化；Duality自有DB1310不能自动算作BioNTech资产。',
'KYTX':'Q4申报完成、FDA受理、获批、上市四件事分开；潜在年中上市在4月之后。已借25M、可申请A余15M和后续有条件贷款不能相加称在手150M。临床/CMC失败仍有大额永久损失可能。',
'LEU':'强成功378.64时四档权证都价内，翻倍270.62时仅第一档价内；行权现金和稀释必须同时算。模型把2032年前后的成熟收益折回2027，不把900M DOE合同或2029新增首产写成未来半年收入。',
'UCTT':'本轮复议补扣NCI未来价值，成功价由172.54降至161.92。期初净金融债约344.1M；目标550–600M属于融资/资金消耗条件。H1自由现金流为负，收入增长不能自动等于归母可分配现金。',
'PSIX':'9月新220M授信替代旧135M并延长到2029；初借35M，名义未用185M受借款基数、LC和契约约束，并非185M自由现金。Q2同比收入下降与环比利润恢复同时为真，未来1.05B成功收入不是公司正式承诺。',
'ACMR':'2.5B上海backlog含已出货待验收，不是下两个季度收入。模型按约27%少数权益扣除，8月4日法律A+B股为69.649196M；国内子公司估值不能全归美国普通股。',
'AOSL':'先进计算在全公司中的占比仍要从业务嵌套口径拆出，AI增长不等于集团扭亏。当前9月季指引的调整毛利与费用仍可能对应经营亏损，成功收入950M/34%毛利显著超越当前状态。',
'RDW':'优先股已转普通股，不能再次扣历史优先本金；2026年新增股融令现金增加，但股数也升至约250M。成功仍约7倍收入/73倍税后经营利润，需要订单兑现；航天、无人机和防务收入不是同一增长来源。',
'CRWV':'RPO103.7B主要在多年履约，不能当6个月收入。目标净债45–58B不是已承诺可提款资金，GPU折旧、利息和设备应付款期限都重要。失望情景股权可归零；只有接受融资与客户验收高风险才适合此条件席位。',
'MU':'FY26Q4为14周，不能直接乘四。68.274B净金融现金与客户履约义务分别处理；32B客户承诺、12.895B负债余额和12.747B融资现金流是不同口径。强成功31万M收入与68%税后经营利润率、11倍同时成立才有2089。',
'SNDK':'Q4 GAAP每股收益含证券收益；新增客户押金和预收款不能永久当经营自由现金。无债、现金充足不防范NAND价格与盈利倍数双降；与MU共有存储周期，不能当独立风险分散。'
}
lines=['# 3–6个月超高收益：最终20家公司研究','',('状态：最终研究版本。' if final else '状态：排版工作稿，未完成主席与最后补充反驳签核。'),'','本轮侧重短期翻倍或多倍的可能路径。以下20家是本项目内优先研究的机会集合，含明确条件席位；并非20个大概率翻倍预测，也不是按情景最高价格排出的名单。上一份3–18个月名单原样保留，本轮独立建档。','','信息截止：2026-10-12 20:50（洛杉矶）；价格锚：10月12日正常收盘、美元。三个月检查点2027-01-12，六个月检查点2027-04-12。盘后已公开信息与收盘价格可能存在时间差。价格收益不含个人税费、汇率、滑点，QQQ/SPY用于事后同窗比较。','','## 最终名单与条件估值','','“工作情景”不是概率均值，也不保证是最可能结果；“强成功”要求多项条件共同成立。下行栏是各公司特定经营/融资压力，严重程度不同，不能直接当可比VaR、止损线或最大亏损。所有价格来自V2条件模型并经控制器独立重算。','','|序|公司|机制/分层|10/12价格|压力价|工作情景|强成功价|强成功涨幅|更强右尾价|','|---:|---|---|---:|---:|---:|---:|---:|---:|']
for e in selection:
    t=e['ticker'];c=models[t];ss=c['scenario_inputs']
    lines.append(f"|{e['rank']}|{t}|{clean(e.get('tier','条件研究'))}|{fmt(c['price'])}|{fmt(ss[0]['result']['price'])}|{fmt(ss[1]['result']['price'])}|{fmt(ss[2]['result']['price'])}|{pct(ss[2]['return_pct'])}|{fmt(ss[3]['result']['price'])}|")
lines+=['','在回报机会相近时，ADBE、VISN、BNTX具有较明确的经营现金或净现金缓冲；它们的翻倍仍分别依赖估值修复、剩余业务与资本配置、临床资产价值提高。IREN、AAOI、CRWV、KYTX、AMPX等的上行更依赖执行/临床/融资跳变，不能称下行有限。MU与SNDK保留同一大趋势的两种弹性，明确属于相关风险。','','## 每家公司为什么入选、怎样被推翻','','金额M为百万美元；BNTX原始现金以欧元计并单独换算。模型使用未来完整年度收入/利润，是假设市场在两次财报或事件后提前定价，不是把年度利润算作半年已经赚到的钱。','']
cards=[]
for e in selection:
    t=e['ticker']; c=models[t]; f=facts[t]; w=work.get(t,{}); s1=roledata['S1'].get(t,{}); s2=roledata['S2'].get(t,{})
    w=dict(w)
    for k,key in [('mechanism','mechanism'),('touch','touch_2x'),('hold','hold_2x_april12'),('left_tail','left_tail'),('dissent','major_dissent'),('change','new_evidence'),('opponents','alternatives')]:
        if key in e: w[k]=e[key]
    card={'decision':e,'chair_working_argument':w,'facts':f,'valuation':c,'role_coverage':{'round1_targeted':trail[t].get('deep_read_roles',[]),'S1':t in roledata['S1'],'S2':t in roledata['S2'],'B1':t in roledata['B1'],'B2':t in roledata['B2'],'V1':True,'V2':True},'controller_note':notes.get(t,''),'source_records':ticker_sources(t)}; cards.append(card)
    lines+= [f"## {e['rank']}. {t} — {universe[t]['name']}",'',w.get('mechanism',f['value_mechanism']),'',f"**三个月检验：** {f['event_3m']}。 **六个月检验：** {f['event_6m']}。",'']
    if t=='CLS': lines+=['日历补正：官方已确认10月26日盘后财报、10月27日投资者日；早版V1的“约10月估计”已被末轮原始资料核验替换。','']
    if t=='ADBE': lines+=['新增确定节点：[Adobe MAX 11月10–12日](https://www.max.adobe.com/)；[新CEO于12月1日履任](https://news.adobe.com/news/2026/09/adobe-announces-anil-chakravarthy-to-become-president-and-ceo)。节点存在不等于商业化成功。','']
    if t=='ADBE': lines+=['外部对照：[10月12日署名多头报道](https://247wallst.com/investing/2026/10/12/adobe-keeps-cratering-one-wall-street-pros-thesis-projects-50-gains-in-the-next-year/)强调企业工作流、现金和AI付费，引用Bernstein 373的12个月目标；[同日另一署名报道](https://www.investing.com/news/stock-market-news/adobe-stock-is-cheap-valuation-a-trap-93CH-4944216)集中于净新增ARR放缓和估值陷阱。这是公开二手报道，未取得原始券商全文。控制器又核了Canva免费Affinity及Anthropic设计工具原文；竞争能力存在并不等于已经造成Adobe实际客户流失。','']
    if t in ['CLS','MOD','SMCI','ENPH'] and e.get('late_rebuttal'):
        lines+=['末轮外部与反方复核：'+e['late_rebuttal'].get('external',e['late_rebuttal'].get('rebuttal',''))+' 详见'+link('B2末轮补充','03_round2/B2_末轮补充反驳.md')+'。','']
    lines += [f"**已核事实与边界：** {f['independent_finding']} 〔[原始资料]({f['source_urls'][0]})；读取范围为相关决定段〕",'', '**翻倍需要什么：** '+model_explain(c),'', '**资本、下行与关键修正：** '+notes.get(t,c['fully_diluted_logic']),'', '**多方观点后的判断：** '+(s1.get('strongest_bull','')+' '+s1.get('strongest_bear','') if s1 else s2.get('bull_bear','见控制器专项、两反驳与主席配对比较。')),'']
    # Preserve attribution: these are this team's interpretations, not analyst price targets.
    lines += ['**最强反驳：** '+str(roledata['B1'].get(t,{}).get('decisive_rebuttal',w.get('dissent',''))),'','**与替代公司的取舍：** '+str(e.get('why_selected',e.get('selection_reason',w.get('change',''))))+' 具体替代：'+'、'.join(w.get('opponents',[]))+'。','', '**反转条件：** '+str(e.get('invalidator',e.get('condition',s2.get('revive_or_kill',w.get('left_tail',''))))),'','**触及与维持：** '+w.get('touch','需事件和估值同时支持。')+' '+w.get('hold','期末维持需后续现金/交付证据。'),'','**保留异议：** '+str(e.get('major_dissent',w.get('dissent','详细见两反驳稿。'))),'','核验链：首轮定向阅读 '+str(len(trail[t].get('deep_read_roles',[])))+' 个角色；'+('/'.join(k for k in roledata if t in roledata[k]))+'；V1 原始事实；V2 数字与资本；控制器独立复算；主席逐项比较。角色重复访问同一公告不视为多个独立事实。','','来源与实际可读范围：','',source_links(t),'']
old='NVDA ADBE MU PNR CLS AVGO PSIX ARGX BNTX SMCI AGCO IREN SNDK BDC ALNY BABA CRM VST KYTX CARR'.split()
overlap=[t for t in selected if t in old];new=[t for t in selected if t not in old];removed=[t for t in old if t not in selected]
lines+=['## 与上一名单的关系','',f"重合 {len(overlap)} 家："+'、'.join(overlap)+'。', '', '本轮新增：'+'、'.join(new)+'。', '', '上一名单保留、但本轮未入选：'+'、'.join(removed)+'。没有因此否定其3–18个月价值；本轮要求更近的翻倍催化。','',link('上一轮完整报告',pathlib.Path('../2026-10-12_20家公司多角色实验/06_final/最终20家公司投资研究.md')),'','## 淘汰、复活与候补','',link('主席完整裁决与配对取舍','05_chair/主席裁决.md')+'记录候补及逐项逆转条件。首轮44家获得正式提名；ICHR虽未在44家内，因设备订单与毛利弹性被重新审查，最终未必胜过末位替代。ADBE仅一位首轮提名，但重新查现金流、AI收入嵌套、竞争产品和外部多空后进入末位对决；提名次数没有决定排名。','','ALNY因版税与净利息的实质纠错，强成功由526降至324，不再因旧85%毛利假设获得翻倍席位。FLNC有反弹潜力，但焊接/交付、未来利润与现金修复门槛更高。POET需兑现从低基数到大规模收入，合同总额和募资额不是交付和现金余额；WOLF/TE的资本结构风险更难优先于现有候选。','', '## 研究规模与复核边界','','本实验使用12个Astra子角色：5位独立研究者、2位专项深研、2位反驳者、2位核验者、1位主席，控制器负责冻结、额外外部核查、回流与算术复算。系统同时最多3个子代理，按阶段轮转；主会话模型和1.5倍速度没有可调用的切换字段，未声称已经切换。','','五位首轮各扫描245家公司结构化资料，再分别定向深读29/30/28/32/32家；不是245家全部报告都被五人逐字读完。945份核心上游资料和200份附加材料冻结留档。阶段依次为全池独立筛查、专项深研、业务/估值反驳、V1/V2核验、主席配对和复活、末轮专项再反驳/数值修订、控制器终检。12是角色数，不能改称12轮独立结论。','','V1与V2各覆盖38家公司；V2给出152个四情景。控制器另写独立程序复算1120项公式、翻倍反解、转换证券、汇率和已有条件现金桥。通过只证明算术一致；很多公司的完整季度资金桥、临床逐合同rNPV仍未闭合，已经在逐卡/模型写明。四个现金桥是条件算术闭合，不是银行额度或预测认证。','','外部观点用于找漏项、推翻错误与检验预期差。原始公告、同源转载、全文、相关段、公开摘要、搜索片段和访问失败分别记录；外部12个月目标价不能直接变成半年目标。源链接数量不是独立证据数，也不自动提高成功概率。','','## 共同风险与何时换名单','','该名单包含多条路径，却仍显著暴露于AI资本开支、存储价格、低利率/高估值和融资窗口。AI验收/扩产同时变慢，可能同时影响IREN、CRWV、AAOI、SMCI、CLS、MOD及存储/设备公司；不能因股票数量20就认为已经充分分散。','','更换条件按事实触发：订单取消或验收延迟、毛利未达而费用/库存上升、融资条款改变每股价值、临床/CMC读出破坏机制、估值已先涨而盈利未跟上。若股价先翻倍但业务证据没有同步增加，触及目标与继续持有是两次不同决策。反之，被排除公司获得新原始证据可以回流，不沿用淘汰标签。','','## 留档与未来回溯','',link('20家公司结构化完整卡','06_final/最终20家公司完整卡.json')+'；'+link('245家公司完整轨迹','06_final/245家公司筛选轨迹.csv')+'；'+link('角色覆盖矩阵','06_final/多角色验证矩阵.md')+'。', '',link('38家四情景模型','04_verification/V2_models.json')+'；'+link('控制器独立复算','04_verification/控制器_模型独立复算.md')+'；'+link('全部外部来源与阅读状态','06_final/外部来源总索引.md')+'；'+link('原名单和上游保全检查','00_control/preservation_audit.json')+'。','','事后对每家分别记录：窗口内最高收盘/最高盘中是否达到2倍、1月12日/4月12日收盘收益、含分配总回报、对QQQ/SPY超额、实际股数/融资/催化与当初假设差异。股拆与分配必须一致调整，不能只复盘赢家或把最终信息填回原始假设。模板在同目录《未来回溯模板.csv》；未设置自动交易或定时任务。','']
if chair.get('reserves'):
    at=lines.index('## 研究规模与复核边界')
    reserve_lines=['候补可随新证据重新进入；此处是本轮3–6个月目标下的取舍。','','|候补序|公司|未进入本轮20的决定性理由|','|---:|---|---|']
    for a in chair['reserves']: reserve_lines.append(f"|{a['reserve_rank']}|{a['ticker']}|{clean(a['reason'])}|")
    lines[at:at]=reserve_lines+['']
(R/outdir/'最终20家公司超高收益研究.md').write_text('\n'.join(lines),encoding='utf-8')
save(outdir+'/最终20家公司完整卡.json',dict(status='final' if final else 'draft',cutoff='2026-10-12T20:50:00-07:00',price_date='2026-10-12',checkpoints=['2027-01-12','2027-04-12'],selection_basis='relative research priority, not calibrated 2x probabilities',overlap_previous=overlap,new_to_list=new,previous_not_in_this_list=removed,companies=cards))
with (R/outdir/'最终20家公司数值总表.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['序','代码','公司','分层','正常收盘USD','压力价','工作情景价','强成功价','强成功涨幅pct','更强右尾价','翻倍价','模型','主要条件'])
    for e in selection:
        t=e['ticker'];c=models[t];s=c['scenario_inputs'];wr.writerow([e['rank'],t,universe[t]['name'],e.get('tier',''),c['price'],*[round(x['result']['price'],4) for x in s[:3]],round(s[2]['return_pct'],4),round(s[3]['result']['price'],4),2*c['price'],c['model_type'],notes.get(t,'')])
matrix=['# 多角色与多轮验证矩阵','','同一角色多次打开同一公告不算多个独立来源。首轮“扫描”与“定向深读”分开；B2末轮新增CLS核验，ADBE专项深研由控制器承担。','', '|代码|首轮扫描角色数|首轮定向角色数|专项|业务反驳|估值反驳|V1|V2|控制器复算|主席|','|---|---:|---:|---|---|---|---|---|---|---|']
for e in selection:
    t=e['ticker'];sp='/'.join(k for k in ['S1','S2'] if t in roledata[k]) or '控制器ADBE专项'
    matrix.append(f"|{t}|5|{len(trail[t].get('deep_read_roles',[]))}|{sp}|{'有' if t in roledata['B1'] else '缺'}|{'有' if t in roledata['B2'] else '待末轮'}|有|有|有|{'已裁决' if final else '待封卷'}|")
(R/outdir/'多角色验证矩阵.md').write_text('\n'.join(matrix)+'\n',encoding='utf-8')
trajectories=[]
for t,u in universe.items():
    a=trail[t];selected_row=next((e for e in selection if e['ticker']==t),None)
    phases=[k for k in roledata if t in roledata[k]]+(['V1'] if t in facts else [])+(['V2'] if t in models else [])
    trajectory=dict(ticker=t,name=u['name'],category=u['category'],round1_scan_count=5,round1_targeted_roles=a.get('deep_read_roles',[]),round1_nominations=a.get('nominations',[]),round1_reserves=a.get('reserves',[]),later_roles=phases,final_rank=selected_row.get('rank') if selected_row else None,status='最终20' if selected_row else ('深研后候补/未入选' if phases else '初筛后未进入本轮重点，不等于无投资价值'),revival=t in ['ICHR','ADBE','CC','UCTT','PENG','AEHR'],source_paths=u['sources'])
    trajectories.append(trajectory)
save(outdir+'/245家公司筛选轨迹.json',trajectories)
with (R/outdir/'245家公司筛选轨迹.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['代码','公司','分类','首轮扫描角色数','首轮定向深读角色','提名数','后续角色','最终序','状态','复活/额外遗漏审查','公司报告路径'])
    for d in trajectories: wr.writerow([d['ticker'],d['name'],d['category'],5,';'.join(map(str,d['round1_targeted_roles'])),len(d['round1_nominations']),';'.join(d['later_roles']),d['final_rank'],d['status'],d['revival'],';'.join(d['source_paths']['company'])])
with (R/outdir/'未来回溯模板.csv').open('w',encoding='utf-8-sig',newline='') as f:
    wr=csv.writer(f);wr.writerow(['代码','参考日','参考价USD','三月观察日','六月观察日','窗口最高盘中_待填','窗口最高收盘_待填','首次触及2倍日_待填','三月收盘_待填','六月收盘_待填','分红拆股调整_待填','含分配总收益_待填','QQQ同窗收益_待填','SPY同窗收益_待填','实际融资股数_待填','事件兑现_待填','原假设哪里错_待填'])
    for t in selected: wr.writerow([t,'2026-10-12',models[t]['price'],'2027-01-12','2027-04-12']+['']*12)
source_index=load('06_final/外部来源总索引.json')
stats=dict(status='final' if final else 'draft',companies=245,final20=selected,overlap_count=len(overlap),source_record_count=source_index['source_record_count'],unique_logged_urls=source_index['unique_logged_urls'],unique_urls_all_references=source_index['unique_urls_all_references'],roles=12,peak_subagent_concurrency=3,model='gpt-6-astra for all specified child roles',speed='1.5x not programmatically set',report_bytes=(R/outdir/'最终20家公司超高收益研究.md').stat().st_size)
save(outdir+'/交付统计.json',stats)
print(json.dumps(stats,ensure_ascii=False))
