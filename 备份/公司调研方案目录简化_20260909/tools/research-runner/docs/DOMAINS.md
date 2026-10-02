# Research Runner Domains

本文件只记录各 domain 的稳定输入边界。具体文件名规则和路径生成逻辑以 `domains/` 代码为准。

| Domain | 主要输入 | 正式输出范围 |
|---|---|---|
| `company` | `基本面/公司调研/研究方法/研究方案/研究方案_yyyymmdd_hhmmss.md`、`公司索引.md` | 索引指定的公司分类目录 |
| `company-investment-decision` | `分析报告/公司情景投资决策/研究方案/研究方案_yyyymmdd_hhmmss.md`、公司调研、行业调研、公司索引 | `分析报告/公司情景投资决策/结果/` |
| `company-comparison` | `分析报告/公司对比/研究方案/研究方案_yyyymmdd_hhmmss.md`、合并后的公司情景投资决策结果、公司索引 | `分析报告/公司对比/` 的正式结果目录 |
| `company-sentiment` | `情绪面/研究方法/研究方案/研究方案_yyyymmdd_hhmmss.md`、公司索引 | `情绪面/公司情绪/` |
| `industry` | `基本面/行业调研/研究方法/行业调研/研究方案/研究方案_yyyymmdd_hhmmss.md`、`行业索引.md` | 索引指定的行业分类目录 |
| `feature-quantization` | `基本面/特征量化/研究方案/` 中与任务主题对应的单个独立方案 | `基本面/特征量化/量化评分/` |
| `file-run` | 队列项目指定的 `promptFile` | `expectedOutputFile`，或提示文件目录中的唯一新输出 |


原 `company-evaluation` domain 已于 2026-09-01 淘汰。经营评估、价值传导、经营四情景和条件估值由一次 `company-investment-decision` 任务完成；历史文件保留在 `分析报告/公司评估_淘汰/`，不属于活动输入或输出。

## 正式输出契约

1. Domain 在正式运行前计算并锁定一个输出路径。
2. 同主题旧版正式文件先移动到该 domain 的 `备份/`。
3. 锁定路径同时用于提示注入、回滚、本地验收和完成归档。
4. 标准 domain 只接受本轮修改的非空正式文件，不启动第二个模型验证器。
5. `备份/`、`tmp/` 和研究方法目录不能作为正式输出目标。
6. 特征量化结果必须包含可校验的版本、截面日期和可交易时间；失败回滚只处理本轮锁定文件，不删除其他形成期快照。

当前同主题备份覆盖公司报告、合并后的公司经营评估与投资决策、公司对比、公司情绪、行业报告和特征评分。准确匹配规则以各 domain 的 `output-path` 与 `output-backup` 实现为准。

## 索引更新

- `add-company --update-index` 可以新增公司索引项，需要同时提供名称和分类。
- `add-industry --update-index` 可以新增行业索引项，需要提供分类。
- 其他 domain 不自动修改公司或行业索引。

研究方案版本目录以各自README.md为准，历史子目录用于追溯，不自动作为新任务入口。
