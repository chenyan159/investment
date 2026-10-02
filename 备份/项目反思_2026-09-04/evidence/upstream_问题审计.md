# 上游研究与自动化传导链问题审计（2026-09-04）

本审计只界定问题、证据和归因边界，不提出改进方案。原研究目录、runner与队列均未修改。价格涨跌采用同项目本次审计的统一收益表，只用于连接问题，不用事后涨跌反写当时应有事实。

## 1. 可复核范围及不能冒充的结论

- 对照当前192家公司索引，取每家公司文件名日期不晚于2026-07-15的最新公司调研，必要时读分类目录下备份。**192/192找齐：90份2026-07-11、102份2026-07-12**。路径、日期、SHA256、字符与行数在`data/upstream_company_inventory.csv`。
- 审核2026-07-10至12的636份company/industry历史prompt-debug，按domain+subject去重取最后一份，得到**192家公司与75个行业**。这是历史实际生成prompt的合同证据，不把636次文件数当成636个独立研究对象或完成运行。
- 以10个公司索引分类各取股票代号字母序首尾2家，形成**20家确定性分层诊断样本**。人工阅读核心结论、经营三情景、订单取消/延期解释、风险与口径说明。另加价格审计关注公司作定向取证。样本不是随机样本，20/20现象不外推为192/192比例。
- 关键词扫描只用于定位：例如192/192报告命中订单不披露/估算语句，192/192出现宏观词，不等于192家都犯了错误，亦不等于宏观被完整量化。**本次未证实“大量公司资料存在基础财务造假或事实错误”。**证据更集中于先验、可识别度、预期基准和期限/决策压缩。

## 2. 最硬结构证据：共同上游在数据缺口处被要求单方向假设

历史75/75行业prompt均含“对于找不到的直接数据可以做大胆乐观的假设”，并要求对AI建设非常乐观；三种情景是基准、乐观、极度超预期乐观。见[7月行业实际prompt L4](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-10T18-34-23-594Z_industry_数据中心电力接入与高压变电_prompt.md:4>)、[L9–15 三情景](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-10T18-34-23-594Z_industry_数据中心电力接入与高压变电_prompt.md:9>)、[L33 统一乐观要求](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-10T18-34-23-594Z_industry_数据中心电力接入与高压变电_prompt.md:33>)。

历史192/192公司prompt均要求基准/乐观/极度乐观的产品收入与产能预测；192/192都明确允许跳过“非AI方面低增速不重要”的产品。见[7月公司实际prompt L8](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-11T08-46-50-405Z_company_DELL_prompt.md:8>)、[L12–18 公司三上行口径](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-11T08-46-50-405Z_company_DELL_prompt.md:12>)。全量计数和对应prompt路径见`upstream_prompt_contract_audit.csv`。

**问题不是“不能做乐观情景”，而是未知数据填充值与研究方向先验同向。**同一先验先进入行业需求池，再成为公司可捕获收入的底稿，再被多种下游方法重复读取。下游方法数量多、每份报告独立运行，不能自然获得多份独立的产业证据。

反面论证：上游报告普遍写了竞争、取消、现金、稀释和估值风险；历史公司评估又增加了悲观行与相对预期标尺，因此不能从prompt直接推出每家基准都乐观或每个结果失真。可以确认的是**原始可选结果空间不对称，修正负担被转交到下游**。

更直接的局部执行错误：[ADI 7月公司调研 L335–339](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/ADI_Analog_Devices_公司调研_2026-07-11.md:335>)对基准/乐观/极乐分配60%/30%/10%，合计100%，三档NTM收入最低仍是15.8B、比TTM至少+24%；而同文风险矩阵承認有订单取消和高估值风险。[AJNMY 7月公司调研 L252](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/AJNMY_味之素 Ajinomoto_公司调研_2026-07-11.md:252>)也对三个上行经营状态分配55%/30%/15%=100%。这不是仅画三个条件上沿，而是**把全部概率质量分给未包含低于基准的结果空间**。结论只落实到这2个明确样本，不由无“悲观”关键词推算全池错误率。VST给概率区间55–65/25–35/5–10，既无唯一联合分配也没有明确低于基准行，属于弱证据，不和前两例等同。

## 3. 数据很多，不等于关键参数已经可观察

20/20分层样本都明确说明实际历史取消率未披露或不可可靠计算；20/20都提供了关键产品层的模型区间，而非完整公司直接披露。它们常有很好的证据标签，**这属于可观察数据边界，不是研究员漏读，也不是已经证实的数字错误**。

但是收入模型所需参数仍常由同一研究过程自由选择。例如AAOI基准取消5%–10%、乐观2%–5%、极乐0%–2%（[AAOI 7月公司调研 L463–477](<D:/drive/Investment/基本面/公司调研/AI网络_光互联_连接器/AAOI_Applied_Optoelectronics_公司调研_2026-07-11.md:463>)）；ABBNY分别3%–7%、1%–3%、0%–2%（[ABBNY 7月公司调研 L151–160](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/备份/ABBNY_2026-07-31T12_02_20-07_00-9846b160b2/ABBNY_ABB_Ltd_公司调研_2026-07-12.md:151>)）；AEHR5%–8%、2%–4%、0%–2%（[AEHR 7月公司调研 L389–406](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:389>)）。这些精细区间没有变成观测数据，只是在把外界无法观察的合同、验收和延期风险写成计算输入。用产品拆分、BOM、收入产能、AI归因、取消率再多次推导，可能产生大量数字，却仍由同一小组无法独立识别的假设支配。

关键反证：MU把100B多年SCA与5B会计RPO分开；ORCL把638B RPO与12%未来一年确认分开；ADBE明确AI-influenced ARR不等于AI增量收入；WOLF完整提示稀释。这些是合格的边界控制，不能批评为“只看订单没看收入质量”。本审计仅证明资料密度不能作为预测置信度的同义词。

## 4. 六个可复算例子：巨大绝对增长未必提供高于市场的新预测

下表只比较当时原报告中自己的数字，不用今天市场共识补填历史。forward PS反推值受数据商预测年度、股数和四舍五入影响，属于近似的一致预期收入锚，不是精确可交易市场全体预期。

| 公司 | 上游基准收入中点 | 当时共识或其近似收入锚 | 中点差 | 单位 |
|---|---:|---:|---:|---|
| MU | 235.000 | 232.704 | +0.99% | USD bn |
| WDC | 16.600 | 16.560 | +0.24% | USD bn |
| ADI | 16.150 | 16.171 | -0.13% | USD bn |
| TXN | 21.500 | 21.600 | -0.46% | USD bn |
| AEHR | 0.085 | 0.085 | +0.00% | USD bn |
| SMCI | 49.500 | 51.710 | -4.27% | USD bn |

来源：MU [MU 7月公司调研 L19](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/MU_2026-08-19T11_05_27-07_00-bb5d89fa56/MU_Micron_Technology_美光科技_公司调研_2026-07-11.md:19>)与[MU 7月公司调研 L60–76](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/MU_2026-08-19T11_05_27-07_00-bb5d89fa56/MU_Micron_Technology_美光科技_公司调研_2026-07-11.md:60>)；WDC [WDC 7月公司调研 L245–258](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/WDC_2026-08-19T11_05_34-07_00-a39a043c98/WDC_WesternDigital_公司调研_2026-07-11.md:245>)；ADI [ADI 7月公司调研 L62–78](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/ADI_Analog_Devices_公司调研_2026-07-11.md:62>)与[ADI 7月公司调研 L333–339](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/ADI_Analog_Devices_公司调研_2026-07-11.md:333>)；TXN [TXN 7月公司调研 L72–88](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/TXN_2026-07-31T12_02_28-07_00-e3267055d7/TXN_德州仪器_公司调研_2026-07-11.md:72>)与[TXN 7月公司调研 L371–379](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/TXN_2026-07-31T12_02_28-07_00-e3267055d7/TXN_德州仪器_公司调研_2026-07-11.md:371>)；AEHR [AEHR 7月公司调研 L22–26](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:22>)；SMCI [SMCI 7月公司调研 L255–266](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/SMCI_Super Micro Computer Inc_公司调研_2026-07-11.md:255>)。**6/6定向例子的基准区间包含或很接近公开共识，不能作为全192家的比例估计。**

MU基准较TTM增长149%–171%，但235B中点只比1.11T/4.77=232.70B的公开forward PS隐含收入高约1%；SMCI基准中点较TTM增长47%，却低于当时FY2027共识51.71B约4.3%。这样的增长可以真实巨大，也可以带来股票回报，但其“专业科技研究额外知道了多少”不能用增速本身回答。

另3个不同性质的例子单独列出，不能混成市场共识：ORCL基准90B就是公司FY2027指引（[ORCL 7月公司调研 L15](<D:/drive/Investment/基本面/公司调研/云算力_IDC_AI软件平台/ORCL_Oracle_Corporation_公司调研_2026-07-12.md:15>)）；ATEYY基准1.420T日元就是公司指引（[ATEYY 7月公司调研 L14–18](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/ATEYY_2026-07-31T12_29_45-07_00-949ba415ab/ATEYY_Advantest_公司调研_2026-07-12.md:14>)）；MOD基准3.90B落在公司3.82–4.29B指引内、数据中心基准1.80B靠近官方1.78–2.00B下端（[MOD 7月公司调研 L162–172](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/MOD_2026-07-31T12_34_49-07_00-97e25fc1ff/MOD_Modine_Manufacturing_公司调研_2026-07-12.md:162>)）。它们首先证明**基准模型重现公开锚**，不证明不具备判断经营质量/估值的附加价值。

反面论证：超额回报可能来自估值折价修复、利润率、资本配置、风险下降，即使收入预测不超过共识仍可能是好投资。SMCI本期为明显赢家，恰好是反证。本问题是“科技研究领先性未被增速证明”，不能变成“没有收入预期差就不会赚钱”。

## 5. 四个坏表现案例，主要警告其实已经在上游开头

- **PENG**：[PENG 7月公司调研 L12–16](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/PENG_Penguin Solutions_公司调研_2026-07-11.md:12>)已写应收+128%、库存+95%、9个月CFO11.2M对归母净利90.8M，现金转换约12.3%；过去52周涨234%、forward PE24.65、空头约20%。还明确表示真正近端利润来自内存短缺，而非尚小CXL。把后续跌幅简单归为“上游没研究现金流”不成立。
- **MOD**：[MOD 7月公司调研 L13–19](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/MOD_2026-07-31T12_34_49-07_00-97e25fc1ff/MOD_Modine_Manufacturing_公司调研_2026-07-12.md:13>)已写4B协议可取消/延迟，165M预付款仅占4.1%；剔预付后FCF从+105.4M到−59.6M；估值已计强增长，产能/供应执行是主要变量。同文还写Climate毛利同比下降510bp（[MOD 7月公司调研 L142–145](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/MOD_2026-07-31T12_34_49-07_00-97e25fc1ff/MOD_Modine_Manufacturing_公司调研_2026-07-12.md:142>)）。
- **WDC**：[WDC 7月公司调研 L249–258](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/WDC_2026-08-19T11_05_34-07_00-a39a043c98/WDC_WesternDigital_公司调研_2026-07-11.md:249>)已写基准约为公开共识；产品/EB涨价和正常化风险均有专节。
- **VST**：[VST 7月公司调研 L195–209](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/VST_Vistra_Corp_公司调研_2026-07-12.md:195>)已区分PPA在2027Q4起、2032Q4满的AWS路径，以及原始负荷queue可执行性；FY2027台阶包含并购/套保/电价，不是未来3个月全部收入兑现。

**可以确认：坏结果的关键反证至少在这几个上游报告已存在。**是否在排序或投资结论压缩中被降权，必须与具体下游字段对照，不能只凭四家公司下跌便指控报告没有传导。其系统含义是“风险有写”与“风险改变推荐强度”是两件事，增加更多文字事实本身无法证明决策纠错。

## 6. 错失案例显示‘收入确认时间’与‘股价确认信息时间’不是同一个时钟

**P/Everpure**：7月调研已经写清Meta业务75%–85%毛利（[P 7月公司调研 L441–451](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/P_Everpure_公司调研_2026-07-11.md:441>)），并把第二hyperscaler列为“模式可复制性的最强证据”（[P 7月公司调研 L711–719](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/P_Everpure_公司调研_2026-07-11.md:711>)）；乐观情景允许第二客户engineering qualification/小批量但不计大额收入（原文L530），极乐才计第二客户量产（L531）。说明研究当时并非完全看不到这条线。可是最终摘要把第二客户与CMX规模采用并排放进极乐（[P 7月公司调研 L752–762](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/P_Everpure_公司调研_2026-07-11.md:752>)），容易在压缩时丢掉“仅客户确认就改变可复制性估值”的作用。是否下游实际这样丢失，待具体决策表交叉。

**AEHR**：7/12报告明确知道两天后7/14财报（[AEHR 7月公司调研 L3–4](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:3>)），并提供可见订单85M基准、120M乐观、170M极乐（[AEHR 7月公司调研 L22–28](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:22>)）；财报核对表对FY2027指引只写至少80–90M及低于85M红旗（[AEHR 7月公司调研 L470–480](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:470>)）。这不等于应该预知后来新指引，但证明当时存在一个**近在两日、能一次改变全年预期的离散观测**，不能只按收入确认验收时间给重要性。4/16一手公告已证明41M大单、FY2027交付、半年订单92M且仍有其他客户需求：[AEHR官方4/16公告](https://www.aehr.com/2026/04/aehr-receives-record-41-million-production-order-from-lead-hyperscale-ai-customer-second-half-bookings-exceed-92-million/)，本次重新核验。

**ATKR、PSIX、SOMMY反对单一解释。**ATKR源报告开头已将其定义为周期材料+战略出售事件股（[ATKR 7月公司调研 L8–18](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/ATKR_Atkore_公司调研_2026-07-12.md:8>)）；PSIX写2026收入下降但FY2027收入共识恢复+21.5%，且规范化PE约11.8（[PSIX 7月公司调研 L8–18](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/PSIX_Power_Solutions_International_公司调研_2026-07-12.md:8>)，L90）；SOMMY专门列非AI的Agro与Pharma增长（[SOMMY 7月公司调研 L250–273](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/SOMMY_住友化学_Sumitomo_Chemical_公司调研_2026-07-11.md:250>)）。因此这些股票本期上涨不能统一归因于“未覆盖非AI”，更不能一律归为AI瓶颈模型预测成功或失败。ATKR实际收购、P第二客户、AEHR新指引的事后事件证据由主审计事件表承担，本文件不抢先以价格倒推因果。

## 7. 三个期限错配层级

一是**用户目标与正式方法目标**：7月实际投资决策prompt把NTM作为经营主窗口、12–18个月作为主要股东回报窗口、3–5年作为正常化校准（[7月正式决策prompt L61–69](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-14T00-53-50-566Z_company-investment-decision_VST_prompt.md:61>)）。这与用户希望的3个月、3–6个月头部推荐是不同任务。即便长周期估值在其期限内正确，也不自动获得季度排序预测能力。

二是**‘一年后’本身并非统一财务窗口**：AJNMY用2027-04至2028-03代替一年后（研究日2026-07，终点远约20.5个月）；VRT和VST用2027日历年，CLS也用2027E；ADI写未来12个月“或”届时年化，TMO写年化/LTM状态。这些是上游内部原文定义，不是按关键词缺失猜测。滚动收入、未来退出年化和次年全年不能无条件进入同一跨公司增长表。

三是**下游估值窗口与短期信息窗口**：P第二客户、AEHR新指引可以先改变长期可复制性/经营曲线的认识，实际收入后到。并非应该把未来收入提前确认，而是已经观察到的定价信息和收入实现分属不同环节。

反证与范围：WDC FY2027截至2027-06，较接近研究日后12个月，不应只因出现FY2027就判错；AAOI清楚分开NTM与退出run-rate，TXN也分产品退出率和公司NTM。下面逐家记录可供复核：

| 样本 | 人工核实的时间口径 | 原文 |
|---|---|---|
| CLS | 2027E；日历年，与滚动NTM有偏移 | [CLS 7月公司调研 L275–310](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/CLS_2026-07-31T12_02_40-07_00-0296e3cb59/CLS_Celestica Inc_公司调研_2026-07-11.md:275>)；[CLS 7月公司调研 L145–150](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/CLS_2026-07-31T12_02_40-07_00-0296e3cb59/CLS_Celestica Inc_公司调研_2026-07-11.md:145>) |
| WDC | FY2027约至2027年6月，近似NTM | [WDC 7月公司调研 L241–258](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/WDC_2026-08-19T11_05_34-07_00-a39a043c98/WDC_WesternDigital_公司调研_2026-07-11.md:241>)；[WDC 7月公司调研 L145–167](<D:/drive/Investment/基本面/公司调研/AI服务器_存储_EMS/备份/WDC_2026-08-19T11_05_34-07_00-a39a043c98/WDC_WesternDigital_公司调研_2026-07-11.md:145>) |
| ADI | 产品层未来12个月或届时年化混用；公司层NTM | [ADI 7月公司调研 L205–234](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/ADI_Analog_Devices_公司调研_2026-07-11.md:205>)；[ADI 7月公司调研 L308–339](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/ADI_Analog_Devices_公司调研_2026-07-11.md:308>) |
| TXN | 产品T+12退出率；公司另列NTM，区分较好 | [TXN 7月公司调研 L212–260](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/TXN_2026-07-31T12_02_28-07_00-e3267055d7/TXN_德州仪器_公司调研_2026-07-11.md:212>)；[TXN 7月公司调研 L330–342](<D:/drive/Investment/基本面/公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/TXN_2026-07-31T12_02_28-07_00-e3267055d7/TXN_德州仪器_公司调研_2026-07-11.md:330>) |
| AAOI | 2026Q3–2027Q2滚动；另列退出率，区分较好 | [AAOI 7月公司调研 L418–445](<D:/drive/Investment/基本面/公司调研/AI网络_光互联_连接器/AAOI_Applied_Optoelectronics_公司调研_2026-07-11.md:418>)；[AAOI 7月公司调研 L463–477](<D:/drive/Investment/基本面/公司调研/AI网络_光互联_连接器/AAOI_Applied_Optoelectronics_公司调研_2026-07-11.md:463>) |
| VISN | 至2027-07-10前滚12个月，清楚 | [VISN 7月公司调研 L263–277](<D:/drive/Investment/基本面/公司调研/AI网络_光互联_连接器/VISN_Vistance Networks_公司调研_2026-07-11.md:263>)；[VISN 7月公司调研 L375–404](<D:/drive/Investment/基本面/公司调研/AI网络_光互联_连接器/VISN_Vistance Networks_公司调研_2026-07-11.md:375>) |
| AJNMY | 一年后定义为FY2027E 2027-04至2028-03，较滚动NTM明显偏远 | [AJNMY 7月公司调研 L250–265](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/AJNMY_味之素 Ajinomoto_公司调研_2026-07-11.md:250>)；[AJNMY 7月公司调研 L21–26](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/AJNMY_味之素 Ajinomoto_公司调研_2026-07-11.md:21>) |
| SOMMY | 未来12个月 | [SOMMY 7月公司调研 L238–273](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/SOMMY_住友化学_Sumitomo_Chemical_公司调研_2026-07-11.md:238>)；[SOMMY 7月公司调研 L379–403](<D:/drive/Investment/基本面/公司调研/半导体材料_化学品_基板/SOMMY_住友化学_Sumitomo_Chemical_公司调研_2026-07-11.md:379>) |
| AEP | 未来12个月；合同实现率和按期上电率分开 | [AEP 7月公司调研 L287–330](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/备份/AEP_2026-07-31T12_37_06-07_00-3b2425a693/AEP_American_Electric_Power_公司调研_2026-07-11.md:287>)；[AEP 7月公司调研 L126–146](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/备份/AEP_2026-07-31T12_37_06-07_00-3b2425a693/AEP_American_Electric_Power_公司调研_2026-07-11.md:126>) |
| VST | FY2027日历年；非滚动NTM | [VST 7月公司调研 L351–399](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/VST_Vistra_Corp_公司调研_2026-07-12.md:351>)；[VST 7月公司调研 L195–209](<D:/drive/Investment/基本面/公司调研/电力_发电_能源_储能/VST_Vistra_Corp_公司调研_2026-07-12.md:195>) |
| AEHR | NTM；FY2027变更带28天过渡期需口径差 | [AEHR 7月公司调研 L235–264](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:235>)；[AEHR 7月公司调研 L387–408](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/AEHR_2026-07-18T13_43_39-07_00-6618995370/AEHR_Aehr_Test_Systems_公司调研_2026-07-12.md:387>) |
| TMO | 写年化/LTM状态，流量和退出率定义含混 | [TMO 7月公司调研 L286–322](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/TMO_2026-07-31T12_02_36-07_00-f7aee9d8c1/TMO_Thermo_Fisher_Scientific_公司调研_2026-07-12.md:286>)；[TMO 7月公司调研 L404–436](<D:/drive/Investment/基本面/公司调研/封测_检测_计量_光罩/备份/TMO_2026-07-31T12_02_36-07_00-f7aee9d8c1/TMO_Thermo_Fisher_Scientific_公司调研_2026-07-12.md:404>) |
| AAON | 未来一年；订单跨期有折扣 | [AAON 7月公司调研 L244–263](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/AAON_AAON_公司调研_2026-07-12.md:244>)；[AAON 7月公司调研 L139–156](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/AAON_AAON_公司调研_2026-07-12.md:139>) |
| VRT | 2027E日历年；非滚动NTM | [VRT 7月公司调研 L276–303](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/VRT_2026-07-31T12_37_01-07_00-50c82bab3a/VRT_Vertiv_公司调研_2026-07-12.md:276>)；[VRT 7月公司调研 L143–151](<D:/drive/Investment/基本面/公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/VRT_2026-07-31T12_37_01-07_00-50c82bab3a/VRT_Vertiv_公司调研_2026-07-12.md:143>) |
| ACLS | 约2027Q2止滚动12个月，清楚 | [ACLS 7月公司调研 L267–285](<D:/drive/Investment/基本面/公司调研/晶圆制造_前道设备/ACLS_Axcelis_Technologies_公司调研_2026-07-12.md:267>)；[ACLS 7月公司调研 L147–166](<D:/drive/Investment/基本面/公司调研/晶圆制造_前道设备/ACLS_Axcelis_Technologies_公司调研_2026-07-12.md:147>) |
| VECO | 滚动未来12个月，但增速比较2026E全年基数 | [VECO 7月公司调研 L207–224](<D:/drive/Investment/基本面/公司调研/晶圆制造_前道设备/VECO_Veeco_Instruments_公司调研_2026-07-12.md:207>)；[VECO 7月公司调研 L323–353](<D:/drive/Investment/基本面/公司调研/晶圆制造_前道设备/VECO_Veeco_Instruments_公司调研_2026-07-12.md:323>) |
| ABBNY | 一年后年化能力；公司另列未来一年增速 | [ABBNY 7月公司调研 L248–296](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/备份/ABBNY_2026-07-31T12_02_20-07_00-9846b160b2/ABBNY_ABB_Ltd_公司调研_2026-07-12.md:248>)；[ABBNY 7月公司调研 L151–160](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/备份/ABBNY_2026-07-31T12_02_20-07_00-9846b160b2/ABBNY_ABB_Ltd_公司调研_2026-07-12.md:151>) |
| WOLF | T+12M表混当前年化/TTM基数 | [WOLF 7月公司调研 L201–213](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/WOLF_Wolfspeed_公司调研_2026-07-12.md:201>)；[WOLF 7月公司调研 L318–347](<D:/drive/Investment/基本面/公司调研/配电_电源_功率器件/WOLF_Wolfspeed_公司调研_2026-07-12.md:318>) |
| ADBE | 产品ARR和公司NTM分列，区分较好 | [ADBE 7月公司调研 L250–264](<D:/drive/Investment/基本面/公司调研/云算力_IDC_AI软件平台/ADBE_Adobe_公司调研_2026-07-12.md:250>)；[ADBE 7月公司调研 L154–171](<D:/drive/Investment/基本面/公司调研/云算力_IDC_AI软件平台/ADBE_Adobe_公司调研_2026-07-12.md:154>) |
| ORCL | FY2027约2026-06至2027-05，较研究日提前约1个月 | [ORCL 7月公司调研 L225–244](<D:/drive/Investment/基本面/公司调研/云算力_IDC_AI软件平台/ORCL_Oracle_Corporation_公司调研_2026-07-12.md:225>)；[ORCL 7月公司调研 L134–150](<D:/drive/Investment/基本面/公司调研/云算力_IDC_AI软件平台/ORCL_Oracle_Corporation_公司调研_2026-07-12.md:134>) |

## 8. 宏观/情绪不能被简单写成‘项目没考虑’，必须分版本与接入方式

7/14首批实际prompt已经有四经营×五市场状态矩阵、市场价/利率/信用/波动/宽度等外部资料入口，但每家公司独立定义并识别全市场（[7月首批实际prompt L28](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-14T00-53-50-566Z_company-investment-decision_VST_prompt.md:28>)）。同一prompt禁止读技术面/公司情绪目录，却明确要求从日度资料与外部时戳资料研究市场状态（[L95–109 资料边界](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-14T00-53-50-566Z_company-investment-decision_VST_prompt.md:95>)）。因此“技术/情绪现成结论未直接接入”可以成立，“宏观完全缺席”不成立。

7/15前版本的方案备份已经改为共享快照及状态联动；当前runner又增加批次绑定、日期和SHA256校验，manifest目前明确列24家8/19批次。当前代码证据：[绑定快照与hash校验](<D:/drive/Investment/tools/research-runner/domains/company-investment-decision.mjs:126>)、[当前24家公司批次](<D:/drive/Investment/tools/research-runner/company-investment-decision.batches.json:5>)。它证明**目前有统一当期状态输入**，不证明7月所有报告都被这样生成，也不把当前修复用于替旧报告消责。

更深问题是五列条件估值回答“若某状态发生怎么办”，不必然回答“未来3–6个月哪种状态会发生、组合会怎样联动”。报告把概率层设为可选，不能把完整20格当成已经建立了可检验的短期联合概率预测。战争、通胀或市场情绪的缺口要落实到其改变需求/成本/折现率/风险溢价/传导时滞中的哪条边，而非列几个宏观名词就当归因完成。

## 9. 研究覆盖与自动化‘成功’的边界

7月75行业实际prompt的输出范围只有四个AI基础设施类别：园区电力机电冷却、服务器存储芯片、网络互联、晶圆设备材料测试（[7月行业实际输出范围](<D:/drive/Investment/tools/research-runner/prompt-debug/2026-07-10T18-34-23-594Z_industry_数据中心电力接入与高压变电_prompt.md:51>)）。其中有调度、网络软件等基础设施软件，不能笼统说75个都只有硬件。当前77行业新增机器人/商业航天属于后续版本。公司池虽包含软件/电力/化学/工具，但独立行业调查预算仍集中于AI建设技术栈。**这是覆盖先验的硬边界，尚不足以证明池外全部涨幅都是错失或把它归罪于执行。**

当前`output-validator.mjs`的完整验收函数主要检查文件名、目录、存在、普通文件、非空、当次mtime（[当前输出验收L91–108](<D:/drive/Investment/tools/research-runner/validators/output-validator.mjs:91>)）；runner通过即标记done并归档（[验收后done链](<D:/drive/Investment/tools/research-runner/runner.mjs:476>)）。没有在此函数验证财务恒等式、近端期限、引用原文支持、低于基准概率或公司一致性。该代码证据只代表当前读取版本，未拿它冒充7月原代码。它解释了**流水线完成率与投资证据有效性不是同一质量指标**，不证明已有每份done结果都存在内容错误。

## 10. 归因结论及本审计不支持的说法

已坐实的问题集中在四类：①共同乐观先验进入行业与公司模型；②不可观察的关键参数被反复转写为精细数字；③巨大绝对增长与相对公开预期的区别没有因“多层调研”自动消失；④财务实现时钟、信息确认时钟与3–6个月推荐期限错位。局部两例概率支持集错误以及多例财务窗口偏移可以直接定位原文。

需要主报告下游证据才能坐实的命题是：已有现金/稀释/事件反证究竟在哪个排序字段被丢失、不同方法是否重复使用同一隐含量、哪一家公司损益由经营/估值/事件/宏观哪一项主导。**现有证据不支持“全池基础事实普遍错误”“风险全部未写”“宏观完全未研究”“低于基准概率为零适用于192家”“只要提前知道事件就应买入”这些过度结论。**

产物：`upstream_company_inventory.csv`、`upstream_prompt_contract_audit.csv`、`upstream_manual_sample_audit.csv`、`upstream_expectation_comparisons.csv`；重跑脚本位于`scripts/upstream_*.py`；原文片段见`evidence/upstream_原文摘录.md`。
