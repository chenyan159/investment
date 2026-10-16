# R2 首轮估值研究中间记录

边界：全程只读01_inputs，不读取02_round1其他研究者结果；无Git、队列及生产写入。信息截止2026-10-12 19:40 PDT。

已完整扫描universe_screen.csv的245行并解析universe.json的245公司证券、金融和报告路径。先按价格、盈利口径、币种、资本结构和周期位置扫描，再选择31家公司读取。不能将同源Yahoo算术校验ok等同于财务真实性或远期EPS可实现性。

已读取公司报告及模型段：ADBE CRM ORCL BABA NVDA AVGO ALNY BNTX PNR ENPH PGR RNR ON MCHP SMCI BDC CLS MOD JBL MKSI MU SNDK STX WDC PLAB GFS QCOM。另阅读AMZN MSFT VST ENS公司前段、VST现金模型。六类资料均已使用：产业背景Token经济/瓶颈、核酸行业、公司、ADBE/PNR/BNTX等情景与对比、全池金融。

推理摘要（非内在思维链）：
- ADBE/PNR的低价格更有近期经营修复依据，但现金/回购不能构成价格下限。
- MU/SNDK极低forward PE同时对应异常毛利，不可仅以PE排序；分别加入FY28价格正常化与合同履约失败压力。
- CRM须从FCF扣SBC并计新增债息。BDC收购后为杠杆权益，不是稳健现金底。
- SMCI优先股股息、转换稀释、负经营现金与不可撤销采购承诺要求极宽下行情景。
- WDC剔除Sandisk持股收益，PLAB扣少数股东，ON补并购稀释；供应商forward EPS可能高于相应独立正常化模型。
- 20个提名是送审池，可包含明确等待价格/事实条件，不能为凑数声称20个现价均具优良赔率。

关键原始核验：
1. MOD已于2026-10-01完成PT分拆及Gentherm组合，9/28记录日每原MOD股得到0.44619 THRM；MOD收到约156m美元用于偿债。10/12买入存续MOD不再得到该历史分派，模型不得计入PT利润或THRM权益。来源：https://investors.modine.com/news/news-details/2026/Modine-Completes-Spin-off-and-Combination-of-its-Performance-Technologies-Business-with-Gentherm/default.aspx 。已经打开正文。
2. PNR已于2026-10-01完成Taco收购，约1.4bn美元，旧9/26公司报告的待交割状态须更新；10/12买家承接合并后的债务与经营，但尚无完整交割后季度资产负债表。来源：https://investors.pentair.com/news-releases/news-release-details/pentair-completes-acquisition-taco-group-holdings 。已经打开正文。
3. 已打开ADBE Q3财报PDF、NVDA Q2 FY27公告、AVGO Q3公告、ALNY Q2公告、PNR Q2 SEC、BDC Q2 IR、BNTX Q2 SEC、MU Q4 SEC、SMCI FY26公告、SNDK Q4 PDF，连同两项交易共12个原始文档。来源表将随最终JSON单独落盘。
