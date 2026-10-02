# Research Runner

Research Runner 使用 Codex SDK 执行 Investment 项目的批量研究任务。它负责队列调度、domain 路由、正式输出备份、路径校验和运行日志，不负责用第二个模型重新评价研究质量。

## 关键边界

- 项目根目录和 Codex 工作目录默认是 `D:\drive\Investment`。
- 活动队列、完成归档和并发控制位于父目录 `tools/`：`queue.jsonl`、`queue.done.jsonl`、`queue.control.json`。
- 历史队列快照统一放在 `queue-backups/`；批量修复队列前先备份活动与完成 JSONL，不原地修改历史快照。
- 队列路径统一使用 Investment 根目录相对路径。
- 正式任务遵循项目 `AGENTS.md` 层级；`备份/`、`tmp/` 和研究方法目录不是正式输出目标。

## 快速开始

```powershell
cd "D:\drive\Investment\tools\research-runner"
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
