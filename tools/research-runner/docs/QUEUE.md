# Research Runner Queue

## 队列文件

- `../queue.jsonl`：活动任务，包括 `pending`、`running`、`retry_pending`、`failed` 和尚未归档的 `done`。
- `../queue.done.jsonl`：已完成任务归档。
- `../queue.control.json`：当前目标并发数。
- `../queue-backups/`：历史快照和隔离实验，不被正式 runner 默认读取。

每行是一个独立 JSON 对象。常用字段包括：

```json
{"id":"company-CEG-1","domain":"company","sourceDate":"2026-05-11","subject":"CEG","displayName":"Constellation Energy","category":"电力_发电_能源_储能","status":"pending","attempts":0,"reasoningEffort":"max"}
```

支持的状态：`pending`、`running`、`retry_pending`、`done`、`failed`。

公司情景投资决策、公司对比的完成记录以 `outputFile` 保存 MD 路径、`companionFile` 保存同名 JSON 路径；领取、失败、配额延期和中断恢复时清空产物记录。两个 domain 固定双输出，不设任务开关；同一 domain 的同一输出主题不并发领取。

`reasoningEffort` 支持 `low`、`medium`、`high`、`xhigh`、`max` 和 `ultra`，缺省值为 `max`。完成记录包含累计 token 使用量和线程汇总；旧归档可能仍包含历史 `verification` 字段。

## 查看和校验

```powershell
npm run queue:status
npm run queue:validate
npm run queue:archive-done
```

`queue:validate` 只校验活动队列。完成归档中的旧 `outputFile` 和 `promptFile` 是完成时记录，不适用当前队列契约校验。

## 添加任务

```powershell
npm run queue:add-company -- --ticker=CEG
npm run queue:add-company-comparison -- --ticker=MU
npm run queue:add-company-investment-decision -- --ticker=VST
npm run queue:add-company-sentiment -- --ticker=MRVL
npm run queue:add-industry -- --subject="数据中心直液冷系统"
npm run queue:add-background -- --subject="数据中心建设规模"
npm run queue:add-background -- --subject="OCP Global Summit 2026"
npm run queue:list-background
npm run queue:add-feature-quantization -- --subject="N01_AI可归因盈利暴露_研究方案"
npm run queue:add-file-run -- --run-id="example" --prompt-file="分析报告/tmp/运行方案.md"
```

所有 add 和 seed 命令都接受 `--reasoning=LEVEL` 或 `--reasoning-effort=LEVEL`。


新增公司或行业索引项：

```powershell
npm run queue:add-company -- --ticker=XYZ --display-name="Company Name" --category="AI计算芯片_EDA_IP_custom_ASIC" --update-index
npm run queue:add-industry -- --subject="新行业名称" --category="AI园区电力_机电_冷却" --update-index
```

## 批量播种

```powershell
npm run queue:seed-industry-from-index -- --dry-run
npm run queue:seed-industry-from-index
npm run queue:seed-feature-quantization-from-plans -- --dry-run
npm run queue:seed-feature-quantization-from-plans
```

公司 Markdown 队列迁移命令只用于历史恢复：

```powershell
npm run queue:migrate-company-md
```

## 11类研究方案版本

映射见[research-plans.json](../research-plans.json)。每个方案目录根部恰好保留一个研究方案_yyyymmdd_hhmmss.md，同名全文归档于yyyymmdd_hhmmss子目录。README及修改记录不进入研究提示。

专用domain照常入队。产业背景专题与会议用 `background` domain 入队；旧的 file-run 入口仍可把--prompt-file设为注册目录、具体版本文件或迁移前路径（兼容映射到现行版），输出同样只能进入 `基本面/产业背景/结果/`，但不做同主题备份。其他file-run保持原有行为。入队绑定planId、planVersion、planEntryFile、planSnapshotFile、planSha256和planBoundAt；启动补齐未绑定活动任务并记录日志。实际运行记录actualPromptFile与actualPromptSha256，完成归档及以后队列备份保留字段，旧归档不回填。

更新方案：从项目根目录运行`node tools/research-runner/research-plan-tools.mjs publish --plan-id=company --source=<完整新方案> --reason=<修改原因>`。命令创建版本子目录的两个文件并替换根目录现行副本，后续手动追加修改内容与效果。
