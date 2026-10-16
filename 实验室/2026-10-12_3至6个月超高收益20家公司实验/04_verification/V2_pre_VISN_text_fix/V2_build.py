from pathlib import Path
import json,csv,re,math,hashlib
R=Path(__file__).resolve().parents[1]
U={x['ticker']:x for x in json.loads((R/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))}
B={x['ticker']:x for x in json.loads((R/'03_round2/B2_valuation_rebuttal.json').read_text(encoding='utf-8-sig'))['companies']}
S1={x['ticker']:x for x in json.loads((R/'03_round2/S1_ai_deep.json').read_text(encoding='utf-8-sig'))['companies']}
S2={x['ticker']:x for x in json.loads((R/'03_round2/S2_nonai_deep.json').read_text(encoding='utf-8-sig'))['companies']}
branches=['失望','工作中枢','强成功','更强右尾']
# Independent conditional operating sets. R/Opex USD millions, N million economic shares.
# EV rows: revenue,gross_margin,opex_rate(including economic SBC),tax,multiple,shares,net_debt.
EV={
'MU':[(180000,.65,.09,.17,7,1170,-65000),(260000,.84,.07,.16,9,1160,-90000),(310000,.87,.07,.15,11,1160,-105000),(350000,.88,.065,.15,13,1165,-120000)],
'SNDK':[(32000,.62,.085,.17,6,158,-5000),(46000,.81,.065,.16,9,157,-9000),(59000,.85,.06,.15,12,158,-13000),(68000,.86,.055,.15,14,160,-16000)],
'IREN':[(4000,.35,.18,.22,18,510,9000),(6500,.40,.15,.20,23,495,8000),(8500,.44,.15,.20,26,500,8500),(11000,.46,.14,.20,30,540,10500)],
'AAOI':[(1300,.24,.15,.20,18,102,-100),(2100,.33,.12,.20,25,104,-300),(3200,.40,.12,.20,30,108,-300),(4300,.42,.105,.20,34,113,-300)],
'CRDO':[(2400,.60,.33,.17,25,211,-500),(3700,.64,.26,.17,33,214,-650),(5500,.65,.23,.17,42,218,-800),(7000,.66,.22,.17,47,225,-900)],
'CRWV':[(17000,.25,.13,.22,18,810,50000),(27000,.34,.12,.20,24,820,48000),(37000,.37,.115,.20,27,850,52000),(48000,.39,.11,.20,30,900,58000)],
'UCTT':[(2800,.16,.105,.22,16,50,600),(3500,.19,.105,.21,20,51,550),(4500,.22,.105,.20,23,52,550),(5500,.24,.10,.20,26,54,600)],
'CLS':[(24000,.115,.055,.22,18,132,-500),(34000,.13,.05,.21,24,132,-800),(44000,.15,.055,.20,28,135,-1000),(53000,.16,.05,.20,31,138,-1200)],
'MOD':[(3000,.24,.11,.23,18,56,500),(4000,.28,.105,.22,23,56.5,400),(5100,.30,.105,.22,27,57,450),(6200,.32,.11,.22,30,58,600)],
'COHR':[(10000,.36,.20,.22,18,211,2200),(13500,.40,.18,.22,25,214,2300),(17000,.43,.17,.21,31,218,2500),(21000,.46,.17,.21,35,225,3000)],
'NVDA':[(430000,.69,.10,.18,19,24400,-90000),(580000,.74,.09,.17,24,24300,-115000),(760000,.76,.09,.17,27,24200,-145000),(900000,.77,.09,.17,30,24200,-170000)],
'TTMI':[(4700,.22,.12,.22,17,113,1800),(5800,.26,.115,.21,23,114,1700),(7300,.29,.12,.21,27,117,1600),(9000,.31,.12,.21,30,120,1700)],
'AEIS':[(2500,.37,.21,.22,19,43,100),(3300,.40,.20,.21,24,44,50),(4300,.44,.205,.21,28,45,0),(5300,.46,.20,.21,32,46,-100)],
'NBIS':[(10000,.24,.16,.22,20,395,13000),(18000,.35,.14,.20,26,405,14000),(27000,.39,.14,.20,30,420,16000),(35000,.42,.14,.20,34,445,19000)]}
# PE rows: revenue,GM,annual economic Opex,net interest cost,tax,NCI fraction,preferred distribution,shares,PE,incremental option EV.
PE={
'PSIX':[(700,.22,80,10,.24,0,0,24,14,0),(870,.265,91,8,.24,0,0,24.5,18,0),(1050,.29,111,8,.24,0,0,25,23,0),(1300,.31,145,10,.24,0,0,26,27,0)],
'ENPH':[(1100,.40,425,0,.22,0,0,136,18,0),(1450,.44,450,-10,.22,0,0,137,23,900),(1850,.46,495,-12,.22,0,0,138,27,2300),(2200,.47,550,-12,.22,0,0,140,30,4500)],
'ACMR':[(1100,.42,250,-10,.20,.25,0,72,18,0),(1500,.44,290,-10,.20,.26,0,73,24,0),(2000,.46,355,-10,.20,.27,0,75,31,0),(2600,.47,440,-10,.20,.28,0,78,35,0)],
'AVAV':[(2200,.27,390,45,.23,0,0,54,24,0),(2800,.31,480,50,.23,0,0,55,31,0),(3400,.34,560,50,.23,0,0,57,38,0),(4200,.36,675,60,.23,0,0,60,42,0)],
'ALNY':[(5500,.72,3400,200,.23,0,0,138,25,0),(6900,.73,3750,210,.23,0,0,140,30,0),(8500,.74,4300,220,.23,0,0,143,34,0),(10500,.75,5000,230,.23,0,0,147,38,0)],
'ADBE':[(26000,.88,14700,0,.22,0,0,395,12,0),(28000,.895,14900,0,.22,0,0,390,18,0),(29500,.90,14800,0,.22,0,0,388,23,0),(31500,.90,15300,0,.22,0,0,385,27,0)],
'PNR':[(3900,.32,630,160,.22,0,0,165,13,0),(4500,.35,640,150,.22,0,0,164,18,0),(4900,.38,670,140,.22,0,0,163,22,0),(5400,.39,720,135,.22,0,0,162,25,0)],
'PLAB':[(820,.31,98,-12,.22,.30,0,60,13,0),(950,.35,107,-13,.22,.30,0,60,18,0),(1100,.38,122,-13,.22,.30,0,61,23,0),(1300,.40,145,-14,.22,.30,0,62,27,0)],
'ICHR':[(1250,.135,135,8,.20,0,0,39,18,0),(1500,.175,140,8,.20,0,0,39.5,23,0),(1800,.205,145,8,.20,0,0,40,26,0),(2100,.225,165,8,.20,0,0,41,29,0)]}
# Sales rows include coherent forward cost budgets to make premium visible, not silently label revenue multiple a profit model.
# revenue,gm,opex,tax,EV/sales,shares,netdebt
SALES={
'AMPX':[(110,.22,60,.22,3,168,-25),(220,.29,62,.22,7,165,-50),(330,.34,75,.22,10,175,-65),(480,.37,95,.22,12,190,-90)],
'RDW':[(460,.22,125,.22,2.5,270,-330),(620,.27,143,.22,5,272,-390),(850,.32,168,.22,7,280,-400),(1100,.35,205,.22,9,300,-420)],
'AOSL':[(610,.24,195,.22,.65,33,-95),(770,.29,202,.22,1.2,33.5,-120),(950,.34,210,.22,2,34,-140),(1200,.37,240,.22,2.7,35,-160)],
'AMBA':[(420,.57,295,.22,3,48,-180),(580,.61,310,.22,6,48,-220),(800,.64,345,.22,9,49,-230),(1100,.66,420,.22,11,51,-250)],
'MRAM':[(60,.48,42,.22,1.5,28,-25),(100,.56,48,.22,4,27,-32),(145,.60,58,.22,7,28,-35),(220,.63,76,.22,9,30,-45)],
'POET':[(25,.20,65,.22,6,320,-530),(100,.40,85,.22,10,315,-600),(240,.50,110,.22,15,330,-650),(450,.55,145,.22,18,360,-700)]}
# EBITDA rows revenue,GM,cash Opex including SBC-equivalent economic cost,DA,tax,K,shares,netdebt,annual maintenance capex.
EBITDA={
'VISN':[(900,.29,166,35,.23,5,231,-550,35),(1080,.33,172,37,.23,7,215,-550,40),(1220,.36,180,42,.23,8.5,210,-530,45),(1400,.38,195,48,.23,10,207,-510,55)],
'FLNC':[(2400,.075,280,40,.22,8,225,500,35),(3000,.12,295,45,.22,13,200,300,40),(3900,.15,345,50,.22,18,202,200,45),(5000,.17,430,60,.22,20,210,100,55)],
'CC':[(5000,.22,410,300,.24,5,157,3800,330),(5550,.245,465,310,.24,6.5,156,3400,350),(6200,.27,510,330,.24,7.5,156,3150,370),(6800,.29,580,350,.24,8.5,157,3000,410)]}
SOURCE={}
def src(t,url,note): SOURCE[t]={'id':'V2_'+t,'ticker':t,'url':url,'access_date_utc':'2026-10-13','access_status':'opened_primary_relevant_passages','note':note,'not_full_filing_audit':True}
# Pick exact independently reopened primary URLs from access transcripts, using path token.
web='\n'.join(json.loads(p.read_text(encoding='utf-8')) for p in sorted((R/'07_logs').glob('V2_web_access_*.json')))
urlall=list(dict.fromkeys(re.findall(r'Source: open\(\{"ref_id":"(https[^" ]+)',web)))
tokens={'MU':'Micron-Technology','SNDK':'sndkq4','SMCI':'smci-20260630.htm','IREN':'iren-reports-fy26','AAOI':'aaoi_ex9901','CRDO':'Credo-Technology','CRWV':'crwv-20260630','UCTT':'q22026pressrelease.htm','CLS':'celestica-announces-second','MOD':'Modine-Reports-First','COHR':'earnings-release-fy26-q4','KYTX':'kytx-ex99_1','AMPX':'detail/172','ENPH':'enphase-energy-reports-financial','PSIX':'d28951d8k','FLNC':'flnc-20260630','VISN':'visn-ex99_1','BNTX':'a991bntx','LEU':'tm2625019d5','RDW':'exhibit991redwire','AVAV':'2e8254ff','AOSL':'aosl-20260630','ACMR':'acmr-20260630','AMBA':'amba-20260731','MRAM':'mram-20260630','CC':'the-chemours-company-reports','ALNY':'ddc78e15','IONS':'000087401526000251','POET':'poet-technologies-reports','ADBE':'adbeex991','PNR':'000007736026000042','PLAB':'node/19681','ICHR':'ichr-20260626','NVDA':'nvidia-announces-financial','APLD':'detail/163','NBIS':'nbis-20260812','TTMI':'d147406dex991','AEIS':'AEIS_2026_Q2'}
for t,k in tokens.items():
    matches=[x for x in urlall if k in x]
    if t=='UCTT': matches=[x for x in matches if '1275014' in x]
    assert matches,(t,k)
    src(t,matches[0],'相关原始资料独开；具体读取段见V2_web_access_*.json，非全文通读。')
SOURCE['AEIS']['access_status']='opened_primary_metadata_and_limited_text; capital facts inherited S1'
# cash,financial debt,date,actual legal shares,date; None means not independently closed, never zero.
ACT={
'MU':(73453,5179,'2026-09-03',1131.423212,'2026-10-02'),'SNDK':(4762,0,'2026-07-03',146.419001,'2026-08-07'),
'SMCI':(7500,8700,'2026-06-30',656.882499,'2026-06-30'),'IREN':(5895.6,None,'2026-06-30',None,None),
'AAOI':(None,None,'2026-06-30',None,None),'CRWV':(None,35551,'2026-06-30',None,None),
'UCTT':(255.9,600,'2026-06-26 principal; carrying599.4',None,None),'CLS':(535.7,None,'2026-06-30',None,None),
'MOD':(95.3,528.2,'2026-06-30',None,None),'COHR':(1987,3222.2,'2026-06-30',None,None),
'KYTX':(199.427,25,'2026-06-30',61.8434,'2026-08 inherited S2'),
'AMPX':(74.517,0,'2026-06-30',None,None),'ENPH':(937.7,575,'2026-06-30',None,None),
'PSIX':(70.1,72.6,'2026-06-30 inherited S2',None,None),'FLNC':(338.9,400,'2026-06-30',184.596369,'2026-07-31'),
'VISN':(None,0,'post-divestiture debt redemption; cash not reconciled',None,None),
'BNTX':(None,None,'2026-06-30 EUR basis',251.204366,'2026-06-30'),
'LEU':(1868.5,1207.5,'2026-06-30 inherited frozen',None,None),'RDW':(None,48.061,'2026-06-30',249.221102,'2026-06-30'),
'AVAV':(580.2,747.5,'2026-07-31 cash inherited S2/debt opened call',None,None),
'AOSL':(180.771,None,'2026-06-30',None,None),'ACMR':(None,None,'2026-06-30',69.649196,'2026-08-04'),
'AMBA':(272.332,None,'2026-07-31',None,None),'MRAM':(43.896,0,'2026-06-30',None,None),
'CC':(671,3900,'2026-06-30 rounded',None,None),'IONS':(2054.585,1345,'2026-06-30 debt inherited S2',None,None),
'PLAB':(672.811,3.893,'2026-08-02',None,None),'ICHR':(256.456,121.875,'2026-06-26 debt principal',37.454229,'2026-07-28'),
'APLD':(None,6400,'2026-08-31 rounded',None,None),'NBIS':(8042.1,None,'2026-06-30',None,None)}
NOTES={
'MU':'原始净金融现金68274；客户押金12895属履约融资，不能既在FCF净除又从净现金再全扣。模型未新增未披露押金。FY26Q4为14周，模型用完整前瞻年度非Q4乘4。强成功87%GM-7%经济费用、15%税才有68%NOPAT。',
'SNDK':'证券1777为市值波动权益资产，不全当现金；当前4762现金并非未来13000。NBM预付用于生产履约，未来FCF不再额外加同一客户款。较高利润率与倍数共同成立为强条件。',
'SMCI':'采用EV经济NOPAT及隐式转换索取权；会计稀释745/761M非2027年经济分母。优先4.3125M股7%股息、最低130.686M普通；2028/2030/2029债转价61.06/55.20/83.44，面值700/2300/1725。价内按经济转换减债增股，不声称法律上已转。另扣剩余优先股息PV，不再扣优先本金；capped calls不计价值为保守压力，未核最终结算。',
'IREN':'5895.6现金不含1724受限；14B现金/承诺/预付不是现金总额。强成功500M股+8.5B净债仍是融资条件非已获，$70 NVIDIA购买权不可在69.60自动视到账。',
'AAOI':'6月508.758包含受限现金；后续588融资需同时加5.694845M股，仅一次。模型现金为扩产后残余，未来100M以上分母含奖励/融资压力；客户warrant未完整按批次闭合。',
'CRDO':'本季SBC87.979M、GAAP经营率25.2%，48.2%调整率不等经济利润。模型强成功65%GM-23%经济费用=42%EBIT，再税17%=34.86%NOPAT，非42%税后。',
'CRWV':'35551现有本金、应付设备和未来扩产均占资本。48–58B净债为条件融资结果，未完成逐项目现金桥，GPU经济折旧已在GM，非EBITDA。不能给予低风险标签。',
'UCTT':'600M可转债本金现金结算，目标股数含溢价/奖励但非已认证。营运库存629.9M，增长不保证现金；未来毛利22%须自制及利用率证实。',
'CLS':'Q2现金535.7，之后3.45B股权融资新增11.129031M股为继承S1并非新增现金全留存。2028收入提前定价需10/27日历与后续两季订单/毛利证实。',
'MOD':'6月净债432.9为分拆前；4月模型对应存续制冷主体，分拆分配已剔除，不加历史THRM权益。强成功15.21%NOPAT低于首轮18%假设。',
'COHR':'1987非受限现金投资/3222.2账债为S1继承，已重开财表相关段但未全核限制。强成功43%GM-17%经济费用=26%EBIT，税21%后20.54%；无法直接用25%税后。',
'KYTX':'25M贷款实借，不等150M额度。模型73M工作股数、75M强成功、90M融资压力；融资后新现金同步记入。贷款受控现金最低额未披露，不虚填。净现金不是失败价格底。',
'AMPX':'74.517现金无金融债为S2继承；OTA总74.793仅22.3初始授权且验收后支付，不加全部到账。sales高倍数意味着跨客户持续扩量预期，非当前利润。',
'ENPH':'剔52M退款、safe-harbor拉货；核心EPS保SBC、全部持续研发，SST只计额外去风险期权，不重复核心收入。2027客户试点不等4月量产。PE已含净利息，不再加937.7现金。',
'PSIX':'220M授信非现金；9/25实际35M借款偿15M旧款与费用，尚未重建6月至9月全部桥。净利息8–10M条件含融资成本；归母PE不重复扣债。',
'FLNC':'7/31 A143.163588+B所附LLC41.432781=184.596369M。全集团经营值除A+LLC，不再扣同一NCI；2030转债21.35在2倍14.14之上不转。EBITDA含经济SBC成本并另显DA/维持资本，强成功仍显著超BMO盈利。',
'VISN':'使用集团经营费用，非只取Aurora core EBITDA。回购150M并减约20–25M股；期末现金550M不是725M+160M退税。2027H2退税不在4月现金。旧分配不归新买入者。',
'BNTX':'6月16634.2M EUR现金证券、251.204366M ADS1:1。四分支EURUSD1.05/1.10/1.15/1.20为汇率假设非即期报价；现金烧钱、回购先在EUR桥再换USD。项目值是伙伴分成后净权益的研究代理，未逐资产闭合BMS及中国伙伴合同分成，不是认证rNPV。',
'LEU':'扩产成熟盈利在2032/33以后，不列FY27；在2027定价需折现及执行折价。普通权证四档各500M，内生解价内行权；基础22.459M含预付权证为继承，奖励/可转溢价另待核。',
'RDW':'原始优先余额0，不能再扣。249.221102M期末普通不是220.467M季均。557.718含受限，目标400净现金须再扣票据与限制；模型为条件非全闭合。',
'AVAV':'官方FY27nonGAAP EPS3.02–3.34为近端基准；强成功模型经济EPS更高需FY28交付上修。FY27资本支出12–14%收入/FCF负影响债；新奖项已在指引不叠加。',
'AOSL':'不能把失望EV/Sales仍设1.5倍。当前近端24.5%nonGAAP GM与46.5M季费仍亏，强成功34%GM/950收入代表转型而非普通恢复；JV出售款已在现金，残余股权未额外估价。',
'ACMR':'8/4封面A64.657388+B4.991808=69.649196M，5.021811为2025年底旧B。归母利润先扣NCI25–28%研究比例；投资收益不年化，PE不再减NCI或全加合并净现金。',
'AMBA':'Q2一次9M研发抵减去除，GM/费用含SBC与经济IP研发成本。9倍销售支撑强成功须客户量产、设计赢转收入及长期利润率溢价，非当前经营倍数。',
'MRAM':'Q2GAAP亏3.589，仅剔4.027诉讼后经济净利0.438；不能加回1.374SBC与1.050NRE后当正常净利。失望销售60M只给1.5倍，非现金底；7倍成功依赖量产和持续许可证明。',
'CC':'毛利率/EBITDA模型保经济SBC，另显正常税和维持CapEx。法律支付已在目标现金桥的部分不再双扣，未定PFAS责任是额外尾部，净债不是全部清偿义务。',
'ALNY':'主席复议纠错：原83–85%总GM没有收入组合支持，已撤回。Q2产品GM74.6%、总GM约76.88%；AMVUTTRA大于1.5B销售部分30%版税，nucresiran尚未上市不能提前抹掉。四档总GM72/73/74/75%；另把净利息由45–60提高200–230M，Q2净利息53.908M且含出售未来版税负债成本，不能漏掉。所有费用含SBC；此修订强成功不再2倍。',
'IONS':'2054.585现金证券减1345可转债≈709.585起点，后续烧钱；Royalty Pharma转让收益权在产品资产归属内扣，不再全当普通金融债扣。失败项目pelacarsen/TTR未加资产值。',
'POET':'官网图表不等已取得SEDAR完整现金表，830融资额不能认证现金。目标600–700净现金与300M以上股数为敏感性；客户权证通过净收入口径和股数处理，尚未逐批闭合。',
'ADBE':'FY26GAAP18.12–18.17 vs非GAAP24.45–24.50，每股SBC调整5.42不能免费剔除。模型费用含全部正常SBC；买回股数对应现金消耗，不再额外加现金。2倍须增长+23倍重估不是仅廉价。',
'PNR':'Taco1.4B融资提高净利息，2027仅0.10–0.15调整EPS增厚不能独撑翻倍；模型含并购后营收费用与140–160M净利息，去34.9M关税退款。',
'PLAB':'Q3合并43.883M净利扣14.967NCI后28.916M归母；现金672.811含JV持份不全可分配。未来60–62M经济股较63M粗代理更贴近58.7M近期稀释，但法律期末仍待核。',
'ICHR':'37.454229M实际基础，未来39–41M；当前13.9%GM到强成功20.5%须自制内容与利用率。保140–165M经济费、8M净利息、20%正常税假设；不是公司保证税率。',
'NVDA':'75%现GM和16–18%税源已核；55.61%成功NOPAT=76%-9%经济费再17%税，非首轮61%。未额外加权益投资浮盈。',
'APLD':'合并NOI不能无调整全归母；模型分项目归属与CHRN权益，先项目债后归属，再母层索取权。股权瀑布仍未核清，只做逆向压力不能授低下行。',
'NBIS':'8042.1非受限与1056受限分开；EigenAI股份298.7M对价不创造现金。前瞻16B净债/420M股为条件，FY28收入27B仍不自动2倍。',
'TTMI':'Epiq1.1B已现金买下，新增300M TLA+800M TLB以及6.75%债；不作为免费期权。经济GM/费用保折旧与SBC，融资在净债桥。',
'AEIS':'现净现金仅约109.8M为S1继承，不是1.4B。未来43–46M比原40M更审慎，经济强成功18.565%NOPAT需制造效率证明。'}

def evcalc(x):
    r,g,o,t,k,n,d=x; e=r*(g-o); z=e*(1-t)
    return dict(revenue_m=r,gross_margin=g,economic_opex_rate=o,tax_rate=t,multiple=k,shares_m=n,net_debt_m=d,other_claims_m=0),dict(ebit_m=e,nopat_m=z,enterprise_value_m=z*k,equity_value_m=z*k-d,price=max(0,(z*k-d)/n))
def pecalc(x):
    r,g,o,i,t,nci,p,n,k,opt=x; e=r*g-o; ni=(e-i)*(1-t)*(1-nci)-p; eps=ni/n
    return dict(revenue_m=r,gross_margin=g,economic_opex_m=o,net_interest_cost_m=i,tax_rate=t,nci_fraction=nci,preferred_distribution_m=p,shares_m=n,PE=k,incremental_option_value_m=opt),dict(ebit_m=e,economic_parent_net_income_m=ni,economic_EPS=eps,core_equity_m=max(0,ni*k),equity_value_m=max(0,ni*k)+opt,price=(max(0,ni*k)+opt)/n)
def salcalc(x):
    r,g,o,t,k,n,d=x; e=r*g-o; z=e*(1-t); ev=r*k
    return dict(revenue_m=r,gross_margin=g,economic_opex_m=o,tax_rate=t,sales_multiple=k,shares_m=n,net_debt_m=d),dict(ebit_m=e,nopat_m=z,enterprise_value_m=ev,equity_value_m=ev-d,price=max(0,(ev-d)/n),implied_EV_NOPAT=ev/z if z>0 else None)
def ebitdacalc(x):
    r,g,o,da,t,k,n,d,cap=x; eb=r*g-o; tax=max(0,eb-da)*t
    return dict(revenue_m=r,gross_margin_before_DA=g,cash_opex_including_SBC_equivalent_m=o,DA_m=da,tax_rate=t,multiple=k,shares_m=n,net_debt_m=d,maintenance_capex_m=cap),dict(EBITDA_m=eb,EBIT_m=eb-da,unlevered_maintenance_FCF_m=eb-tax-cap,enterprise_value_m=eb*k,equity_value_m=eb*k-d,price=max(0,(eb*k-d)/n))
M=[]
def add(t,kind,rows,fun):
    price=float(U[t]['finance']['最新价格']); a=ACT.get(t,(None,None,None,None,None)); c,d,date,n,ndate=a
    scenarios=[]
    for label,row in zip(branches,rows):
        inp,res=fun(row); scenarios.append({'branch':label,'formula_type':kind,'input_status':'V2 independent research assumptions, not guidance or expectation','forward_operating_period':'FY/CY2027-2028 complete forward year priced on 2027-04-12','inputs':inp,'result':res,'return_pct':100*(res['price']/price-1)})
    b=B.get(t,{}); s=S1.get(t,{}); s2=S2.get(t,{})
    bridge={'status':'not_fully_closed','as_of':'2027-04-12','starting_net_financial_cash_m':c-d if c is not None and d is not None else None,'scenario_target_net_debt_m':[x['inputs'].get('net_debt_m') for x in scenarios],'required_net_cash_change_m':[(-x['inputs']['net_debt_m']-(c-d)) if 'net_debt_m'in x['inputs'] and c is not None and d is not None else None for x in scenarios],'reason':'价格情景内现金/债是研究条件。未逐季核对全部经营、投资、股融、受限账户和回购，不能把差額解释为已获融资。PE模型不再次把净现金加到股价。'}
    M.append(dict(ticker=t,price=price,price_date='2026-10-12 normal close',currency='USD',security_identity='NASDAQ/NYSE listed ordinary common; ADS 1:1 for BNTX only',snapshot_shares_unverified=U[t]['finance']['shares_outstanding'],current_actual_shares={'value_m':n,'date':ndate,'status':'source-specific dated actual; inherited if date label says so' if n else 'not independently extracted; do not substitute snapshot or weighted average'},current_cash_debt={'cash_and_liquid_securities_m':c,'financial_debt_m':d,'date':date,'source_id':'V2_'+t,'status':'mixed verified and explicitly inherited, see note; null is unknown not zero'},fully_diluted_logic=NOTES[t],target_cash_bridge=bridge,model_type=kind,scenario_inputs=scenarios,source_ids=['V2_'+t],source_urls=[SOURCE[t]['url']],baseline_source_notes=NOTES[t],three_month_check=s2.get('checkpoints',{}).get('by_2027_01_12',s.get('inherited_three_month_case',b.get('window_test','下一次季度/年度报告中的增长、利润率、现金与融资检查；精确日历以V1为准'))),six_month_check=s2.get('checkpoints',{}).get('by_2027_04_12',s.get('inherited_six_month_case','4月前至少一至两次实绩/事件同时支持前瞻模型及资本桥，触及不代表站稳。')),alternative=b.get('alternative',s.get('alternative','和核心名单最接近经营/融资替代比较，见V2报告')),unresolved=['现金/法律稀释全桥仍未完全闭合，见逐项说明','情景联合可行性需后续事实验证；没有校准概率']))
for t,v in EV.items(): add(t,'EV_NopAT',v,evcalc)
for t,v in PE.items(): add(t,'economic_parent_EPS_PE_plus_incremental_option',v,pecalc)
for t,v in SALES.items(): add(t,'EV_Sales_with_profit_crosscheck',v,salcalc)
for t,v in EBITDA.items(): add(t,'EV_EBITDA_with_maintenance_FCF_crosscheck',v,ebitdacalc)

# Clinical asset values are conditional risk-discounted market EVs, NOT invented calibrated trial probabilities.
def assetcalc(x):
    assets,cash,shares=x; total=sum(assets.values())
    return {'risk_adjusted_asset_values_m':assets,'net_cash_m':cash,'net_debt_m':-cash,'shares_m':shares}, {'enterprise_value_m':total,'equity_value_m':total+cash,'price':max(0,(total+cash)/shares)}
add('KYTX','conditional_owned_asset_SOTP',[
({'SPS':100,'PMS_gMG_other':30},25,78),({'SPS':450,'PMS_gMG_other':220},75,73),({'SPS':750,'PMS_gMG_other':550},100,75),({'SPS':1200,'PMS_gMG_other':1250},190,90)],assetcalc)
add('BNTX','conditional_owned_asset_SOTP_EUR_cash',[
({'COVID_franchise':500,'oncology_owned_share':3000},(16634.2-2200-300)*1.05,253),({'COVID_franchise':1000,'oncology_owned_share':13000},(16634.2-1700-450)*1.10,249),({'COVID_franchise':1500,'oncology_owned_share':31000},(16634.2-1500-600)*1.15,249),({'COVID_franchise':2200,'oncology_owned_share':47000},(16634.2-1300-700)*1.20,250)],assetcalc)
add('IONS','conditional_owned_asset_SOTP',[
({'marketed_owned_products_royalty_net':3000,'other_pipeline_net':1000},200,180),({'marketed_owned_products_royalty_net':6500,'other_pipeline_net':2800},350,178),({'marketed_owned_products_royalty_net':11000,'other_pipeline_net':4800},400,180),({'marketed_owned_products_royalty_net':15500,'other_pipeline_net':8500},500,187)],assetcalc)

def leu_price(ev,nc,base):
    strikes=[226.8625,272.235,317.6075,362.98]
    for n in range(5):
        shares=base+sum(500/k for k in strikes[:n]); price=(ev+nc+500*n)/shares
        if (n==0 or price>=strikes[n-1]) and (n==4 or price<strikes[n]): return price,shares,500*n
    raise ValueError('warrant fixed point')
def leu(x):
    trade,profit,k,years,discount,execution,remainingfund,nc,base=x
    expansion=profit*k/(1+discount)**years*execution-remainingfund
    ev=trade+max(0,expansion); p,n,proceeds=leu_price(ev,nc,base)
    return dict(existing_trade_EV_m=trade,mature_incremental_NOPAT_m=profit,mature_multiple=k,years_to_mature=years,discount_rate=discount,conditional_execution_discount=execution,remaining_unfunded_capital_PV_m=remainingfund,net_cash_before_warrants_m=nc,base_shares_m=base,warrant_strikes=[226.8625,272.235,317.6075,362.98],warrant_cash_per_tranche_m=500,shares_m=n,net_debt_m=-nc-proceeds),dict(expansion_EV_m=max(0,expansion),enterprise_value_m=ev,warrant_proceeds_m=proceeds,equity_value_m=ev+nc+proceeds,price=p)
add('LEU','discounted_expansion_SOTP_endogenous_warrants',[(600,120,20,7,.14,.40,500,800,22.8),(850,350,25,6,.12,.65,700,950,23),(1100,650,27,5,.11,.80,1000,1000,23.2),(1400,1000,30,5,.10,.9,1300,1100,23.6)],leu)

def smci_price(ev,cash,base,bank,prefpv):
    notes=[(700,61.06),(2300,55.20),(1725,83.44)]
    lo,hi=0.,500.
    def claims(p):
        pr=36.364 if p<27.4997 else (1000/p if p<=32.9989 else 30.304)
        ns=4.3125*pr; debt=bank
        for face,k in notes:
            if p>k: ns+=face/k
            else: debt+=face
        return base+ns,debt
    for _ in range(100):
        mid=(lo+hi)/2;n,d=claims(mid)
        if mid*n+d+prefpv>ev+cash:hi=mid
        else:lo=mid
    p=(lo+hi)/2;n,d=claims(p)
    return p,n,d
def smci(x):
    r,g,op,t,k,c,base,bank,pref=x; e=r*g-op; z=e*(1-t); ev=z*k;p,n,d=smci_price(ev,c,base,bank,pref)
    return dict(revenue_m=r,gross_margin=g,economic_opex_m=op,tax_rate=t,multiple=k,cash_m=c,base_common_plus_employee_shares_m=base,remaining_bank_debt_m=bank,preferred_dividends_PV_m=pref,preferred_units_m=4.3125,preferred_min_rate=30.304,preferred_max_rate=36.364,preferred_initial_price=27.4997,preferred_threshold_price=32.9989,convertible_notes=[{'principal_m':700,'strike':61.06},{'principal_m':2300,'strike':55.20},{'principal_m':1725,'strike':83.44}],shares_m=n,net_debt_m=d-c),dict(ebit_m=e,nopat_m=z,enterprise_value_m=ev,remaining_debt_m=d,equity_value_m=p*n,price=p)
add('SMCI','EV_NOPAT_endogenous_convertibles_and_preferred',[(58000,.095,2300,.21,12,6000,675,5500,600),(72000,.11,2500,.21,16,7200,677,5000,600),(85000,.125,2800,.21,19,8000,680,4700,600),(105000,.14,3400,.21,22,9000,695,4500,600)],smci)

def apld(x):
    noi,k,projectdebt,ownership,chrn,motherclaims,n=x
    parent=max(0,noi*k-projectdebt)*ownership+chrn-motherclaims
    return dict(project_NOI_m=noi,NOI_multiple=k,project_net_debt_m=projectdebt,parent_economic_ownership=ownership,ChronoScale_owned_equity_m=chrn,mother_net_debt_preferred_other_claims_m=motherclaims,shares_m=n),dict(project_EV_m=noi*k,parent_equity_m=parent,price=max(0,parent/n))
add('APLD','project_equity_waterfall',[(450,14,8000,.7,500,700,350),(1000,18,10500,.75,1000,900,360),(1600,21,13000,.75,1600,1100,380),(2300,24,17000,.8,2400,1300,420)],apld)

# Legal liabilities beyond the six-month cash window remain separate from financial net debt.
cc=next(m for m in M if m['ticker']=='CC')
for s,pv in zip(cc['scenario_inputs'],[1300,1050,850,700]):
    s['inputs']['remaining_environment_legal_cash_PV_m']=pv
    s['inputs']['PV_status']='research stress amount for payments after 2027-04-12; not booked liability or liability cap'
    s['result']['equity_value_m']-=pv
    s['result']['price']=max(0,s['result']['equity_value_m']/s['inputs']['shares_m'])
    s['return_pct']=100*(s['result']['price']/cc['price']-1)
cc['baseline_source_notes']+=' 淨金融债与4月后法律环境支出PV分开：1300/1050/850/700M研究压力。未来净债假设仅含4月前支付；后续PV不再含已付部分。原始NC455M的50%为Chemours，跨15年；不能把整个1453M会计环境及诉讼余额全当即期PFAS或责任上限。'
cc['source_urls']+=['https://www.sec.gov/Archives/edgar/data/1627223/000162722326000029/cc-20260910.htm','https://www.sec.gov/Archives/edgar/data/1627223/000162722326000029/cc-ex10_1.htm']
# Inverse precisely uses each strong scenario's cost/capital assumptions, not an imposed 2x result.
uct=next(m for m in M if m['ticker']=='UCTT')
for s,ni in zip(uct['scenario_inputs'],[12,16,24,32]):
    claim=ni*s['inputs']['multiple']
    s['inputs'].update(other_claims_m=claim,NCI_annual_economic_profit_m=ni,NCI_valuation_multiple=s['inputs']['multiple'])
    s['result']['equity_value_m']-=claim
    s['result']['price']=max(0,s['result']['equity_value_m']/s['inputs']['shares_m'])
    s['return_pct']=100*(s['result']['price']/uct['price']-1)
uct['baseline_source_notes']+=' 主席复议后扣NCI研究公允值192/320/552/832M，对应年NCI利润12/16/24/32M乘16/20/23/26；Q2实际3.2、H1 6.2、账面77.3不能当未来公允值。全集团现金债与NCI价值保持同一口径，未再次扣NCI利润。'
for m in M:
    s=m['scenario_inputs'][2];x=s['inputs']; p=2*m['price']; n=x['shares_m']; typ=m['model_type']; inv={'target_price':p,'shares_m':n,'benchmark_branch':'强成功 cost/multiple/capital held constant','not_probability':True}
    if typ=='EV_NopAT':
        ev=p*n+x['net_debt_m']+x.get('other_claims_m',0); nop=ev/x['multiple']; inv.update(required_EV_m=ev,required_NOPAT_m=nop,required_revenue_m=nop/((x['gross_margin']-x['economic_opex_rate'])*(1-x['tax_rate'])))
    elif typ=='economic_parent_EPS_PE_plus_incremental_option':
        ni=(p*n-x['incremental_option_value_m'])/x['PE']; pre=(ni+x['preferred_distribution_m'])/((1-x['tax_rate'])*(1-x['nci_fraction'])); inv.update(required_parent_NI_m=ni,required_EPS=ni/n,required_revenue_m=(pre+x['net_interest_cost_m']+x['economic_opex_m'])/x['gross_margin'])
    elif typ=='EV_Sales_with_profit_crosscheck': inv.update(required_EV_m=p*n+x['net_debt_m'],required_revenue_m=(p*n+x['net_debt_m'])/x['sales_multiple'],required_sales_multiple_at_branch_revenue=(p*n+x['net_debt_m'])/x['revenue_m'])
    elif typ=='EV_EBITDA_with_maintenance_FCF_crosscheck':
        eb=(p*n+x['net_debt_m']+x.get('remaining_environment_legal_cash_PV_m',0))/x['multiple']; inv.update(required_EBITDA_m=eb,required_revenue_m=(eb+x['cash_opex_including_SBC_equivalent_m'])/x['gross_margin_before_DA'])
    elif typ.startswith('conditional_owned_asset'): inv.update(required_owned_pipeline_and_franchise_EV_m=p*n-x['net_cash_m'])
    elif typ.startswith('discounted_expansion'):
        count=sum(p>k for k in x['warrant_strikes']); nn=x['base_shares_m']+sum(500/k for k in x['warrant_strikes'][:count]); ev=p*nn-x['net_cash_before_warrants_m']-count*500
        req=(ev-x['existing_trade_EV_m']+x['remaining_unfunded_capital_PV_m'])*(1+x['discount_rate'])**x['years_to_mature']/(x['mature_multiple']*x['conditional_execution_discount'])
        inv.update(shares_m=nn,warrant_tranches_in_money=count,required_EV_m=ev,required_mature_incremental_NOPAT_m=req)
    elif typ.startswith('EV_NOPAT_endogenous'):
        pref=4.3125*(36.364 if p<27.4997 else 1000/p if p<=32.9989 else 30.304); nn=x['base_common_plus_employee_shares_m']+pref; dd=x['remaining_bank_debt_m']
        for no in x['convertible_notes']:
            if p>no['strike']:nn+=no['principal_m']/no['strike']
            else:dd+=no['principal_m']
        ev=p*nn+dd-x['cash_m']+x['preferred_dividends_PV_m']; nop=ev/x['multiple'];inv.update(shares_m=nn,remaining_debt_m=dd,required_EV_m=ev,required_NOPAT_m=nop,required_revenue_m=(nop/(1-x['tax_rate'])+x['economic_opex_m'])/x['gross_margin'])
    else:
        req=(((p*n+x['mother_net_debt_preferred_other_claims_m']-x['ChronoScale_owned_equity_m'])/x['parent_economic_ownership'])+x['project_net_debt_m'])/x['NOI_multiple'];inv.update(required_project_NOI_m=req)
    m['two_x_inverse']=inv

# Numeric capital bridges where a conditional arithmetic reconciliation is defensible; other rows remain unclosed.
D={x['ticker']:x for x in M}
for m in M:
    t=m['ticker'];m['security_identity']=U[t]['finance'].get('listing_type','listed ordinary common/equity')
    m['share_bridge']={'current_legal_shares_m':m['current_actual_shares']['value_m'],'future_economic_shares_m':[s['inputs']['shares_m'] for s in m['scenario_inputs']],'status':'future minus legal actual includes conditional financing, existing awards, conversion and employee issuance; not all legally committed; see instrument-specific inputs'}
    if t in S2:m['inherited_S2_observed_share_hint']=S2[t].get('shares_m')
D['ADBE']['current_actual_shares']={'value_m':389.2,'date':'2026-09-18','status':'inherited controller primary reopening; V2 independently reopened earnings guide389M weighted denominator only'}
D['ADBE']['share_bridge']['current_legal_shares_m']=389.2
D['ADBE']['three_month_check']='官方MAX 2026-11-10至12与CEO 2026-12-01交接；12月和3月财报时间尚为估计。检查有机ARR、净新增付费、GAAP利润及SBC，不把会议日期等同收益。'
D['BNTX']['current_cash_debt']['financial_currency']='EUR'
D['BNTX']['current_cash_debt']['cash_securities_EUR_m']=16634.2
D['BNTX']['security_identity']='one NASDAQ ADS represents one ordinary share; financial reporting EUR; prices USD'
D['FLNC']['security_identity']='Class A traded plus Class B-linked LLC economic units in full-group denominator; no double subtraction of corresponding NCI'
D['ACMR']['security_identity']='Class A traded, economically equal Class B included; consolidated subsidiary NCI deducted in earnings'
D['LEU']['two_x_inverse']['historical_base_22_459M_comparison']={'base_shares_m':22.459,'first_tranche_added_shares_m':500/226.8625,'cash_proceeds_m':500,'cashless_added_shares_m':(500/226.8625)*(1-226.8625/(2*D['LEU']['price'])),'note':'main forward model additionally carries 0.741M employee/convert premium pressure; old base comparison not substitute'}
def bridge(t,starting,components,notes):
    vals=[]
    for i,cs in enumerate(components):
        ending=starting+sum(cs.values()); vals.append({'branch':branches[i],'starting_net_cash_m':starting,'movements_m':cs,'calculated_ending_net_cash_m':ending,'target_net_cash_m':-D[t]['scenario_inputs'][i]['inputs']['net_debt_m'],'residual_m':ending+D[t]['scenario_inputs'][i]['inputs']['net_debt_m']})
    D[t]['target_cash_bridge'].update(status='arithmetically_closed_conditional_not_forecast_verified',branches=vals,reason=notes)
bridge('MU',68274,[{'net_operating_cash_ex_new_customer_deposits':26000,'net_capex':-25000,'dividends_buybacks_tax_award_and_other':-4274},{'net_operating_cash_ex_new_customer_deposits':52000,'net_capex':-27000,'dividends_buybacks_tax_award_and_other':-3274},{'net_operating_cash_ex_new_customer_deposits':72000,'net_capex':-30000,'dividends_buybacks_tax_award_and_other':-5274},{'net_operating_cash_ex_new_customer_deposits':92000,'net_capex':-33000,'dividends_buybacks_tax_award_and_other':-7274}],'从9/3至4/12流量研究假设；CFO已净掉新增客户押金且含营运资本及税，不能再扣旧12895。不是FY28现金。')
bridge('KYTX',174.427,[{'operating_capex_interest_burn':-149.427},{'operating_capex_interest_burn':-129.427,'equity_net_proceeds':30},{'operating_capex_interest_burn':-139.427,'equity_net_proceeds':65},{'operating_capex_interest_burn':-164.427,'equity_net_proceeds':180}],'从6/30到4/12约9.4个月，不是6个月。贷款新增15同时现金+15债+15，不增加净现金，未在净桥假装额外价值；受控现金约束未知，仍可能触发融资。73/75/90M含现61.8434、奖励/融资条件。')
bridge('AMPX',74.517,[{'operating_wc_capex_cash_burn':-49.517},{'operating_wc_capex_cash_burn':-24.517},{'operating_wc_capex_cash_burn':-29.517,'equity_net_proceeds':20},{'operating_wc_capex_cash_burn':-44.517,'equity_net_proceeds':60}],'不把22.3或74.793拨款算自由现金；若收OTA里程碑，同时对应项目成本。模型资本桥为条件，费用、营运与融资尚未公司指引。')
bridge('MRAM',43.896,[{'operating_capex_IP_burn':-18.896},{'operating_capex_IP_burn':-11.896},{'operating_capex_IP_burn':-8.896},{'operating_capex_IP_and_finance_net':1.104}],'现金从6/30至4/12；按H1负FCF5.924M校准数量级，最后分支净增依赖量产并非当前实绩。')
for i,s in enumerate(D['BNTX']['scenario_inputs']):
    s['inputs']['cash_bridge_EUR']={'opening_EUR_m':16634.2,'research_operating_investing_burn_EUR_m':[2200,1700,1500,1300][i],'buyback_EUR_m':[300,450,600,700][i],'EURUSD_assumption':[1.05,1.10,1.15,1.20][i]}
D['BNTX']['target_cash_bridge']['status']='EUR arithmetic cash bridge explicit; debt/royalty/ownership residual not fully closed'
D['VISN']['target_cash_bridge']['buyback_pair']={'pre_buyback_cash_m':700,'cash_paid_m':150,'post_buyback_cash_m':550,'pre_buyback_shares_m':230.63,'post_buyback_central_shares_m':215,'implied_average_buyback_price':150/(230.63-215),'status':'research assumption; not execution record; 160M H2 refund excluded'}
D['LEU']['scenario_inputs'][0]['forward_operating_period']='现有贸易 + 2032-2034成熟扩产盈利折现至2027-04-12'
for s in D['LEU']['scenario_inputs']:s['forward_operating_period']='Existing trade plus 2032-2034 mature expansion discounted to 2027-04-12'
for t in ['KYTX','BNTX','IONS']:
    for s in D[t]['scenario_inputs']:s['forward_operating_period']='conditional owned pipeline/franchise risk-adjusted EV as of 2027-04-12; not six-month sales'
for t in ['LEU','SMCI']:
    D[t]['target_cash_bridge']['status']='capital_instrument_price_consistency_solved; cash_flow_funding_bridge_not_closed'
exec((R/'07_logs/V2_chair_addendum.py').read_text(encoding='utf-8'))
order='MU SNDK SMCI IREN AAOI CRDO CRWV UCTT CLS MOD COHR KYTX AMPX ENPH PSIX FLNC VISN BNTX LEU RDW AVAV AOSL ACMR AMBA MRAM CC ALNY IONS POET ADBE PNR PLAB ICHR NVDA APLD NBIS TTMI AEIS'.split()
M=[D[t] for t in order]
assert len(M)==38 and len(set(order))==38
out={'role':'V2 independent numeric verification','status':'sealed_conditional_models_not_capital_audit_certificate','cutoff':'2026-10-12 20:50 America/Los_Angeles','price_date':'2026-10-12 normal close','valuation_date':'2027-04-12','units':'USD millions, shares millions; BNTX cash EUR explicit','probabilities':'none; branch membership and clinical asset risk discounts are subjective conditional assumptions, not calibrated probabilities','coverage_count':38,'core_count':34,'formula_definitions':{'EV_NopAT':'P=max(0,[R*(GM-economic_opex_rate)*(1-tax)*K-net_debt-other_claims]/N)','economic_parent_EPS_PE_plus_incremental_option':'NI=[R*GM-economic_opex-net_interest]*(1-tax)*(1-NCI)-preferred; P=[max(0,NI*PE)+incremental_option]/N; NO extra cash/debt adjustment','EV_Sales_with_profit_crosscheck':'P=max(0,[R*sales_multiple-net_debt]/N); economic NOPAT=[R*GM-economic_opex]*(1-tax) shown for compatibility','EV_EBITDA_with_maintenance_FCF_crosscheck':'EBITDA=R*GM_before_DA-economic_cash_opex; P=max(0,[EBITDA*K-net_debt-remaining_environment_legal_cash_PV]/N); remaining legal PV is zero except CC and excludes pre-target payments; maintenance FCF=EBITDA-max(0,EBITDA-DA)*tax-maintenance_capex','clinical_SOTP':'P=[sum(risk_adjusted_owned_asset_EV)+net_cash]/N; asset values conditional, no invented precise clinical probability','LEU':'EV=trade_EV+max(0,mature_NOPAT*K/(1+discount)^years*execution_discount-unfunded_capital_PV); solve P=[EV+netcash+500*ITM_tranches]/[base_shares+sum(500/strike ITM)]','SMCI':'EV=R*GM-economic_opex, times(1-tax)*K; solve P*N(P)+unconverted_debt(P)+preferred_dividends_PV=EV+cash; preferred conversion shares and debt conversion economic, not legal prediction','APLD':'Parent equity=max(0,project_NOI*K-project_netdebt)*ownership+CHRN_owned_equity-mother_netdebt_preferred_claims'},'limitations':['所有38有重开原始URL，部分只相关段或元信息，不声称全部财报全文。','未能逐个闭合所有38法律完全稀释与逐季度资金桥；null代表未知。四家公司给条件算术桥，其余明确不认证。','所有预测输入为V2条件研究，非公司承诺、数学期望、精确概率。强成功不强制2倍，所有失望不是最大亏损。','PE已含经济SBC和利息，销售倍数另外显示盈利交叉检验；负利润不能得到正常盈利支持。'],'companies':M}
(R/'04_verification/V2_models.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
with (R/'04_verification/V2_models.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['ticker','price','branch','formula_type','inputs_json','result_json','scenario_price','return_pct','two_x_inverse_json','capital_bridge_status']);w.writeheader()
    for m in M:
        for s in m['scenario_inputs']:w.writerow(dict(ticker=m['ticker'],price=m['price'],branch=s['branch'],formula_type=s['formula_type'],inputs_json=json.dumps(s['inputs'],ensure_ascii=False),result_json=json.dumps(s['result'],ensure_ascii=False),scenario_price=s['result']['price'],return_pct=s['return_pct'],two_x_inverse_json=json.dumps(m['two_x_inverse'],ensure_ascii=False),capital_bridge_status=m['target_cash_bridge']['status']))
(R/'07_logs/V2_sources.json').write_text(json.dumps({'role':'V2','access_date_utc':'2026-10-13','sources':list(SOURCE.values()),'raw_access_logs':[p.name for p in (R/'07_logs').glob('V2_web_access_*.json')],'inherited_local_inputs':['01_inputs/universe.json','03_round2/S1_ai_deep.json','03_round2/S2_nonai_deep.json','03_round2/B2_valuation_rebuttal.json','04_verification/控制器*.md'],'failures':['LEU 424B5 initial open Internal Error; pricing EX99-2 succeeded, base shares inherited','AVAV node21391 Internal Error; official hosted call PDF succeeded','CC SEC 10Q Internal Error; company financial release succeeded'],'reading_scope':'Original accesses are not evidence of complete full-document reading. Facts and arithmetic pass coverage distinct.'},ensure_ascii=False,indent=2),encoding='utf-8')
head=['# V2独立数字核验：38家公司可重算条件模型','', '截至2026-10-12 20:50洛杉矶；2026-10-12正常收盘为基准，2027-04-12估值。34核心（交接33加NVDA）与4替代均有四分支及2倍反解。金额USD百万、股数百万。','', '**结论：数字模型已逐项生成并复算，但不能称38家资本桥全部已审计闭合。** 研究输入是条件而非期望收益。半年度一度触及与4月仍站稳不同；后者须经营/临床和融资同时兑现。','', '重要改动：SMCI按价格求可转/优先经济索取权；LEU新产能先折现再按权证价内求解；ACMR/FLNC按各日期A+B经济股核对；BNTX现金按EUR桥换USD；AOSL/MRAM失望真实压缩销售溢价。','', '|公司|收盘|失望|工作中枢|强成功|更强右尾|强成功/现价|','|---|---:|---:|---:|---:|---:|---:|']
for m in M:
    ps=[s['result']['price'] for s in m['scenario_inputs']];head.append('|'+m['ticker']+'|'+str(m['price'])+'|'+'|'.join(f'{p:.2f}' for p in ps)+f'|{ps[2]/m["price"]:.2f}x|')
head+=['','## 方法与资金桥诚实边界','', 'EV模型扣正常税与经济SBC，不把非GAAP的全部加回当利润。PE模型从收入、毛利、经济费用、利息、税、NCI逐步算归母，不另加同一现金。EV/Sales是事件去风险溢价；其隐含EV/NOPAT在JSON中展示，亏损时显示null而非假造PE。EBITDA旁列维护资本和正常税后的FCF，但增长资本另占现金。','', '当前实绩和目标资本分开。MU/KYTX/AMPX/MRAM给出条件算术桥；这只证明加减闭合，不证明现金必然发生。其余保留缺口/未知，不用“其他现金流”强行归零。净现金桥中借款同时增现金和债，不产生股权净价值；转换会减债增股。除特别说明，股数为2027压力/经济分母，并非今日法律股数。','', '## 冷复活比较','', 'ADBE：经济利润与现金自给较清楚，强成功可越2倍，核心条件是增长保住且PE回到23倍；不需要把5.42美元SBC抹掉。相较POET/FLNC，融资与当前盈利不确定性较小；相较MU，短期事件冲击更弱但可作下行偏好的真实替代。','', 'PNR：普通修复中枢不足翻倍；Taco已完成不等新增催化。强成功需4900收入、38%毛利、利息140、22倍经济PE，仍应作为条件复活而非现金稳所以必选。','', 'PLAB：低融资风险是真优势，但2倍需要接近1100收入、38%毛利、归母分成及23倍同时成立。与ICHR比较，其当前现金和盈利更稳、经营加速坡度较低。','', 'ICHR：39–41M经济股与20%以上毛利仍能产生2倍路径，值得从漏选复活；相较UCTT，低股权体量的弹性更大，当前毛利/营运资本证据较弱。不能把39M分母和40M反解混用。','', '## 逐家公司资本与逆向门槛']
for m in M:
    head+=['',f'### {m["ticker"]}', '',m['baseline_source_notes'],'',f'原始来源：[V2 {m["ticker"]}]({m["source_urls"][0]})。相关段与访问失败见来源日志；继承项目资料仅导航，不是第二条独立事实。','', '2倍反解（强成功成本/资本固定）：`'+json.dumps(m['two_x_inverse'],ensure_ascii=False)+'`','', '资本桥状态：'+m['target_cash_bridge']['status']+'。','', '3个月检查：'+m['three_month_check'],'','替代比较：'+m['alternative']]
head+=['','## 封卷边界','', '没有为任何情景赋未经校准的精确发生概率，也没有把全部强成功强制调到2倍。法律股数、净债和资产归属缺口可实质改变排序；主席应把此类公司标条件机会。V2任务是可计算与口径核验，不代表订单、监管批准或市场倍数认证。']
(R/'04_verification/V2_numeric_verification.md').write_text('\n'.join(head)+'\n',encoding='utf-8')
(R/'07_logs/V2_reading_notes.md').write_text('# V2阅读与继承边界\n\n根目录AGENTS、实验章程、交接、universe已读；S1/S2/B2结构化卡与控制器指定纠错用于线索。原始链接重新打开，相关财表/条款find/open记录完整保留在V2_web_access_1–26.json。不是38份财报全文审计。\n\n'+ '\n\n'.join('## '+t+'\n'+NOTES[t]+'\n原始：'+SOURCE[t]['url'] for t in order)+'\n\n模型全部预测值独立条件设定，未认证B2等比例四分支。未完逐季度现金桥明列而非统一勾选。\n',encoding='utf-8')
print(json.dumps({'count':len(M),'strong_success_2x':[m['ticker'] for m in M if m['scenario_inputs'][2]['result']['price']>=2*m['price']],'rows':len(M)*4},ensure_ascii=False))
