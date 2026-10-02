# Investment Research Site

本目录是 Project Ananta 的只读研究看板。站点把 Investment 内的公司、行业、排序、估值、特征和金融资料转换成静态 JSON 与页面，不在站点目录维护研究原文。

## 数据来源

ETL 主要读取：

- `基本面/公司调研/`
- `基本面/行业调研/`
- `分析报告/公司评估_淘汰/结果/`（只读历史展示）、`公司对比/`、`公司排序/`
- `基本面/特征量化/`
- `金融资料/`
- `技术面/站点数据/current.json`

公司横评是一个明确例外：站点不再直接解析 `公司对比/结果/` 下的研究 Markdown，而只读取
`分析报告/公司对比/站点数据/`。该目录由同级 `生成站点数据.mjs` 从正式结果生成，
包含一个全局索引和按 Ticker 拆分的明细文件；研究格式变化只需维护这一处转换。

公司情景投资决策沿用同一单向兼容边界：

2026-09-01 起，经营评估已合并进公司情景投资决策；站点仍可展示旧公司评估，但会明确标记为淘汰历史资料，不能把它当作当前正式判断。

- 研究侧生成器：`分析报告/公司情景投资决策/生成站点数据.mjs`。
- 研究侧稳定契约：`分析报告/公司情景投资决策/站点数据/current.json` 和 `companies/<Ticker>.json`。
- Site 唯一输入：上述 `站点数据/`，不直接扫描 `结果/`、`备份/`、研究方案或上游公司/行业资料。

生成器负责把四种经营情景、五种市场状态、当前纯格子、必要的复合定位、板块修正、估值区间和完整 Markdown 收敛成稳定字段；Site ETL 只做公司覆盖、4×5矩阵、明细身份和契约版本校验。依赖方向固定为 `正式研究结果 → 公司情景投资决策站点数据 → Site ETL → public/data/scenario-decisions.json`。研究报告格式变化只影响研究侧生成器，页面布局变化不反向影响研究目录。

具体文件匹配、排序方案和字段口径以 `etl/build-data.mjs` 为准，不在 README 复制动态清单。

公司排序采用与公司横评相同的“研究侧生成、站点侧消费”边界：

- 研究侧入口：`00_运行与榜单注册表.csv`、`00_当前评估.json`和`00_站点发布策略.csv`。
- 研究侧生成器：`分析报告/公司排序/生成站点数据.mjs`。
- Site唯一输入：`分析报告/公司排序/站点数据/current.json`。

站点不扫描公司排序目录、不解析原始CSV、不跟随旧兼容junction，也不在前端维护公开名单。研究侧生成器负责筛除退出、明显反向和证据不足的方案，并把生成后证据与生成前历史回看分开整理；站点只校验公开方法数、榜单数、每榜名次和公司覆盖。新产物不符合契约时，该模块保留并使用上一版有效数据。

技术面也采用相同的单向兼容边界，但保持为一个文件：

- 技术面发布摘要：`技术面/站点发布.json`。
- 技术面生成器：`技术面/生成站点数据.mjs`，自动选择 `MF001–MF018` 每个编号的最新正式报告并嵌入完整 Markdown。
- Site 唯一输入：`技术面/站点数据/current.json`。

`tools/site` 不扫描 `技术面/因子研究/`，也不依赖研究方案、原始数据或脚本。依赖方向固定为 `技术面研究 → 技术面 current.json → Site ETL → public/data/technical-research.json`；报告结构变化只影响技术面生成器，页面字段变化只通过稳定契约进入站点。

## 目录

- `src/`：React 看板界面。
- `etl/`：读取上游研究并生成站点数据。
- `public/data/`：本地构建使用的生成数据，不手工编辑。
- `docs/`：GitHub Pages 发布包，由构建命令生成，不手工编辑。
- `dist/`：临时 Vite 构建输出。

## 构建与检查

```powershell
cd "D:\investment\tools\site"
npm install
npm run pages:prepare
Get-Content public\data\meta.json
```

`pages:prepare` 会独立生成公司对比、情景决策、公司排序、技术面和每日新闻五个模块，再运行核心 ETL、Vite 构建并刷新 `docs/`。

每个模块只写自己的 staging 目录。新产物通过同一套站点消费契约后才原子替换当前 `站点数据`；生成或校验失败时，当前有效产物保持不变，该模块在 `meta.json` 的 `moduleBuilds` 中标记为 `stale`，其他模块继续更新。只有模块既生成失败又没有有效上一版，或者核心 ETL / Vite 无法形成完整可解析站点时，整次构建才失败。

单独调试模块可使用 `npm run build:company-comparisons`、`build:scenario-decisions`、`build:rankings`、`build:technical-research` 或 `build:daily-news`；这些入口同样经过 staging、契约校验和回退。模块隔离测试使用 `npm run test:modules`。

本地预览：

```powershell
npm run preview
```

默认预览地址为 `http://127.0.0.1:8080/`。

## 公开边界

GitHub Pages 和对应仓库是公开的。ETL 读取的报告正文、相对来源路径、排序和生成 JSON 都可能公开；不得在上游研究目录放入会被 ETL 读取的凭据、账户数据或私人笔记。

发布方式、域名和 DNS 维护见 [DEPLOYMENT.md](DEPLOYMENT.md)。
