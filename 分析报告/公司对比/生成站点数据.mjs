import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(ROOT, "..", "..");
const RESULT_ROOT = path.join(ROOT, "结果");
const BACKUP_ROOT = path.join(RESULT_ROOT, "备份");
const DEFAULT_OUTPUT_ROOT = path.join(ROOT, "站点数据");
const OUTPUT_ROOT = process.env.PROJECT_ANANTA_OUTPUT_ROOT?.trim()
  ? path.resolve(process.env.PROJECT_ANANTA_OUTPUT_ROOT)
  : DEFAULT_OUTPUT_ROOT;
const COMPANY_OUTPUT_ROOT = path.join(OUTPUT_ROOT, "companies");
const COMPANY_INDEX_FILE = path.join(PROJECT_ROOT, "基本面", "公司调研", "公司索引.md");
const RESEARCH_PLAN_FILE = path.join(ROOT, "研究方案.md");

const EXPECTED_COMPANY_COUNT = 192;
const REPORT_PATTERN = /^([A-Z0-9.-]+)_逐家公司投资思路对比_(\d{4}-\d{2}-\d{2})\.md$/i;
const TICKER_ALIASES = new Map([["PSTG", "P"]]);

const DIMENSIONS = [
  { key: "near", label: "近端兑现", header: "近端兑现驱动" },
  { key: "long", label: "长期复利", header: "长期复利质量" },
  { key: "odds", label: "价格赔率", header: "价格赔率" },
  { key: "defense", label: "防守资本保全", header: "防守资本保全" },
  { key: "explosion", label: "爆发突破", header: "爆发增长与产业突破" },
  { key: "mispricing", label: "市场定价错位", header: "市场定价错位" },
];

async function main() {
  const companyIndex = await readCompanyIndex();
  const indexByTicker = new Map(companyIndex.map((row) => [row.ticker, row]));
  const currentFiles = await findCurrentReports();
  const currentReports = await Promise.all(currentFiles.map((item) => parseReportFile(item, indexByTicker)));
  const currentValidation = validateCurrentReports(currentReports, companyIndex);

  const previousFiles = await findPreviousReports(new Set(companyIndex.map((row) => row.ticker)));
  const previousReports = await Promise.all(previousFiles.map((item) => parseReportFile(item, indexByTicker)));

  const currentRun = buildRun(currentReports, companyIndex);
  const previousRun = previousReports.length ? buildRun(previousReports, companyIndex) : null;
  const researchPlan = await fs.readFile(RESEARCH_PLAN_FILE, "utf8");
  const reportDates = unique(currentReports.map((report) => report.reportDate)).sort();
  const reportDate = reportDates.at(-1) || "";
  const reportDateCounts = Object.fromEntries(
    reportDates.map((date) => [date, currentReports.filter((report) => report.reportDate === date).length]),
  );
  const reportDateLabel = reportDates.length > 1
    ? `${reportDates[0]} 至 ${reportDates.at(-1)}（${reportDates.length} 个报告日）`
    : reportDate;
  const priceDate = mostCommon(currentReports.map((report) => report.priceDate).filter(Boolean));
  const summaries = buildCompanySummaries(currentRun, previousRun, companyIndex);
  const summaryByTicker = new Map(summaries.map((row) => [row.ticker, row]));
  const finalRanking = currentRun.overallRanking.map((row) => ({
    ...row,
    name: indexByTicker.get(row.ticker)?.name || row.ticker,
    category: indexByTicker.get(row.ticker)?.category || "",
    dataFile: `reports/company-comparison/${row.ticker}.json`,
  }));
  const previousRanks = previousRun ? new Map(previousRun.overallRanking.map((row) => [row.ticker, row.rank])) : new Map();
  const rankCorrelation = previousRun
    ? spearman(
        currentRun.overallRanking.map((row) => row.rank),
        currentRun.overallRanking.map((row) => previousRanks.get(row.ticker)),
      )
    : null;
  const currentTop20 = new Set(currentRun.overallRanking.slice(0, 20).map((row) => row.ticker));
  const previousTop20 = new Set(previousRun?.overallRanking.slice(0, 20).map((row) => row.ticker) || []);
  const parseWarnings = currentReports.flatMap((report) => report.parseWarnings);
  const sourceHash = hashText(
    currentReports
      .map((report) => `${report.ticker}:${report.sourceHash}`)
      .sort()
      .join("\n"),
  );

  const payload = {
    schemaVersion: 1,
    generatedAt: new Date().toISOString(),
    sourceRoot: "分析报告/公司对比",
    resultRoot: "分析报告/公司对比/结果",
    reportDate,
    reportDateLabel,
    reportDates,
    reportDateCounts,
    priceDate,
    holdingPeriod: "8—16个月",
    researchPlanHash: hashText(researchPlan).slice(0, 16),
    sourceHash: sourceHash.slice(0, 16),
    companyCount: summaries.length,
    rowCount: currentRun.directedRowCount,
    pairCount: currentRun.pairCount,
    missing: [],
    dimensions: DIMENSIONS.map(({ key, label }) => ({ key, label })),
    quality: {
      complete: currentValidation.complete,
      status: parseWarnings.length ? "warning" : "ok",
      expectedCompanyCount: EXPECTED_COMPANY_COUNT,
      expectedRowsPerCompany: EXPECTED_COMPANY_COUNT - 1,
      expectedDirectedRows: EXPECTED_COMPANY_COUNT * (EXPECTED_COMPANY_COUNT - 1),
      expectedPairCount: (EXPECTED_COMPANY_COUNT * (EXPECTED_COMPANY_COUNT - 1)) / 2,
      parseWarningCount: parseWarnings.length,
      parseWarnings: parseWarnings.slice(0, 50),
      reportDates,
      reportDateCounts,
      previousReportDates: unique(previousReports.map((report) => report.reportDate)).sort(),
    },
    metrics: {
      reciprocal: addPercentages(currentRun.reciprocal, currentRun.pairCount),
      dimensionReciprocal: Object.fromEntries(
        DIMENSIONS.map((dimension) => [
          dimension.key,
          addPercentages(currentRun.dimensionReciprocal[dimension.key], currentRun.pairCount),
        ]),
      ),
      overallDimensionCorrelation: Object.fromEntries(
        DIMENSIONS.map((dimension) => [
          dimension.key,
          round(
            spearman(
              summaries.map((row) => row.finalRank),
              summaries.map((row) => row.dimensionStats[dimension.key].rank),
            ),
            4,
          ),
        ]),
      ),
      dimensionCorrelation: buildDimensionCorrelation(summaries),
      version: {
        available: Boolean(previousRun),
        previousReportDates: unique(previousReports.map((report) => report.reportDate)).sort(),
        rankCorrelation: rankCorrelation === null ? null : round(rankCorrelation, 4),
        top20Overlap: [...currentTop20].filter((ticker) => previousTop20.has(ticker)).length,
      },
    },
    rankings: {
      overall: attachCompanyMeta(currentRun.overallRanking, indexByTicker),
      consistent: attachCompanyMeta(currentRun.consistentRanking, indexByTicker),
      highConfidence: attachCompanyMeta(currentRun.highConfidenceRanking, indexByTicker),
      dimensions: Object.fromEntries(
        DIMENSIONS.map((dimension) => [
          dimension.key,
          attachCompanyMeta(currentRun.dimensionRankings[dimension.key], indexByTicker),
        ]),
      ),
    },
    categories: buildCategoryStats(summaries),
    insights: buildInsights(summaries),
    finalRanking,
    top20: finalRanking.slice(0, 20),
    companies: summaries,
    reports: {},
    qualityNote: `每家公司使用项目内当前最新报告；报告日期为 ${reportDateLabel || "未知"}。完整覆盖 ${summaries.length} 家公司、${formatNumber(currentRun.directedRowCount)} 项定向判断。`,
  };

  await prepareOutput();
  await writeJson(path.join(OUTPUT_ROOT, "current.json"), payload);
  for (const report of currentReports) {
    const summary = summaryByTicker.get(report.ticker);
    await writeJson(path.join(COMPANY_OUTPUT_ROOT, `${report.ticker}.json`), {
      schemaVersion: 1,
      ticker: report.ticker,
      name: summary.name,
      category: summary.category,
      reportDate: report.reportDate,
      priceDate: report.priceDate,
      sourcePath: report.sourcePath,
      summary,
      pairs: buildCompanyPairs(report, currentRun),
      markdown: redactLocalPaths(report.markdown),
    }, false);
  }

  console.log(
    `Company comparison site data: ${summaries.length} companies, ${formatNumber(currentRun.directedRowCount)} directed rows, ${formatNumber(currentRun.pairCount)} reciprocal pairs.`,
  );
  console.log(`Current report dates: ${reportDates.join(", ") || "none"}; previous report dates: ${unique(previousReports.map((report) => report.reportDate)).sort().join(", ") || "none"}.`);
  console.log(`Parse warnings: ${parseWarnings.length}; rank correlation to previous: ${rankCorrelation === null ? "n/a" : round(rankCorrelation, 4)}.`);
  console.log(`Wrote ${OUTPUT_ROOT}`);
}

async function readCompanyIndex() {
  const markdown = await fs.readFile(COMPANY_INDEX_FILE, "utf8");
  const rows = parseMarkdownTables(markdown)
    .flatMap((table) => table.rows)
    .filter((row) => row["股票代号"] && row["公司名称"])
    .map((row) => ({
      ticker: canonicalTicker(row["股票代号"]),
      name: cleanCell(row["公司名称"]),
      category: cleanInline(row["目录"]).replace(/[\\/]+$/, ""),
    }));
  if (rows.length !== EXPECTED_COMPANY_COUNT) {
    throw new Error(`公司索引应有 ${EXPECTED_COMPANY_COUNT} 家，实际 ${rows.length} 家。`);
  }
  return rows;
}

async function findCurrentReports() {
  const dirents = await fs.readdir(RESULT_ROOT, { withFileTypes: true });
  const candidates = [];
  for (const dirent of dirents) {
    if (!dirent.isFile()) continue;
    const match = dirent.name.match(REPORT_PATTERN);
    if (!match) continue;
    const file = path.join(RESULT_ROOT, dirent.name);
    const stat = await fs.stat(file);
    candidates.push({ ticker: canonicalTicker(match[1]), reportDate: match[2], file, sortTime: stat.mtimeMs });
  }
  return chooseLatestByTicker(candidates);
}

async function findPreviousReports(universe) {
  const dirs = await fs.readdir(BACKUP_ROOT, { withFileTypes: true });
  const candidates = [];
  for (const dirent of dirs) {
    if (!dirent.isDirectory()) continue;
    const dir = path.join(BACKUP_ROOT, dirent.name);
    const dirStat = await fs.stat(dir);
    const files = await fs.readdir(dir, { withFileTypes: true });
    for (const fileEntry of files) {
      if (!fileEntry.isFile()) continue;
      const match = fileEntry.name.match(REPORT_PATTERN);
      if (!match) continue;
      const ticker = canonicalTicker(match[1]);
      if (!universe.has(ticker)) continue;
      candidates.push({
        ticker,
        reportDate: match[2],
        file: path.join(dir, fileEntry.name),
        sortTime: dirStat.mtimeMs,
      });
    }
  }
  return chooseLatestByTicker(candidates);
}

function chooseLatestByTicker(candidates) {
  const latest = new Map();
  for (const item of candidates.sort((a, b) => b.sortTime - a.sortTime || b.reportDate.localeCompare(a.reportDate))) {
    if (!latest.has(item.ticker)) latest.set(item.ticker, item);
  }
  return [...latest.values()].sort((a, b) => a.ticker.localeCompare(b.ticker));
}

async function parseReportFile(item, indexByTicker) {
  const markdown = await fs.readFile(item.file, "utf8");
  const rows = [];
  const parseWarnings = [];
  for (const rawRow of parseFixedComparisonRows(markdown)) {
      const sequence = Number(cleanCell(valueByHeader(rawRow, "序号")));
      if (!Number.isFinite(sequence)) continue;
      const companyText = valueByHeader(rawRow, "公司B");
      const opponentTicker = extractTicker(companyText);
      if (!opponentTicker) {
        parseWarnings.push({ ticker: item.ticker, opponent: "", field: "公司B", value: companyText, issue: "无法识别Ticker" });
        continue;
      }
      const opponentIndexed = indexByTicker.get(opponentTicker);
      const dimensions = {};
      for (const dimension of DIMENSIONS) {
        const raw = valueByHeader(rawRow, dimension.header);
        const outcome = parseOutcome(raw, item.ticker, opponentTicker);
        dimensions[dimension.key] = outcome;
        if (outcome.status === "invalid") {
          parseWarnings.push({ ticker: item.ticker, opponent: opponentTicker, field: dimension.label, value: raw, issue: outcome.issue });
        }
      }
      const overallRaw = valueByHeader(rawRow, "总体风险调整判断");
      const overall = parseOutcome(overallRaw, item.ticker, opponentTicker);
      if (overall.status === "invalid") {
        parseWarnings.push({ ticker: item.ticker, opponent: opponentTicker, field: "总体风险调整判断", value: overallRaw, issue: overall.issue });
      }
      rows.push({
        sequence,
        opponentTicker,
        opponentName: extractCompanyName(companyText) || opponentIndexed?.name || opponentTicker,
        opponentCategory: cleanInline(valueByHeader(rawRow, "公司B分类")) || opponentIndexed?.category || "",
        relation: cleanCell(valueByHeader(rawRow, "可比关系")),
        dimensions,
        overall,
        reason: cleanCell(valueByHeader(rawRow, "最关键理由")),
      });
  }
  const dedupedRows = [...new Map(rows.map((row) => [row.opponentTicker, row])).values()].sort((a, b) => a.sequence - b.sequence);
  return {
    ticker: item.ticker,
    name: indexByTicker.get(item.ticker)?.name || item.ticker,
    category: indexByTicker.get(item.ticker)?.category || "",
    reportDate: firstMatch(markdown, /(?:研究截止|生成日期)[:：]\*{0,2}(\d{4}-\d{2}-\d{2})/) || item.reportDate,
    priceDate: firstMatch(markdown, /价格截止[:：]\*{0,2}(\d{4}-\d{2}-\d{2})/) || "",
    sourcePath: `分析报告/公司对比/结果/${path.basename(item.file)}`,
    sourceHash: hashText(markdown),
    markdown,
    rows: dedupedRows,
    parseWarnings,
  };
}

function parseFixedComparisonRows(markdown) {
  const headers = [
    "序号",
    "公司B",
    "公司B分类",
    "可比关系",
    "近端兑现驱动",
    "长期复利质量",
    "价格赔率",
    "防守资本保全",
    "爆发增长与产业突破",
    "市场定价错位",
    "总体风险调整判断",
    "最关键理由",
  ];
  return markdown
    .split(/\r?\n/)
    .filter((line) => /^\|\s*\d+\s*\|/.test(line.trim()))
    .map(splitMarkdownRow)
    .filter((cells) => cells.length === headers.length)
    .map((cells) => Object.fromEntries(headers.map((header, index) => [header, cells[index]])));
}

function validateCurrentReports(reports, companyIndex) {
  const expectedTickers = new Set(companyIndex.map((row) => row.ticker));
  const actualTickers = new Set(reports.map((report) => report.ticker));
  const missing = [...expectedTickers].filter((ticker) => !actualTickers.has(ticker));
  const extra = [...actualTickers].filter((ticker) => !expectedTickers.has(ticker));
  const errors = [];
  if (reports.length !== EXPECTED_COMPANY_COUNT) errors.push(`报告数 ${reports.length}`);
  if (missing.length) errors.push(`缺失 ${missing.join(", ")}`);
  if (extra.length) errors.push(`额外 ${extra.join(", ")}`);
  for (const report of reports) {
    if (report.rows.length !== EXPECTED_COMPANY_COUNT - 1) {
      errors.push(`${report.ticker} 只有 ${report.rows.length} 行`);
    }
    const expectedOpponents = new Set([...expectedTickers].filter((ticker) => ticker !== report.ticker));
    const actualOpponents = new Set(report.rows.map((row) => row.opponentTicker));
    const reportMissing = [...expectedOpponents].filter((ticker) => !actualOpponents.has(ticker));
    const reportExtra = [...actualOpponents].filter((ticker) => !expectedOpponents.has(ticker));
    if (reportMissing.length || reportExtra.length) {
      errors.push(`${report.ticker} 对手集合异常：缺 ${reportMissing.join(",") || "无"}；多 ${reportExtra.join(",") || "无"}`);
    }
  }
  if (errors.length) throw new Error(`公司对比站点数据不完整，拒绝生成：\n- ${errors.slice(0, 30).join("\n- ")}`);
  return { complete: true };
}

function buildRun(reports, companyIndex) {
  const tickers = companyIndex.map((row) => row.ticker);
  const reportByTicker = new Map(reports.map((report) => [report.ticker, report]));
  const overallStats = makeStatsMap(tickers);
  const targetStats = new Map(tickers.map((ticker) => [ticker, { wins: 0, losses: 0, close: 0, unavailable: 0 }]));
  const dimensionStats = Object.fromEntries(DIMENSIONS.map((dimension) => [dimension.key, makeStatsMap(tickers)]));
  const highConfidenceStats = makeStatsMap(tickers);
  let directedRowCount = 0;

  for (const report of reports) {
    for (const row of report.rows) {
      directedRowCount += 1;
      applyOutcome(overallStats, report.ticker, row.opponentTicker, row.overall);
      applyTargetOutcome(targetStats.get(report.ticker), report.ticker, row.opponentTicker, row.overall);
      for (const dimension of DIMENSIONS) {
        const outcome = row.dimensions[dimension.key];
        applyOutcome(dimensionStats[dimension.key], report.ticker, row.opponentTicker, outcome);
        if (outcome.status === "winner" && outcome.confidence === "高" && outcome.strength === 2) {
          applyOutcome(highConfidenceStats, report.ticker, row.opponentTicker, outcome);
        }
      }
    }
  }

  const reciprocal = emptyReciprocal();
  const dimensionReciprocal = Object.fromEntries(DIMENSIONS.map((dimension) => [dimension.key, emptyReciprocal()]));
  const consistentStats = makeStatsMap(tickers);
  const companyReciprocal = new Map(tickers.map((ticker) => [ticker, emptyCompanyReciprocal()]));
  const pairStatus = new Map();
  const pairCount = (tickers.length * (tickers.length - 1)) / 2;

  for (let i = 0; i < tickers.length; i += 1) {
    for (let j = i + 1; j < tickers.length; j += 1) {
      const a = tickers[i];
      const b = tickers[j];
      const rowFromA = reportByTicker.get(a)?.rows.find((row) => row.opponentTicker === b);
      const rowFromB = reportByTicker.get(b)?.rows.find((row) => row.opponentTicker === a);
      const status = classifyReciprocal(a, b, rowFromA?.overall, rowFromB?.overall);
      reciprocal[status] += 1;
      pairStatus.set(pairKey(a, b), status);
      incrementCompanyReciprocal(companyReciprocal.get(a), status);
      incrementCompanyReciprocal(companyReciprocal.get(b), status);
      if (status === "sameWinner") {
        const winner = rowFromA.overall.winner;
        const loser = winner === a ? b : a;
        consistentStats.get(winner).wins += 1;
        consistentStats.get(loser).losses += 1;
      }
      for (const dimension of DIMENSIONS) {
        const dimensionStatus = classifyReciprocal(a, b, rowFromA?.dimensions[dimension.key], rowFromB?.dimensions[dimension.key]);
        dimensionReciprocal[dimension.key][dimensionStatus] += 1;
      }
    }
  }

  return {
    reports,
    reportByTicker,
    directedRowCount,
    pairCount,
    overallStats,
    targetStats,
    dimensionStats,
    highConfidenceStats,
    reciprocal,
    dimensionReciprocal,
    companyReciprocal,
    pairStatus,
    overallRanking: rankStats(overallStats),
    consistentRanking: rankStats(consistentStats),
    highConfidenceRanking: rankStats(highConfidenceStats),
    dimensionRankings: Object.fromEntries(DIMENSIONS.map((dimension) => [dimension.key, rankStats(dimensionStats[dimension.key])])),
  };
}

function buildCompanySummaries(currentRun, previousRun, companyIndex) {
  const indexByTicker = new Map(companyIndex.map((row) => [row.ticker, row]));
  const overallByTicker = indexRanking(currentRun.overallRanking);
  const consistentByTicker = indexRanking(currentRun.consistentRanking);
  const highByTicker = indexRanking(currentRun.highConfidenceRanking);
  const previousByTicker = previousRun ? indexRanking(previousRun.overallRanking) : new Map();
  const dimensionByTicker = Object.fromEntries(DIMENSIONS.map((dimension) => [dimension.key, indexRanking(currentRun.dimensionRankings[dimension.key])]));

  return currentRun.overallRanking.map((overall) => {
    const ticker = overall.ticker;
    const indexed = indexByTicker.get(ticker);
    const report = currentRun.reportByTicker.get(ticker);
    const self = currentRun.targetStats.get(ticker);
    const reciprocal = currentRun.companyReciprocal.get(ticker);
    const consistent = consistentByTicker.get(ticker);
    const high = highByTicker.get(ticker);
    const previous = previousByTicker.get(ticker);
    const dimensionStats = Object.fromEntries(
      DIMENSIONS.map((dimension) => {
        const ranked = dimensionByTicker[dimension.key].get(ticker);
        return [dimension.key, { key: dimension.key, label: dimension.label, ...ranked }];
      }),
    );
    const breadthTop20 = DIMENSIONS.filter((dimension) => dimensionStats[dimension.key].rank <= 20).length;
    const strongestStyles = Object.values(dimensionStats)
      .sort((a, b) => a.rank - b.rank)
      .slice(0, 3)
      .map((row) => ({ thought: row.label, score: row.net, rank: row.rank }));
    const weakestStyles = Object.values(dimensionStats)
      .sort((a, b) => b.rank - a.rank)
      .slice(0, 3)
      .map((row) => ({ thought: row.label, score: row.net, rank: row.rank }));
    const rankChange = previous ? previous.rank - overall.rank : null;
    const archetype = classifyArchetype({ overall, consistent, high, breadthTop20, dimensionStats });
    return {
      ticker,
      name: indexed?.name || ticker,
      category: indexed?.category || "",
      reportDate: report?.reportDate || "",
      sourcePath: report?.sourcePath || "",
      dataFile: `reports/company-comparison/${ticker}.json`,
      comparedCount: report?.rows.length || 0,
      rank: overall.rank,
      finalRank: overall.rank,
      previousRank: previous?.rank || null,
      rankChange,
      wins: overall.wins,
      losses: overall.losses,
      close: overall.close,
      unavailable: overall.unavailable,
      net: overall.net,
      finalWins: overall.wins,
      finalLosses: overall.losses,
      finalNet: overall.net,
      selfWins: self.wins,
      selfLosses: self.losses,
      selfClose: self.close,
      selfUnknown: self.unavailable,
      selfNet: self.wins - self.losses,
      consistentRank: consistent.rank,
      consistentWins: consistent.wins,
      consistentLosses: consistent.losses,
      consistentNet: consistent.net,
      highConfidenceRank: high.rank,
      highConfidenceWins: high.wins,
      highConfidenceLosses: high.losses,
      highConfidenceNet: high.net,
      reciprocal,
      reciprocalConflictRate: round(((reciprocal.eachOther + reciprocal.eachSelf) / Math.max(1, currentRun.reports.length - 1)) * 100, 1),
      breadthTop20,
      archetype,
      dimensionStats,
      strongestStyles,
      weakestStyles,
      onePage: [
        `总体风险调整 #${overall.rank}；双向一致 #${consistent.rank}；六维高置信 #${high.rank}。`,
        `${breadthTop20} 个投资哲学进入前20，类型为“${archetype}”。`,
        previous ? `相较上一版${rankChange > 0 ? `上升 ${rankChange}` : rankChange < 0 ? `下降 ${Math.abs(rankChange)}` : "排名不变"}。` : "暂无上一版可比排名。",
      ],
    };
  });
}

function buildCompanyPairs(report, run) {
  return report.rows.map((row) => {
    const reverse = run.reportByTicker.get(row.opponentTicker)?.rows.find((item) => item.opponentTicker === report.ticker);
    const reciprocalStatus = classifyReciprocal(report.ticker, row.opponentTicker, row.overall, reverse?.overall);
    return {
      sequence: row.sequence,
      opponentTicker: row.opponentTicker,
      opponentName: row.opponentName,
      opponentCategory: row.opponentCategory,
      relation: row.relation,
      overall: publicOutcome(row.overall),
      reason: row.reason,
      reciprocal: {
        status: reciprocalStatus,
        reverseOverall: publicOutcome(reverse?.overall),
      },
    };
  });
}

function buildDimensionCorrelation(summaries) {
  return Object.fromEntries(
    DIMENSIONS.map((left) => [
      left.key,
      Object.fromEntries(
        DIMENSIONS.map((right) => [
          right.key,
          round(
            spearman(
              summaries.map((row) => row.dimensionStats[left.key].rank),
              summaries.map((row) => row.dimensionStats[right.key].rank),
            ),
            4,
          ),
        ]),
      ),
    ]),
  );
}

function buildCategoryStats(summaries) {
  const groups = new Map();
  for (const row of summaries) {
    if (!groups.has(row.category)) groups.set(row.category, []);
    groups.get(row.category).push(row);
  }
  return [...groups.entries()]
    .map(([category, rows]) => {
      const ordered = [...rows].sort((a, b) => a.finalRank - b.finalRank);
      const ranks = rows.map((row) => row.finalRank).sort((a, b) => a - b);
      return {
        category,
        companyCount: rows.length,
        averageRank: round(rows.reduce((sum, row) => sum + row.finalRank, 0) / rows.length, 1),
        medianRank: median(ranks),
        top20Count: rows.filter((row) => row.finalRank <= 20).length,
        leader: ordered[0]?.ticker || "",
        leaderRank: ordered[0]?.finalRank || null,
      };
    })
    .sort((a, b) => a.averageRank - b.averageRank);
}

function buildInsights(summaries) {
  const byRank = [...summaries].sort((a, b) => a.finalRank - b.finalRank);
  const byChange = summaries.filter((row) => row.rankChange !== null).sort((a, b) => b.rankChange - a.rankChange);
  return {
    robustCore: byRank.filter((row) => row.finalRank <= 25 && row.consistentRank <= 25 && row.highConfidenceRank <= 25 && row.breadthTop20 >= 3).slice(0, 10).map(compactCompany),
    valueSpecialists: byRank.filter((row) => (row.dimensionStats.odds.rank <= 20 || row.dimensionStats.mispricing.rank <= 20) && row.breadthTop20 <= 3).slice(0, 10).map(compactCompany),
    offenseCandidates: [...summaries].filter((row) => row.dimensionStats.explosion.rank <= 20 || row.dimensionStats.near.rank <= 20).sort((a, b) => Math.min(a.dimensionStats.explosion.rank, a.dimensionStats.near.rank) - Math.min(b.dimensionStats.explosion.rank, b.dimensionStats.near.rank)).slice(0, 12).map(compactCompany),
    biggestRisers: byChange.slice(0, 10).map(compactCompany),
    biggestFallers: byChange.slice(-10).reverse().map(compactCompany),
  };
}

function compactCompany(row) {
  return {
    ticker: row.ticker,
    name: row.name,
    rank: row.finalRank,
    previousRank: row.previousRank,
    rankChange: row.rankChange,
    archetype: row.archetype,
  };
}

function classifyArchetype({ overall, consistent, high, breadthTop20, dimensionStats }) {
  if (overall.rank <= 25 && consistent.rank <= 25 && high.rank <= 25 && breadthTop20 >= 3) return "综合核心";
  if (dimensionStats.near.rank <= 20 && dimensionStats.explosion.rank <= 20) return "进攻爆发";
  if (dimensionStats.long.rank <= 20 && dimensionStats.defense.rank <= 20) return "复利防守";
  if ((dimensionStats.odds.rank <= 20 || dimensionStats.mispricing.rank <= 20) && (dimensionStats.near.rank > 50 || dimensionStats.explosion.rank > 50)) return "价格修复";
  if (dimensionStats.explosion.rank <= 20) return "爆发候选";
  if (overall.rank <= 40) return "均衡候选";
  return "观察";
}

function buildRelationStats(report) {
  const groups = new Map();
  for (const row of report?.rows || []) {
    const key = row.relation || "未分类";
    if (!groups.has(key)) groups.set(key, { relation: key, total: 0, wins: 0, losses: 0, close: 0, unknown: 0 });
    const group = groups.get(key);
    group.total += 1;
    if (row.overall.status === "winner" && row.overall.winner === report.ticker) group.wins += 1;
    else if (row.overall.status === "winner") group.losses += 1;
    else if (row.overall.status === "close") group.close += 1;
    else group.unknown += 1;
  }
  return [...groups.values()].sort((a, b) => b.total - a.total || a.relation.localeCompare(b.relation, "zh-Hans-CN"));
}

function buildDirectPeers(report) {
  return (report?.rows || [])
    .filter((row) => row.relation === "直接同业")
    .map((row) => ({ ticker: row.opponentTicker, company: row.opponentName, final: row.overall.text, reason: row.reason }));
}

function buildLosses(report) {
  return (report?.rows || [])
    .filter((row) => row.overall.status === "winner" && row.overall.winner === row.opponentTicker)
    .slice(0, 30)
    .map((row) => ({ ticker: row.opponentTicker, company: row.opponentName, relation: row.relation, reason: row.reason }));
}

function applyOutcome(stats, aTicker, bTicker, outcome) {
  const a = stats.get(aTicker);
  const b = stats.get(bTicker);
  if (!a || !b) return;
  if (outcome?.status === "winner") {
    const winner = stats.get(outcome.winner);
    const loser = stats.get(outcome.winner === aTicker ? bTicker : aTicker);
    if (!winner || !loser) return;
    winner.wins += 1;
    loser.losses += 1;
  } else if (outcome?.status === "close") {
    a.close += 1;
    b.close += 1;
  } else {
    a.unavailable += 1;
    b.unavailable += 1;
  }
}

function applyTargetOutcome(stats, aTicker, bTicker, outcome) {
  if (outcome?.status === "winner") {
    if (outcome.winner === aTicker) stats.wins += 1;
    else if (outcome.winner === bTicker) stats.losses += 1;
    else stats.unavailable += 1;
  } else if (outcome?.status === "close") stats.close += 1;
  else stats.unavailable += 1;
}

function classifyReciprocal(aTicker, bTicker, fromA, fromB) {
  if (!fromA || !fromB || [fromA.status, fromB.status].some((status) => status === "unavailable" || status === "invalid")) return "unavailable";
  if (fromA.status === "close" && fromB.status === "close") return "bothClose";
  if (fromA.status === "close" || fromB.status === "close") return "oneDecisiveOneClose";
  if (fromA.status === "winner" && fromB.status === "winner" && fromA.winner === fromB.winner) return "sameWinner";
  if (fromA.winner === bTicker && fromB.winner === aTicker) return "eachOther";
  if (fromA.winner === aTicker && fromB.winner === bTicker) return "eachSelf";
  return "unavailable";
}

function incrementCompanyReciprocal(stats, status) {
  stats[status] += 1;
}

function makeStatsMap(tickers) {
  return new Map(tickers.map((ticker) => [ticker, { ticker, wins: 0, losses: 0, close: 0, unavailable: 0 }]));
}

function rankStats(stats) {
  const rows = [...stats.values()]
    .map((row) => ({ ...row, net: row.wins - row.losses }))
    .sort((a, b) => b.net - a.net || b.wins - a.wins || a.losses - b.losses || a.ticker.localeCompare(b.ticker));
  rows.forEach((row, index) => {
    row.rank = index + 1;
  });
  return rows;
}

function indexRanking(ranking) {
  return new Map(ranking.map((row) => [row.ticker, row]));
}

function attachCompanyMeta(rows, indexByTicker) {
  return rows.map((row) => ({
    ...row,
    name: indexByTicker.get(row.ticker)?.name || row.ticker,
    category: indexByTicker.get(row.ticker)?.category || "",
  }));
}

function emptyReciprocal() {
  return { sameWinner: 0, eachOther: 0, eachSelf: 0, oneDecisiveOneClose: 0, bothClose: 0, unavailable: 0 };
}

function emptyCompanyReciprocal() {
  return emptyReciprocal();
}

function addPercentages(counts, total) {
  return {
    total,
    ...counts,
    percentages: Object.fromEntries(Object.entries(counts).map(([key, value]) => [key, round((value / Math.max(1, total)) * 100, 2)])),
  };
}

function parseOutcome(rawText, aTicker, bTicker) {
  const text = cleanInline(rawText);
  const confidence = firstMatch(text, /([高中低])置信/) || "";
  if (!text) return { status: "unavailable", winner: "", confidence, strength: 0, text: "" };
  if (/^(接近|难分|大致平衡|基本平衡)/.test(text)) return { status: "close", winner: "", confidence, strength: 0, text };
  if (/^(资料不足|信息不足|无法判断|不可判断)/.test(text)) return { status: "unavailable", winner: "", confidence, strength: 0, text };
  const sideMatch = text.match(/^([AB])\s*(?:明显更优|略优|更优)/i);
  const tickerMatch = text.match(/^([A-Z0-9.-]+)\s*(?=明显更优|略优|更优|：|:|（|\(|$)/i);
  const candidate = sideMatch ? (sideMatch[1].toUpperCase() === "A" ? aTicker : bTicker) : tickerMatch ? canonicalTicker(tickerMatch[1]) : "";
  if (candidate === aTicker || candidate === bTicker) {
    return {
      status: "winner",
      winner: candidate,
      confidence,
      strength: text.includes("明显更优") ? 2 : 1,
      text,
    };
  }
  return {
    status: "invalid",
    winner: "",
    confidence,
    strength: 0,
    text,
    issue: candidate ? `胜方 ${candidate} 不属于 ${aTicker}/${bTicker}` : "无法解析胜方",
  };
}

function publicOutcome(outcome) {
  if (!outcome) return { status: "unavailable", winner: "", confidence: "", strength: 0, text: "" };
  return {
    status: outcome.status,
    winner: outcome.winner || "",
    confidence: outcome.confidence || "",
    strength: outcome.strength || 0,
    text: outcome.text || "",
  };
}

function parseMarkdownTables(markdown) {
  const lines = markdown.split(/\r?\n/);
  const tables = [];
  for (let index = 0; index < lines.length - 1; index += 1) {
    if (!lines[index].trim().startsWith("|")) continue;
    const headers = splitMarkdownRow(lines[index]);
    const separator = splitMarkdownRow(lines[index + 1]);
    if (!headers.length || separator.length !== headers.length || !separator.every((cell) => /^:?-{3,}:?$/.test(cell.replace(/\s/g, "")))) continue;
    const rows = [];
    let cursor = index + 2;
    while (cursor < lines.length && lines[cursor].trim().startsWith("|")) {
      const cells = splitMarkdownRow(lines[cursor]);
      if (cells.length === headers.length) {
        rows.push(Object.fromEntries(headers.map((header, cellIndex) => [header, cells[cellIndex]])));
      }
      cursor += 1;
    }
    tables.push({ headers, normalizedHeaders: headers.map(normalizeHeader), rows });
    index = cursor - 1;
  }
  return tables;
}

function splitMarkdownRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map(cleanCell);
}

function valueByHeader(row, desiredHeader) {
  const desired = normalizeHeader(desiredHeader);
  const key = Object.keys(row).find((header) => normalizeHeader(header) === desired);
  return key ? row[key] : "";
}

function normalizeHeader(value) {
  return cleanCell(value).replace(/\s+/g, "").replace(/[（）()]/g, "");
}

function cleanCell(value) {
  return String(value ?? "").replace(/<br\s*\/?>/gi, " ").trim();
}

function cleanInline(value) {
  return cleanCell(value)
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTicker(value) {
  const match = cleanInline(value).match(/^([A-Z0-9.-]+)/i);
  return match ? canonicalTicker(match[1]) : "";
}

function extractCompanyName(value) {
  const text = cleanInline(value);
  const slash = text.indexOf("/");
  return slash >= 0 ? text.slice(slash + 1).trim() : "";
}

function canonicalTicker(value) {
  const ticker = cleanCell(value).toUpperCase();
  return TICKER_ALIASES.get(ticker) || ticker;
}

function firstMatch(text, pattern) {
  return String(text ?? "").match(pattern)?.[1]?.trim() || "";
}

function pairKey(a, b) {
  return [a, b].sort().join("|");
}

function spearman(left, right) {
  const pairs = left.map((value, index) => [Number(value), Number(right[index])]).filter(([a, b]) => Number.isFinite(a) && Number.isFinite(b));
  if (pairs.length < 2) return null;
  const leftMean = pairs.reduce((sum, pair) => sum + pair[0], 0) / pairs.length;
  const rightMean = pairs.reduce((sum, pair) => sum + pair[1], 0) / pairs.length;
  let numerator = 0;
  let leftSquare = 0;
  let rightSquare = 0;
  for (const [a, b] of pairs) {
    const leftDelta = a - leftMean;
    const rightDelta = b - rightMean;
    numerator += leftDelta * rightDelta;
    leftSquare += leftDelta ** 2;
    rightSquare += rightDelta ** 2;
  }
  const denominator = Math.sqrt(leftSquare * rightSquare);
  return denominator ? numerator / denominator : null;
}

function median(values) {
  if (!values.length) return null;
  const middle = Math.floor(values.length / 2);
  return values.length % 2 ? values[middle] : round((values[middle - 1] + values[middle]) / 2, 1);
}

function mostCommon(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) || 0) + 1);
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || b[0].localeCompare(a[0]))[0]?.[0] || "";
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function round(value, digits = 2) {
  if (value === null || value === undefined || !Number.isFinite(value)) return null;
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function hashText(value) {
  return crypto.createHash("sha256").update(String(value)).digest("hex");
}

function formatNumber(value) {
  return Number(value).toLocaleString("en-US");
}

function redactLocalPaths(markdown) {
  return String(markdown).replace(/[A-Z]:\\drive\\Investment\\/gi, "Investment/").replace(/[A-Z]:\/drive\/Investment\//gi, "Investment/");
}

async function prepareOutput() {
  const resolved = path.resolve(OUTPUT_ROOT);
  const expected = path.resolve(DEFAULT_OUTPUT_ROOT);
  const isStaging = path.basename(resolved).startsWith(".站点数据-");
  if (path.dirname(resolved) !== path.resolve(ROOT) || (resolved !== expected && !isStaging)) {
    throw new Error(`拒绝清理非预期目录：${resolved}`);
  }
  await fs.rm(resolved, { recursive: true, force: true });
  await fs.mkdir(COMPANY_OUTPUT_ROOT, { recursive: true });
}

async function writeJson(file, value, pretty = true) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${JSON.stringify(value, null, pretty ? 2 : 0)}\n`, "utf8");
}

main().catch((error) => {
  console.error(error.stack || error.message || error);
  process.exitCode = 1;
});
