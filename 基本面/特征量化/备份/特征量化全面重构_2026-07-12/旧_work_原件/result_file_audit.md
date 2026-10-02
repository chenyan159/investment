# 52 个正式特征结果文件抽取与一致性审计

审计日期：2026-07-12

审计边界：只读取 `基本面/特征量化/量化评分/` 根目录中匹配 `Fdd_*_量化评分_YYYY-MM-DD.md` 的 52 个正式文件；没有递归读取或混入 `量化评分/备份/`。

## 1. 生成日期证据

- 52 个文件的文件名日期全部为 `2026-06-04`。
- 52 个文件首行标题日期全部为 `2026-06-04`。
- 52 个文件“运行元信息”中的“评分日期”全部为 `2026-06-04`。
- 52 个文件引用的每日金融数据快照日期全部为 `2026-06-03`。
- 文件系统本地 `CreationTime` 从 `2026-06-04 00:47:51.622 -07:00`（F21）延续到 `2026-06-04 04:07:37.057 -07:00`（F52）；`LastWriteTime` 的整体窗口相同。
- 正文没有任何一个文件记录精确到时分秒的“本次运行时间”。17 个文件写出的 `2026-06-03 13:41:46 PDT` 是输入金融快照的生成/采集时间，不是特征结果运行时间。
- F37 的 `CreationTime=2026-06-04 03:15:28.799 -07:00`，反而晚于 `LastWriteTime=2026-06-04 03:15:06.936 -07:00` 约 21.9 秒，说明文件系统创建时间可能受复制、恢复或迁移影响，不能单独作为生成时刻。

结论：可以高置信确认这批正式结果的运行/评分日期是 `2026-06-04`，输入金融数据截止日是 `2026-06-03`；无法仅凭正文恢复每个文件的精确运行时刻，精确时刻只能把文件系统时间当代理证据。

逐文件三类日期、文件系统时间及原始运行元信息见 `feature_files_metadata.csv` 和 `feature_files_metadata.json`。

## 2. 样本覆盖和字段质量

- 52 个文件都声明 180 家公司，也都实际解析出 180 行；合计 `52 × 180 = 9,360` 行。
- 52 个文件的 ticker 集合完全相同：180 个 ticker，ticker-set SHA-256 只有 1 种。
- 每个文件均无重复 ticker、无缺失/重复排名，排名完整覆盖 1-180，且分数按降序排列。
- 所有分数都在 1.0-10.0 内并满足一位小数；证据等级均为 A-D；置信度均为高/中/低。
- 全公司排序表 10 列表头和数据列数一致，未发现结构破损行。

统一股票池完整表见 `unified_ticker_pool.csv`。股票池 ticker 如下：

AAOI, AAON, ABBNY, ACLS, ACMR, ADBE, ADI, AEHR, AEP, AJNMY, ALAB, ALLE, AMAT, AMD, AMKR, AMPX, AMZN, ANET, AOSL, APD, APH, APLD, ARM, ASGLY, ASMIY, ASML, ASMVY, ASX, ATEYY, ATKR, AVGO, AXTI, BABA, BDC, BE, BELFB, BESIY, BWXT, CAMT, CARR, CAT, CC, CDNS, CEG, CIEN, CLS, CMI, COHR, COHU, CRDO, CRWD, CRWV, CSCO, DCI, DELL, DIOD, DLR, DOV, DSCSY, DTE, ECL, EME, ENPH, ENS, ENTG, EQIX, ET, ETN, ETR, FCEL, FIX, FLEX, FLNC, FN, FORM, FTV, GEV, GFS, GLW, GNRC, GOOGL, HOCPY, HPE, HUBB, IBM, ICHR, IESC, IFNNY, IMOS, INTC, IREN, JBL, JCI, KEYS, KLAC, KLIC, LFUS, LIN, LITE, LRCX, LWLG, MCHP, META, MICLF, MIELY, MKSI, MMM, MOD, MPWR, MRAM, MRVL, MSFT, MSI, MTRN, MTSI, MU, MXL, MYRG, NBIS, NDSN, NOK, NTAP, NTNX, NVDA, NVMI, NVT, NVTS, OKLO, ON, ONTO, ORCL, PENG, PH, PLAB, PNR, POET, POWI, POWL, PSIX, PSTG, PWR, Q, QCOM, RKLB, RMBS, ROG, RYCEY, SANM, SHECY, SIMO, SITM, SMCI, SMR, SMTC, SNDK, SNPS, SOMMY, ST, STM, STX, TDY, TEL, TER, TMO, TSEM, TSLA, TSM, TT, TXN, UCTT, UMC, VECO, VIAV, VICR, VISN, VRT, VSH, VST, WDC, WOLF

## 3. 标识一致性异常

股票池 ticker 一致，但显示标签并不一致：

- 71 个 ticker 出现两种公司名称写法，差异全部来自 F10；多数是简称、法定名称、中英文名的差别。
- 至少有两处 F10 明确偏离上游 `公司调研/公司索引.md`：
  - `ASGLY`：上游索引和另外 51 个特征均为 `AGC Inc`，F10 写成 `Asahi Group Holdings`。
  - `MICLF`：上游索引和另外 51 个特征均为 `Mycronic AB`，F10 写成 `Micronics Japan`；F10 证据正文也在谈 probe card 与 mask writer，实际评价对象发生了替换，不能只当显示名问题。
- 180 个 ticker 都出现三种分类目录字符串；根因是 F11 把分类写为反引号包裹的目录路径，F27 保留结尾 `/`，其余 50 个特征使用无反引号、无结尾 `/` 的分类名。

下游回测应始终以 ticker 为连接键，并从公司索引统一回填公司名和标准分类；在修正 F10 的 ASGLY/MICLF 前，不应把这两行直接纳入特征有效性归因。

## 4. 重复分数列与高相似度

- 52 列分数向量没有任何完全相同列；52 列排名向量也没有任何完全相同列。
- 1,326 个特征对中，没有绝对 Pearson 相关系数达到 0.95。
- 有 20 对分数相关系数达到 0.85，说明不存在机械复制列，但存在明显的高重叠簇。最高几对为：
  - F39 6-12月催化剂强度 vs F43 基本面兑现确定性：`0.940852`
  - F05 当前估值赔率 vs F07 估值隐含增长压力：`0.911146`
  - F20 下一代平台适配度 vs F21 功能瓶颈强度：`0.903178`
  - F35 竞争优势持续性 vs F46 替代风险可控性：`0.899045`
  - F16 1-3月交付承接能力 vs F17 3-6月产能释放能力：`0.887794`
  - F08 财务承压可控性 vs F09 现金流转换质量：`0.885363`

相关性不等于语义重复，但这些高相关对是重构时优先检查共同证据、评分锚点和重复权重的候选。完整成对结果见 `feature_pairwise_similarity.csv`，0.85 以上子集见 `high_similarity_score_pairs_ge_0_85.csv`。

## 5. 中间产物和复现

- `feature_scores_long.csv/json`：9,360 行长表，含特征、ticker、公司、分类、分数、排名、证据等级和置信度。
- `feature_scores_wide.csv`：180 行 × 52 个分数列，供收益率合并和特征有效性评估。
- `feature_ranks_wide.csv`、`feature_confidence_wide.csv`：排名和置信度宽表。
- `feature_files_metadata.csv/json`：逐文件日期证据和文件系统时间。
- `feature_qa.csv`：逐特征覆盖、排名、分数、表结构和哈希验收。
- `unified_ticker_pool.csv`：统一股票池、名称/分类变体、缺失特征。
- `feature_pairwise_similarity.csv`：全部 1,326 对分数/排名相似度。
- `audit_manifest.json`：范围、计数和所有输出路径。

复现命令：

```powershell
pwsh -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "D:\drive\Investment\基本面\特征量化\_work\restructure_20260712\audit_feature_results.ps1"
```
