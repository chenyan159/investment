import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(ROOT, "..", "..");
const RESULT_ROOT = path.join(ROOT, "结果");
const DEFAULT_OUTPUT_ROOT = path.join(ROOT, "站点数据");
const OUTPUT_ROOT = process.env.PROJECT_ANANTA_OUTPUT_ROOT?.trim()
  ? path.resolve(process.env.PROJECT_ANANTA_OUTPUT_ROOT)
  : DEFAULT_OUTPUT_ROOT;
const COMPANY_OUTPUT_ROOT = path.join(OUTPUT_ROOT, "companies");
const COMPANY_INDEX_FILE = path.join(PROJECT_ROOT, "基本面", "公司调研", "公司索引.md");
const RESEARCH_PLAN_FILE = path.join(ROOT, "研究方案.md");

const EXPECTED_COMPANY_COUNT = 192;
const REPORT_PATTERN = /^([A-Z0-9.-]+)_经营情景市场状态投资决策_(\d{4}-\d{2}-\d{2})\.md$/i;
const TICKER_ALIASES = new Map([["PSTG", "P"]]);

const OPERATING_SCENARIOS = [
  { key: "pessimistic", label: "悲观 / 受损", shortLabel: "悲观" },
  { key: "base", label: "基准 / 正常兑现", shortLabel: "基准" },
  { key: "optimistic", label: "乐观 / 超预期", shortLabel: "乐观" },
  { key: "breakthrough", label: "突破 / 非线性", shortLabel: "突破" },
];

const MARKET_STATES = [
  { key: "broad", label: "宽基风险扩张", shortLabel: "宽基扩张" },
  { key: "theme", label: "窄幅 / 主题主导上涨", shortLabel: "主题上涨" },
  { key: "range", label: "震荡 / 均值回归", shortLabel: "震荡" },
  { key: "orderly", label: "有序风险收缩", shortLabel: "有序收缩" },
  { key: "liquidity", label: "流动性 / 信用压力", shortLabel: "流动性压力" },
];

const ADVICE_LEVELS = [
  { key: "strongNo", label: "强烈不建议投资", rank: 0, group: "negative" },
  { key: "no", label: "不建议投资", rank: 1, group: "negative" },
  { key: "neutral", label: "中性 / 等待", rank: 2, group: "neutral" },
  { key: "cautious", label: "谨慎建议投资", rank: 3, group: "positive" },
  { key: "yes", label: "建议投资", rank: 4, group: "positive" },
  { key: "strongYes", label: "强烈建议投资", rank: 5, group: "positive" },
];

const scenarioByKey = new Map(OPERATING_SCENARIOS.map((row) => [row.key, row]));
const marketByKey = new Map(MARKET_STATES.map((row) => [row.key, row]));
const adviceByKey = new Map(ADVICE_LEVELS.map((row) => [row.key, row]));

async function main() {
  const companyIndex = await readCompanyIndex();
  const indexByTicker = new Map(companyIndex.map((row) => [row.ticker, row]));
  const reports = await findCurrentReports();
  const parsed = await Promise.all(reports.map((item) => parseReport(item, indexByTicker)));
  const validation = validateReports(parsed, companyIndex);
  const researchPlan = await fs.readFile(RESEARCH_PLAN_FILE, "utf8");
  const summaries = parsed.map((report) => buildCompanySummary(report));
  const summaryByTicker = new Map(summaries.map((row) => [row.ticker, row]));
  const reportDates = unique(parsed.map((report) => report.reportDate)).sort();
  const sourceHash = hashText(parsed.map((report) => `${report.ticker}:${report.sourceHash}`).sort().join("\n"));
  const aggregates = buildAggregates(summaries, parsed);

  const payload = {
    schemaVersion: 1,
    source: "companyScenarioDecisionSiteData",
    generatedAt: new Date().toISOString(),
    sourceRoot: "分析报告/公司情景投资决策",
    resultRoot: "分析报告/公司情景投资决策/结果",
    reportDate: reportDates.at(-1) || "",
    reportDates,
    researchPlanHash: hashText(researchPlan).slice(0, 16),
    sourceHash: sourceHash.slice(0, 16),
    companyCount: summaries.length,
    cellCount: parsed.reduce((sum, report) => sum + report.cells.length, 0),
    estimableCellCount: parsed.reduce((sum, report) => sum + report.cells.filter((cell) => cell.estimable).length, 0),
    operatingScenarios: OPERATING_SCENARIOS,
    marketStates: MARKET_STATES,
    adviceLevels: ADVICE_LEVELS,
    quality: {
      complete: validation.errors.length === 0,
      status: validation.warnings.length ? "warning" : "ok",
      expectedCompanyCount: EXPECTED_COMPANY_COUNT,
      expectedCellsPerCompany: OPERATING_SCENARIOS.length * MARKET_STATES.length,
      errorCount: validation.errors.length,
      warningCount: validation.warnings.length,
      errors: validation.errors,
      warnings: validation.warnings.slice(0, 100),
      snapshotIdentityCount: unique(summaries.map((row) => row.current.marketSnapshotIdentity).filter(Boolean)).length,
    },
    metrics: aggregates.metrics,
    scenarioGrid: aggregates.scenarioGrid,
    categories: aggregates.categories,
    insights: aggregates.insights,
    companies: summaries,
    qualityNote: `完整覆盖 ${summaries.length} 家公司和 ${aggregates.metrics.estimableCellCount.toLocaleString("en-US")} 个可估值条件格；概率层不参与汇总。`,
  };

  if (validation.errors.length) {
    throw new Error(`公司情景投资决策站点数据校验失败：\n- ${validation.errors.slice(0, 40).join("\n- ")}`);
  }

  await prepareOutput();
  await writeJson(path.join(OUTPUT_ROOT, "current.json"), payload);
  for (const report of parsed) {
    const summary = summaryByTicker.get(report.ticker);
    await writeJson(
      path.join(COMPANY_OUTPUT_ROOT, `${report.ticker}.json`),
      {
        schemaVersion: 1,
        source: "companyScenarioDecisionDetail",
        ticker: report.ticker,
        name: summary.name,
        category: summary.category,
        title: report.title,
        reportDate: report.reportDate,
        sourcePath: report.sourcePath,
        summary,
        cells: report.cells,
        markdown: redactLocalPaths(report.markdown),
      },
      false,
    );
  }

  console.log(
    `Company scenario decision site data: ${summaries.length} companies, ${payload.estimableCellCount}/${payload.cellCount} estimable cells.`,
  );
  console.log(
    `Current advice: ${aggregates.metrics.current.positive} positive, ${aggregates.metrics.current.neutral} neutral, ${aggregates.metrics.current.negative} negative.`,
  );
  console.log(`Validation: ${validation.errors.length} errors, ${validation.warnings.length} warnings. Wrote ${OUTPUT_ROOT}`);
}

async function readCompanyIndex() {
  const markdown = await fs.readFile(COMPANY_INDEX_FILE, "utf8");
  const rows = parseMarkdownTables(markdown)
    .flatMap((table) => table.rows)
    .filter((row) => row["股票代号"] && row["公司名称"])
    .map((row) => ({
      ticker: canonicalTicker(row["股票代号"]),
      name: cleanInline(row["公司名称"]),
      category: cleanInline(row["目录"]).replace(/[\\/]+$/, ""),
    }));
  if (rows.length !== EXPECTED_COMPANY_COUNT) {
    throw new Error(`公司索引应有 ${EXPECTED_COMPANY_COUNT} 家，实际 ${rows.length} 家。`);
  }
  return rows;
}

async function findCurrentReports() {
  const dirents = await fs.readdir(RESULT_ROOT, { withFileTypes: true });
  const reports = [];
  for (const dirent of dirents) {
    if (!dirent.isFile()) continue;
    const match = dirent.name.match(REPORT_PATTERN);
    if (!match) continue;
    reports.push({
      ticker: canonicalTicker(match[1]),
      reportDate: match[2],
      file: path.join(RESULT_ROOT, dirent.name),
    });
  }
  return reports.sort((a, b) => a.ticker.localeCompare(b.ticker));
}

async function parseReport(item, indexByTicker) {
  const markdown = await fs.readFile(item.file, "utf8");
  const tables = parseMarkdownTables(markdown);
  const title = firstMatch(markdown, /^#\s+(.+)$/m) || path.basename(item.file, ".md");
  const currentQuote = firstMatch(markdown, /^(>\s*\*\*当前条件定位[^\n]*)$/m) || "";
  const mainTable = tables.find((table) => isMainMatrixTable(table));
  if (!mainTable) throw new Error(`${item.ticker} 未找到四行五列主矩阵。`);

  const detailTable = tables.find((table) => isDetailMatrixTable(table));
  const details = detailTable ? parseDetailTable(detailTable) : new Map();
  const cells = parseMainMatrix(mainTable).map((cell) => ({
    ...cell,
    ...(details.get(`${cell.operatingScenario}:${cell.marketState}`) || {}),
    adviceKey: cell.adviceKey || details.get(`${cell.operatingScenario}:${cell.marketState}`)?.adviceKey || null,
    adviceLabel:
      cell.adviceLabel || details.get(`${cell.operatingScenario}:${cell.marketState}`)?.adviceLabel || (cell.estimable ? "" : "NA"),
  }));
  const current = parseCurrentPosition(currentQuote, cells, markdown);
  const indexed = indexByTicker.get(item.ticker);

  return {
    ticker: item.ticker,
    name: indexed?.name || item.ticker,
    category: indexed?.category || "",
    title: cleanInline(title),
    reportDate: item.reportDate,
    sourcePath: `分析报告/公司情景投资决策/结果/${path.basename(item.file)}`,
    sourceHash: hashText(markdown),
    current,
    cells,
    markdown,
  };
}

function parseMainMatrix(table) {
  const marketColumns = table.headers
    .map((header, index) => ({ index, marketState: normalizeMarket(header) }))
    .filter((row) => row.marketState);
  const cells = [];
  for (const rawRow of table.rawRows) {
    const operatingScenario = normalizeScenario(rawRow[0]);
    if (!operatingScenario) continue;
    for (const column of marketColumns) {
      const parsed = parseMatrixCell(rawRow[column.index] || "");
      cells.push({
        operatingScenario,
        operatingLabel: scenarioByKey.get(operatingScenario).label,
        marketState: column.marketState,
        marketLabel: marketByKey.get(column.marketState).label,
        ...parsed,
      });
    }
  }
  return cells;
}

function parseDetailTable(table) {
  const result = new Map();
  for (const row of table.rows) {
    const operatingScenario = normalizeScenario(valueByHeader(row, ["经营情景"]));
    const marketState = normalizeMarket(valueByHeader(row, ["市场状态"]));
    if (!operatingScenario || !marketState) continue;
    const adviceRaw = valueByHeader(row, ["投资建议强度", "条件建议", "投资建议"]);
    const adviceKey = normalizeAdvice(adviceRaw);
    const returnText = cleanInline(valueByHeader(row, ["目标期股东总回报区间", "目标期总回报区间", "总回报区间", "回报区间", "总回报", "回报"]));
    result.set(`${operatingScenario}:${marketState}`, {
      valuationMethod: cleanInline(valueByHeader(row, ["主估值理念", "估值理念", "估值方法"])),
      equityValue: cleanInline(valueByHeader(row, ["稀释后股权市值区间", "稀释后市值区间", "股权市值区间", "稀释后市值", "股权市值"])),
      perShareValue: cleanInline(valueByHeader(row, ["每股价值区间", "每股价值"])),
      returnRangeText: returnText,
      returnRange: extractPercentRange(returnText),
      adviceKey,
      adviceLabel: adviceKey ? adviceByKey.get(adviceKey).label : cleanInline(adviceRaw),
      decisiveReason: cleanInline(valueByHeader(row, ["决定性理由", "核心理由", "决定因素"])),
      changeCondition: cleanInline(valueByHeader(row, ["结论改变条件", "改变条件", "转正条件"])),
      confidence: normalizeConfidence(valueByHeader(row, ["估值置信度", "置信度"])),
    });
  }
  return result;
}

function parseMatrixCell(raw) {
  const text = cleanInline(raw);
  const adviceKey = normalizeAdvice(text);
  const estimable = Boolean(adviceKey) && !/^NA(?:\b|\s|｜|\/)/i.test(text);
  return {
    estimable,
    adviceKey,
    adviceLabel: adviceKey ? adviceByKey.get(adviceKey).label : "NA",
    adviceRank: adviceKey ? adviceByKey.get(adviceKey).rank : null,
    adviceGroup: adviceKey ? adviceByKey.get(adviceKey).group : "unavailable",
    returnRangeText: extractPercentRangeText(text),
    returnRange: extractPercentRange(text),
    confidence: normalizeConfidence(text),
  };
}

function parseCurrentPosition(quoteRaw, cells, markdown) {
  const quote = cleanInline(quoteRaw.replace(/^>\s*/, ""));
  const scenarioStart = quote.indexOf("最接近");
  const operatingScenario = findFirstScenario(scenarioStart >= 0 ? quote.slice(scenarioStart) : quote);
  const lockStart = quote.indexOf("锁定");
  const marketState = findFirstMarket(lockStart >= 0 ? quote.slice(lockStart) : quote);
  const pureCell = cells.find((cell) => cell.operatingScenario === operatingScenario && cell.marketState === marketState) || null;
  const composite = detectCompositePosition(quote);
  const compositeAdvice = composite ? findCompositeAdvice(quote) : null;
  const rotationAdvice = findRotationAdvice(quote);
  const adviceMatch = rotationAdvice || compositeAdvice;
  const adviceKey = rotationAdvice?.adviceKey || compositeAdvice?.adviceKey || pureCell?.adviceKey || null;
  const adviceStart = adviceMatch?.index ?? 0;
  const currentFragment = composite ? quote.slice(adviceStart) : "";
  const returnRange = (composite ? extractPercentRange(currentFragment) : null) || pureCell?.returnRange || null;
  const perShareValue = (composite ? extractPerShareRange(currentFragment) : "") || pureCell?.perShareValue || "";
  const weakLink = extractWeakLink(quote);
  const priceBoundary = extractPriceBoundary(quote);
  const marketSnapshotIdentity = extractMarketSnapshotIdentity(quote);
  const currentPrice = extractCurrentPrice(markdown);

  return {
    operatingScenario,
    operatingLabel: scenarioByKey.get(operatingScenario)?.label || "",
    marketState,
    marketLabel: marketByKey.get(marketState)?.label || "",
    composite,
    rotationAdjusted: Boolean(rotationAdvice),
    adjustmentType: rotationAdvice ? "sectorRotation" : composite ? "composite" : "pure",
    adviceKey,
    adviceLabel: adviceKey ? adviceByKey.get(adviceKey).label : "",
    adviceRank: adviceKey ? adviceByKey.get(adviceKey).rank : null,
    adviceGroup: adviceKey ? adviceByKey.get(adviceKey).group : "",
    pureAdviceKey: pureCell?.adviceKey || null,
    pureAdviceLabel: pureCell?.adviceLabel || "",
    pureAdviceRank: pureCell?.adviceRank ?? null,
    pureReturnRange: pureCell?.returnRange || null,
    pureReturnRangeText: pureCell?.returnRangeText || "",
    perShareValue,
    returnRange,
    returnRangeText: returnRange ? formatPercentRange(returnRange) : pureCell?.returnRangeText || "",
    currentPrice,
    weakLink,
    priceBoundary,
    marketSnapshotIdentity,
    summary: quote,
  };
}

function buildCompanySummary(report) {
  const estimable = report.cells.filter((cell) => cell.estimable);
  const positive = estimable.filter((cell) => cell.adviceGroup === "positive");
  const neutral = estimable.filter((cell) => cell.adviceGroup === "neutral");
  const negative = estimable.filter((cell) => cell.adviceGroup === "negative");
  const baseCells = estimable.filter((cell) => cell.operatingScenario === "base");
  const stressCells = estimable.filter((cell) => cell.marketState === "liquidity");
  const rowPositive = Object.fromEntries(
    OPERATING_SCENARIOS.map((scenario) => [scenario.key, positive.filter((cell) => cell.operatingScenario === scenario.key).length]),
  );
  const marketPositive = Object.fromEntries(
    MARKET_STATES.map((market) => [market.key, positive.filter((cell) => cell.marketState === market.key).length]),
  );

  return {
    ticker: report.ticker,
    name: report.name,
    category: report.category,
    title: report.title,
    reportDate: report.reportDate,
    sourcePath: report.sourcePath,
    dataFile: `reports/scenario-decision/${report.ticker}.json`,
    current: report.current,
    matrix: {
      cellCount: report.cells.length,
      estimableCellCount: estimable.length,
      positiveCellCount: positive.length,
      neutralCellCount: neutral.length,
      negativeCellCount: negative.length,
      positiveShare: round(positive.length / Math.max(1, estimable.length), 4),
      basePositiveCount: baseCells.filter((cell) => cell.adviceGroup === "positive").length,
      stressPositiveCount: stressCells.filter((cell) => cell.adviceGroup === "positive").length,
      rowPositive,
      marketPositive,
      firstPositiveScenario: OPERATING_SCENARIOS.find((scenario) => rowPositive[scenario.key] > 0)?.key || null,
      breakthroughDependent: rowPositive.base === 0 && rowPositive.optimistic === 0 && rowPositive.breakthrough > 0,
    },
  };
}

function buildAggregates(summaries, reports) {
  const allCells = reports.flatMap((report) => report.cells);
  const estimableCells = allCells.filter((cell) => cell.estimable);
  const currentAdviceCounts = countByLevels(summaries.map((row) => row.current.adviceKey));
  const pureCurrentAdviceCounts = countByLevels(summaries.map((row) => row.current.pureAdviceKey));
  const matrixAdviceCounts = countByLevels(estimableCells.map((cell) => cell.adviceKey));
  const scenarioGrid = OPERATING_SCENARIOS.flatMap((scenario) =>
    MARKET_STATES.map((market) => {
      const cells = allCells.filter((cell) => cell.operatingScenario === scenario.key && cell.marketState === market.key);
      const estimable = cells.filter((cell) => cell.estimable);
      const positive = estimable.filter((cell) => cell.adviceGroup === "positive");
      const negative = estimable.filter((cell) => cell.adviceGroup === "negative");
      const returns = estimable.map((cell) => cell.returnRange).filter(Boolean);
      return {
        operatingScenario: scenario.key,
        operatingLabel: scenario.label,
        marketState: market.key,
        marketLabel: market.label,
        companyCount: cells.length,
        estimableCount: estimable.length,
        positiveCount: positive.length,
        neutralCount: estimable.length - positive.length - negative.length,
        negativeCount: negative.length,
        positiveShare: round(positive.length / Math.max(1, estimable.length), 4),
        medianLowReturn: median(returns.map((range) => range.low)),
        medianHighReturn: median(returns.map((range) => range.high)),
      };
    }),
  );

  const scenarioStats = OPERATING_SCENARIOS.map((scenario) => aggregateCells(estimableCells.filter((cell) => cell.operatingScenario === scenario.key), scenario));
  const marketStats = MARKET_STATES.map((market) => aggregateCells(estimableCells.filter((cell) => cell.marketState === market.key), market));
  const categories = [...new Set(summaries.map((row) => row.category))]
    .sort((a, b) => a.localeCompare(b, "zh-Hans-CN"))
    .map((category) => {
      const rows = summaries.filter((row) => row.category === category);
      return {
        category,
        companyCount: rows.length,
        positive: rows.filter((row) => row.current.adviceGroup === "positive").length,
        neutral: rows.filter((row) => row.current.adviceGroup === "neutral").length,
        negative: rows.filter((row) => row.current.adviceGroup === "negative").length,
        baseAnyPositive: rows.filter((row) => row.matrix.basePositiveCount > 0).length,
        medianPositiveCells: median(rows.map((row) => row.matrix.positiveCellCount)),
      };
    });

  const positiveCurrent = summaries.filter((row) => row.current.adviceGroup === "positive");
  const currentNeutral = summaries.filter((row) => row.current.adviceGroup === "neutral");
  const currentNegative = summaries.filter((row) => row.current.adviceGroup === "negative");
  const byRobustness = [...summaries].sort(
    (a, b) => b.matrix.basePositiveCount - a.matrix.basePositiveCount || b.matrix.positiveCellCount - a.matrix.positiveCellCount || a.ticker.localeCompare(b.ticker),
  );

  return {
    metrics: {
      companyCount: summaries.length,
      cellCount: allCells.length,
      estimableCellCount: estimableCells.length,
      current: {
        positive: positiveCurrent.length,
        neutral: currentNeutral.length,
        negative: currentNegative.length,
        positiveShare: round(positiveCurrent.length / Math.max(1, summaries.length), 4),
        adviceCounts: currentAdviceCounts,
        pure: {
          positive: summaries.filter((row) => adviceByKey.get(row.current.pureAdviceKey)?.group === "positive").length,
          neutral: summaries.filter((row) => adviceByKey.get(row.current.pureAdviceKey)?.group === "neutral").length,
          negative: summaries.filter((row) => adviceByKey.get(row.current.pureAdviceKey)?.group === "negative").length,
          adviceCounts: pureCurrentAdviceCounts,
        },
        operatingCounts: countBy(summaries.map((row) => row.current.operatingScenario)),
        marketCounts: countBy(summaries.map((row) => row.current.marketState)),
        compositeCount: summaries.filter((row) => row.current.composite).length,
        rotationAdjustedCount: summaries.filter((row) => row.current.rotationAdjusted).length,
      },
      matrix: {
        positive: estimableCells.filter((cell) => cell.adviceGroup === "positive").length,
        neutral: estimableCells.filter((cell) => cell.adviceGroup === "neutral").length,
        negative: estimableCells.filter((cell) => cell.adviceGroup === "negative").length,
        positiveShare: round(estimableCells.filter((cell) => cell.adviceGroup === "positive").length / Math.max(1, estimableCells.length), 4),
        adviceCounts: matrixAdviceCounts,
        scenarioStats,
        marketStats,
        noBasePositiveCount: summaries.filter((row) => row.matrix.basePositiveCount === 0).length,
        noPositiveCount: summaries.filter((row) => row.matrix.positiveCellCount === 0).length,
      },
    },
    scenarioGrid,
    categories,
    insights: {
      robustBase: byRobustness.filter((row) => row.matrix.basePositiveCount >= 3).slice(0, 12),
      currentPositive: [...positiveCurrent].sort((a, b) => b.current.adviceRank - a.current.adviceRank || b.matrix.basePositiveCount - a.matrix.basePositiveCount).slice(0, 20),
      stressResilient: byRobustness.filter((row) => row.matrix.stressPositiveCount > 0).slice(0, 20),
      breakthroughDependent: summaries.filter((row) => row.matrix.breakthroughDependent).sort((a, b) => b.matrix.positiveCellCount - a.matrix.positiveCellCount).slice(0, 20),
      noPositive: summaries.filter((row) => row.matrix.positiveCellCount === 0),
    },
  };
}

function aggregateCells(cells, descriptor) {
  const positive = cells.filter((cell) => cell.adviceGroup === "positive").length;
  const neutral = cells.filter((cell) => cell.adviceGroup === "neutral").length;
  return {
    key: descriptor.key,
    label: descriptor.label,
    shortLabel: descriptor.shortLabel,
    estimableCount: cells.length,
    positiveCount: positive,
    neutralCount: neutral,
    negativeCount: cells.length - positive - neutral,
    positiveShare: round(positive / Math.max(1, cells.length), 4),
  };
}

function validateReports(reports, companyIndex) {
  const errors = [];
  const warnings = [];
  const expectedTickers = new Set(companyIndex.map((row) => row.ticker));
  const actualTickers = new Set(reports.map((row) => row.ticker));
  const missing = [...expectedTickers].filter((ticker) => !actualTickers.has(ticker));
  const extra = [...actualTickers].filter((ticker) => !expectedTickers.has(ticker));
  if (reports.length !== EXPECTED_COMPANY_COUNT) errors.push(`公司数应为 ${EXPECTED_COMPANY_COUNT}，实际 ${reports.length}`);
  if (missing.length) errors.push(`缺失公司：${missing.join(", ")}`);
  if (extra.length) errors.push(`额外公司：${extra.join(", ")}`);

  for (const report of reports) {
    const keys = new Set(report.cells.map((cell) => `${cell.operatingScenario}:${cell.marketState}`));
    if (report.cells.length !== 20 || keys.size !== 20) errors.push(`${report.ticker} 主矩阵应有20个唯一格子，实际 ${report.cells.length}/${keys.size}`);
    if (!report.current.operatingScenario) errors.push(`${report.ticker} 未解析当前经营情景`);
    if (!report.current.marketState) errors.push(`${report.ticker} 未解析当前市场状态`);
    if (!report.current.adviceKey) errors.push(`${report.ticker} 未解析当前建议`);
    if (!report.current.weakLink) warnings.push(`${report.ticker} 未解析当前最弱传导环节`);
    const unavailable = report.cells.filter((cell) => !cell.estimable).length;
    if (unavailable) warnings.push(`${report.ticker} 有 ${unavailable} 个 NA 格子`);
  }
  return { errors, warnings };
}

function isMainMatrixTable(table) {
  if (!table.headers[0]?.includes("经营情景")) return false;
  const markets = new Set(table.headers.map(normalizeMarket).filter(Boolean));
  const scenarios = new Set(table.rawRows.map((row) => normalizeScenario(row[0])).filter(Boolean));
  const adviceCellCount = table.rawRows.flatMap((row) => row.slice(1)).filter((cell) => normalizeAdvice(cell)).length;
  return markets.size === 5 && scenarios.size === 4 && adviceCellCount >= 15;
}

function isDetailMatrixTable(table) {
  const joined = table.headers.join("|");
  return table.headers.includes("经营情景") && table.headers.includes("市场状态") && /投资建议|条件建议/.test(joined) && /每股价值/.test(joined);
}

function parseMarkdownTables(markdown) {
  const lines = markdown.split(/\r?\n/);
  const tables = [];
  for (let i = 0; i < lines.length - 1; i += 1) {
    if (!lines[i].trim().startsWith("|")) continue;
    if (!isSeparatorRow(lines[i + 1])) continue;
    const headers = splitMarkdownRow(lines[i]).map(cleanInline);
    const rawRows = [];
    for (let j = i + 2; j < lines.length && lines[j].trim().startsWith("|"); j += 1) {
      if (isSeparatorRow(lines[j])) continue;
      const cells = splitMarkdownRow(lines[j]);
      if (!cells.some((cell) => cleanInline(cell))) continue;
      rawRows.push(cells);
      i = j;
    }
    const rows = rawRows.map((cells) => Object.fromEntries(headers.map((header, index) => [header, cleanInline(cells[index] || "")])));
    tables.push({ headers, rawRows, rows });
  }
  return tables;
}

function splitMarkdownRow(line) {
  const source = line.trim().replace(/^\|/, "").replace(/\|$/, "");
  const cells = [];
  let current = "";
  let escaped = false;
  for (const char of source) {
    if (escaped) {
      current += char;
      escaped = false;
    } else if (char === "\\") {
      current += char;
      escaped = true;
    } else if (char === "|") {
      cells.push(current.trim());
      current = "";
    } else {
      current += char;
    }
  }
  cells.push(current.trim());
  return cells;
}

function isSeparatorRow(line) {
  return /^\s*\|?\s*:?-{3,}/.test(line) && !/[\p{L}\p{N}]/u.test(line.replace(/[\s|:-]/g, ""));
}

function valueByHeader(row, candidates) {
  for (const candidate of candidates) {
    const exact = Object.keys(row).find((header) => header === candidate);
    if (exact) return row[exact];
    const partial = Object.keys(row).find((header) => header.includes(candidate));
    if (partial) return row[partial];
  }
  return "";
}

function normalizeScenario(value) {
  const text = cleanInline(value);
  if (/悲观|受损/.test(text)) return "pessimistic";
  if (/基准|正常兑现/.test(text)) return "base";
  if (/乐观|超预期/.test(text)) return "optimistic";
  if (/突破|非线性/.test(text)) return "breakthrough";
  return null;
}

function normalizeMarket(value) {
  const text = cleanInline(value);
  if (/宽基/.test(text)) return "broad";
  if (/窄幅|主题/.test(text)) return "theme";
  if (/震荡|均值回归/.test(text)) return "range";
  if (/有序.*收缩|风险收缩/.test(text)) return "orderly";
  if (/流动性|信用压力/.test(text)) return "liquidity";
  return null;
}

function normalizeAdvice(value) {
  const text = cleanInline(value).replace(/\s+/g, "");
  if (/强烈不建议投资|强烈不建议/.test(text)) return "strongNo";
  if (/谨慎建议投资|谨慎建议/.test(text)) return "cautious";
  if (/强烈建议投资|强烈建议/.test(text)) return "strongYes";
  if (/不建议投资|不建议/.test(text)) return "no";
  if (/中性(?:\/|／)?等待|中性|等待/.test(text)) return "neutral";
  if (/建议投资|建议/.test(text)) return "yes";
  return null;
}

function normalizeConfidence(value) {
  const text = cleanInline(value);
  const match = text.match(/(?:估值)?置信度(?:为)?\s*(中高|中低|高|中|低)/) || text.match(/(?:｜|\|)\s*(中高|中低|高|中|低)\s*$/);
  return match?.[1] || "";
}

function findFirstScenario(text) {
  const candidates = OPERATING_SCENARIOS.map((row) => ({ key: row.key, index: firstScenarioIndex(text, row.key) })).filter((row) => row.index >= 0);
  return candidates.sort((a, b) => a.index - b.index)[0]?.key || null;
}

function firstScenarioIndex(text, key) {
  const patterns = {
    pessimistic: [/悲观/, /受损/],
    base: [/基准/, /正常兑现/],
    optimistic: [/乐观/, /超预期/],
    breakthrough: [/突破/, /非线性/],
  }[key];
  const indices = patterns.map((pattern) => text.search(pattern)).filter((index) => index >= 0);
  return indices.length ? Math.min(...indices) : -1;
}

function findFirstMarket(text) {
  const candidates = MARKET_STATES.map((row) => ({ key: row.key, index: firstMarketIndex(text, row.key) })).filter((row) => row.index >= 0);
  return candidates.sort((a, b) => a.index - b.index)[0]?.key || null;
}

function firstMarketIndex(text, key) {
  const patterns = {
    broad: [/宽基/],
    theme: [/窄幅/, /主题/],
    range: [/震荡/, /均值回归/],
    orderly: [/有序.*?收缩/, /风险收缩/],
    liquidity: [/流动性/, /信用压力/],
  }[key];
  const indices = patterns.map((pattern) => text.search(pattern)).filter((index) => index >= 0);
  return indices.length ? Math.min(...indices) : -1;
}

function detectCompositePosition(quote) {
  if (/复合定位[^。；]{0,180}(?:未达到|没有达到|不需要|无需|不建立)/.test(quote) || /不需要复合定位/.test(quote)) return false;
  return /(?:需要复合定位|复合定位[^。；]{0,180}(?:达到(?:使用)?门槛|达到门槛|成立|适用))/.test(quote);
}

function findCompositeAdvice(quote) {
  const advice = "(强烈不建议投资|谨慎建议投资|强烈建议投资|不建议投资|中性\\s*[/／]\\s*等待|中性|建议投资)";
  const patterns = [
    new RegExp(`复合定位\\s*[×x]\\s*主状态[^。；]{0,100}?(?:条件建议(?:均)?为|为)\\s*[“\"]?${advice}`),
    new RegExp(`复合定位(?:在)?[^。；]{0,220}?条件建议(?:均)?为\\s*[“\"]?${advice}`),
    new RegExp(`复合口径[^。；]{0,220}?建议为\\s*[“\"]?${advice}`),
    new RegExp(`当前复合格子[^。；]{0,180}?${advice}`),
  ];
  for (const pattern of patterns) {
    const match = quote.match(pattern);
    const matchedAdvice = match ? match.slice(1).find((value) => normalizeAdvice(value)) : null;
    const adviceKey = normalizeAdvice(matchedAdvice || "");
    if (adviceKey) return { adviceKey, index: match.index || 0, snippet: match[0] };
  }
  const changed = quote.match(new RegExp(`建议由\\s*[“\"]?${advice}[^。；]{0,40}?(?:降为|上调为|升为)\\s*[“\"]?${advice}`));
  if (changed) {
    const matches = changed.slice(1).filter((value) => normalizeAdvice(value));
    const adviceKey = normalizeAdvice(matches.at(-1) || "");
    if (adviceKey) return { adviceKey, index: changed.index || 0, snippet: changed[0] };
  }
  return null;
}

function findRotationAdvice(quote) {
  const advice = "(强烈不建议投资|谨慎建议投资|强烈建议投资|不建议投资|中性\\s*[/／]\\s*等待|中性|建议投资)";
  const pattern = new RegExp(`按规则[^。；]{0,180}?(?:下调|上调)[^。；]{0,60}?(?:至|为)\\s*[“\"]?${advice}`);
  const match = quote.match(pattern);
  const matchedAdvice = match ? match.slice(1).find((value) => normalizeAdvice(value)) : null;
  const adviceKey = normalizeAdvice(matchedAdvice || "");
  return adviceKey ? { adviceKey, index: match.index || 0, snippet: match[0] } : null;
}

function extractPercentRange(value) {
  const values = [...cleanInline(value).matchAll(/([+\-−]?\d+(?:\.\d+)?)\s*%/g)].map((match) => Number(match[1].replace("−", "-")));
  if (values.length < 2) return null;
  return { low: values[0], high: values[1] };
}

function extractPercentRangeText(value) {
  const range = extractPercentRange(value);
  return range ? formatPercentRange(range) : "";
}

function formatPercentRange(range) {
  const signed = (value) => `${value > 0 ? "+" : ""}${Number.isInteger(value) ? value : round(value, 1)}%`;
  return `${signed(range.low)}—${signed(range.high)}`;
}

function extractPerShareRange(quote) {
  const match = quote.match(/每(?:股价值|股)\s*(?:为)?\s*\$?\s*([\d,.]+)\s*[—–~～-]\s*\$?\s*([\d,.]+)/);
  return match ? `$${match[1]}—$${match[2]}` : "";
}

function extractWeakLink(quote) {
  const match = quote.match(/(?:当前)?最弱传导环节(?:仍)?(?:是|为)\s*(.*?)(?:；|。|：)/);
  return match ? cleanInline(match[1]).replace(/^[“"]|[”"]$/g, "") : "";
}

function extractPriceBoundary(quote) {
  const patterns = [
    /(?:最高买入价|最高价格|价格边界|买入边界|价格降至)约?\s*\$?\s*([\d,.]+)/,
    /(?:最高买入价|最高价格|价格边界|买入边界)[^$\d]{0,30}\$\s*([\d,.]+)/,
  ];
  for (const pattern of patterns) {
    const match = quote.match(pattern);
    if (match) return `$${match[1]}`;
  }
  return "";
}

function extractMarketSnapshotIdentity(quote) {
  const match = quote.match(/共享市场快照(?:身份)?\s*(.*?)(?:锁定|，锁定)/);
  return match ? cleanInline(match[1]).replace(/^[：:“”"`]+|[：:“”"`]+$/g, "").trim() : "";
}

function extractCurrentPrice(markdown) {
  const patterns = [
    /\|\s*(?:收盘价|当前股价|冻结股价|参考股价)[^|]*\|\s*\*{0,2}\$?\s*([\d,.]+)/,
    /(?:当前价|现价|收盘价)[^\n$]{0,30}\$\s*([\d,.]+)/,
  ];
  for (const pattern of patterns) {
    const match = markdown.match(pattern);
    if (match) return Number(match[1].replace(/,/g, ""));
  }
  return null;
}

function countByLevels(keys) {
  return Object.fromEntries(ADVICE_LEVELS.map((level) => [level.key, keys.filter((key) => key === level.key).length]));
}

function countBy(values) {
  const result = {};
  for (const value of values.filter(Boolean)) result[value] = (result[value] || 0) + 1;
  return result;
}

function canonicalTicker(value) {
  const ticker = cleanInline(value).toUpperCase();
  return TICKER_ALIASES.get(ticker) || ticker;
}

function cleanInline(value) {
  return String(value || "")
    .replace(/<br\s*\/?\s*>/gi, " ")
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1")
    .replace(/[*_`]/g, "")
    .replace(/\\\|/g, "|")
    .replace(/\s+/g, " ")
    .trim();
}

function firstMatch(text, pattern) {
  return text.match(pattern)?.[1] || "";
}

function redactLocalPaths(markdown) {
  return markdown
    .replace(/D:\\drive\\Investment\\/gi, "Investment/")
    .replace(/D:\/drive\/Investment\//gi, "Investment/")
    .replace(/C:\\Users\\[^\s`|)]+/gi, "[本地路径已省略]");
}

async function prepareOutput() {
  assertOutputRoot();
  await fs.mkdir(OUTPUT_ROOT, { recursive: true });
  await fs.rm(COMPANY_OUTPUT_ROOT, { recursive: true, force: true });
  await fs.mkdir(COMPANY_OUTPUT_ROOT, { recursive: true });
}

function assertOutputRoot() {
  const resolved = path.resolve(OUTPUT_ROOT);
  const expected = path.resolve(DEFAULT_OUTPUT_ROOT);
  const isStaging = path.basename(resolved).startsWith(".站点数据-");
  if (path.dirname(resolved) !== path.resolve(ROOT) || (resolved !== expected && !isStaging)) {
    throw new Error(`拒绝写入非预期目录：${resolved}`);
  }
}

async function writeJson(file, value, pretty = true) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${JSON.stringify(value, null, pretty ? 2 : 0)}\n`, "utf8");
}

function hashText(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function unique(values) {
  return [...new Set(values)];
}

function median(values) {
  const clean = values.filter((value) => Number.isFinite(value)).sort((a, b) => a - b);
  if (!clean.length) return null;
  const middle = Math.floor(clean.length / 2);
  return clean.length % 2 ? clean[middle] : round((clean[middle - 1] + clean[middle]) / 2, 4);
}

function round(value, digits = 4) {
  if (!Number.isFinite(value)) return null;
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

await main();
