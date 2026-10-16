import json, csv, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U=json.loads((ROOT/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))
BY={x['ticker']:x for x in U}
DEEP='CRDO AAOI COHR MU SNDK IREN CRWV APLD NBIS POET NVTS PSIX MOD FLNC SMCI AVGO NVDA CLS TTMI AEIS ALAB AXTI LITE ACMR UCTT AMBA KYTX ASTS LEU ENPH'.split()

# All model capital/operating numbers below are explicit research assumptions,
# not reported balances. B = USD billion and billion shares.
# Four branches: disappointment, central, success, exceptional.
MODELS={
'MU':(1.16,-70,[180,260,310,350],[.45,.65,.68,.70],[6,8,11,14],'FY2027/28'),
'SNDK':(.158,-12,[32,48,58,65],[.45,.64,.67,.68],[6,8,12,15],'FY2027/28'),
'IREN':(.480,7,[4,6,8.5,11],[.18,.22,.23,.25],[20,25,25,30],'CY2028可持续盈利代理'),
'AAOI':(.102,-.5,[1.5,2.6,3.8,5.2],[.05,.15,.22,.25],[20,30,30,36],'CY2027/28'),
'SMCI':(.800,7,[50,65,75,90],[.04,.055,.075,.09],[10,13,15,18],'FY2027/28'),
'CRDO':(.210,-.6,[2.4,3.4,4.6,6],[.27,.36,.42,.44],[22,35,45,50],'FY2028'),
'CRWV':(.700,45,[22,32,38,50],[.13,.17,.20,.24],[20,23,25,30],'CY2028'),
'ENPH':(.138,-.25,[1.0,1.4,2.3,3.0],[.05,.12,.16,.18],[20,25,27,32],'CY2028/29，成功含SST；不能当已签订单'),
'FLNC':(.210,.25,[2.6,3.2,4.0,5.0],[.005,.025,.045,.065],[12,20,20,25],'FY2028修复盈利'),
'COHR':(.210,2,[10,13.5,16,20],[.14,.20,.25,.27],[18,25,31,36],'FY2028'),
'CLS':(.130,-1,[25,34,42,52],[.05,.07,.08,.09],[18,24,28,32],'CY2027/28'),
'MOD':(.056,.35,[3,3.8,4.8,6],[.10,.15,.18,.20],[18,24,25,30],'存续MOD FY2028/29'),
'NVDA':(24.3,-150,[520,690,820,1000],[.45,.56,.61,.62],[15,19,23,28],'FY2028'),
'TTMI':(.112,1.5,[4.8,5.8,7,8.5],[.08,.13,.16,.18],[18,24,25,30],'CY2027/28'),
'AEIS':(.040,0,[2.5,3.25,4.0,4.8],[.12,.18,.22,.24],[20,24,27,32],'CY2027/28'),
'UCTT':(.047,.5,[2.8,3.5,4.3,5.2],[.04,.065,.08,.09],[16,20,21,25],'CY2027/28'),
'PSIX':(.0235,0,[.60,.80,1.05,1.35],[.075,.115,.15,.17],[12,17,18,22],'CY2027/28'),
'AVGO':(5.10,40,[145,185,245,310],[.43,.50,.54,.56],[15,22,28,30],'FY2027/28'),
}

# Thesis | near-window catalyst | calendar confidence | funding | buffer | risks |
# alternative | why | kill / re-entry | supporting ids
TEXT={
'MU': ['低估值对应极高现实盈利，短期并不需要收入翻倍；两次财报证明高利润延续可使市场撤销极端周期折价。','2026年12月、2027年3月财报窗口：FY27Q1/Q2价格、HBM年度重定价、SSD交付和现金。','财报月为历史节奏估计；经营指引已披露；未来准确日待公告。','模型1.16B股、可分配净现金70B为条件代理；大额CapEx、押金退款及SBC需扣，净现金不能全部直接派发。','已实现高现金流及规模业务；但正常化价格下降会使股价先于利润下行。','86%以上毛利不可永续；客户降规格、容量迁移、2027供给释放。','SNDK','DRAM/HBM/NAND跨产品缓冲更好；翻倍所需倍数仍仅约11倍经济NOPAT。','若价格及现金连续两季实质下修，撤销重估；若利润确认而倍数不升，可继续比较SNDK。','S08 S10 S01'],
'SNDK':['长约与企业SSD使传统纯现货周期折价可能过高；业绩持续性验证比HBF概念更能支持6个月重估。','10月29日及2027年1–2月财报，Q1指引兑现、下一季接近12B收入、剔除客户保证金的FCF。','10月29日来自冻结正式报告所引公司日历，本轮未独立重开日历；后季估计。','155–158M经济股数代理；净现金12B为扣客户资金/税款后的情景假设；JV支出不因权益法消失。','已有利润现金与最低价格合同提高承受力；押金与最低价格不保证永久80%毛利。','NAND新增供给、NBM重置、消费者缩容量；HBF2027样品不是大收入。','MU','纯NAND右尾更集中；风险相近时仍排MU之后，非凭更高牛价压过MU。','NBM发生实质取消/底价重置或企业SSD净价量同时下滑即降级；不因HBF无当期收入单独否决。','S09 S10 S08'],
'IREN':['Horizon验收到计费是窗口内真实去风险；当前规模小、已签ARR大，确认收入的速度足以触发资本化方式变化。','2026Q4 Horizon2–4交付，公司计划；11月/2月财报验证AI收入、2027容量签约与融资。','Q4交付为公司目标，非保证；财报月估计。','成功模型480M股、净债7B；微软GPU债成本6%，3.31%含无息预款；Mackenzie9%且追索不同。预付款抵未来账单，不能重复计现金。','自有园区、Horizon1实交付、已签客户与现金；大型扩建与GPU更新可耗尽缓冲。','迟交退款、非投资级客户、短债摊还、稀释、设备经济寿命；Maia自研影响续约价格。','CRWV','较低股权起点和自有设施利于交付去风险弹性，融资责任仍很重；不是无杠杆替代。','两个季度资金缺口无可提款资金覆盖或核心验收失败终止则杀死；新增低成本无重稀释资金可上调。','S03 S04 S01'],
'AAOI':['800G/1.6T由资格到大批交付使盈利基数非线性；新ATM已完成降低近端筹资压力，不能继续把未售额度当悬而未决。','11月Q3与2027年2–3月Q4财报：800G跃迁、1.6T首批交付及40%毛利目标进度。','财报月估计；资格/物料和Q4交付为公司计划；10/5ATM完成为事实。','10/5已售5,694,845股、净收588M；102M未来经济股数是假设，要另桥员工/可转债；若冻结股本已含本批不可再加一次。','融资给了设备投入时间；没有利润或清算底；CATV应收与设备预付占款很大。','客户极集中、材料瓶颈、良率、不断增发；220券商目标不是6个月保证。','COHR','小收入底盘使6m触及2×机制更强，但站住需要量/毛利/回款，COHR下行稳健性更优。','1.6T推迟跨过Q1且无替代交付、毛利30%停滞/再低价募资则降级；有跨客户复购再上调。','S07 S06'],
'SMCI':['低利润倍数可在营运资本恢复和Rubin交付后重估；营收增长只能解释一半，真正催化是现金转正。','11月与2027年2月FY27Q1/Q2，交付至少两季持续、毛利10–12%区间和回款。','财报月估计；Rubin出货为冻结原始报道，本轮未独立打开。','800M经济股数计优先/可转工具的情景代理；净债7B假设。不可取消采购34.2B是义务而非全部已欠债。','已经有盈利和渠道业务；治理和供应资格受损可穿透普通失望价。','收入大多GPU转售；毛利组合回落、库存应收、出口与治理调查、内控缺陷。','CLS','更便宜且现金修复能直接释放估值；CLS经营确定性较强，但相同翻倍需更高系统份额。','两季合计仍明显烧钱、库存与应收增长快于交付，或供应资格/审计恶化则取消成功分支。','L-SMCI'],
'CRDO':['AEC已创造利润，光DSP/PIC/整模块是第二增长柱；比纯光概念更有现金基础。','2026年12月与2027年3月FY27Q2/Q3财报，光业务>600M全年目标的进度；OCP仅技术展示。','官方下一季收入525–535M；年度光目标来自冻结电话会转录；财报月估计。','210M经济股数、净现金600M为代理；Dust收购与或有股份、员工奖励需承担，SBC不得全剔除。','盈利AEC与现金；客户采购可延期，库存和产能预约不能同步撤回。','前二直接客户71%集中、二供、模块毛利稀释、光收入重复计DSP/PIC。','ALAB','同样连接增量，CRDO现实利润和更低重估门槛更好；ALAB倍数/大客户权证代价更高。','光出货停留演示、FY27光目标实质下修或AEC主要客户失单；反之光复购与回款提高排序。','S05 S11'],
'CRWV':['已收费大规模GPU云，2027引导与持续融资可驱动股权杠杆重估；不需要假装EBITDA就是自由现金。','11月/2月财报、2027收入和建设指引；APLD已交付机房带来客户GPU验收机会。','财报月估计；APLD截至10/1合计250MW交付为供应商事实，不等于CRWV客户已验收。','700M股、45B净债为成功条件代理；9月4.2B可转券票息2.875%，可用款低于本金；巨额CapEx仍需新筹资。','104B backlog与付费客户证明需求，设备残值和债权先于股东，无可靠价格底。','六年折旧与经济寿命差、利息、长期租约、客户集中及融资反身性。','IREN','同类中业务已更成熟而杠杆右尾更大；排名在IREN后因永久损失风险。','收入达标而资金缺口扩大不升级；融资利差下降/客户预付覆盖且单位经济利润改善才复活为更高顺位。','S14 S15 S01'],
'ENPH':['住宅底盘改善叠加SST全系统验证，可能从受压住宅股获得AI电力期权；必须由客户付费而非演示视频支撑。','2026年11月SST完整系统演示；2027客户试点及10月/1月住宅财报。','11月演示和2027试点为9/8官方计划；没有截至4/12必须完成试点或采购日期。','138M股及250M净现金为压力后代理；原有575M债本金、保修/研发和45X回款需覆盖。','成熟安装渠道和现金储备优于零收入电源概念；政策依赖削弱底部。','演示不等于订单，2028/29收入前瞻跨度大；住宅终端与税抵免。','NVTS','住宅现金基础、已明确11月系统事件使期权更可验证；NVTS关键Claros规模2028/29且当前估值高。','没有外部现场试点/价格/责任条款，不把演示成功升级为长期EPS；住宅非safe-harbor连续转差降级。','S12'],
'FLNC':['暴跌式经营失误后的存续/修复重估；若制造质量、损失和现金止血，可在收入恢复前先撤销融资危机折价。','11月FY26全年与2027年2月Q1，FY27执行方案、资金需求与Houston产量。','公司承诺年报给计划，具体月按惯例；CFO中性至正仅目标。','210M经济等价股数涵盖Up-C结构的代理，不能仅A股分母；净债/TRA及融资准备250M为条件扣减，法定桥待专员核。','2.9B待交付与真实客户；3.39亿非受限现金可快速耗尽。','9月下调不只是收入递延，赔偿/质量成本永久损失；借款契约和保函。','ENPH','修复目标与股权起点更低，6m可能更强弹性；ENPH生存缓冲更强，所以不把FLNC视为同风险。','新增异常履约损失未收敛或必须大额折价股融则取消中枢；库存变现/经营现金中性可复活。','S13'],
'COHR':['PhotonLink收费爬坡与InP扩产使利润预期可上修，既有规模收入增加验证可靠性。','CY26Q4 PhotonLink开始收入爬坡、11月/2月FY27季度结果。','Q4爬坡为9/21公司计划；未披露分项量价与不可撤销年度订单。','210M股、净债2B为模型；现金需剔受限SiC资金，NVIDIA股权款不是收入。','多产品、成熟制造与客户承诺；库存/CapEx使FCF缓冲弱于调整利润。','在制品爬坡、1.6T价格、非独家客户支持及冷启动投入。','LITE','相近光学路线而当前盈利门槛相对更可承受；LITE新工厂2028无法作本窗口交付。','Q4平台无收费或库存/应收长期快于收入则降级；连续毛利和收款提升才给31倍成功估值。','S02'],
'CLS':['新网络/定制系统交付可在投资者日提高2027收入和利润路线可信度。','10月26日Q3、27日投资者日（冻结官方引用），2027年1月年度结果。','前两日冻结资料官方已定，本轮未重开日历；1月估计。','130M经济股数包含8月11.129M新股后的模型代理；净现金1B扣除经营/现金结算激励储备。','成熟生产与客户资格，新增34.5亿融资提高爬坡能力。','GPU/交换芯片价值属于供应商，平台拓扑可减少交换数量，客户集中。','SMCI','现金和执行较稳；翻倍需FY28收入/利润及估值同时上修，因此顺位不只因安全高于SMCI。','2027引导低于已知高预期或产能/现金缺口扩大则降级；独立客户合格量产才加份额。','L-CLS S01'],
'MOD':['分拆完成后存续业务更聚焦，数据中心利润率恢复可快于收入增长；不再计汽车分部。','11月、2027年2月存续口径财报；DC EBITDA margin从14.8%恢复和4B长协释放。','财报月估计；10/1分拆已完成不是未来催化。','56M股、净债350M为代理；156M分拆现金已偿债。10/12买入者不能再获得0.44619THRM历史分派。','商用HVAC和既有DC业务；165M预付款改善历史FCF但不能重复收取。','暖水架构降低冷水机内容，扩产低效、客户集中、长协取消条款。','VRT','更低估值与利润修复弹性；VRT确定性更强但规模/价格使6m翻倍门槛更大。','两季DC利润率仍不能改善或长协取消则降级；新CDU收入必须净掉被替代冷水机。','S16'],
'NVDA':['以现实利润购买Rubin和持续AI计算需求，成功情景能靠盈利+温和重估翻倍；不像小云股需要连续股权救助。','11月及2027年2月财报，FY28正式展望与Rubin毛利/回款。','11/17冻结报告引用官方日历未本轮重开；2月估计。','24.3B股、150B净现金为前瞻模型；供应承诺与105B担保不是现金债务，但不可忽略或有损失。','已盈利及生态、强现金能力；客户融资集中与应收使缓冲非无限。','Maia/TPU替代、每任务效率提高、客户支出与最终付费脱节。','AVGO','平台现金获取与通用工作负载较强；Maia是实际替代反证，不能因NVIDIA既有优势忽略。','毛利和DSO同时持续恶化且FY28客户资金不足即降级；单一芯片性能新闻不直接减全部GPU收入。','S01 L-NVDA'],
'TTMI':['M+N高复杂PCB Q4交付台阶可抬升2027EPS，中小市值使估值弹性可观。','11月/2027年2月，Q4 M+N400M目标与并购后2027盈利指引。','M+N为公司目标；准确财报日未本轮确认。','112M股、1.5B净债模型；Epiq1.1B融资先消耗利息，不以EBITDA增厚冒充EPS。','国防收入提供不同周期；合同资产不是已收现金。','良率材料成本、进度确认、收购整合和扩产现金。','CLS','小基数M+N台阶更陡；但现金与收购约束较强，因此低于CLS。','Q4目标显著不达且无延期交付证据、经营现金不跟随则降级；单季确认前置不可外推。','L-TTMI'],
'AEIS':['现有半导体电源和数据中心需求已放量，制造杠杆可能使EPS上修快于销售。','11月/2月季度结果、泰国产线合格产出和新增客户量产。','季度估计；800V显著收入最早2028，不写入2026/27营收。','40M股、净债0为前瞻代理；6月现金1.397B对应本金1.287B，不能声称14亿净现金。','经营利润且传统设备资格；库存增长消耗FCF。','退款抬毛利、两个市场集中、800V替代旧电源及竞争。','NVTS','同样电源升级，已有收入和近端利润验证使下行/时间更好；NVTS突破可更大但发生时点弱。','剔退款毛利及库存现金都恶化即降级；第二批客户实际收入可提高成功分支。','L-AEIS'],
'UCTT':['低倍数承接WFE复苏和复杂子系统放量，若产品毛利与现金同步回升可快速重估。','10–11月Q3、2027年2月Q4/2027指引，按周比较53周年份。','月份估计；客户CapEx不是UCTT订单。','47M股、500M净债条件代理；库存持续增加可能新增贷款/稀释。','成熟客户制造业务与服务收入；低毛利放大失误。','两客户集中、库存、价格转嫁、OEM内制。','ACMR','美国设备需求无需少数股权穿透和跨境现金折价；ACMR产品自有性较强但近端现金更弱。','Products毛利两季不改善或现金继续全被库存吸收则撤销重估；合格产出/回款共振复活。','L-UCTT'],
'PSIX':['小市值、真实盈利和发电集成复苏具备翻倍操作杠杆；不能假设同行景气自动传导。','11月/2027年3月财报，订单排产恢复与潍柴供应框架续签。','季度月份估计；续签日期未知，本轮不能作已确定事件。','23.5M股模型，不假设大股融资；退款负债剔除可分配现金，净债0为条件代理。','盈利底盘与较小扩张规模；治理/客户损失可能压穿失望价。','2026H1收入下降、税项转回夸大利润、客户自制机罩、潍柴控制。','GNRC','小基数盈利恢复更容易翻倍；GNRC实际订单更强，所以PSIX需先验证公司份额。','收入继续落后同行且毛利回落则淘汰；供应关系及连续客户排产确认可快速复活。','L-PSIX'],
'AVGO':['定制ASIC与网络现实盈利扩张，FY28路径提前获客户支撑可导致长端盈利在6m资本化。','2026年12月/2027年3月财报与FY27展望、主要客户ASIC生产和资金落实。','月份估计；客户多年代际协议不是全部近期采购。','5.10B股及40B净债前瞻代理；采购126.8B与机架租赁最大29B敞口分开，不能简单总当债。','软件和芯片现金，较云运营商融资缓冲强。','同一客户资金池、系统内容稀释毛利、软件前置许可证、租赁担保。','NVDA','作为ASIC分散路径，Maia强化自研大势却未证明AVGO赢该设计；同风险优先NVDA，故排末。','客户项目未变采购/验收或资金支持损失扩大则降级；两代明确交付可上调FY28可信度。','S01 L-AVGO'],
}

EARLY={
'KYTX':dict(prices=[2.2,8.5,15,25],shares=.085,netcash=.080,target_ev=.975,
thesis='非AI对照：SPS滚动BLA完成及获受理可将临床资产从不确定申报切换为明确审评；gMG是独立右尾。',
catalyst='2026Q4完成SPS BLA、随后约60日受理审查；2027Q1可看到受理/审评路径和融资。',
status='Q4为公司目标；受理、优先审评及PDUFA日期未确定，不假造2027年4月前批准。',
fund='85M股为融资后情景，现金80M为消耗/筹资后代理；6月199.4M现金，H1烧81.9M；150M贷款仅部分可提款。',
buffer='临床数据有疗效信号和剩余现金，失败可下跌大半；现金不能当清算底。',risk='单臂26人数据、CMC/监管、商业患者池、gMG竞争与融资。',alt='BNTX',why='单一明确申报使6m事件密度高，BNTX资金更强但大市值与分散研发令短期翻倍门槛不同。',kill='BLA再延期/CMC缺口显著或融资毁损则降级；受理并给可行审评日期可提升。',src='S17',
formula='2×6.21×0.085B−0.080B=0.9757B所需风险调整资产EV；相当于5B成功资产价值×19.5%净风险权重。5B不是现有收入：若6×峰值销售需约0.833B峰值销售，并先扣未融资开发/商业化现金。受理可改变折价但不能证明资产值。'),
'POET':dict(prices=[3,6.8,14,22],shares=.300,netcash=.650,target_ev=3.196,
thesis='资金充裕的光引擎商业化期权；若Lumilens与第二客户从资格跨到连续交付，估值可在收入成熟前跳升。',
catalyst='2026Q4至2027Q1季度收入、Lumilens资格与首批验收，工厂真实产量和独立客户。',
status='没有已确认的批量订单确认日；作为条件候选，窗口时点证据弱。',
fund='300M股含未来激励/融资压力代理；净现金650M在6月796M基础上扣消耗，非当前实测。Lumilens最多22.92M股权证涉及净收入抵减及股数，不能双漏。',
buffer='现金较大降低近端生存风险；现金使用与权证会侵蚀每股底。',risk='Celestial订单已取消；Lumilens50M附条件，500M潜力不是合同收入；净价和制造良率未知。',alt='NVTS',why='POET资金与光引擎客户量产窗口更接近，NVTSClaros主收入2028/29；但两者均非最高证据。',kill='Lumilens资格失败/取消或连续收入依旧只NRE则降级；净激励后可重复产品销售复活。',src='L-POET',
formula='2×6.41×0.300B−0.650B=3.196B EV；20×净产品销售需0.160B收入，10×需0.320B。均远高于H1约1.07M实绩，故只是2027/28大规模资格/采购已去风险后才有的估值，不是未来两季收入预测。'),
}

ORDER='MU SNDK IREN AAOI SMCI CRDO CRWV KYTX ENPH FLNC COHR CLS MOD NVDA TTMI AEIS UCTT PSIX POET AVGO'.split()
SOURCES=[
('S01','https://blogs.microsoft.com/blog/2026/10/12/microsoft-to-expand-azure-maia-system-to-multi-gigawatt-deployments/','2026-10-12','客户原始披露','Maia 300','Maia200已生产、300于2027生产部署，8HBM4/96芯片/167kW；未证明选定供应商订单；确切盘前盘后时分未取得'),
('S02','https://ir.coherent.com/news-releases/news-release-details/coherent-launches-photonlinktm-integrated-optics-platform-ai','2026-09-21','公司原始披露','PhotonLink','超过10 CPO及10 NPO接洽、锚定LTA、Q4收入爬坡目标；接洽不是独立收入'),
('S03','https://iren.gcs-web.com/news-releases/news-release-details/iren-closes-365bn-investment-grade-gpu-financing','2026-06-01','公司原始披露','IREN微软GPU融资','36.5亿融资债息6%，含预款3.31%；仅GPU资本开支覆盖96%'),
('S04','https://iren.gcs-web.com/news-releases/news-release-details/iren-reports-fy26-results','2026-08-27','公司原始披露','IREN FY26','Horizon1交付、2调试、3–4Q4目标；4B签约ARR与1B运行ARR分开'),
('S05','https://business.thepilotnews.com/thepilotnews/article/bizwire-2026-10-9-credo-to-showcase-broad-portfolio-of-connectivity-solutions-for-ai-scale-out-and-scale-up-fabrics-at-2026-ocp-global-summit','2026-10-09','公司BusinessWire稿转载，非独立媒体验证','Credo OCP','1.6T ALC/AEC/光模块、Weaver FPGA展示；没有新增订单数量'),
('S06','https://247wallst.com/investing/2026/10/09/applied-optoelectronics-has-fallen-hard-for-6-months-this-wall-street-analyst-expects-its-going-to-double-soon/','2026-10-09','具名媒体Alex Sirois转述Rosenblatt Mike Genovese','AAOI多头券商观点','220目标作灵感；文内1.6T 17M与冻结电话会70–80M冲突，未擅自消除；目标期限非本轮6m'),
('S07','https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-announces-completion-previously','2026-10-05','公司原始披露','AAOI第三次ATM','完成600M、5,694,845股、均价105.36、净588M；覆盖旧报告未售状态'),
('S08','https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/default.aspx','2026-09-30','公司原始财报','MU FY26Q4','收入54.23B，GAAP EPS32.87，CFO43.97B；短期盈利已实现，非未来模拟'),
('S09','https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results','2026-08-05','公司原始披露','SNDK FY26Q4','首次open返回415行但未返回正文，后续403；不计独立实读，数字继承冻结原文待复核'),
('S10','https://www.trendforce.com/presscenter/news/20260930-13258.html','2026-09-30','专业研究机构原始调查','Q4内存价格','DRAM10–15%、NAND15–20%预测；企业SSD强同时消费端承压，预测不等于成交价格'),
('S11','https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results/default.aspx','2026-09-01','公司原始财报','CRDO FY27Q1','479M收入；Q2官方525–535M，不能把本地535–555M研究路径标官方'),
('S12','https://investor.enphase.com/news-releases/news-release-details/enphase-advances-iq-solid-state-transformer-development-ai-data','2026-09-08','公司原始披露','ENPH SST','11月完整演示、2027试点为计划，模块在造不是大型订单'),
('S13','https://ir.fluenceenergy.com/news-releases/news-release-details/fluence-energy-announces-revised-guidance-fiscal-year-2026','2026-09-16','公司原始披露','FLNC预警','FY26收入2.4B、EBITDA亏200M；FY27现金中性至正是目标'),
('S14','https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx','2026-08-11','公司原始财报','CRWV Q2','收入2.575B、调整EBITDA1.510B、调整经营利润128M、净利息640M；backlog104B'),
('S15','https://ir.applieddigital.com/news-events/press-releases/detail/163/applied-digital-reports-fiscal-first-quarter-2027-results','2026-10-07','供应商原始披露','APLD FY27Q1','已交付/基础租金路线；首次open正文未展开，具体250MW继承冻结原文，待进一步重读'),
('S16','https://investors.modine.com/news/news-details/2026/Modine-Completes-Spin-off-and-Combination-of-its-Performance-Technologies-Business-with-Gentherm/default.aspx','2026-10-01','公司原始披露','MOD分拆','已完成，每旧股0.44619THRM；156M现金用于还债；10/12新购不含旧分派'),
('S17','https://ir.kyvernatx.com/news-releases/news-release-details/kyverna-therapeutics-reports-positive-one-year-data','2026-09-24','公司原始披露','KYTX一年随访','已打开133行待进一步展开；Q4BLA与26人疗效继承冻结原文，非独立全表核验'),
('S18','https://www.zacks.com/stock/news/3002016/aaoi-stock-gains-17-in-a-month-should-you-buy-sell-or-hold','2026-10-07','具名媒体线索','AAOI相反观点','访问反爬，未读正文，不据此证明Hold细节'),
('S19','https://finance.yahoo.com/technology/ai/articles/iren-stock-gains-report-names-180840206.html','2026-10-12','媒体转载线索','IREN Anthropic传闻','429未读正文；可能只是8月匿名客户身份揭示，不增算新合同'),
]
src=[]
for sid,url,date,kind,event,claim in SOURCES:
    status='已实读返回正文主要相关段落'
    if sid in ['S09','S15','S17']:status='已打开但正文未充分展开/部分失败，见claim'
    if sid in ['S18','S19']:status='访问失败，仅线索'
    src.append(dict(id=sid,url=url,published_date=date,access_status=status,source_type=kind,root_event=event,claim_supported_or_challenged=claim))
SM={s['id']:s for s in src}

def scenario_model(t):
    s,d,rs,ms,ks,period=MODELS[t]
    result=[]
    # These are conditional repricing models at Apr12, not forecasts that annual
    # revenue will all have been earned by Apr12. Financing stress is separate.
    for label,r,m,k in zip(['disappointment','central','success','exceptional'],rs,ms,ks):
        p=max(0,(r*m*k-d)/s)
        result.append(dict(branch=label,forward_period=period,revenue_B=r,economic_NOPAT_margin=m,economic_NOPAT_B=round(r*m,4),EV_NOPAT_multiple=k,net_debt_B=d,shares_B=s,price=round(p,2)))
    p0=float(BY[t]['finance']['最新价格']); m=ms[2];k=ks[2]
    hurdle=(2*p0*s+d)/(m*k)
    formula=f'P=(R×经济NOPAT率×EV/NOPAT倍数−净债)/经济股数；2P={2*p0:.2f}，S={s}B，净债={d}B，m={m:.1%}，K={k}，所需{period}收入R={hurdle:.3f}B、NOPAT={hurdle*m:.3f}B。此m扣正常税、经济折耗及SBC等价成本，非公司调整EBITDA。若股数再+20%且净债不变，门槛收入={(2*p0*s*1.2+d)/(m*k):.3f}B。'
    return result,formula

nom=[]
for rank,t in enumerate(ORDER,1):
    x=BY[t];p=float(x['finance']['最新价格'])
    if t in TEXT:
        th,cat,stat,fund,buf,risk,alt,why,kill,ids=TEXT[t];models,formula=scenario_model(t);prices=[a['price'] for a in models]
    else:
        a=EARLY[t];th,cat,stat,fund,buf,risk,alt,why,kill,ids=[a[k] for k in ['thesis','catalyst','status','fund','buffer','risk','alt','why','kill','src']];prices=a['prices'];formula=a['formula'];models={'method':'风险调整资产EV/净销售估值门槛；各价为条件事件估值，不是盈利折现已完成证明','shares_B':a['shares'],'netcash_B':a['netcash']}
    used=[i for i in ids.split() if i in SM]
    ev=[f'冻结原文：{k}: {v[0]}' for k,v in x['sources'].items() if v]
    ev += [f'{i}: {SM[i]["claim_supported_or_challenged"]}' for i in used]
    tier='A 短期翻倍机制相对优先' if rank<=6 else ('B 事件/融资条件成立后' if rank<=13 else 'C 20名额内优先机会，但6个月翻倍支撑较弱')
    three='检查点2027-01-12：以已公布季度及事件判断，不能假定第二次财报已发布。'+cat+' 三个月主要为预期更新，尚不足以证明全部成功盈利。'
    six='观察日2027-04-12：成功价是两季兑现后对前瞻完整年度的交易定价；不是六个月已赚取该年度利润。窗口内一度触及2×比期末站住2×更容易；期末需要交付、毛利、现金与融资一起验证。'
    n=dict(rank=rank,ticker=t,tier=tier,reference_price=p,reference_price_date='2026-10-12',currency='USD',thesis=th,catalyst_window=cat,catalyst_date_status=stat,three_month_case=three,six_month_case=six,disappointment_price=prices[0],central_price=prices[1],upside_price=prices[2],multibagger_price=prices[3],double_hurdle_formula=formula,dilution_and_funding=fund,downside_buffer=buf,risks=risk,closest_alternative=alt,why_preferred=why,reentry_or_kill_conditions=kill,evidence=ev,source_urls=[SM[i]['url'] for i in used],model=models,touch_double_likelihood='主观相对中等，未经校准' if rank<=8 else '主观相对低至中等，未经校准',hold_double_likelihood='低于窗口触及；尚无高把握承诺',tail_loss='融资/治理/技术失败时可低于失望价；模型非损失底')
    nom.append(n)

RES={
'NBIS':'2027放量强，但210.06起点、308.7M以上股本、潜在新增资金及Vineland合规使2×门槛高。若380M股/12B净债/30×20%NOPAT，需约28.6B收入，明显高于2027已构建路径；资金/许可闭合后复活。',
'APLD':'250MW交付实质，但12.75%优先资本和项目债使名义租约不属于普通股；6m2×需重做优先权益瀑布，先列候补。',
'ALAB':'Scorpio增长强且Aries7新品，但现价46.8×TTM销售、客户权证以及50.7×异期forwardPE，近端正常兑现不足以2×。多独立预算客户与2027大上修才复活。',
'AXTI':'InP实绩和预付强、10/29财报有日历，但6英寸爬坡主要2027后半且许可约束；当前61.98要兑现大幅盈利跃迁；出口/6英寸合格交付可复活。',
'LITE':'OCS和1.6T已有收入，不过当前995.41及混用FY28 forwardEPS易显便宜；Greensboro2028不能算6m供给；OCS大量付费交付可复活。',
'NVTS':'现金缓冲和Claros真实技术期权；当前高销售倍数而集团盈亏平衡需约4×季度销售，关键VPD2028/29。必须出真实客户定点经济条款再复活。',
'AMBA':'X7送样/视觉平台长期价值，最新季度剔一次性研发抵减仍亏；6m盈利反转证据弱于前20。CV8量产及库存现金改善再看。',
'ASTS':'2027初45星公司目标提供窗口，但发射、展开、连续覆盖和付费不是同一事件；高估值与融资限制，事件可触及2×却很难证明站住。',
'LEU':'年底首机/政府资金为真正事件，但新增量产2029及资本庞大；在当前135.31需市场提前给2030以后资产价值。更多非稀释资金/可执行大LEU长约复活。',
'ACMR':'9月订单约2.5B USD（171亿元人民币），不可混币；2027Q1面板电镀为目标，需现金/少数股权穿透；新产品复购和回款可复活。',
}
res=[dict(ticker=t,reference_price=float(BY[t]['finance']['最新价格']),reason=s) for t,s in RES.items()]
result=dict(role='X2_AI供应链与短期盈利错价',screened_count=len(U),deep_read_tickers=DEEP,nominations=nom,reserves=res,method='独立245结构化第一遍；30家公司原始冻结公司/情景/比较中的经营、近期季度、融资和对比段定向深读；非全文逐字审计。外部原文更新13项有用正文，媒体仅线索。EV/经济NOPAT统一反解，少数无利润用事件资产/净销售门槛。排名考虑时间、资金与下行，不是牛价排序；不读取上一实验终榜或其他X结论。',limitations=['价格采用冻结10/12正常收盘快照，未逐笔外部复核；数据商forward EPS财年不一，未直接当估值锚。','18个EV模型为可复算必要门槛与简化情景，资本S/D为明确研究代理，尚未逐公司闭合6个月逐季现金流、价内转换、税款和全部法定权益；需后续核验角色补齐，不能称最终估值认证。','本角色完成30家公司定向段落深读，并非每家公司所有原文全文阅读；一些大批次返回被截断，未读部分不算完成。','多数候选中央价不达2×，20是优先研究机会，不是20个同强度翻倍预测。','技术演示/公司计划与正式采购、交付、收入、股东现金分层；Maia/OCP不自动增加供应商收入。','S09访问不足/403，S18反爬、S19 429；S15/S17正文未充分返回，事实继承冻结须二次核。','信息截止10/12 20:50LA，后访问不扩展事件集；10/12 Maia披露精确时分未知，不能声称已完全反映在收盘价。'])
(ROOT/'02_round1/X2_ai.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'07_logs/X2_sources.json').write_text(json.dumps(src,ensure_ascii=False,indent=2),encoding='utf-8')

lines=['# X2独立首轮：AI瓶颈、盈利错价与非AI事件对照','', '信息截至2026-10-12 20:50 America/Los_Angeles；参考10/12正常收盘；检查2027-01-12，期末2027-04-12。','', '**优先MU/SNDK的盈利持续性重估，以及IREN/AAOI/SMCI/CRDO的交付或现金拐点。保留最强多头分支，但没有20个同样可信的六个月翻倍。** 第一层是相对顺位，不代表高统计胜率；20名单后半属条件观察。','', '## 新证据怎样改变判断','', '- AAOI 10/5 ATM已完成：净588M、569.4845万新股；不得继续沿用8月“只是额度”，也不得重复增加已含的股数。[公司原文]('+SM['S07']['url']+')','- CRDO Q2官方指引525–535M，冻结报告535–555M若引用只能标研究条件；OCP是产品演示，Weaver还是FPGA实现。[财报]('+SM['S11']['url']+')','- Maia300 2027 multi-GW部署、8堆HBM4、167kW/96芯片，支持内存/互连/冷却需求，也反驳GPU无限份额；没有证明名单内光学供应商的订单分配。[微软]('+SM['S01']['url']+')','- MOD分拆10/1完成；新买10/12 MOD不能再计旧股0.44619THRM分派。[公司]('+SM['S16']['url']+')','- IREN债息6%不等于含预款3.31%；Anthropic报道访问未成功，且可能只是8月匿名客户揭名，不另增合同。','', '## 条件价格与顺位','', '|#|公司|10/12|失望|中枢|成功|极强分支|成功/现价|','|---:|---|---:|---:|---:|---:|---:|---:|']
for n in nom:lines.append(f'|{n["rank"]}|{n["ticker"]}|{n["reference_price"]:.2f}|{n["disappointment_price"]:.2f}|{n["central_price"]:.2f}|{n["upside_price"]:.2f}|{n["multibagger_price"]:.2f}|{n["upside_price"]/n["reference_price"]:.2f}×|')
lines+=['','价格均USD/股，全部未来值为条件研究算例；“极强分支”不保证一定达到3×。失望价不是清算底，部分尾部可以接近零。年度盈利是事件后市场可能前瞻定价的对象，绝不是窗口内已实现利润。大幅上涨后融资更容易是反身性，不是免费资金。','', '## 逐公司事件与反解']
for n in nom:
    lines += ['',f'### {n["rank"]}. {n["ticker"]} — {n["tier"]}', '', n['thesis'], '',f'**催化：**{n["catalyst_window"]} {n["catalyst_date_status"]}',f'**三月/六月：**{n["three_month_case"]} {n["six_month_case"]}',f'**翻倍门槛：**{n["double_hurdle_formula"]}',f'**资金/股数：**{n["dilution_and_funding"]}',f'**下行与风险：**{n["downside_buffer"]} {n["risks"]}',f'**替代比较：**{n["closest_alternative"]}；{n["why_preferred"]}',f'**撤回/复活：**{n["reentry_or_kill_conditions"]}']
    if isinstance(n['model'],list):
        lines+=['','|分支|前瞻收入B|经济NOPAT率|EV/NOPAT|净债B|经济股数B|价格|','|---|---:|---:|---:|---:|---:|---:|']
        for a in n['model']:lines.append(f'|{a["branch"]}|{a["revenue_B"]}|{a["economic_NOPAT_margin"]:.1%}|{a["EV_NOPAT_multiple"]}|{a["net_debt_B"]}|{a["shares_B"]}|{a["price"]}|')
    lines+=['','本轮直接外部核验：'+('; '.join(f'[{i}]({SM[i]["url"]})' for i in TEXT.get(n['ticker'],['']*10)[9].split() if i in SM) if n['ticker'] in TEXT else '; '.join(n['source_urls']))+'；其余事实来自冻结公司/情景/比较原文，详见JSON evidence与读书日志。']
lines+=['','## 候补与复活']+[f'- **{x["ticker"]}**：{x["reason"]}' for x in res]
lines+=['','## 完成范围与待核']+['- '+s for s in result['limitations']]
(ROOT/'02_round1/X2_ai.md').write_text('\n'.join(lines),encoding='utf-8')

notes=['# X2定向阅读与来源日志','','245首遍先做；公司池来自universe.json。未读上一实验终榜、其他X结论。','', '## 30家定向阅读轨迹','', '阅读方式：公司原文前部经营摘要和决定性财务表；情景的近期季度/资本/稀释/融资段；比较的结论与反证。不是全文逐字复核。原文的旧目标年份只用于核对机制，未平移为六个月目标。','']
for t in DEEP:
    notes += [f'### {t}']
    for kind,paths in BY[t]['sources'].items():
        notes += [f'- {kind}: {p}' for p in paths]
    if t in TEXT:notes += ['- 本轮取舍：'+TEXT[t][0],'- 反证：'+TEXT[t][5]]
    elif t in RES:notes += ['- 本轮取舍：'+RES[t]]
    else:notes += ['- 本轮取舍：'+EARLY[t]['thesis']]
notes+=['','## 行业原文','- 2026-10-10 AI云算力外包和NeoCloud：区分GPU云收入与机房租金，H100短租与新代合同分化，不用59%EBITDA当经济收益。','- 2026-10-10 液冷小组件与流体控制：连接点/千瓦下降与开放互配可抵消功率增长；MOD收入强而利润弱是反证。','- 2026-10-10 HBM与存储测试设备：内存涨价不等于测试设备量增；混合键合时间和测试并行度不能拍脑袋。','', '## 原始外部来源与访问状态']
for s in src:notes += [f'- {s["id"]} {s["published_date"]} {s["source_type"]} / {s["access_status"]}: {s["claim_supported_or_challenged"]} {s["url"]}']
notes += ['', '## 最强多头保留与审查请求','- 不将行业报告偏保守估值自动当结论；CRDO成功允许45×经济利润、AAOI30×，但必须交付/净价/现金去风险。','- 云股不按名义合同估值：IREN/CRWV用2028经济NOPAT与净债反解；绝不把10x ARR当已经得到的股东现金。','- 后续审查优先：AAOI三次ATM完整股数桥；MU/SNDK客户资金及税款净现金；SMCI优先/可转工具分支；FLNC Up-C/TRA；POET客户权证既影响收入又影响经济股本，应避免双算也不能双漏。','- S06媒体的1.6T17M与冻结原话70–80M存在数值冲突，不用该细节作为门槛事实；应重开8月6日原始电话会。']
(ROOT/'07_logs/X2_reading_notes.md').write_text('\n'.join(notes),encoding='utf-8')

# Upgrade first-pass record with nomination/reserve status without erasing screen.
p=ROOT/'07_logs/X2_full245_screen.csv'
rows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
for row in rows:
    t=row['ticker'];row['round1_result']='nomination' if t in ORDER else ('reserve' if t in RES else 'not_prioritized')
    row['rank']=str(ORDER.index(t)+1) if t in ORDER else ''
    row['specific_reason']=TEXT[t][0] if t in TEXT else (RES.get(t,EARLY.get(t,{}).get('thesis',row['reason'])))
with p.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(json.dumps({'screened':len(rows),'deep':len(DEEP),'nominated':len(nom),'reserves':len(res),'direct_useful_body_sources':sum(s['access_status']=='已实读返回正文主要相关段落' for s in src)},ensure_ascii=False))
