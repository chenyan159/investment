# 产业背景目录说明

本目录保存行业调研的上游研究：横向背景专题和会议调研。

- `研究方案/<专题>/`：各专题的现行方案和历史版本，说明见 `研究方案/README.md`。
- `结果/`：只放最新报告，不建子目录。背景专题命名 `<专题>_YYYY-MM-DD.md`；会议命名 `会议调研_<会议系列>_<年份>_YYYY-MM-DD.md`，同一会议系列只保留最新一届。
- `备份/`：被新版替代的报告，runner 重跑前自动移入。`迁移前_2026-10-10/` 存放迁移前的旧版本和 `旧路径映射.csv`。
- `tmp/`：执行中的临时文件，可删除。

## 运行

用 research runner 的 background 任务，从项目根目录：

- 背景专题：`node tools/research-runner/queue-tools.mjs add-background --subject=<专题名>`
- 会议：`node tools/research-runner/queue-tools.mjs add-background --subject="<会议系列> <年份>"`，例如 `--subject="OCP Global Summit 2026"`
- `node tools/research-runner/queue-tools.mjs list-background` 列出现有专题和会议系列。新一届会议沿用已有系列名，才能把上一届移入备份。

## 读取边界

- 下游的行业调研、公司调研和公司对比只读取 `结果/`，不读取 `备份/`、`tmp/` 和 `研究方案/`。
- 各专题研究独立联网完成，不读取本目录或项目内其他研究成果作为输入。
