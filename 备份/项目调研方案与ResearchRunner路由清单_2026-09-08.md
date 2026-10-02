# 项目调研方案与 Research Runner 路由清单

核查日期：2026-09-08。依据当前磁盘方案、活动domain代码、排序注册表与队列文件。统计现行研究入口及可复用模板，不把备份、已并入/冻结/退出的方法、旧迭代版本、临时包装提示和prompt-debug重复计入。共64份现行入口文件，另1份回测模板。

字数口径：读取UTF-8全文，删除所有空白字符后计算字符数；含汉字、英文字母、数字、标点和Markdown标记。不等于纯汉字数、Word词数或token数，也不含runner追加的提示。

## 调度与实际执行

队列源为 [tools/queue.jsonl](D:/drive/Investment/tools/queue.jsonl)，完成记录进入 [tools/queue.done.jsonl](D:/drive/Investment/tools/queue.done.jsonl)。本次读取时活动队列为空。runner不自动遍历全部研究方案，也不自动读取排序注册表生成任务。

优先级：industry → company → feature-quantization与company-sentiment同组 → company-investment-decision → company-comparison与file-run同组。高组存在pending/running/retry_pending时阻塞低组；同组按队列顺序领取，可并发。默认并发10，当前queue.control.json配置15。当前代码模型gpt-6-astra；推理强度取任务reasoningEffort，缺省high。

每项任务校验输入路径、锁定输出路径、按domain规则备份旧结果、组装方案全文及输出要求，再通过Codex SDK在独立线程中执行，启用联网搜索。完成后检查本轮新增/更新的非空正式文件；特征量化追加元数据校验；成功归档，失败按重试和回滚契约处理。此验收不等于研究质量获得第二模型认可。

file-run只把promptFile全文与输出要求拼成提示，不自动替换主题占位符，不把displayName/runId变成研究对象说明。它没有方案专属业务路由，输入边界由方案规定；新任务应显式指定expectedOutputFile。

代码证据：[活动domain](D:/drive/Investment/tools/research-runner/domains/index.mjs)、[调度常量](D:/drive/Investment/tools/research-runner/runner.mjs:46)、[领取逻辑](D:/drive/Investment/tools/research-runner/queue-store.mjs:299)、[提示组装目录](D:/drive/Investment/tools/research-runner/prompts)、[file-run组装](D:/drive/Investment/tools/research-runner/prompts/file-run.mjs)。

## 分类统计

|分类|文件数|字数合计|
|---|---:|---:|
|产业背景与会议|6|49377|
|公司排序：experiment|2|6843|
|公司排序：paired_experiment|6|20483|
|公司排序：routine|8|29290|
|基础专用方案|5|34720|
|技术面独立因子|18|37549|
|可复用回测模板|1|1328|
|特征量化|19|56977|

## 产业背景与会议

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/基本面/行业调研/研究方法/产业背景：全球AI需求与Token经济框架.md](<D:/drive/Investment/基本面/行业调研/研究方法/产业背景：全球AI需求与Token经济框架.md>)|9953|`file-run`：promptFile直接读取本方案；输出到基本面/行业调研/产业背景的指定日期化文件。完成归档有同路径运行记录，但不能据此认定当前修订版本已经运行。|
|[D:/drive/Investment/基本面/行业调研/研究方法/产业背景：数据中心建设规模.md](<D:/drive/Investment/基本面/行业调研/研究方法/产业背景：数据中心建设规模.md>)|15401|`file-run`：promptFile直接读取本方案；输出到基本面/行业调研/产业背景的指定日期化文件。完成归档有同路径运行记录，但不能据此认定当前修订版本已经运行。|
|[D:/drive/Investment/基本面/行业调研/研究方法/产业背景：头部AI芯片.md](<D:/drive/Investment/基本面/行业调研/研究方法/产业背景：头部AI芯片.md>)|6165|`file-run`：promptFile直接读取本方案；输出到基本面/行业调研/产业背景的指定日期化文件。完成归档有同路径运行记录，但不能据此认定当前修订版本已经运行。|
|[D:/drive/Investment/基本面/行业调研/研究方法/产业背景：AI产业链瓶颈与反证指标总表.md](<D:/drive/Investment/基本面/行业调研/研究方法/产业背景：AI产业链瓶颈与反证指标总表.md>)|7336|`file-run`：promptFile直接读取本方案；输出到基本面/行业调研/产业背景的指定日期化文件。完成归档有同路径运行记录，但不能据此认定当前修订版本已经运行。|
|[D:/drive/Investment/基本面/行业调研/研究方法/产业背景：AI产业链全局图谱与口径字典.md](<D:/drive/Investment/基本面/行业调研/研究方法/产业背景：AI产业链全局图谱与口径字典.md>)|7436|`file-run`：promptFile直接读取本方案；输出到基本面/行业调研/产业背景的指定日期化文件。完成归档有同路径运行记录，但不能据此认定当前修订版本已经运行。|
|[D:/drive/Investment/基本面/行业调研/研究方法/会议调研方案.md](<D:/drive/Investment/基本面/行业调研/研究方法/会议调研方案.md>)|3086|`file-run`：唯一会议入口；文件全文原样载入。会议名称、年份和截止应明确，不能只写在displayName。file-run不替换会议占位符；现有入口说明允许由明确输出文件名传递对象。历史临时包装方案不是当前入口。|

## 公司排序：experiment

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/分析报告/公司排序/03_观察_待更新/09_弹性成长_原02/迭代版本/R10_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/03_观察_待更新/09_弹性成长_原02/迭代版本/R10_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3285|`file-run`：09 弹性成长；输出：分析报告/公司排序/03_观察_待更新/09_弹性成长_原02/迭代版本/R10_2026-09-07_期限证据与选择语义/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N05_市场状态自适应双阶段/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N05_市场状态自适应双阶段/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3558|`file-run`：N05 市场状态自适应双阶段；输出：分析报告/公司排序/06_候选新方案_待验证/N05_市场状态自适应双阶段/迭代版本/R03_2026-09-07_期限证据与选择语义/02_排序结果.md|

## 公司排序：paired_experiment

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md>)|3415|`file-run`：E04 风险调整赔率输入隔离；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md>)|3430|`file-run`：E04 ABCDE对照；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E04_风险调整赔率_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md>)|3413|`file-run`：E05 极简基准兑现输入隔离；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md>)|3428|`file-run`：E05 ABCDE对照；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E05_极简基准兑现_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/01_研究方案.md>)|3391|`file-run`：E06 尾部生存输入隔离；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/BCDE/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/01_研究方案.md>)|3406|`file-run`：E06 ABCDE对照；输出：分析报告/公司排序/07_输入扩展对照方案_待验证/E06_尾部生存_输入隔离/迭代版本/R01_2026-09-08_输入隔离/ABCDE/02_排序结果.md|

## 公司排序：routine

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U01_赔率与基准承载/迭代版本/R01_2026-09-08_双判断/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U01_赔率与基准承载/迭代版本/R01_2026-09-08_双判断/01_研究方案.md>)|4156|`file-run`：01 风险调整赔率；输出：分析报告/公司排序/08_常规研究单元/U01_赔率与基准承载/迭代版本/R01_2026-09-08_双判断/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/01_暂时有效_核心/02_预期兑现概率_十二句话S02_原10/迭代版本/R11_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/01_暂时有效_核心/02_预期兑现概率_十二句话S02_原10/迭代版本/R11_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3375|`file-run`：02 预期兑现概率；输出：分析报告/公司排序/01_暂时有效_核心/02_预期兑现概率_十二句话S02_原10/迭代版本/R11_2026-09-07_期限证据与选择语义/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/02_暂时有效_辅助/04_极简基准兑现_迭代实验_原06/迭代版本/R24_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/02_暂时有效_辅助/04_极简基准兑现_迭代实验_原06/迭代版本/R24_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3377|`file-run`：04 极简基准兑现；输出：分析报告/公司排序/02_暂时有效_辅助/04_极简基准兑现_迭代实验_原06/迭代版本/R24_2026-09-07_期限证据与选择语义/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/02_暂时有效_辅助/06_双源三视图_原01/迭代版本/R04_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/02_暂时有效_辅助/06_双源三视图_原01/迭代版本/R04_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3471|`file-run`：06 双源三视图；输出：分析报告/公司排序/02_暂时有效_辅助/06_双源三视图_原01/迭代版本/R04_2026-09-07_期限证据与选择语义/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U07_收入台阶与现金转化/迭代版本/R01_2026-09-08_双判断/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U07_收入台阶与现金转化/迭代版本/R01_2026-09-08_双判断/01_研究方案.md>)|4211|`file-run`：07 未来收入台阶；输出：分析报告/公司排序/08_常规研究单元/U07_收入台阶与现金转化/迭代版本/R01_2026-09-08_双判断/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U08_证据与经济风险审查/迭代版本/R01_2026-09-08_联合审查/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/08_常规研究单元/U08_证据与经济风险审查/迭代版本/R01_2026-09-08_联合审查/01_研究方案.md>)|3815|`file-run`：N02 反证闭环与尾部生存；输出：分析报告/公司排序/08_常规研究单元/U08_证据与经济风险审查/迭代版本/R01_2026-09-08_联合审查/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N03_预期差增量与证据升级/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N03_预期差增量与证据升级/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3424|`file-run`：N03 预期差增量与证据升级；输出：分析报告/公司排序/06_候选新方案_待验证/N03_预期差增量与证据升级/迭代版本/R03_2026-09-07_期限证据与选择语义/02_排序结果.md|
|[D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N06_超高增长与多倍价值/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md](<D:/drive/Investment/分析报告/公司排序/06_候选新方案_待验证/N06_超高增长与多倍价值/迭代版本/R03_2026-09-07_期限证据与选择语义/01_研究方案.md>)|3461|`file-run`：N06 超高增长与多倍价值；输出：分析报告/公司排序/06_候选新方案_待验证/N06_超高增长与多倍价值/迭代版本/R03_2026-09-07_期限证据与选择语义/02_排序结果.md|

## 基础专用方案

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/基本面/公司调研/研究方法/调研方案.md](<D:/drive/Investment/基本面/公司调研/研究方法/调研方案.md>)|6983|`company`：每个股票代号一项任务；替换公司占位符；输出到公司索引指定分类。|
|[D:/drive/Investment/基本面/行业调研/研究方法/行业调研方案.md](<D:/drive/Investment/基本面/行业调研/研究方法/行业调研方案.md>)|3170|`industry`：每个行业一项任务；替换行业占位符，并按索引附加researchScope；输出到行业分类。|
|[D:/drive/Investment/分析报告/公司情景投资决策/研究方案.md](<D:/drive/Investment/分析报告/公司情景投资决策/研究方案.md>)|15319|`company-investment-decision`：每家公司一项任务；替换股票代号；输出到公司情景投资决策/结果。|
|[D:/drive/Investment/分析报告/公司对比/研究方案.md](<D:/drive/Investment/分析报告/公司对比/研究方案.md>)|5414|`company-comparison`：以公司A股票代号触发比较；替换公司A占位符；输出由domain锁定。|
|[D:/drive/Investment/情绪面/研究方法/研究方案.md](<D:/drive/Investment/情绪面/研究方法/研究方案.md>)|3834|`company-sentiment`：每家公司一项情绪研究；输出到情绪面/公司情绪。|

## 技术面独立因子

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/技术面/研究方案/MF001_价格趋势与时间序列动量_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF001_价格趋势与时间序列动量_研究方案.md>)|2083|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF002_实现波动率与波动状态_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF002_实现波动率与波动状态_研究方案.md>)|1968|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF003_期权隐含波动率与方差风险溢价_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF003_期权隐含波动率与方差风险溢价_研究方案.md>)|2080|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF004_市场宽度离散度与集中度_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF004_市场宽度离散度与集中度_研究方案.md>)|1901|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF005_盈利预期修正与盈利Nowcast_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF005_盈利预期修正与盈利Nowcast_研究方案.md>)|2080|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF006_信用利差与金融条件_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF006_信用利差与金融条件_研究方案.md>)|1986|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF007_利率曲线实际利率与货币政策意外_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF007_利率曲线实际利率与货币政策意外_研究方案.md>)|2289|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF008_宏观增长通胀就业与数据意外_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF008_宏观增长通胀就业与数据意外_研究方案.md>)|2148|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF009_新闻文本政策不确定性与地缘风险_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF009_新闻文本政策不确定性与地缘风险_研究方案.md>)|2165|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF010_聚合卖空与Short_Interest_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF010_聚合卖空与Short_Interest_研究方案.md>)|2190|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF011_尾部风险回撤概率与条件分位数_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF011_尾部风险回撤概率与条件分位数_研究方案.md>)|2123|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF012_QQQ小盘与半导体相对强弱_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF012_QQQ小盘与半导体相对强弱_研究方案.md>)|2058|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF013_总派息回购与净发行_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF013_总派息回购与净发行_研究方案.md>)|2057|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF014_CFTC仓位资金流与市场拥挤_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF014_CFTC仓位资金流与市场拥挤_研究方案.md>)|2162|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF015_跨资产风险传导_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF015_跨资产风险传导_研究方案.md>)|1970|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF016_估值风险溢价与实际利率差_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF016_估值风险溢价与实际利率差_研究方案.md>)|2157|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF017_市场微观结构与交易流动性_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF017_市场微观结构与交易流动性_研究方案.md>)|2073|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|
|[D:/drive/Investment/技术面/研究方案/MF018_季节性再平衡期权到期与事件日历_研究方案.md](<D:/drive/Investment/技术面/研究方案/MF018_季节性再平衡期权到期与事件日历_研究方案.md>)|2059|`file-run`：promptFile指向本文件；expectedOutputFile指定技术面/因子研究下的日期化报告。无专用技术面domain。|

## 可复用回测模板

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/分析报告/公司排序/91_通用研究方案/排序结果_生成后股价验证_file-run方案模板.md](<D:/drive/Investment/分析报告/公司排序/91_通用研究方案/排序结果_生成后股价验证_file-run方案模板.md>)|1328|`file-run（先复制填写）`：先复制为具体版本回测目录的01_评估方案.md，填写参数，再指定同目录02_评估结果.md运行。|

## 特征量化

|具体路径（点击打开）|字数|Runner路由与运行方式|
|---|---:|---|
|[D:/drive/Investment/基本面/特征量化/研究方案/G01_PIT证据与数据质量门槛_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/G01_PIT证据与数据质量门槛_研究方案.md>)|3243|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/G02_流动性与可投资性门槛_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/G02_流动性与可投资性门槛_研究方案.md>)|3080|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/G03_监管地缘风险覆盖层_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/G03_监管地缘风险覆盖层_研究方案.md>)|3098|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N01_AI可归因盈利暴露_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N01_AI可归因盈利暴露_研究方案.md>)|2870|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N02_系统瓶颈不可替代性_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N02_系统瓶颈不可替代性_研究方案.md>)|2922|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N03_AI需求传导与价值量弹性_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N03_AI需求传导与价值量弹性_研究方案.md>)|3179|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N04_已披露基本面动量_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N04_已披露基本面动量_研究方案.md>)|2681|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N05_风险调整估值赔率_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N05_风险调整估值赔率_研究方案.md>)|2877|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N06_财务质量与融资韧性_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N06_财务质量与融资韧性_研究方案.md>)|2816|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N07_前瞻基本面修正期限结构_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N07_前瞻基本面修正期限结构_研究方案.md>)|3104|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N08_产能交付执行兑现_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N08_产能交付执行兑现_研究方案.md>)|3465|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N09_商业化与平台路线适配_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N09_商业化与平台路线适配_研究方案.md>)|3010|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N10_持久护城河与替代风险_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N10_持久护城河与替代风险_研究方案.md>)|2798|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N11_客户与订单质量_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N11_客户与订单质量_研究方案.md>)|3059|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N12_供需景气与定价捕获_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N12_供需景气与定价捕获_研究方案.md>)|3200|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N13_催化剂事件期限结构_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N13_催化剂事件期限结构_研究方案.md>)|2944|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N14_有符号预期差_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N14_有符号预期差_研究方案.md>)|2749|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N15_情景收益不对称性_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N15_情景收益不对称性_研究方案.md>)|2908|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|
|[D:/drive/Investment/基本面/特征量化/研究方案/N16_行业中性相对强度_研究方案.md](<D:/drive/Investment/基本面/特征量化/研究方案/N16_行业中性相对强度_研究方案.md>)|2974|`feature-quantization`：subject为不含.md的文件名；每次只读取本方案；追加版本、截面日与可交易时间元数据；输出量化评分。|

## 注册身份与实际完成记录的区别

排序注册表当前含8个routine、2个experiment、3组成对实验（6份文件）；absorbed/historical不属于默认执行入口。注册表是选任务依据，不是调度器。当前完成归档已有E04/E05/E06的BCDE路径done记录，因此注册表或说明中的“未运行”状态可能滞后；仅有路径记录也不能证明当前文件哈希版本曾运行，更不能认定整组成对实验完成。

旧公司评估位于 [分析报告/公司评估_淘汰](D:/drive/Investment/分析报告/公司评估_淘汰)，company-evaluation已不在活动domain列表。旧排序迭代、冻结方法及历史评估方案仍保留，但不与现行入口混计。金融资料本轮未发现以研究方案/调研方案命名的现行Markdown入口；数据生成脚本、新闻工作流不是这7个domain中的独立研究类型。

## 入队方式

在D:/drive/Investment/tools/research-runner运行对应queue:add-company、queue:add-industry、queue:add-company-investment-decision、queue:add-company-comparison、queue:add-company-sentiment或queue:add-feature-quantization命令。特征量化也可queue:seed-feature-quantization-from-plans播种，行业可从索引播种；这些是显式命令，不是runner自动扫描。

通用形式：`node tools/research-runner/queue-tools.mjs add-file-run --run-id=<唯一ID> --prompt-file=<项目相对方案路径> --expected-output-file=<项目相对结果路径>`（从项目根目录执行；带空格参数应加引号）。排序从注册表提取两条路径；技术面指定因子研究输出；会议使用唯一方案并提供明确对象。已生成排序结果须新建独立版本目录后再跑。入队后由runner统一调度。本次只读取与生成清单，没有入队或启动研究。