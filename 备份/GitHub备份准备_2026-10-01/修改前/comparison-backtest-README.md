# company-comparison 专项审计交付索引

阅读顺序：

1. [主报告](00_company-comparison专项回测与重做建议.md)：结论、证据、七维效果、跨流程比较、根因与逐节修改建议。
2. [192家公司逐股与逐报告表](01_192家公司逐股与逐报告回测.md)：每家公司自己的报告日期、入场价格、末价日期、收益、回撤与七维排名。
3. [证据链与方法附表](02_证据链与比较方法附表.md)：QCOM的42条原文、28榜单、更新前后同起点回测、SMCI事件分段。
4. [研究方案重写建议稿](03_company-comparison研究方案重写建议稿.md)：可供后续正式采用的正文，以及提示词改动和运行层能力的边界。

全部内容为一次性审计成品；正式目录的研究方案、原始报告、runner与队列未修改。

## 数据要点

`original_0714`为恢复的完整7/14批次；`latest_0718`为176份7/14加16份7/18的当前快照。后者不是192份同时重新运行的结果。

`next_open`为报告日之后第一个交易日开盘，`report_close`为报告日或此前最近收盘的敏感性口径，后者不能保证发布后可成交。统计截止9/4，MICLF仅有9/3有效末价，已单独披露。

`start_cutoff`是信息截止日，不是实际入场日；具体价格日期在`price_observations.csv`。统一跨方法采用截止7/15、7/16开盘入场。

收益、优势、最大回撤在CSV中以小数保存，0.065表示6.5%。优势为所选股票收益减未选股票收益，不是百分比比值。组合为派生排名前30等权买入持有，不含费用，亦非原始报告直接发布的持仓。

七维代码为near近端、long长期、odds赔率、defense防守、explosion爆发、mispricing错位、overall总体。`both`为主排名规则，其余variant为敏感性诊断，不从中择优作为主策略。

## 大型原始明细

- `comparison_pairs_parsed.csv`：两批次逐行原文及全部七维解析，保留源文件和行号。
- `comparison_pair_outcomes_next_open.csv`：逐方向、逐视角的胜者与双方实现收益。重复公司对并非独立试验。
- `reciprocal_pairs.csv`：反向判断、一致性分类、相对收益与原文定位。

这些文件较大，用Python或数据库筛选比直接用电子表格打开更合适。所有摘要均可由它们和冻结行情复算。

## 复算顺序

使用Python、pandas和numpy，工作目录为`D:/drive/Investment`：

```powershell
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/analyze_comparison.py'
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/extend_analysis.py'
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/frontier_diagnostics.py'
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/verify_and_enrich.py'
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/write_reports.py'
python -X utf8 '备份/company-comparison专项回测_2026-09-05/scripts/final_qa.py'
```

严格顺序执行。依赖上一轮`备份/项目反思_2026-09-04/data`中的冻结输入和原始报告；如果原始文件改变，哈希校验会停止。重写建议稿为人工撰写，不由脚本覆盖。`evidence/verification_run.log`保存本次最后一次顺序复核输出；`data/verification.json`、`data/final_qa.json`保存核验结果。
