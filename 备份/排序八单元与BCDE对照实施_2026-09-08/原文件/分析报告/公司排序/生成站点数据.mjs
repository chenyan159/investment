import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(ROOT, "..", "..");
const REGISTRY_FILE = path.join(ROOT, "00_运行与榜单注册表.csv");
const POLICY_FILE = path.join(ROOT, "00_站点发布策略.csv");
const EVALUATION_POINTER_FILE = path.join(ROOT, "00_当前评估.json");
const COMPANY_INDEX_FILE = path.join(PROJECT_ROOT, "基本面", "公司调研", "公司索引.md");
const DEFAULT_OUTPUT_ROOT = path.join(ROOT, "站点数据");
const OUTPUT_ROOT = process.env.PROJECT_ANANTA_OUTPUT_ROOT?.trim()
  ? path.resolve(process.env.PROJECT_ANANTA_OUTPUT_ROOT)
  : DEFAULT_OUTPUT_ROOT;
const OUTPUT_FILE = path.join(OUTPUT_ROOT, "current.json");

const EXPECTED_COMPANY_COUNT = 192;
const EXPECTED_METHOD_COUNT = 26;
const EXPECTED_LIST_COUNT = 28;
const TICKER_ALIASES = new Map([["PSTG", "P"]]);

async function main() {
  const [registryText, policyText, evaluationText, companyIndexText] = await Promise.all([
    fs.readFile(REGISTRY_FILE, "utf8"),
    fs.readFile(POLICY_FILE, "utf8"),
    fs.readFile(EVALUATION_POINTER_FILE, "utf8"),
    fs.readFile(COMPANY_INDEX_FILE, "utf8"),
  ]);
  const registry = parseCsv(registryText)
    .filter((row) => asBoolean(row.is_current))
    .sort((a, b) => number(a.display_order) - number(b.display_order));
  const policies = parseCsv(policyText).sort((a, b) => number(a.display_order) - number(b.display_order));
  const evaluation = JSON.parse(evaluationText.replace(/^\uFEFF/, ""));
  const companies = parseCompanyIndex(companyIndexText);

  validateAuthority(registry, policies, evaluation, companies);

  const sourceFiles = {
    normalized: resolveRootSource(evaluation.normalized_rankings_path),
    listMetrics: resolveRootSource(evaluation.list_metrics_path),
    methodMetrics: resolveRootSource(evaluation.method_metrics_path),
    priceReturns: resolveRootSource(evaluation.price_returns_path),
    inputComparisons: resolveRootSource(evaluation.input_comparisons_path),
    report: resolveRootSource(evaluation.report_path),
  };
  const sourceTexts = await Promise.all([
    fs.readFile(sourceFiles.normalized, "utf8"),
    fs.readFile(sourceFiles.listMetrics, "utf8"),
    fs.readFile(sourceFiles.methodMetrics, "utf8"),
    fs.readFile(sourceFiles.priceReturns, "utf8"),
    fs.readFile(sourceFiles.inputComparisons, "utf8"),
  ]);
  const [normalizedRows, listMetricRows, methodMetricRows, priceRows, inputComparisonRows] = sourceTexts.map(parseCsv);

  const policyByMethod = new Map(policies.map((row) => [row.method_id, row]));
  const registryByMethod = groupRows(registry, "method_id");
  const normalizedByList = groupRows(normalizedRows, "list_id");
  const listMetricsById = new Map(listMetricRows.map((row) => [row.list_id, row]));
  const methodMetricsById = new Map(methodMetricRows.map((row) => [row.method_id, row]));
  const priceByTicker = new Map(priceRows.map((row) => [canonicalTicker(row.ticker), row]));
  const companyByTicker = new Map(companies.map((row) => [row.ticker, row]));
  const publishedPolicies = policies.filter((row) => asBoolean(row.site_publish));
  const publishedMethodIds = new Set(publishedPolicies.map((row) => row.method_id));
  const publishedRegistry = registry.filter((row) => publishedMethodIds.has(row.method_id));

  const historyTexts = new Map();
  const effectivenessMethods = [];
  for (const policy of publishedPolicies) {
    const methodRows = registryByMethod.get(policy.method_id) || [];
    const first = methodRows[0];
    const historyFile = path.join(resolveRootSource(first.method_path), "效果评估", "效果历史.csv");
    const historyText = await fs.readFile(historyFile, "utf8");
    historyTexts.set(policy.method_id, historyText);
    const history = parseCsv(historyText);
    const strictPostRows = history
      .filter((row) => row.evidence_type.startsWith("生成后样本外"))
      .map(normalizePostGenerationRow);
    const currentRunIds = new Set(methodRows.map((row) => row.run_id));
    const exactCurrentRows = strictPostRows.filter((row) => currentRunIds.has(row.runId));
    const historicalMetrics = normalizeCurrentRankingMetrics(methodMetricsById.get(policy.method_id));
    if (!Number.isFinite(historicalMetrics.rankIc3m) || !Number.isFinite(historicalMetrics.rankIc6m)) {
      throw new Error(`缺少 ${policy.method_id} 的当前3个月或6个月评估指标`);
    }
    effectivenessMethods.push({
      methodId: policy.method_id,
      label: first.method_name,
      group: policy.site_group,
      evidenceLabel: policy.evidence_label,
      publishReason: policy.reason,
      lifecycle: first.lifecycle,
      status: first.status,
      role: first.role,
      currentRunId: first.run_id,
      currentRunDate: first.run_date,
      listIds: methodRows.map((row) => row.list_id),
      consensusEligible: asBoolean(policy.consensus_eligible),
      postGeneration: {
        relationToCurrentRun: exactCurrentRows.length
          ? "当前运行已有严格生成后样本"
          : strictPostRows.length
            ? "证据来自同方法家族前身版本；当前运行尚无严格生成后样本"
            : "当前运行及前身均无严格生成后样本",
        exactCurrentRunCheckCount: exactCurrentRows.length,
        familyPredecessorCheckCount: strictPostRows.length - exactCurrentRows.length,
        checkCount: strictPostRows.length,
        positiveCheckCount: strictPostRows.filter(
          (row) => Number.isFinite(row.rankIc) && row.rankIc > 0 && Number.isFinite(row.topUniverseExcessPct) && row.topUniverseExcessPct > 0,
        ).length,
        medianRankIc: median(strictPostRows.map((row) => row.rankIc)),
        medianTopUniverseExcessPct: median(strictPostRows.map((row) => row.topUniverseExcessPct)),
        medianTopBottomSpreadPct: median(strictPostRows.map((row) => row.topBottomSpreadPct)),
        minHoldingDays: finiteMin(strictPostRows.map((row) => row.holdingDays)),
        maxHoldingDays: finiteMax(strictPostRows.map((row) => row.holdingDays)),
        rows: strictPostRows,
      },
      historicalLookback: {
        evidenceType: evaluation.evidence_type,
        priceAsOf: evaluation.price_as_of,
        exactCurrentRun: true,
        metrics: historicalMetrics,
      },
    });
  }

  const { runs, order } = await buildPublishedRuns({
    publishedPolicies,
    registryByMethod,
    normalizedByList,
    listMetricsById,
    companyByTicker,
    evaluation,
    sourceFiles,
  });
  const defaultPolicies = publishedPolicies.filter((row) => asBoolean(row.site_default));
  if (defaultPolicies.length !== 1) throw new Error(`站点默认方法必须恰好一个，实际 ${defaultPolicies.length}`);
  const defaultRunKey = (registryByMethod.get(defaultPolicies[0].method_id) || [])[0]?.list_id;
  if (!defaultRunKey || !runs[defaultRunKey]) throw new Error("站点默认榜单未发布");

  const consensusMethodIds = new Set(
    publishedPolicies.filter((row) => asBoolean(row.consensus_eligible)).map((row) => row.method_id),
  );
  const consensus = buildConsensus({
    consensusMethodIds,
    registryByMethod,
    normalizedByList,
    companyByTicker,
    priceByTicker,
  });
  const publishedMethodSet = new Set(publishedPolicies.map((row) => row.method_id));
  const inputComparisons = inputComparisonRows
    .filter((row) => publishedMethodSet.has(row.base) && publishedMethodSet.has(row.extended))
    .map((row) => ({
      base: row.base,
      extended: row.extended,
      rankSimilarity: numberOrNull(row.spearman_rank_similarity),
      top10Overlap: numberOrNull(row.top10_overlap),
      top20Overlap: numberOrNull(row.top20_overlap),
      meanAbsoluteRankChange: numberOrNull(row.mean_abs_rank_change),
    }));

  const publishedMethodMetrics = effectivenessMethods.map((method) => ({
    methodId: method.methodId,
    label: method.label,
    lifecycle: method.lifecycle,
    status: method.status,
    group: method.group,
    evidenceLabel: method.evidenceLabel,
    ...method.historicalLookback.metrics,
  }));
  const topMethods = (field) =>
    [...publishedMethodMetrics]
      .filter((row) => Number.isFinite(row[field]))
      .sort((a, b) => b[field] - a[field])
      .slice(0, 5);
  const groupCounts = Object.fromEntries(
    [...new Set(publishedPolicies.map((row) => row.site_group))].map((group) => [
      group,
      publishedPolicies.filter((row) => row.site_group === group).length,
    ]),
  );
  const strictPostMethodCount = effectivenessMethods.filter((row) => row.postGeneration.checkCount > 0).length;
  const exactCurrentPostMethodCount = effectivenessMethods.filter(
    (row) => row.postGeneration.exactCurrentRunCheckCount > 0,
  ).length;

  const payload = {
    schemaVersion: 3,
    source: "companySortingSiteData",
    generatedAt: new Date().toISOString(),
    sourceHash: hashText(
      [registryText, policyText, evaluationText, companyIndexText, ...sourceTexts, ...historyTexts.values()].join("\n"),
    ).slice(0, 16),
    sourceRoot: "分析报告/公司排序",
    contract: {
      registryPath: relativeProject(REGISTRY_FILE),
      publicationPolicyPath: relativeProject(POLICY_FILE),
      evaluationPointerPath: relativeProject(EVALUATION_POINTER_FILE),
      generatorPath: relativeProject(__filename),
      siteInputPath: relativeProject(OUTPUT_FILE),
      dependencyRule: "研究目录生成一个current.json；Site只校验并消费该文件，不扫描研究目录、不解释CSV。",
    },
    publicationPolicy: {
      registeredMethodCount: new Set(registry.map((row) => row.method_id)).size,
      registeredListCount: registry.length,
      publishedMethodCount: publishedPolicies.length,
      publishedListCount: publishedRegistry.length,
      excludedMethodCount: policies.length - publishedPolicies.length,
      excludedListCount: registry.length - publishedRegistry.length,
      consensusMethodCount: consensusMethodIds.size,
      strictPostEvidenceMethodCount: strictPostMethodCount,
      exactCurrentRunPostEvidenceMethodCount: exactCurrentPostMethodCount,
      groups: groupCounts,
      criteria: [
        "退出方案、明显反向方案和缺乏区分力的冻结或候选方案不发布公司榜。",
        "前身版本短窗生成后证据与当前版本生成前历史回看分开展示，不合成为一个分数。",
        "只有仍在投票的独立方法家族进入站点共识；06三视图只计算一个家族。",
      ],
    },
    defaultRunKey,
    order,
    runs,
    effectiveness: {
      definitions: {
        postGeneration: "排序生成后才发生的未见价格窗口；当前可用窗口仅14至32个交易日，多数证据来自同方法家族前身版本。",
        historicalLookback: "当前排名生成以前已经发生的3个月和6个月价格回看，只能检查逻辑同向性，不能证明未来预测能力。",
        currentRunStatus: exactCurrentPostMethodCount
          ? `${exactCurrentPostMethodCount}个发布方法已有当前运行生成后样本。`
          : "所有2026-07-13当前运行都尚无严格生成后样本。",
      },
      methods: effectivenessMethods,
    },
    currentEvaluation: {
      id: evaluation.evaluation_id,
      title: evaluation.title,
      evidenceType: evaluation.evidence_type,
      generatedAt: evaluation.generated_at,
      priceAsOf: evaluation.price_as_of,
      reportPath: relativeProject(sourceFiles.report),
      coverage: {
        methodCount: publishedPolicies.length,
        listCount: publishedRegistry.length,
        registeredMethodCount: Number(evaluation.method_count),
        registeredListCount: Number(evaluation.list_count),
        rankedCompanyCount: Number(evaluation.ranked_company_count),
        pricedCompanyCount: Number(evaluation.priced_company_count),
        strictPostEvidenceMethodCount: strictPostMethodCount,
        exactCurrentRunPostEvidenceMethodCount: exactCurrentPostMethodCount,
        consensusMethodCount: consensusMethodIds.size,
      },
      topMethods3m: topMethods("rankIc3m"),
      topMethods6m: topMethods("rankIc6m"),
      methodMetrics: publishedMethodMetrics,
      consensus: consensus.slice(0, 20),
      inputComparisons,
      caveats: [
        "当前版本的3个月和6个月结果全部发生在排名生成前，属于历史回看，不是样本外验证。",
        "严格生成后证据最长32个交易日、最新14个交易日，且多数对应前身版本，统计力度很低。",
        `${evaluation.priced_company_count}/${evaluation.ranked_company_count}家公司有完整3个月和6个月价格历史。`,
        "页面只公开值得继续跟踪的方法；未公开方案仍完整保留在研究目录。",
      ],
    },
    validation: {
      methodCount: publishedPolicies.length,
      listCount: publishedRegistry.length,
      expectedMethodCount: publishedPolicies.length,
      expectedListCount: publishedRegistry.length,
      expectedRowsPerList: EXPECTED_COMPANY_COUNT,
      registeredMethodCount: EXPECTED_METHOD_COUNT,
      registeredListCount: EXPECTED_LIST_COUNT,
      complete: true,
    },
  };

  assertOutputRoot();
  await fs.mkdir(OUTPUT_ROOT, { recursive: true });
  await fs.writeFile(OUTPUT_FILE, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(
    `Company sorting site data: ${payload.validation.methodCount} published methods, ${payload.validation.listCount} lists, ${EXPECTED_COMPANY_COUNT} companies each.`,
  );
  console.log(
    `Evidence: ${strictPostMethodCount} methods with family post-generation checks; ${exactCurrentPostMethodCount} with exact-current-run checks.`,
  );
  console.log(`Wrote ${OUTPUT_FILE}`);
}

async function buildPublishedRuns({
  publishedPolicies,
  registryByMethod,
  normalizedByList,
  listMetricsById,
  companyByTicker,
  evaluation,
  sourceFiles,
}) {
  const runs = {};
  const order = [];
  for (const policy of publishedPolicies) {
    const methodRows = (registryByMethod.get(policy.method_id) || []).sort(
      (a, b) => number(a.display_order) - number(b.display_order),
    );
    for (const registry of methodRows) {
      const methodDir = resolveRootSource(registry.method_path);
      const planFile = resolveRootSource(registry.plan_path);
      const resultFile = resolveRootSource(registry.result_path);
      await Promise.all([fs.access(methodDir), fs.access(planFile), fs.access(resultFile)]);
      if (path.basename(planFile) !== "01_研究方案.md" || path.basename(resultFile) !== "02_排序结果.md") {
        throw new Error(`${registry.list_id} 没有绑定标准研究方案和结果文件`);
      }
      const rawRows = normalizedByList.get(registry.list_id) || [];
      const expectedRows = number(registry.expected_row_count);
      const ranks = new Set(rawRows.map((row) => number(row.rank)));
      const tickers = new Set(rawRows.map((row) => canonicalTicker(row.ticker)));
      const missingTickers = [...companyByTicker.keys()].filter((ticker) => !tickers.has(ticker));
      if (
        rawRows.length !== expectedRows ||
        ranks.size !== expectedRows ||
        tickers.size !== expectedRows ||
        missingTickers.length
      ) {
        throw new Error(
          `${registry.list_id} 榜单无效：rows=${rawRows.length}, ranks=${ranks.size}, tickers=${tickers.size}, missing=${missingTickers.length}`,
        );
      }
      const rows = rawRows
        .map((row) => {
          const ticker = canonicalTicker(row.ticker);
          const company = companyByTicker.get(ticker);
          return {
            rank: number(row.rank),
            ticker,
            name: company.name,
            category: company.category,
            score: cleanCell(row.score),
          };
        })
        .sort((a, b) => a.rank - b.rank);
      const listMetric = listMetricsById.get(registry.list_id);
      if (!listMetric) throw new Error(`缺少 ${registry.list_id} 当前评估指标`);
      const iterationCount = (await safeReadDirents(path.join(methodDir, "迭代版本"))).filter((item) => item.isDirectory()).length;
      const label = registry.method_id === "06" ? `${registry.method_name} · ${registry.list_name}` : registry.list_name;
      runs[registry.list_id] = {
        key: registry.list_id,
        methodId: registry.method_id,
        listId: registry.list_id,
        label,
        methodName: registry.method_name,
        listName: registry.list_name,
        siteGroup: policy.site_group,
        evidenceLabel: policy.evidence_label,
        publishReason: policy.reason,
        strategy: registry.lifecycle,
        lifecycle: registry.lifecycle,
        status: registry.status,
        useCase: registry.role,
        caution: `${evaluation.evidence_type}；当前运行尚不能据此证明生成后有效性。`,
        runId: registry.run_id,
        date: registry.run_date,
        sourcePath: relativeProject(resultFile),
        planPath: relativeProject(planFile),
        folderPath: relativeProject(methodDir),
        evaluationPath: relativeProject(sourceFiles.report),
        iterationCount,
        metrics: normalizeCurrentRankingMetrics(listMetric),
        rowCount: rows.length,
        rows,
      };
      order.push(registry.list_id);
    }
  }
  return { runs, order };
}

function buildConsensus({ consensusMethodIds, registryByMethod, normalizedByList, companyByTicker, priceByTicker }) {
  const methodRanks = new Map();
  for (const methodId of consensusMethodIds) {
    const lists = registryByMethod.get(methodId) || [];
    const tickerRankArrays = new Map();
    for (const list of lists) {
      for (const row of normalizedByList.get(list.list_id) || []) {
        const ticker = canonicalTicker(row.ticker);
        if (!tickerRankArrays.has(ticker)) tickerRankArrays.set(ticker, []);
        tickerRankArrays.get(ticker).push(number(row.rank));
      }
    }
    const averages = [...tickerRankArrays.entries()]
      .map(([ticker, ranks]) => ({ ticker, value: mean(ranks) }))
      .sort((a, b) => a.value - b.value || a.ticker.localeCompare(b.ticker));
    methodRanks.set(methodId, new Map(averages.map((row, index) => [row.ticker, index + 1])));
  }

  return [...companyByTicker.values()]
    .map((company) => {
      const ranks = [...consensusMethodIds].map((methodId) => methodRanks.get(methodId)?.get(company.ticker)).filter(Number.isFinite);
      const price = priceByTicker.get(company.ticker) || {};
      return {
        ticker: company.ticker,
        name: company.name,
        category: company.category,
        meanRank: round(mean(ranks), 2),
        top20Count: ranks.filter((rank) => rank <= 20).length,
        methodCount: ranks.length,
        bestRank: Math.min(...ranks),
        worstRank: Math.max(...ranks),
        return3m: numberOrNull(price.ret_3m),
        return6m: numberOrNull(price.ret_6m),
      };
    })
    .sort((a, b) => a.meanRank - b.meanRank || b.top20Count - a.top20Count || a.ticker.localeCompare(b.ticker));
}

function validateAuthority(registry, policies, evaluation, companies) {
  if (Number(evaluation.schema_version) !== 1) throw new Error("不支持的当前评估指针版本");
  if (registry.length !== EXPECTED_LIST_COUNT) throw new Error(`当前注册表应有${EXPECTED_LIST_COUNT}张榜，实际${registry.length}`);
  const methodIds = new Set(registry.map((row) => row.method_id));
  const listIds = new Set(registry.map((row) => row.list_id));
  if (methodIds.size !== EXPECTED_METHOD_COUNT || listIds.size !== EXPECTED_LIST_COUNT) {
    throw new Error(`当前注册表方法/榜单数异常：${methodIds.size}/${listIds.size}`);
  }
  if (Number(evaluation.method_count) !== EXPECTED_METHOD_COUNT || Number(evaluation.list_count) !== EXPECTED_LIST_COUNT) {
    throw new Error("当前评估指针与注册表总量不一致");
  }
  if (companies.length !== EXPECTED_COMPANY_COUNT) throw new Error(`公司索引应有${EXPECTED_COMPANY_COUNT}家，实际${companies.length}`);
  if (policies.length !== EXPECTED_METHOD_COUNT || new Set(policies.map((row) => row.method_id)).size !== EXPECTED_METHOD_COUNT) {
    throw new Error(`发布策略必须覆盖${EXPECTED_METHOD_COUNT}个方法且不得重复`);
  }
  const missingPolicy = [...methodIds].filter((methodId) => !policies.some((row) => row.method_id === methodId));
  const extraPolicy = policies.filter((row) => !methodIds.has(row.method_id)).map((row) => row.method_id);
  if (missingPolicy.length || extraPolicy.length) {
    throw new Error(`发布策略与注册表不一致：missing=${missingPolicy.join(",")}, extra=${extraPolicy.join(",")}`);
  }
  if (policies.some((row) => Number(row.schema_version) !== 1)) throw new Error("不支持的发布策略版本");
}

function assertOutputRoot() {
  const resolved = path.resolve(OUTPUT_ROOT);
  const expected = path.resolve(DEFAULT_OUTPUT_ROOT);
  const isStaging = path.basename(resolved).startsWith(".站点数据-");
  if (path.dirname(resolved) !== path.resolve(ROOT) || (resolved !== expected && !isStaging)) {
    throw new Error(`拒绝写入非预期目录：${resolved}`);
  }
}

function normalizePostGenerationRow(row) {
  return {
    sourceSchemeId: cleanCell(row.source_scheme_id),
    runRole: cleanCell(row.run_role),
    runId: cleanCell(row.run_id),
    rankingGeneratedDate: cleanCell(row.ranking_generated_date),
    evaluationStart: cleanCell(row.evaluation_start),
    evaluationEnd: cleanCell(row.evaluation_end),
    holdingDays: numberOrNull(row.holding_days),
    rankedCount: numberOrNull(row.ranked_count),
    validCount: numberOrNull(row.valid_count),
    topBucketN: numberOrNull(row.top_bucket_n),
    bottomBucketN: numberOrNull(row.bottom_bucket_n),
    topBucketReturnPct: numberOrNull(row.top_bucket_return_pct),
    universeReturnPct: numberOrNull(row.universe_return_pct),
    topUniverseExcessPct: numberOrNull(row.top_universe_excess_pct),
    topBottomSpreadPct: numberOrNull(row.top_bottom_spread_pct),
    rankIc: numberOrNull(row.spearman_rank_ic),
    categoryNeutralRankIc: numberOrNull(row.category_neutral_rank_ic),
    maxDrawdownPct: numberOrNull(row.top_bucket_max_drawdown_pct),
    sourcePath: cleanCell(row.source),
  };
}

function normalizeCurrentRankingMetrics(row = {}) {
  const metric = (field) => numberOrNull(row[field]);
  return {
    rankedCount: metric("ranked_n"),
    validCount3m: metric("valid_n_3m"),
    validCount6m: metric("valid_n_6m"),
    universeMean3m: metric("universe_mean_3m"),
    universeMean6m: metric("universe_mean_6m"),
    top20Mean3m: metric("top20_mean_3m"),
    top20Mean6m: metric("top20_mean_6m"),
    top20Bottom20Spread3m: metric("top20_bottom20_spread_3m"),
    top20Bottom20Spread6m: metric("top20_bottom20_spread_6m"),
    rankIc3m: metric("rank_ic_3m"),
    rankIc6m: metric("rank_ic_6m"),
    categoryNeutralRankIc3m: metric("category_neutral_rank_ic_3m"),
    categoryNeutralRankIc6m: metric("category_neutral_rank_ic_6m"),
    top20CategoryExcessMean3m: metric("top20_category_excess_mean_3m"),
    top20CategoryExcessMean6m: metric("top20_category_excess_mean_6m"),
    top20PositiveRate3m: metric("top20_positive_rate_3m"),
    top20PositiveRate6m: metric("top20_positive_rate_6m"),
  };
}

function parseCompanyIndex(markdown) {
  const lines = markdown.split(/\r?\n/);
  const headerIndex = lines.findIndex(
    (line) => line.trim().startsWith("|") && line.includes("股票代号") && line.includes("公司名称") && line.includes("目录"),
  );
  if (headerIndex < 0) throw new Error("公司索引没有找到标准表头");
  const header = splitMarkdownRow(lines[headerIndex]);
  const tickerIndex = header.indexOf("股票代号");
  const nameIndex = header.indexOf("公司名称");
  const categoryIndex = header.indexOf("目录");
  const rows = [];
  for (const line of lines.slice(headerIndex + 2)) {
    if (!line.trim().startsWith("|")) break;
    const cells = splitMarkdownRow(line);
    const ticker = canonicalTicker(cells[tickerIndex]);
    if (!ticker) continue;
    rows.push({
      ticker,
      name: cleanCell(cells[nameIndex]),
      category: cleanCell(cells[categoryIndex]).replace(/[\\/]+$/, ""),
    });
  }
  return rows;
}

function splitMarkdownRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map(cleanCell);
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  const input = text.replace(/^\uFEFF/, "");
  for (let index = 0; index < input.length; index += 1) {
    const character = input[index];
    if (quoted) {
      if (character === '"' && input[index + 1] === '"') {
        field += '"';
        index += 1;
      } else if (character === '"') {
        quoted = false;
      } else {
        field += character;
      }
    } else if (character === '"') {
      quoted = true;
    } else if (character === ",") {
      row.push(field);
      field = "";
    } else if (character === "\n") {
      row.push(field.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += character;
    }
  }
  if (field || row.length) {
    row.push(field.replace(/\r$/, ""));
    rows.push(row);
  }
  const nonEmpty = rows.filter((cells) => cells.some((cell) => cell !== ""));
  if (!nonEmpty.length) return [];
  const headers = nonEmpty[0].map(cleanCell);
  return nonEmpty.slice(1).map((cells) => Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""])));
}

function resolveRootSource(relative) {
  const source = cleanCell(relative);
  if (!source || path.isAbsolute(source) || source.split(/[\\/]+/).includes("..")) {
    throw new Error(`公司排序相对路径无效：${relative}`);
  }
  const resolved = path.resolve(ROOT, source.replaceAll("/", path.sep));
  const fromRoot = path.relative(ROOT, resolved);
  if (!fromRoot || fromRoot.startsWith("..") || path.isAbsolute(fromRoot)) {
    throw new Error(`公司排序路径越界：${relative}`);
  }
  return resolved;
}

function groupRows(rows, field) {
  const grouped = new Map();
  for (const row of rows) {
    const key = cleanCell(row[field]);
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key).push(row);
  }
  return grouped;
}

function canonicalTicker(value) {
  const ticker = cleanCell(value).toUpperCase();
  return TICKER_ALIASES.get(ticker) || ticker;
}

function cleanCell(value) {
  return String(value ?? "")
    .replace(/`/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function number(value) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) throw new Error(`需要数值，实际为 ${value}`);
  return parsed;
}

function numberOrNull(value) {
  if (value === "" || value === null || value === undefined) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function asBoolean(value) {
  return String(value).trim().toLowerCase() === "true";
}

function mean(values) {
  const finite = values.filter(Number.isFinite);
  return finite.length ? finite.reduce((sum, value) => sum + value, 0) / finite.length : null;
}

function median(values) {
  const finite = values.filter(Number.isFinite).sort((a, b) => a - b);
  if (!finite.length) return null;
  const middle = Math.floor(finite.length / 2);
  return finite.length % 2 ? finite[middle] : (finite[middle - 1] + finite[middle]) / 2;
}

function finiteMin(values) {
  const finite = values.filter(Number.isFinite);
  return finite.length ? Math.min(...finite) : null;
}

function finiteMax(values) {
  const finite = values.filter(Number.isFinite);
  return finite.length ? Math.max(...finite) : null;
}

function round(value, digits = 4) {
  if (!Number.isFinite(value)) return null;
  return Number(value.toFixed(digits));
}

function hashText(text) {
  return crypto.createHash("sha256").update(text, "utf8").digest("hex");
}

function relativeProject(file) {
  return path.relative(PROJECT_ROOT, file).split(path.sep).join("/");
}

async function safeReadDirents(dir) {
  try {
    return await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || error);
  process.exitCode = 1;
});
