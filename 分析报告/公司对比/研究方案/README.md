# 公司对比研究方案

当前版本：`20261022_031413`。在 `20261011_044451` 基础上确立标准导向与核心矛盾自主深挖原则，将六个正交投资角度与综合投资裁决结构化打通去重，并在正文对比总表及配套 JSON 中升级分视角对比优劣（`compounding_preference`/`convexity_preference` 及 `both_avoid`）与三层结构化综合决策（`decision`）。固定交付 MD＋JSON。使用最新方案重新入队，不回填既有报告和队列，不更新站点。

## 目录

- 根目录唯一的 `研究方案_yyyymmdd_hhmmss.md`：供runner选择的现行版本。
- `yyyymmdd_hhmmss/`：每次修改的档案目录，包含同名方案全文及`修改记录以及效果.md`。

## 每次修改

1. 创建日期时间子目录，写入新的完整方案及修改记录以及效果.md，说明修改原因、内容和预期效果。
2. 用新子目录中的方案替换根目录旧方案：文件名同时更新，根目录只保留一份，内容与子目录副本一致。
3. 历史方案全文保留；后续运行及效果追加到对应版本的修改记录以及效果.md。

统一使用America/Los_Angeles时间，命名为yyyymmdd_hhmmss。runner只扫描根目录，不递归选择历史方案。入队时绑定版本，执行时读取绑定的副本；活动队列、完成归档及新生成的队列备份保留版本字段，日志记录使用版本。README和修改效果记录不拼入研究提示。

可从项目根目录使用：

`node tools/research-runner/research-plan-tools.mjs publish --plan-id=company-comparison --source=<修改后方案文件> --reason=<修改原因>`

原有专用domain入队命令继续使用。
