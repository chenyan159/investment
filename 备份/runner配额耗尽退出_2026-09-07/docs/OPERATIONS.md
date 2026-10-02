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

- 每个正式任务开始前查询 Codex 使用窗口；达到代码设定阈值时，任务返回 `retry_pending`，不消耗尝试次数。
- 配额查询失败采用 fail-open；本地路径验收失败不重新查询配额。
- 普通运行失败按 `max-attempts` 和队列规则处理，具体退避与优先级以 `runner.mjs` 和 `queue-store.mjs` 为准。

## 日志

- `logs/current.jsonl`：本次运行日志。
- 下次启动时，旧 current 日志移动到 `logs/archive/`。
- 保留数量和天数由代码控制；错误与普通事件写入同一 JSONL，并通过 `level` 区分。
- `runner.lock` 和 `prompt-debug/` 是运行辅助文件；旧 `runner.log` 只为历史引用保留。

当前模型、默认 sandbox、调度优先级、并发初值和日志保留策略均以实现代码为权威来源，避免在操作文档中复制易漂移常量。
