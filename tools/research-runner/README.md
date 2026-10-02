# Research Runner

Research Runner 使用 Codex SDK 执行 Investment 项目的批量研究任务。它负责队列调度、domain 路由、正式输出备份、路径校验和运行日志，不负责用第二个模型重新评价研究质量。

## 关键边界

- 项目根目录和 Codex 工作目录默认是 `D:\investment`。
- 活动队列、完成归档和并发控制位于父目录 `tools/`：`queue.jsonl`、`queue.done.jsonl`、`queue.control.json`。
- 历史队列快照统一放在 `queue-backups/`；批量修复队列前先备份活动与完成 JSONL，不原地修改历史快照。
- 队列路径统一使用 Investment 根目录相对路径。
- 正式任务遵循项目 `AGENTS.md` 层级；`备份/`、`tmp/` 和研究方法目录不是正式输出目标。

## 快速开始

```powershell
cd "D:\investment\tools\research-runner"
npm install
npm run queue:validate
npm run queue:status
npm run once
```

Runner 使用 ChatGPT/Codex 订阅登录，不需要设置 `OPENAI_API_KEY` 或 `CODEX_API_KEY`。

## 目录

- `runner.mjs`：调度、Codex 调用、配额检查和运行生命周期。
- `queue-store.mjs`、`queue-tools.mjs`：队列存储、校验和维护命令。
- `domains/`：各研究类型的输入、输出路径和备份规则。
- `prompts/`：各研究类型的提示组装。
- `validators/`：确定性本地输出校验。
- `logs/`：当前运行日志和归档日志。
- `queue-backups/`：队列快照和隔离实验。

## 运行约定

- 每项任务使用独立 Codex 线程，并以队列中的 `reasoningEffort` 运行。
- domain 在运行前锁定一个正式输出路径，并备份同主题旧文件；成功后只接受本轮生成或修改的非空正式文件。
- 如果正式路径缺失但恰好存在一个符合 domain 规则的新文件，runner 可以将其规范化到锁定路径。
- 当前状态只通过 `npm run queue:status` 查看，不维护 Markdown 状态文件。
- 模型、默认并发、调度优先级和配额阈值以代码常量为准，不在 README 重复维护。

## 详细文档

- [Domains](docs/DOMAINS.md)：各任务类型的输入、输出和备份边界。
- [Queue](docs/QUEUE.md)：队列文件、字段和管理命令。
- [Operations](docs/OPERATIONS.md)：运行参数、并发、配额和日志。

## 通用执行器与研究独立性

- Runner 是通用、稳定的研究执行器；调度、隔离执行、输入输出路径、备份和通用校验契约应保持固化，确保各项研究独立执行。
- 一次性研究的公司名单、日期、价格锚、市场判断、共享材料和特殊流程，应放在该次研究方案或 file-run 输入中，不得为此修改 runner、domain、通用提示组装或增加永久批次前置条件。
- Runner 不替研究方案预先选择研究结论，不注入覆盖研究方案的市场分类，也不因某次研究需求关闭方案已有的缺失资料处理规则。
- 只有明确需要通用能力变更时才修改执行器，并验证兼容性；不得把一次性研究安排升级为所有后续任务必须满足的约束。

## 11类研究方案版本

映射见[research-plans.json](research-plans.json)。每个方案目录根部恰好保留一个研究方案_yyyymmdd_hhmmss.md，同名全文归档于yyyymmdd_hhmmss子目录。README及修改记录不进入研究提示。

专用domain照常入队。背景与会议的file-run可以将--prompt-file设为注册目录、具体版本文件或迁移前路径（兼容映射到现行版）；其他file-run保持原有行为。入队绑定planId、planVersion、planEntryFile、planSnapshotFile、planSha256和planBoundAt；启动补齐未绑定活动任务并记录日志。实际运行记录actualPromptFile与actualPromptSha256，完成归档及以后队列备份保留字段，旧归档不回填。

更新方案：从项目根目录运行`node tools/research-runner/research-plan-tools.mjs publish --plan-id=company --source=<完整新方案> --reason=<修改原因>`。命令创建版本子目录的两个文件并替换根目录现行副本，后续手动追加修改内容与效果。

## 横向专题路径契约

六个背景/会议方案集中在 `基本面/行业调研/横向专题/<专题>/研究方案/`。注册表中的 `directoryAliases` 保留迁移前目录兼容，历史版本迁移后继续校验原哈希。`defaultOutputDir` 提供 file-run 默认输出位置，`outputRoot` 约束显式输出也只能进入 `基本面/行业调研/产业背景/`；会议默认进入其 `顶级会议信息/` 子目录。普通未注册 file-run 的默认行为不变。
