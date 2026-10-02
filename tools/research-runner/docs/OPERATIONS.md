# Research Runner Operations

## Dry Run

Dry run 检查输入和路径，不调用 Codex：

```powershell
npm run dry-run
npm run dry-run -- --ticker=CEG
npm run dry-run -- --domain=company-comparison --ticker=MU
npm run dry-run -- --domain=file-run --run-id="example" --prompt-file="分析报告/tmp/运行方案.md"
```

## 正式运行

```powershell
npm start
npm run once
```

常用参数：

```powershell
node runner.mjs --once
node runner.mjs --timeout-minutes=180
node runner.mjs --max-attempts=7
node runner.mjs --max-jobs=3
node runner.mjs --concurrency=3
node runner.mjs --sandbox-mode=danger-full-access
```

## 并发控制

- 显式 `--concurrency=N` 会在运行前更新 `../queue.control.json`。
- 运行中 runner 会持续重读控制文件；提高数值会继续领取任务，降低数值只停止新领取，不取消已运行任务。
- `concurrency: 0` 停止领取新任务；活动任务完成后 runner 正常退出。
- 无显式参数时使用控制文件中的值；初始默认值和合法范围以代码为准。

## 配额和失败

- 每个正式任务开始前查询 Codex 使用窗口；达到代码设定阈值时，任务返回 `retry_pending`，不消耗尝试次数。任一使用窗口的可用额度剩余 5% 或更少（使用率达到 95%）时，记录配额和退出原因，停止领取新任务；已有任务收尾后退出进程并释放锁，不驻留等待自然重置。在途任务仍会消耗额度，退出时的实际剩余额度可能低于 5%。手动 reset 或自然恢复额度后，需重新启动 runner；新进程重新查询配额。
- 配额查询失败采用 fail-open；本地路径验收失败不重新查询配额。
- 普通运行失败按 `max-attempts` 和队列规则处理，具体退避与优先级以 `runner.mjs` 和 `queue-store.mjs` 为准。

## 研究完成与进程退出

- 正式执行使用 SDK 事件流。收到成功的 `turn.completed` 后，最多等待 120 秒让进程退出；正常退出立即进入既有文件验收，不额外等待。
- 超出退出宽限后取消所属进程，并独立确认其退出，避免 SDK 已经不再返回时无限等待。只有主动取消产生的 `AbortError` 可作为收尾异常处理；真实研究错误继续走失败流程。
- 总研究超时由 `--timeout-minutes` 控制。到点仅补查一次本轮 thread 的持久会话；要求本轮唯一根 turn、会话最后一条记录是无错误的 `task_complete`，且有非空最终答复。仅有报告文件、带错误的完成记录，或完成后还有其他事件的会话，不自动恢复。
- 成功恢复仍须通过原有文件验收，使用同一条归档与 token 用量统计路径。文件验收不是研究内容质量评审。
- 取消后 10 秒仍无法确认进程退出时，保留输出和 `running` 状态，用现有 `note` 字段记录 `codex_cleanup_unconfirmed:`，停止领取新任务。下次启动也拒绝自动恢复该项，需先检查并清理对应进程再人工处理队列，防止重复写入。
- 子进程归属通过 Node 的 `child_process` diagnostics channel 与异步上下文关联，不修改 SDK 安装文件，不按进程名批量终止其他任务。

## 日志记录

- `logs/current.jsonl`：本次运行日志。
- 下次启动时，旧 current 日志移动到 `logs/archive/`。
- 保留数量和天数由代码控制；错误与普通事件写入同一 JSONL，并通过 `level` 区分。
- `runner.lock` 和 `prompt-debug/` 是运行辅助文件；旧 `runner.log` 只为历史引用保留。

当前模型、默认 sandbox、调度优先级、并发初值和日志保留策略均以实现代码为权威来源，避免在操作文档中复制易漂移常量。
