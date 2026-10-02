# Investment 工具目录

本目录保存跨研究域使用的自动化工具和共享队列文件。

- `research-runner/`：通过 Codex SDK 执行公司、行业、情绪、评估和量化研究队列。
- `site/`：把正式研究资料构建为静态公开看板。
- `update-github.ps1`：将整个项目当前文件状态提交并推送到 GitHub；用法和失败处理见根目录 `README.md`。
- `queue.jsonl`：活动研究队列。
- `queue.done.jsonl`：完成任务归档。
- `queue.control.json`：运行时目标并发数。

具体安装、命令和维护边界以各工具自己的 `README.md` 为准。队列备份进入 `research-runner/queue-backups/`，不要在 tools 根目录散放临时快照。
