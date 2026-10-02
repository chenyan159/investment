# 审计复现说明

这些脚本是本次一次性审计的辅助文件，不是 research runner 的新流程，也不会入队、启动研究或修改正式研究方案。

- `inventory_workflows.py`：读取当前入口、队列及历史 file-run 提示路径，生成清单与 hash。
- `company_industry_inventory.py`、`company_industry_local_links.py`：复算公司/行业文件与本地链接清单。
- `decisions_current_audit.py`：复算192情景、192对比的结构、日期与双向冲突。
- `decisions_snapshot_live_check.mjs`：只读验证批次快照绑定；不运行模型。
- `audit_features.py`：解析19特征结果，重建16个收益特征的逐公司行与覆盖统计。
- `audit_sorting_current.py`：核对26排序入口，复用上一轮已冻结的行情数据，计算Top30等指标。
- `validate_audit_delivery.py`：验证审计正文的本地链接、非空引用行及已记录源文件的hash。

`write_*.py`、`build_feature_report.py`、`company_industry_write_audit.py`用于初稿生成；交付Markdown又经过人工与独立子审稿修订，不能把重新生成的初稿当作最终审阅版。数据计算可复现不等于文字生成器已经包含所有审阅修辞。重跑会覆盖本审计目录的同名中间产物，需先保留要比较的审计版本。

Python使用UTF-8模式执行：`python -X utf8 <脚本路径>`。当前源如已更新，重新审计会得到新的截面，不能据此反写本次2026-09-05时点的证据。只读核验不代表新研究方案已经运行或投资有效性已经得到验证。
