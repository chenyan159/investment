# Project Ananta

以公司情景与公司对比为核心的静态研究工作台。线上入口为 https://projectananta.com/ 。网站解释和展示已有研究，不生成投资研究、不执行队列、不修改正式报告。

## 五个只读来源

| 来源 | 网站用途 |
| --- | --- |
| 分析报告/公司情景投资决策/结果、结构化数据 | 四种经营情景、DCF／纯业务／目标交易价、证据与报告全文 |
| 分析报告/公司对比/结果、结构化数据 | 情景复核、六项判断、三项配置决策、逐家公司双视角比较及报告全文 |
| 基本面/产业背景/结果 | 上游产业背景摘要与原文 |
| 基本面/行业调研/结果 | 行业研究摘要与原文 |
| 基本面/公司调研/结果 | 公司事实底稿摘要与原文 |

公司和行业索引仅用于名称、分类和定位。当前正式结果为唯一研究输入；历史备份、研究方案、临时材料、其他研究域均不进入网站。价格是报告注明日期的参考价，不是实时行情；派生回报使用同一公司、同一报告的参考价和目标日。不同币种不直接比较绝对股价，证据强度不转换为概率。

## 模块和边界

- `etl/`：独立读取与校验五个来源，只写站点内生成数据。原研究目录不再保留网站专用生成器和站点副本。
- `src/`：React 交互界面、SVG 可视化、全文阅读和筛选。公司详情与研究正文按需加载。
- `public/data/`：完整生成的静态接口，不手工编辑；结构见 `data-contract.md`。
- `dist/`：Vite 临时构建；`docs/`：GitHub Pages 发布包。
- `qa/`：发布包与线上内容的只读验证。

网站不导入 research-runner，不读取或修改运行锁、队列与研究执行配置。网站构建可以单独运行，来源不存在或不合规时应报错，不能把旧站点数据当作新研究。

## 本地运行

使用 Node.js 22 或更新版本，在本目录执行：

```powershell
npm ci
npm run build:data
npm run dev
```

开发预览为 http://127.0.0.1:5173 。首次需要生成数据；后续修改界面无须重复读取研究。

## 验证与构建

```powershell
npm test
npm run pages:prepare
npm run validate:data
npm run verify:publish
```

pages:prepare 顺序执行数据构建、Vite 构建与发布包同步。生成数据包含来源、报告日期和覆盖信息；仅数据重新生成，不向上游回写。

## 发布

保持现有双仓库职责：网站源码由 chenyan159/investment 根仓库跟踪，tools/site 内独立的 chenyan159/projectananta-research 仅跟踪 docs/。本机 .git 指针不属于源码。具体发布与回滚见 [DEPLOYMENT.md](DEPLOYMENT.md)。

域名与 Cloudflare DNS 保持不变，托管为 GitHub Pages；不使用 Tunnel、Access、Workers 或 R2。
