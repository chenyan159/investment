# Research Runner Dashboard

本目录是 `research-runner` 的独立 localhost UI。Dashboard 可以读取和有限控制 runner，但 runner 不引用、不启动、也不依赖本目录中的任何文件。

## 启动

双击：

```text
open-dashboard.cmd
```

启动器校验服务标识和研究主目录，避免误打开其他服务。端口被其他程序占用时明确报错，不停止已有进程。启动器会检查 `http://127.0.0.1:4319/api/health`，只在需要时隐藏启动 Dashboard Node 服务，然后使用 Windows 默认浏览器打开页面。关闭 Dashboard 不影响已经独立运行的 research runner；浏览器关闭且 15 分钟没有状态请求后，Dashboard 默认自动退出。

也可以直接运行：

```powershell
cd "D:\investment\tools\research-runner\dashboard"
npm start
```

环境变量：

- `RESEARCH_DASHBOARD_PORT`：本地端口，默认 `4319`。
- `RESEARCH_DASHBOARD_IDLE_MINUTES`：无页面请求后的自动退出分钟数，默认 `15`；设为 `0` 可禁用。

## 功能边界

- 只监听 `127.0.0.1`，不接受局域网连接。
- 普通状态每 5 秒刷新；quota 每 60 秒刷新并缓存。
- 运行中任务按最新优先完整列出，首屏显示 10 个并可向下滚动；完成列表展示最近 30 项并支持滚动，异常和路径问题保留最近 8 个。
- 页面保留队列统计，并在运行中及最近完成任务中显示任务绑定的研究方案版本；旧任务没有版本字段时显示“未记录”，不按当前方案猜测。
- 显示启动配置中的模型、默认推理强度和已安装 SDK 版本；运行中任务显示自己的推理强度。
- 并发默认值与 runner 共用配置，保留已有控制文件设置；额度暂停阈值与 runner 共用定义。
- ETA 只采用相同模型和推理强度的历史样本；样本不足时显示暂不可估算。Quota 显示实时剩余百分比，固定 token 额度换算未经当前模型校准时不预测完成时额度或触及阈值时间。
- 支持 queue validate、合并式 Runner 启停按钮、并发设置（含 `0`）和二次确认的强制停止。
- 不提供本地文件快捷操作，不直接编辑 queue 任务状态、attempt、优先级、重试或 stale 状态。
- 调度、优先级、重试、quota gate 和 stale recovery 始终由 runner 自己负责。

## 独立性

Dashboard 只依赖 runner 已存在的以下接口和文件：

- `runner.lock`
- `../queue.jsonl`
- `../queue.done.jsonl`
- `../queue.control.json`
- `logs/current.jsonl`
- `queue-store.mjs` 的并发控制写入
- `quota-control.mjs` 的 quota 查询
- `queue-tools.mjs validate`
- `runner.mjs` 的正式启动命令

所有 Dashboard 代码、页面、测试和启动器都保留在本目录。删除整个 `dashboard/` 不会改变 runner 的运行方式。

## 测试

```powershell
cd "D:\investment\tools\research-runner\dashboard"
npm test
```
