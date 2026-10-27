# Project Ananta 数据接口 v1

站点数据只由 `node etl/build-data.mjs` 生成。上游报告、结构化 JSON、索引和研究队列均只读；网站生成器不回写研究目录，也不调用研究 runner。

## 唯一数据来源

1. `分析报告/公司情景投资决策/结果/*.md`，以及同名 `结构化数据/*.json`。
2. `分析报告/公司对比/结果/*.md`，以及同名 `结构化数据/*.json`。
3. `基本面/产业背景/结果/*.md`。
4. `基本面/行业调研/结果/<分类>/*.md`，使用行业索引定位名称。
5. `基本面/公司调研/结果/<分类>/*.md`，使用公司索引确定股票代号、名称和分类。

不读取备份、临时目录、研究方案、金融行情、旧站点数据、排序或队列。所有解析、适配、验证、页面打包逻辑位于 `tools/site/`。

## 索引

`data/index.json`：

```text
{
  schemaVersion: 1,
  generatedAt: ISO 时间,
  meta: 元数据,
  companies: 公司摘要数组,
  research: 背景/行业/公司调研摘要数组
}
```

公司摘要：

```text
{
  ticker, name, sector, tags, industries: string[], notes, indexed: boolean,
  scenario: 情景摘要 | null,
  comparison: 对比摘要 | null,
  companyResearch: 调研摘要 | null,
  detailUrl: "data/companies/TICKER.json"
}
```

`indexed` 仅表示是否在当前公司索引登记，不表示投资评级或研究质量。保留正式结果中未登记公司的报告，不能把这些报告自动当成新投资对象。

情景摘要完整保留正式 JSON 的原始字段，并增加展示元数据：

```text
{
  ticker, research_date, information_cutoff,
  reference_price: {value, date, currency} | null,
  target_date,
  scenarios: {
    bear|base|bull|breakthrough: {
      dcf_price?: [number, number] | null,
      business_price: [number, number] | null,
      target_price: [number, number] | null,
      evidence: "strong"|"medium"|"weak"|"insufficient",
      review?: "adopt"|"revise"|"reestimate"
    }
  },
  title, summary, source, jsonSource,
  reportUrl, rawUrl,
  structuredAvailable: boolean,
  priceApplicable: boolean,
  priceNote
}
```

对比摘要额外原样保留：

- `views`：`near_term_delivery`、`long_term_compounding`、`base_valuation`、`upside_potential`、`downside_resilience`、`relative_attractiveness`，值为 `positive|mixed|negative`。
- `decision`：`steady_allocation` 为 `preferred_participate|conditional_wait|avoid`；`offense_allocation` 为 `high_priority_offense|small_option_bet|avoid`；`near_term_timing` 为 `build_now|wait_for_trigger|avoid`。
- `comparisons[]`：`peer`、`relation`、`compounding_preference`、`convexity_preference`、`verdict`、`reason`。
- `relation` 为 `direct_competitor|alternative|value_chain|opportunity_cost`。
- 两种 preference 为 `target_preferred|peer_preferred|comparable|both_avoid`，`verdict` 另允许 `split_by_mandate`。

正式 Markdown 存在但缺少同名 JSON 时，保留原文；`structuredAvailable=false`、`priceApplicable=false`、`rawUrl=null`、`reference_price=null`、`scenarios={}`，对比的 `views/decision={}`、`comparisons=[]`。不从文字猜数，不回退到同代码的旧 JSON。

## 详情与原文

`data/companies/TICKER.json` 包含公司摘要，`scenario` 和 `comparison` 扩展为：

```text
{ ...摘要, markdown: 完整正式报告, sections: [{id,title,level,markdown}], raw: 原始JSON | null }
```

`companyResearch` 扩展为完整调研详情。研究详情独立位于 `data/research/ID.json`，摘要为：

```text
{
  id, kind: "background"|"industry"|"company",
  title, subject, date, category, ticker: string|null,
  name, summary, scope, source, detailUrl, reportUrl
}
```

研究详情增加 `markdown`、`sections`。所有报告正文按需加载；首页不载入全量 Markdown。

- 原文下载：前端以详情里的完整 `markdown` 生成 Blob 下载；`reportUrl=null`，不重复打包一套 Markdown 文件。
- 原始 JSON 下载：`data/structured/scenario/TICKER.json`、`data/structured/comparison/TICKER.json`。
- Markdown 是研究内容，不是可信 HTML；前端渲染必须清理 HTML/URL，不能执行报告内的脚本或未授权外链操作。本地相对引用需映射到站内结果或作为文本呈现。

## 元数据和计算口径

`data/meta.json` 与 `index.meta` 相同，含 `schemaVersion`、`generatedAt`、`buildId`、`counts`、`dates`、`warnings`、`sources`、`conventions`。

- `counts.companies` 为展示公司身份数；`indexedCompanies` 为权威索引登记数。
- `scenarios` 为情景报告数；`pricedScenarios` 为有可用情景价格的报告数。
- `comparisonReports` 为对比全文数；`comparisons` 为有结构化 JSON 的对比数。
- `peerComparisons` 为各报告中定向比较关系总数；不表示去重后的无向公司对数。
- `companyResearch`、`industries`、`backgrounds` 为正式研究条目数。
- `dates` 的五个研究域各为 `{earliest,latest}`，按正式文件日期统计，不是实时行情日期。
- `generatedAt` 是网站构建时间，不能冒充报告研究时间。
- 价格累计回报 = `(目标价格 / 本报告参考价 - 1) × 100%`。
- 若显示年化价格回报，年数按参考报价日期至目标日期的实际天数除以 `365.25`；不包含股息，不将不同目标年的累计回报直接当可比年化回报。
- `null` 表示缺失或不适用，绝不替换为 `0`；证据等级不是概率，不进行加权期望目标价。
- 原公司情景和公司对比校准结果分开保留，不互相覆盖，不把各公司互相矛盾的单向比较合成为伪造总排名。

## 构建和完整性

生成器先在 `site/.build/` 建立 staging，通过数据校验后原子替换 `public/data/`；失败保留上一版。全部输入在 `data/source-manifest.json` 记录相对路径、字节数、SHA256。发布前再次读取所有输入核对 SHA256，若 runner 在构建期间改动报告则构建失败，需要重跑；不会锁定或暂停 runner。

Windows 文件监控程序可能临时占用输出目录；原子重命名会做有限重试。若开发服务的 watcher 持续导致 `EPERM`，先停止 `vite dev` 再重建。验收优先使用只读 `vite preview` 服务，不退回先删除现有产物的覆盖方式。

`node --test etl/*.test.mjs` 检查空值、区间、参考价、路径边界、重复身份、正文段落和缺 JSON 的版本选择。`node etl/validate-data.mjs` 校验全部输出 JSON、完整报告及下载文件一致性、计数、价格语义和允许来源。`node etl/sync-docs.mjs` 校验完整构建和 `CNAME=projectananta.com` 后替换 `docs/`，不更改 DNS。
