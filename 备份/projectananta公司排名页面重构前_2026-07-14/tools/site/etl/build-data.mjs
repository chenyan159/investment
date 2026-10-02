import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, "..");
const PROJECT_ROOT = path.resolve(SITE_ROOT, "..", "..");
const PUBLIC_DATA = path.join(SITE_ROOT, "public", "data");
const COMPANY_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "company");
const COMPANY_EVALUATION_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "company-evaluation");
const COMPANY_COMPARISON_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "company-comparison");
const INDUSTRY_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "industry");

const FUND_ROOT = path.join(PROJECT_ROOT, "基本面");
const COMPANY_ROOT = path.join(FUND_ROOT, "公司调研");
const INDUSTRY_ROOT = path.join(FUND_ROOT, "行业调研");
const COMPANY_SORTING_ROOT = path.join(FUND_ROOT, "分析报告", "公司排序");
const COMPANY_SORTING_RUN_REGISTRY = path.join(COMPANY_SORTING_ROOT, "00_运行与榜单注册表.csv");
const COMPANY_SORTING_CURRENT_EVALUATION = path.join(COMPANY_SORTING_ROOT, "00_当前评估.json");
const COMPANY_EVALUATION_ROOT = path.join(FUND_ROOT, "分析报告", "公司评估");
const COMPANY_COMPARISON_ROOT = path.join(FUND_ROOT, "分析报告", "公司对比");
const COMPANY_COMPARISON_SITE_DATA_ROOT = path.join(COMPANY_COMPARISON_ROOT, "站点数据");
const COMPANY_COMPARISON_CURRENT_DATA = path.join(COMPANY_COMPARISON_SITE_DATA_ROOT, "current.json");
const FEATURE_QUANT_ROOT = path.join(FUND_ROOT, "特征量化");
const FEATURE_ROOT = path.join(FEATURE_QUANT_ROOT, "量化评分");
const EFFECTIVE_FEATURE_REGISTRY = path.join(FEATURE_QUANT_ROOT, "有效指标清单_latest.json");
const FEATURE_SCORE_FILE_PATTERN = /^([NG]\d{2})_([\s\S]+)_量化评分_(\d{4}-\d{2}-\d{2})\.md$/u;
const DEFAULT_ALPHA_FEATURE_IDS = Array.from({ length: 16 }, (_, index) => `N${String(index + 1).padStart(2, "0")}`);
const DEFAULT_GATE_IDS = Array.from({ length: 3 }, (_, index) => `G${String(index + 1).padStart(2, "0")}`);
const TICKER_ALIASES = new Map([
  ["PSTG", "P"],
]);
const FINANCE_ROOT = path.join(FUND_ROOT, "日度资料", "每日金融数据");
const DAILY_NEWS_ROOT = path.join(FUND_ROOT, "日度资料", "最新AI新闻");
const DAILY_NEWS_SCRIPT_ROOT = path.join(DAILY_NEWS_ROOT, "新闻稿");
const DAILY_NEWS_AUDIO_ROOT = path.join(DAILY_NEWS_ROOT, "语音输出");
const DAILY_NEWS_PUBLIC_DIR = path.join(PUBLIC_DATA, "daily-news");
const DAILY_NEWS_AUDIO_DIR = path.join(DAILY_NEWS_PUBLIC_DIR, "audio");
const DAILY_NEWS_LIMIT = 10;

const companyToIndustryCategory = {
  "AI服务器_存储_EMS": "AI服务器_存储_芯片",
  "AI计算芯片_EDA_IP_custom_ASIC": "AI服务器_存储_芯片",
  "AI网络_光互联_连接器": "AI网络_光互联_铜互联",
  "半导体材料_化学品_基板": "晶圆制造_设备_材料_测试",
  "电力_发电_能源_储能": "AI园区电力_机电_冷却",
  "封测_检测_计量_光罩": "晶圆制造_设备_材料_测试",
  "机电_冷却_工程_水处理_边缘工业AI": "AI园区电力_机电_冷却",
  "晶圆制造_前道设备": "晶圆制造_设备_材料_测试",
  "配电_电源_功率器件": "AI园区电力_机电_冷却",
  "云算力_IDC_AI软件平台": "AI服务器_存储_芯片",
};

async function main() {
  await prepareOutput();
  const companyIndex = await parseCompanyIndex();
  const industryIndex = await parseIndustryIndex();
  const industryReports = await buildIndustryReports(industryIndex);
  const companyEvaluations = await buildCompanyEvaluations(companyIndex);
  const companies = await buildCompanies(companyIndex, industryReports, companyEvaluations);
  const companyComparisons = await buildCompanyComparisons(companyIndex);
  const rankings = await buildRankings(companyIndex);
  const features = await buildFeatures(companies);
  const dailyNews = await buildDailyNews();
  const industries = attachIndustryCompanyCounts(industryIndex, industryReports, companies, rankings);
  const duplicateCompanyReports = await findDuplicateCompanyReports(companyIndex);
  const latestFinancialDate = await latestDateFromFiles(FINANCE_ROOT, /^每日金融数据_(\d{4}-\d{2}-\d{2})\.md$/);
  const quality = buildQuality({
    companies,
    companyIndex,
    industries,
    industryIndex,
    rankings,
    features,
    industryReports,
    duplicateCompanyReports,
    dailyNews,
    companyComparisons,
  });
  const meta = buildMeta({ companies, industries, rankings, features, quality, latestFinancialDate, dailyNews, companyComparisons });

  await writeJson(path.join(PUBLIC_DATA, "meta.json"), meta);
  await writeJson(path.join(PUBLIC_DATA, "companies.json"), companies);
  await writeJson(path.join(PUBLIC_DATA, "industries.json"), industries);
  await writeJson(path.join(PUBLIC_DATA, "rankings.json"), rankings);
  await writeJson(path.join(PUBLIC_DATA, "company-comparisons.json"), companyComparisons);
  await writeJson(path.join(PUBLIC_DATA, "features.json"), features);
  await writeJson(path.join(PUBLIC_DATA, "quality.json"), quality);
  await writeJson(path.join(PUBLIC_DATA, "daily-news.json"), dailyNews);

  console.log(`Wrote site data to ${PUBLIC_DATA}`);
  console.log(
    `Companies: ${companies.length}, comparisons: ${companyComparisons.companies.length}, industries: ${industries.length}, features: ${features.features.length}, effective features: ${features.effectiveFeatureIds.length}, daily news: ${dailyNews.items.length}`,
  );
}

async function prepareOutput() {
  await fs.mkdir(PUBLIC_DATA, { recursive: true });
  await fs.rm(DAILY_NEWS_PUBLIC_DIR, { recursive: true, force: true });
  await fs.mkdir(COMPANY_REPORT_DIR, { recursive: true });
  await fs.mkdir(COMPANY_EVALUATION_REPORT_DIR, { recursive: true });
  await fs.mkdir(COMPANY_COMPARISON_REPORT_DIR, { recursive: true });
  await fs.mkdir(INDUSTRY_REPORT_DIR, { recursive: true });
  await fs.mkdir(DAILY_NEWS_AUDIO_DIR, { recursive: true });
  await cleanJsonDir(COMPANY_REPORT_DIR);
  await cleanJsonDir(COMPANY_EVALUATION_REPORT_DIR);
  await cleanJsonDir(COMPANY_COMPARISON_REPORT_DIR);
  await cleanJsonDir(INDUSTRY_REPORT_DIR);
  await cleanGeneratedMetadata(path.join(SITE_ROOT, "public"));
}

async function cleanJsonDir(dir) {
  const files = await safeReadDir(dir);
  await Promise.all(files.filter((name) => name.endsWith(".json")).map((name) => fs.rm(path.join(dir, name), { force: true })));
}

async function cleanGeneratedMetadata(dir) {
  const dirents = await safeReadDirents(dir);
  for (const dirent of dirents) {
    const target = path.join(dir, dirent.name);
    if (dirent.isDirectory()) {
      await cleanGeneratedMetadata(target);
    } else if (dirent.name.toLowerCase() === "desktop.ini") {
      await fs.rm(target, { force: true });
    }
  }
}

async function parseCompanyIndex() {
  const file = path.join(COMPANY_ROOT, "公司索引.md");
  const text = await readText(file);
  const rows = parseMarkdownTables(text)
    .flat()
    .filter((row) => row["股票代号"] && row["公司名称"]);
  return rows.map((row) => ({
    ticker: cleanCell(row["股票代号"]).toUpperCase(),
    name: cleanCell(row["公司名称"]),
    category: cleanCell(row["目录"]).replace(/[\\/]+$/, ""),
  }));
}

async function parseIndustryIndex() {
  const file = path.join(INDUSTRY_ROOT, "行业索引.md");
  const text = await readText(file);
  const rows = parseMarkdownTables(text)
    .flat()
    .filter((row) => row["行业名称"] && row["目录"]);
  return rows.map((row) => ({
    name: cleanCell(row["行业名称"]),
    category: cleanCell(row["目录"]).replace(/[\\/]+$/, ""),
    slug: stableSlug(cleanCell(row["行业名称"])),
  }));
}

async function buildCompanyEvaluations(indexRows) {
  const dirents = await safeReadDirents(COMPANY_EVALUATION_ROOT);
  const files = dirents
    .filter((dirent) => dirent.isFile() && dirent.name.toLowerCase().endsWith(".md"))
    .map((dirent) => path.join(COMPANY_EVALUATION_ROOT, dirent.name));
  const evaluationsByTicker = new Map();

  for (const row of indexRows) {
    const candidates = files.filter((file) => companyEvaluationFileMatches(row.ticker, path.basename(file)));
    if (!candidates.length) continue;

    const evaluationPath = chooseLatestFile(candidates);
    const content = redactLocalPaths(await readText(evaluationPath));
    const meta = parseReportMeta(content, evaluationPath);
    const dataFile = `reports/company-evaluation/${row.ticker}.json`;
    const evaluation = {
      title: meta.title,
      reportDate: meta.reportDate,
      sourcePath: relativePath(evaluationPath),
      dataFile,
    };
    await writeJson(path.join(PUBLIC_DATA, dataFile), {
      ticker: row.ticker,
      name: row.name,
      category: row.category,
      ...evaluation,
      markdown: content,
    });
    evaluationsByTicker.set(row.ticker, evaluation);
  }

  return evaluationsByTicker;
}

async function buildCompanies(indexRows, industryReports, companyEvaluations) {
  const reportFiles = await directMarkdownFilesByCategory(COMPANY_ROOT, ["研究方法", "tmp", "评估备份"]);
  const reportsByTicker = new Map();
  for (const row of indexRows) {
    const categoryFiles = reportFiles.get(row.category) || [];
    const candidates = categoryFiles.filter((file) => tickerInFileName(row.ticker, path.basename(file)));
    if (candidates.length) {
      reportsByTicker.set(row.ticker, chooseLatestFile(candidates));
    }
  }

  const industryByCategory = new Map();
  for (const industry of industryReports.values()) {
    if (!industryByCategory.has(industry.category)) industryByCategory.set(industry.category, []);
    industryByCategory.get(industry.category).push(industry.slug);
  }

  const companies = [];
  for (const row of indexRows) {
    const reportPath = reportsByTicker.get(row.ticker);
    const evaluation = companyEvaluations.get(row.ticker) || null;
    const relatedIndustryCategory = companyToIndustryCategory[row.category];
    const relatedIndustrySlugs = relatedIndustryCategory ? industryByCategory.get(relatedIndustryCategory) || [] : [];
    let report = null;
    if (reportPath) {
      const content = redactLocalPaths(await readText(reportPath));
      const meta = parseReportMeta(content, reportPath);
      const dataFile = `reports/company/${row.ticker}.json`;
      report = {
        title: meta.title,
        reportDate: meta.reportDate,
        sourcePath: relativePath(reportPath),
        dataFile,
      };
      await writeJson(path.join(PUBLIC_DATA, dataFile), {
        ticker: row.ticker,
        name: row.name,
        category: row.category,
        ...report,
        markdown: content,
      });
    }
    companies.push({
      ticker: row.ticker,
      name: row.name,
      category: row.category,
      relatedIndustrySlugs,
      hasReport: Boolean(report),
      hasEvaluation: Boolean(evaluation),
      report,
      evaluation,
    });
  }
  return companies;
}

async function buildCompanyComparisons(indexRows) {
  const payload = JSON.parse(await readText(COMPANY_COMPARISON_CURRENT_DATA));
  const expectedCompanyCount = indexRows.length;
  const expectedDirectedRows = expectedCompanyCount * (expectedCompanyCount - 1);
  const expectedPairCount = expectedDirectedRows / 2;
  const expectedTickers = new Set(indexRows.map((row) => row.ticker));
  const actualTickers = new Set((payload.companies || []).map((row) => row.ticker));
  const missing = [...expectedTickers].filter((ticker) => !actualTickers.has(ticker));
  const extra = [...actualTickers].filter((ticker) => !expectedTickers.has(ticker));

  const errors = [];
  if (!payload.quality?.complete) errors.push("上游站点数据未标记为完整");
  if (payload.companyCount !== expectedCompanyCount || payload.companies?.length !== expectedCompanyCount) {
    errors.push(`公司数应为 ${expectedCompanyCount}，实际 ${payload.companyCount}/${payload.companies?.length || 0}`);
  }
  if (payload.rowCount !== expectedDirectedRows) errors.push(`定向记录应为 ${expectedDirectedRows}，实际 ${payload.rowCount}`);
  if (payload.pairCount !== expectedPairCount) errors.push(`公司对应为 ${expectedPairCount}，实际 ${payload.pairCount}`);
  if (missing.length) errors.push(`缺失公司：${missing.join(", ")}`);
  if (extra.length) errors.push(`额外公司：${extra.join(", ")}`);

  for (const row of payload.companies || []) {
    const source = path.join(COMPANY_COMPARISON_SITE_DATA_ROOT, "companies", `${row.ticker}.json`);
    const detail = JSON.parse(await readText(source));
    if (detail.pairs?.length !== expectedCompanyCount - 1) {
      errors.push(`${row.ticker} 明细应有 ${expectedCompanyCount - 1} 个对手，实际 ${detail.pairs?.length || 0}`);
      continue;
    }
    const target = path.join(PUBLIC_DATA, row.dataFile);
    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.copyFile(source, target);
  }

  if (errors.length) {
    throw new Error(`公司横评站点数据校验失败：\n- ${errors.slice(0, 30).join("\n- ")}`);
  }
  return payload;
}

async function buildIndustryReports(indexRows) {
  const reportFiles = await directMarkdownFilesByCategory(INDUSTRY_ROOT, ["研究方法", "产业背景"]);
  const byStandardName = new Map();
  const bySlug = new Map();

  for (const [category, files] of reportFiles.entries()) {
    for (const file of files) {
      const content = redactLocalPaths(await readText(file));
      const meta = parseIndustryMeta(content, file, category);
      const canonical = canonicalIndustryKey(meta.standardName);
      const slug = stableSlug(meta.standardName);
      const dataFile = `reports/industry/${slug}.json`;
      const report = {
        name: meta.standardName,
        slug,
        category: meta.category || category,
        reportDate: meta.reportDate,
        title: meta.title,
        sourcePath: relativePath(file),
        dataFile,
      };
      byStandardName.set(canonical, report);
      bySlug.set(slug, report);
      await writeJson(path.join(PUBLIC_DATA, dataFile), {
        ...report,
        markdown: content,
      });
    }
  }

  for (const row of indexRows) {
    const canonical = canonicalIndustryKey(row.name);
    const matched = byStandardName.get(canonical) || bySlug.get(stableSlug(row.name));
    if (matched) {
      matched.indexName = row.name;
      matched.indexCategory = row.category;
    }
  }

  return byStandardName;
}

function attachIndustryCompanyCounts(indexRows, reportMap, companies, rankings) {
  const defaultRows = rankings.runs[rankings.defaultRunKey]?.rows || Object.values(rankings.runs)[0]?.rows || [];
  const rankingByTicker = new Map(defaultRows.map((row) => [row.ticker, row]));
  return indexRows.map((row) => {
    const report = reportMap.get(canonicalIndustryKey(row.name)) || null;
    const relatedCompanies = companies.filter((company) => company.relatedIndustrySlugs.includes(row.slug));
    const rankedCompanies = relatedCompanies
      .map((company) => rankingByTicker.get(company.ticker))
      .filter(Boolean)
      .sort((a, b) => Number(a.rank) - Number(b.rank));
    return {
      ...row,
      companyCount: relatedCompanies.length,
      topCompanyTickers: rankedCompanies.slice(0, 8).map((r) => r.ticker),
      hasReport: Boolean(report),
      hasReportText: report ? "有" : "缺失",
      reportDate: report?.reportDate || "",
      report,
    };
  });
}

async function buildRankings(companyIndex) {
  const registryRows = parseCsv(await readText(COMPANY_SORTING_RUN_REGISTRY))
    .filter((row) => String(row.is_current).toLowerCase() === "true")
    .sort((a, b) => (parseNumber(a.display_order) ?? 9999) - (parseNumber(b.display_order) ?? 9999));
  const evaluation = JSON.parse(await readText(COMPANY_SORTING_CURRENT_EVALUATION));
  if (Number(evaluation.schema_version) !== 1) throw new Error("Unsupported company sorting evaluation schema");
  if (!registryRows.length || registryRows.some((row) => Number(row.schema_version) !== 1)) {
    throw new Error("Company sorting run registry is empty or uses an unsupported schema");
  }

  const methodIds = new Set(registryRows.map((row) => row.method_id));
  const listIds = new Set(registryRows.map((row) => row.list_id));
  if (methodIds.size !== Number(evaluation.method_count) || listIds.size !== Number(evaluation.list_count)) {
    throw new Error(
      `Company sorting registry mismatch: ${methodIds.size}/${evaluation.method_count} methods, ${listIds.size}/${evaluation.list_count} lists`,
    );
  }
  if (listIds.size !== registryRows.length) throw new Error("Company sorting registry has duplicate current list ids");

  const sourceFiles = {
    normalized: resolveCompanySortingSource(evaluation.normalized_rankings_path),
    listMetrics: resolveCompanySortingSource(evaluation.list_metrics_path),
    methodMetrics: resolveCompanySortingSource(evaluation.method_metrics_path),
    consensus: resolveCompanySortingSource(evaluation.consensus_path),
    inputComparisons: resolveCompanySortingSource(evaluation.input_comparisons_path),
    report: resolveCompanySortingSource(evaluation.report_path),
  };
  const [normalizedRows, listMetricRows, methodMetricRows, consensusRows, inputComparisonRows] = await Promise.all([
    readText(sourceFiles.normalized).then(parseCsv),
    readText(sourceFiles.listMetrics).then(parseCsv),
    readText(sourceFiles.methodMetrics).then(parseCsv),
    readText(sourceFiles.consensus).then(parseCsv),
    readText(sourceFiles.inputComparisons).then(parseCsv),
  ]);

  const normalizedByList = groupRows(normalizedRows, "list_id");
  const listMetricsById = new Map(listMetricRows.map((row) => [row.list_id, row]));
  const methodMetricsById = new Map(methodMetricRows.map((row) => [row.method_id, row]));
  const companyByTicker = new Map(companyIndex.map((company) => [canonicalTicker(company.ticker), company]));
  const registryByMethod = new Map();
  for (const row of registryRows) {
    if (!registryByMethod.has(row.method_id)) registryByMethod.set(row.method_id, []);
    registryByMethod.get(row.method_id).push(row);
  }

  const runs = {};
  const order = [];
  for (const registry of registryRows) {
    const planFile = resolveCompanySortingSource(registry.plan_path);
    const resultFile = resolveCompanySortingSource(registry.result_path);
    const methodDir = resolveCompanySortingSource(registry.method_path);
    await Promise.all([fs.access(planFile), fs.access(resultFile)]);
    if (path.basename(planFile) !== "01_研究方案.md" || path.basename(resultFile) !== "02_排序结果.md") {
      throw new Error(`Non-standard plan/result binding for ${registry.list_id}`);
    }

    const rawRows = normalizedByList.get(registry.list_id) || [];
    const expectedRows = Number(registry.expected_row_count);
    const ranks = new Set(rawRows.map((row) => Number(row.rank)));
    const tickers = new Set(rawRows.map((row) => canonicalTicker(row.ticker)).filter(Boolean));
    if (rawRows.length !== expectedRows || ranks.size !== expectedRows || tickers.size !== expectedRows) {
      throw new Error(
        `${registry.list_id} normalized ranking invalid: rows=${rawRows.length}, ranks=${ranks.size}, tickers=${tickers.size}, expected=${expectedRows}`,
      );
    }

    const rows = rawRows
      .map((row) => {
        const ticker = canonicalTicker(row.ticker);
        const company = companyByTicker.get(ticker) || {};
        return {
          rank: Number(row.rank),
          ticker,
          name: company.name || "",
          category: company.category || "",
          score: cleanCell(row.score),
        };
      })
      .sort((a, b) => a.rank - b.rank);
    const listMetric = listMetricsById.get(registry.list_id);
    if (!listMetric) throw new Error(`Missing current evaluation metrics for ${registry.list_id}`);
    const iterationCount = (await safeReadDirents(path.join(methodDir, "迭代版本"))).filter((dirent) => dirent.isDirectory()).length;
    const label = registry.method_id === "06" ? `${registry.method_name} · ${registry.list_name}` : registry.list_name;
    const run = {
      key: registry.list_id,
      methodId: registry.method_id,
      listId: registry.list_id,
      label,
      methodName: registry.method_name,
      listName: registry.list_name,
      strategy: registry.lifecycle,
      lifecycle: registry.lifecycle,
      status: registry.status,
      useCase: registry.role,
      caution: `${evaluation.evidence_type}；不能把当前3个月或6个月结果解释为生成后有效性证明。`,
      runId: registry.run_id,
      date: registry.run_date,
      sourcePath: relativePath(resultFile),
      normalizedSourcePath: relativePath(sourceFiles.normalized),
      planPath: relativePath(planFile),
      folderPath: relativePath(methodDir),
      evaluationPath: relativePath(sourceFiles.report),
      iterationCount,
      metrics: normalizeCurrentRankingMetrics(listMetric),
      rowCount: rows.length,
      rows,
    };
    runs[run.key] = run;
    order.push(run.key);
  }

  const methodMetrics = methodMetricRows.map((row) => {
    const registry = registryByMethod.get(row.method_id)?.[0] || {};
    return {
      methodId: row.method_id,
      label: registry.method_name || row.name || row.method_id,
      lifecycle: registry.lifecycle || "",
      status: registry.status || "",
      ...normalizeCurrentRankingMetrics(row),
    };
  });
  const topMethods = (field) =>
    [...methodMetrics]
      .filter((row) => Number.isFinite(row[field]))
      .sort((a, b) => b[field] - a[field])
      .slice(0, 6);
  const currentEvaluation = {
    id: evaluation.evaluation_id,
    title: evaluation.title,
    evidenceType: evaluation.evidence_type,
    generatedAt: evaluation.generated_at,
    priceAsOf: evaluation.price_as_of,
    reportPath: relativePath(sourceFiles.report),
    coverage: {
      methodCount: methodIds.size,
      listCount: listIds.size,
      rankedCompanyCount: Number(evaluation.ranked_company_count),
      pricedCompanyCount: Number(evaluation.priced_company_count),
    },
    topMethods3m: topMethods("rankIc3m"),
    topMethods6m: topMethods("rankIc6m"),
    methodMetrics,
    consensus: consensusRows.slice(0, 16).map((row) => ({
      ticker: canonicalTicker(row.ticker),
      name: row.company || "",
      meanRank: parseNumber(row.all26_mean_rank),
      top20Count: parseNumber(row.all26_top20_count),
      independentMeanRank: parseNumber(row.independent23_mean_rank),
      return3m: parseNumber(row.ret_3m),
      return6m: parseNumber(row.ret_6m),
    })),
    inputComparisons: inputComparisonRows.map((row) => ({
      base: row.base,
      extended: row.extended,
      rankSimilarity: parseNumber(row.spearman_rank_similarity),
      top10Overlap: parseNumber(row.top10_overlap),
      top20Overlap: parseNumber(row.top20_overlap),
      meanAbsoluteRankChange: parseNumber(row.mean_abs_rank_change),
    })),
    caveats: [
      "3个月和6个月窗口都早于当前排名生成日，属于生成前历史回看，不是样本外验证。",
      `${evaluation.priced_company_count}/${evaluation.ranked_company_count}家公司有完整价格历史；缺失公司不参与收益统计。`,
      "生命周期状态结合既有历史与生成后证据管理，不因单次生成前回看自动改变。",
    ],
  };

  return {
    schemaVersion: 2,
    source: "companySortingRegistry",
    registryPath: relativePath(COMPANY_SORTING_RUN_REGISTRY),
    evaluationPointerPath: relativePath(COMPANY_SORTING_CURRENT_EVALUATION),
    defaultRunKey: order[0] || "",
    order,
    runs,
    currentEvaluation,
    validation: {
      methodCount: methodIds.size,
      listCount: listIds.size,
      expectedMethodCount: Number(evaluation.method_count),
      expectedListCount: Number(evaluation.list_count),
      expectedRowsPerList: Number(evaluation.ranked_company_count),
    },
  };
}

function resolveCompanySortingSource(relative) {
  const source = cleanCell(relative);
  if (!source || path.isAbsolute(source) || source.split(/[\\/]+/).includes("..")) {
    throw new Error(`Invalid company sorting relative source: ${relative}`);
  }
  const resolved = path.resolve(COMPANY_SORTING_ROOT, source.replaceAll("/", path.sep));
  const fromRoot = path.relative(COMPANY_SORTING_ROOT, resolved);
  if (!fromRoot || fromRoot.startsWith("..") || path.isAbsolute(fromRoot)) {
    throw new Error(`Company sorting source escapes root: ${relative}`);
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

function normalizeCurrentRankingMetrics(row = {}) {
  const metric = (field) => parseNumber(row[field]);
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

function extractTickerRaw(valueText) {
  const text = cleanCell(valueText);
  if (!text) return "";
  const first = text.split(/[\/／\s]+/)[0];
  const match = first.match(/[A-Za-z][A-Za-z0-9.-]{0,9}/);
  return match ? match[0].toUpperCase() : "";
}

function canonicalTicker(ticker) {
  const normalized = String(ticker || "").trim().toUpperCase();
  return TICKER_ALIASES.get(normalized) || normalized;
}

async function buildFeatures(companies) {
  const effectiveRegistry = await readEffectiveFeatureRegistry();
  const alphaRegistryById = new Map((effectiveRegistry.features || []).map((feature) => [feature.id, feature]));
  const gateRegistryById = new Map((effectiveRegistry.gates || []).map((gate) => [gate.id, gate]));
  const alphaFeatureIds = effectiveRegistry.activeArchitecture.alphaFeatureIds;
  const gateIds = effectiveRegistry.activeArchitecture.gateIds;
  const activeIds = [...alphaFeatureIds, ...gateIds];
  const activeIdSet = new Set(activeIds);
  const allFiles = (await safeReadDir(FEATURE_ROOT))
    .map((name) => {
      const match = name.match(FEATURE_SCORE_FILE_PATTERN);
      if (!match || !activeIdSet.has(match[1])) return null;
      return { file: path.join(FEATURE_ROOT, name), id: match[1], featureName: match[2], date: match[3] };
    })
    .filter(Boolean)
    .sort((a, b) => path.basename(a.file).localeCompare(path.basename(b.file)));
  const latestByFeature = new Map();
  for (const item of allFiles) {
    const current = latestByFeature.get(item.id);
    if (!current || item.date > current.date) latestByFeature.set(item.id, item);
  }
  const companyByTicker = new Map(companies.map((company) => [company.ticker, company]));
  const features = [];
  const allScores = [];
  const byFeature = {};
  const scoresByTicker = {};
  const scoreIndex = {};
  const parseProblems = [];
  const effectiveFeatureIds = (effectiveRegistry.effectiveFeatureIds || []).filter((id) => alphaFeatureIds.includes(id));
  const effectiveFeatureIdSet = new Set(effectiveFeatureIds);

  for (const id of activeIds) {
    const layer = id.startsWith("N") ? "alpha" : "gate";
    const registryEntry = layer === "alpha" ? alphaRegistryById.get(id) : gateRegistryById.get(id);
    const scoreFile = latestByFeature.get(id);
    const featureName = registryEntry?.name || scoreFile?.featureName || id;
    let rows = [];
    if (scoreFile) {
      const text = await readText(scoreFile.file);
      rows = parseFeatureTable(text, {
        id,
        featureName,
        date: scoreFile.date,
        sourcePath: relativePath(scoreFile.file),
      });
      if (!rows.length) parseProblems.push(`${path.basename(scoreFile.file)}: no rows parsed`);
    }
    features.push({
      id,
      name: featureName,
      layer,
      layerLabel: layer === "alpha" ? "收益型特征" : "门槛层",
      date: scoreFile?.date || "",
      sourcePath: scoreFile ? relativePath(scoreFile.file) : "",
      rowCount: rows.length,
      hasScores: Boolean(scoreFile && rows.length),
      isEffective: layer === "alpha" && effectiveFeatureIdSet.has(id),
      registryStatus: registryEntry?.status || (layer === "alpha" ? "awaiting_forward_cohorts" : "not_alpha"),
      concept: registryEntry?.concept || registryEntry?.use || "",
      gateUse: layer === "gate" ? registryEntry?.use || "" : "",
      forwardValidation: layer === "alpha" ? forwardValidationSummary(registryEntry) : null,
    });
    byFeature[id] = rows.map((row) => {
      const company = companyByTicker.get(row.ticker);
      return {
        ...row,
        featureId: id,
        featureName,
        companyName: row.companyName || company?.name || "",
        category: row.category || company?.category || "",
      };
    });
    for (const row of byFeature[id]) {
      allScores.push(row);
      if (!scoresByTicker[row.ticker]) scoresByTicker[row.ticker] = [];
      if (!scoreIndex[row.ticker]) scoreIndex[row.ticker] = {};
      scoresByTicker[row.ticker].push(row);
      scoreIndex[row.ticker][id] = row;
    }
  }

  for (const rows of Object.values(scoresByTicker)) {
    rows.sort((a, b) => a.featureId.localeCompare(b.featureId));
  }

  return {
    features,
    scores: allScores,
    byFeature,
    scoresByTicker,
    scoreIndex,
    effectiveRegistry,
    featureGroups: {
      alpha: alphaFeatureIds,
      gates: gateIds,
      validatedAlpha: effectiveFeatureIds,
    },
    alphaFeatureIds,
    gateIds,
    effectiveFeatureIds,
    scoreFileCount: latestByFeature.size,
    parseProblems,
  };
}

function forwardValidationSummary(entry = {}) {
  return {
    status: entry.status || "awaiting_forward_cohorts",
    nCohorts: Number.isFinite(Number(entry.nCohorts)) ? Number(entry.nCohorts) : 0,
    oosStart: entry.oosStart || "",
    oosEnd: entry.oosEnd || "",
    holdingPeriods: Array.isArray(entry.holdingPeriods) ? entry.holdingPeriods : [],
    meanSpearmanIc: entry.meanSpearmanIc ?? null,
    meanNeutralSpearmanIc: entry.meanNeutralSpearmanIc ?? null,
    icir: entry.icir ?? null,
    directionConsistency: entry.directionConsistency ?? null,
    significantCohortShare: entry.significantCohortShare ?? null,
    qValue: entry.qValue ?? null,
    meanTopBottomNetReturn: entry.meanTopBottomNetReturn ?? null,
    turnover: entry.turnover ?? null,
    dataQualityGate: entry.dataQualityGate || "insufficient",
  };
}

async function buildDailyNews() {
  const scriptFiles = groupByDate(
    await datedFiles(DAILY_NEWS_SCRIPT_ROOT, /^每日新闻稿_(\d{4}-\d{2}-\d{2})(?:[\s\S]*)\.(md|txt)$/i),
  );
  const audioFiles = groupByDate(
    await datedFiles(DAILY_NEWS_AUDIO_ROOT, /^每日AI产业链新闻_(\d{4}-\d{2}-\d{2})(?:[\s\S]*)\.(mp3|wav|m4a|ogg)$/i),
  );
  const dates = [...scriptFiles.keys()].sort().reverse().slice(0, DAILY_NEWS_LIMIT);
  const items = [];

  for (const date of dates) {
    const script = chooseDailyNewsScript(scriptFiles.get(date) || []);
    if (!script) continue;
    const rawMarkdown = redactLocalPaths(await readText(script.file));
    const audio = chooseDailyNewsAudio(audioFiles.get(date) || []);
    let audioPayload = null;

    if (audio) {
      const extension = path.extname(audio.name).toLowerCase();
      const publicFileName = `daily-ai-news-${date}${extension}`;
      await fs.copyFile(audio.file, path.join(DAILY_NEWS_AUDIO_DIR, publicFileName));
      audioPayload = {
        url: `data/daily-news/audio/${publicFileName}`,
        format: extension.replace(/^\./, ""),
        sourcePath: relativePath(audio.file),
        originalFileName: audio.name,
        sizeBytes: audio.size,
      };
    }

    items.push({
      date,
      title: firstMatch(rawMarkdown, /^#\s+(.+)$/m) || `每日新闻稿 ${date}`,
      summary: markdownSummary(rawMarkdown),
      sourcePath: relativePath(script.file),
      fileName: script.name,
      sizeBytes: script.size,
      markdown: rawMarkdown,
      audio: audioPayload,
    });
  }

  return {
    generatedAt: new Date().toISOString(),
    limit: DAILY_NEWS_LIMIT,
    latestDate: items[0]?.date || "",
    oldestDate: items.at(-1)?.date || "",
    sourceDirs: {
      scripts: relativePath(DAILY_NEWS_SCRIPT_ROOT),
      audio: relativePath(DAILY_NEWS_AUDIO_ROOT),
    },
    items,
  };
}

async function datedFiles(dir, pattern) {
  const names = await safeReadDir(dir);
  const files = [];
  for (const name of names) {
    const match = name.match(pattern);
    if (!match) continue;
    const file = path.join(dir, name);
    const stat = await fs.stat(file).catch(() => null);
    if (!stat?.isFile()) continue;
    files.push({
      date: match[1],
      ext: path.extname(name).toLowerCase(),
      file,
      name,
      size: stat.size,
      mtimeMs: stat.mtimeMs,
    });
  }
  return files;
}

function groupByDate(files) {
  const byDate = new Map();
  for (const file of files) {
    if (!byDate.has(file.date)) byDate.set(file.date, []);
    byDate.get(file.date).push(file);
  }
  return byDate;
}

function chooseDailyNewsScript(files) {
  return [...files].sort((a, b) => {
    const priority = dailyNewsScriptPriority(b) - dailyNewsScriptPriority(a);
    if (priority) return priority;
    return b.name.localeCompare(a.name, "zh-Hans-CN");
  })[0] || null;
}

function dailyNewsScriptPriority(file) {
  let score = 0;
  if (file.ext === ".md") score += 100;
  if (!file.name.includes("口播稿")) score += 10;
  return score;
}

function chooseDailyNewsAudio(files) {
  return [...files].sort((a, b) => {
    const priority = dailyNewsAudioPriority(b) - dailyNewsAudioPriority(a);
    if (priority) return priority;
    return b.mtimeMs - a.mtimeMs;
  })[0] || null;
}

function dailyNewsAudioPriority(file) {
  let score = 0;
  if (file.ext === ".mp3") score += 100;
  if (file.name.includes("新闻口播稿")) score += 10;
  if (file.name.includes("中文语音")) score += 5;
  return score;
}

function markdownSummary(markdown) {
  const paragraph = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .find((line) => line && !line.startsWith("#") && !line.startsWith("|") && !/^-{3,}$/.test(line));
  if (!paragraph) return "";
  const compact = paragraph.replace(/\s+/g, " ");
  return compact.length > 220 ? `${compact.slice(0, 217)}...` : compact;
}

function parseFeatureTable(markdown, feature) {
  const lines = markdown.split(/\r?\n/);
  let start = lines.findIndex((line) => line.includes("全公司排序表"));
  if (start < 0) start = lines.findIndex((line) => line.includes("排序表"));
  if (start < 0) return [];
  const tableLines = [];
  for (let i = start + 1; i < lines.length; i += 1) {
    const line = lines[i].trim();
    if (!line) {
      if (tableLines.length) break;
      continue;
    }
    if (line.startsWith("|")) tableLines.push(line);
    else if (tableLines.length) break;
  }
  if (tableLines.length < 3) return [];
  const header = splitMarkdownRow(tableLines[0]);
  const rows = [];
  const indices = {
    rank: findHeader(header, ["排名"]),
    ticker: findHeader(header, ["股票代号", "代码", "Ticker"]),
    companyName: findHeader(header, ["公司名称", "公司"]),
    category: findHeader(header, ["分类目录", "分类"]),
    score: findHeader(header, ["特征分", "分数", "评分"]),
    evidenceGrade: findHeader(header, ["证据等级", "证据"]),
    confidence: findHeader(header, ["置信度"]),
    evidence: findHeader(header, ["核心证据", "证据摘要"]),
  };
  for (const line of tableLines.slice(2)) {
    if (/^\|?\s*:?-{3,}/.test(line)) continue;
    const cells = splitMarkdownRow(line);
    const ticker = cleanCell(cells[indices.ticker] || "").toUpperCase();
    if (!ticker || ticker === "股票代号") continue;
    rows.push({
      featureId: feature.id,
      featureName: feature.featureName,
      rank: cleanCell(cells[indices.rank]),
      ticker,
      companyName: cleanCell(cells[indices.companyName]),
      category: cleanCell(cells[indices.category]),
      score: parseNumber(cleanCell(cells[indices.score])),
      evidenceGrade: cleanCell(cells[indices.evidenceGrade]),
      confidence: cleanCell(cells[indices.confidence]),
      evidence: cleanCell(cells[indices.evidence]),
    });
  }
  return rows;
}

function buildQuality({
  companies,
  companyIndex,
  industries,
  industryIndex,
  rankings,
  features,
  industryReports,
  duplicateCompanyReports,
  dailyNews,
  companyComparisons,
}) {
  const alerts = [];
  const companyReportMissing = companies.filter((company) => !company.hasReport);
  if (companyReportMissing.length) {
    alerts.push({
      severity: "warn",
      type: "company-report-missing",
      title: "公司索引中存在未匹配正式报告",
      message: companyReportMissing.map((c) => c.ticker).join(", "),
    });
  }

  const companyEvaluationMissing = companies.filter((company) => !company.hasEvaluation);
  if (companyEvaluationMissing.length) {
    alerts.push({
      severity: "warn",
      type: "company-evaluation-missing",
      title: "公司索引中存在未匹配公司评估",
      message: companyEvaluationMissing.map((c) => c.ticker).join(", "),
    });
  }

  if (duplicateCompanyReports.length) {
    alerts.push({
      severity: "info",
      type: "company-report-duplicates",
      title: "部分公司存在多份正式报告",
      message: duplicateCompanyReports.map((item) => `${item.ticker}(${item.count})`).join(", "),
    });
  }

  const defaultRun = rankings.runs[rankings.defaultRunKey] || Object.values(rankings.runs)[0];
  if (!defaultRun) {
    alerts.push({
      severity: "error",
      type: "ranking-empty",
      title: "当前公司排序为空",
      message: "运行注册表、当前评估指针或规范化榜单没有生成可用排序。",
    });
  }
  if (defaultRun) {
    const tickers = new Set(defaultRun.rows.map((row) => row.ticker));
    const missing = companyIndex.filter((company) => !tickers.has(company.ticker)).map((company) => company.ticker);
    if (missing.length) {
      alerts.push({
        severity: "warn",
        type: "ranking-missing-default",
        title: `${defaultRun.label}排名未覆盖全部公司`,
        message: `缺失 ${missing.length} 家：${missing.join(", ")}`,
      });
    }
  }

  const rankingCoverage = rankings.currentEvaluation?.coverage;
  if (rankingCoverage && rankingCoverage.pricedCompanyCount < rankingCoverage.rankedCompanyCount) {
    alerts.push({
      severity: "info",
      type: "ranking-price-history-partial",
      title: "部分排名公司缺少完整历史价格",
      message: `${rankingCoverage.pricedCompanyCount}/${rankingCoverage.rankedCompanyCount} 家有当前评估所需的完整价格历史。`,
    });
  }

  const missingIndustryReports = industries.filter((industry) => !industry.hasReport);
  if (missingIndustryReports.length) {
    alerts.push({
      severity: "info",
      type: "industry-report-missing",
      title: "行业索引中存在未匹配正式报告",
      message: missingIndustryReports.map((industry) => industry.name).join("；"),
    });
  }

  for (const feature of features.features) {
    if (defaultRun && feature.rowCount !== defaultRun.rowCount) {
      alerts.push({
        severity: "info",
        type: `feature-coverage-${feature.id}`,
        title: `${feature.id} 覆盖数与默认公司排序不同`,
        message: `${feature.name}: ${feature.rowCount} 行，默认公司排序 ${defaultRun.rowCount || 0} 行`,
      });
    }
  }

  if (features.parseProblems.length) {
    alerts.push({
      severity: "warn",
      type: "feature-parse",
      title: "部分特征评分表解析不完整",
      message: features.parseProblems.join("；"),
    });
  }

  if (!dailyNews.items.length) {
    alerts.push({
      severity: "warn",
      type: "daily-news-empty",
      title: "最近 AI 新闻未生成",
      message: "未从 日度资料/最新AI新闻/新闻稿 匹配到可发布文件。",
    });
  }

  if (companyComparisons.missing.length) {
    alerts.push({
      severity: "warn",
      type: "company-comparison-missing",
      title: "公司对比结果未覆盖全部公司",
      message: `缺失 ${companyComparisons.missing.length} 家：${companyComparisons.missing.join(", ")}`,
    });
  }

  const missingDailyNewsAudio = dailyNews.items.filter((item) => !item.audio).map((item) => item.date);
  if (missingDailyNewsAudio.length) {
    alerts.push({
      severity: "warn",
      type: "daily-news-audio-missing",
      title: "部分 AI 新闻缺少语音文件",
      message: missingDailyNewsAudio.join(", "),
    });
  }

  return {
    summary: {
      companyIndexCount: companyIndex.length,
      companyReportUnique: companies.filter((company) => company.hasReport).length,
      companyEvaluationUnique: companies.filter((company) => company.hasEvaluation).length,
      industryIndexCount: industryIndex.length,
      industryReportUnique: industries.filter((industry) => industry.hasReport).length,
      featureDefinitionCount: features.features.length,
      featureFileCount: features.scoreFileCount,
      alphaFeatureCount: features.alphaFeatureIds.length,
      gateCount: features.gateIds.length,
      effectiveFeatureCount: features.effectiveFeatureIds.length,
      effectiveFeatureAsOf: features.effectiveRegistry.asOf || "",
      companyComparisonCount: companyComparisons.companyCount,
      companyComparisonRowCount: companyComparisons.rowCount,
      companyComparisonDate: companyComparisons.reportDate,
      dailyNewsCount: dailyNews.items.length,
      rankingMethodCount: rankings.validation?.methodCount || 0,
      rankingListCount: rankings.validation?.listCount || 0,
      rankingExpectedListCount: rankings.validation?.expectedListCount || 0,
      rankingEvaluationId: rankings.currentEvaluation?.id || "",
      rankingRuns: Object.fromEntries(Object.entries(rankings.runs).map(([key, run]) => [key, run.rowCount])),
      rawIndustryReportCount: industryReports.size,
    },
    alerts,
  };
}

async function findDuplicateCompanyReports(companyIndex) {
  const reportFiles = await directMarkdownFilesByCategory(COMPANY_ROOT, ["研究方法", "tmp", "评估备份"]);
  const duplicates = [];
  for (const row of companyIndex) {
    const categoryFiles = reportFiles.get(row.category) || [];
    const matches = categoryFiles.filter((file) => tickerInFileName(row.ticker, path.basename(file)));
    if (matches.length > 1) {
      duplicates.push({
        ticker: row.ticker,
        count: matches.length,
        files: matches.map(relativePath),
      });
    }
  }
  return duplicates;
}

function buildMeta({ companies, industries, rankings, features, quality, latestFinancialDate, dailyNews, companyComparisons }) {
  const rankingDates = Object.values(rankings.runs)
    .map((run) => run.date)
    .filter(Boolean)
    .sort();
  return {
    generatedAt: new Date().toISOString(),
    generatedAtDisplay: new Date().toLocaleString("zh-CN", { hour12: false }),
    sourceRootName: "Investment",
    siteRoot: "tools/site",
    companyCount: companies.length,
    companyReportCount: companies.filter((company) => company.hasReport).length,
    companyEvaluationCount: companies.filter((company) => company.hasEvaluation).length,
    industryCount: industries.length,
    industryReportCount: industries.filter((industry) => industry.hasReport).length,
    featureCount: features.features.length,
    featureScoreFileCount: features.scoreFileCount,
    alphaFeatureCount: features.alphaFeatureIds.length,
    gateCount: features.gateIds.length,
    effectiveFeatureCount: features.effectiveFeatureIds.length,
    effectiveFeatureAsOf: features.effectiveRegistry.asOf || "",
    latestRankingDate: rankingDates.at(-1) || "",
    rankingMethodCount: rankings.validation?.methodCount || 0,
    rankingListCount: rankings.validation?.listCount || 0,
    currentRankingEvaluationId: rankings.currentEvaluation?.id || "",
    currentRankingEvidenceType: rankings.currentEvaluation?.evidenceType || "",
    currentRankingPriceAsOf: rankings.currentEvaluation?.priceAsOf || "",
    latestCompanyComparisonDate: companyComparisons.reportDate,
    companyComparisonCount: companyComparisons.companyCount,
    companyComparisonRowCount: companyComparisons.rowCount,
    latestFinancialDate,
    latestDailyNewsDate: dailyNews.latestDate,
    dailyNewsCount: dailyNews.items.length,
    qualityAlertCount: quality.alerts.length,
  };
}

async function readEffectiveFeatureRegistry() {
  const fallback = {
    schemaVersion: 2,
    status: "registry_unavailable",
    asOf: "",
    policy: {},
    activeArchitecture: {
      alphaFeatureCount: DEFAULT_ALPHA_FEATURE_IDS.length,
      gateCount: DEFAULT_GATE_IDS.length,
      alphaFeatureIds: DEFAULT_ALPHA_FEATURE_IDS,
      gateIds: DEFAULT_GATE_IDS,
    },
    effectiveFeatureIds: [],
    effectiveFeatureCount: 0,
    features: [],
    gates: [],
  };
  try {
    const parsed = JSON.parse(await readText(EFFECTIVE_FEATURE_REGISTRY));
    if (Number(parsed.schemaVersion) !== 2) return { ...fallback, status: "unsupported_registry_schema" };
    const alphaFeatureIds = (parsed.activeArchitecture?.alphaFeatureIds || []).filter((id) => /^N\d{2}$/.test(id));
    const gateIds = (parsed.activeArchitecture?.gateIds || []).filter((id) => /^G\d{2}$/.test(id));
    return {
      ...fallback,
      ...parsed,
      activeArchitecture: {
        alphaFeatureCount: alphaFeatureIds.length,
        gateCount: gateIds.length,
        alphaFeatureIds: alphaFeatureIds.length ? alphaFeatureIds : DEFAULT_ALPHA_FEATURE_IDS,
        gateIds: gateIds.length ? gateIds : DEFAULT_GATE_IDS,
      },
      effectiveFeatureIds: (parsed.effectiveFeatureIds || []).filter((id) => /^N\d{2}$/.test(id)),
      features: (parsed.features || []).filter((feature) => /^N\d{2}$/.test(feature?.id || "")),
      gates: (parsed.gates || []).filter((gate) => /^G\d{2}$/.test(gate?.id || "")),
    };
  } catch {
    return fallback;
  }
}

async function directMarkdownFilesByCategory(root, excludedDirs) {
  const dirs = await fs.readdir(root, { withFileTypes: true });
  const map = new Map();
  for (const dirent of dirs) {
    if (!dirent.isDirectory() || excludedDirs.includes(dirent.name)) continue;
    const dir = path.join(root, dirent.name);
    const files = (await safeReadDir(dir))
      .filter((name) => name.endsWith(".md") && name !== "AGENTS.md")
      .map((name) => path.join(dir, name));
    map.set(dirent.name, files);
  }
  return map;
}

function parseReportMeta(content, file) {
  return {
    title: firstMatch(content, /^#\s+(.+)$/m) || path.basename(file, ".md"),
    reportDate: firstMatch(content, /报告日期[:：]\s*(\d{4}-\d{2}-\d{2})/) || firstDate(path.basename(file)),
  };
}

function parseIndustryMeta(content, file, fallbackCategory) {
  const fallbackName = path.basename(file, ".md").replace(/^行业调研_/, "").replace(/_\d{4}-\d{2}-\d{2}$/, "");
  const category =
    firstMatch(content, /(?:分类目录|所属目录|标准目录|标准分类目录|行业索引分类)[:：]\s*`?([^`\n]+)`?/) ||
    fallbackCategory;
  return {
    title: firstMatch(content, /^#\s+(.+)$/m) || path.basename(file, ".md"),
    standardName:
      cleanIndustryStandardName(firstMatch(content, /标准行业名称[:：]\s*(.+)/)) ||
      fallbackName,
    category: cleanIndustryCategory(category),
    reportDate: firstMatch(content, /报告日期[:：]\s*(\d{4}-\d{2}-\d{2})/) || firstDate(path.basename(file)),
  };
}

function parseMarkdownTables(markdown) {
  const lines = markdown.split(/\r?\n/);
  const tables = [];
  for (let i = 0; i < lines.length; i += 1) {
    if (!lines[i].trim().startsWith("|")) continue;
    const header = splitMarkdownRow(lines[i]);
    const sep = lines[i + 1] || "";
    if (!/^\s*\|?[\s:|-]+\|/.test(sep)) continue;
    const rows = [];
    i += 2;
    while (i < lines.length) {
      const line = lines[i].trim();
      if (!line) {
        if (rows.length) break;
        i += 1;
        continue;
      }
      if (!line.startsWith("|")) break;
      const cells = splitMarkdownRow(line);
      if (cells.length >= header.length) {
        rows.push(Object.fromEntries(header.map((key, index) => [cleanCell(key), cleanCell(cells[index])])));
      }
      i += 1;
    }
    tables.push(rows);
  }
  return tables;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (inQuotes) {
      if (char === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (char === '"') {
        inQuotes = false;
      } else {
        cell += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
    } else if (char !== "\r") {
      cell += char;
    }
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0].map((h) => h.replace(/^\ufeff/, "").trim());
  return rows
    .slice(1)
    .filter((r) => r.some((c) => c.trim()))
    .map((r) => Object.fromEntries(header.map((key, index) => [key, r[index] ?? ""])));
}

function splitMarkdownRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function findHeader(header, names) {
  const idx = header.findIndex((cell) => names.some((name) => cleanCell(cell).includes(name)));
  return idx >= 0 ? idx : -1;
}

function tickerInFileName(ticker, fileName) {
  const escaped = ticker.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`(^|[_\\-\\s])${escaped}([_\\-\\s]|$)`, "i").test(fileName);
}

function companyEvaluationFileMatches(ticker, fileName) {
  return fileName.toUpperCase().startsWith(`${ticker.toUpperCase()}_`) || tickerInFileName(ticker, fileName);
}

function chooseLatestFile(files) {
  return [...files].sort((a, b) => {
    const da = firstDate(path.basename(a)) || "";
    const db = firstDate(path.basename(b)) || "";
    if (da !== db) return db.localeCompare(da);
    return path.basename(b).localeCompare(path.basename(a));
  })[0];
}

async function latestDateFromFiles(dir, pattern) {
  const files = await safeReadDir(dir);
  return files
    .map((name) => name.match(pattern)?.[1])
    .filter(Boolean)
    .sort()
    .at(-1) || "";
}

function cleanCell(value) {
  return value === undefined || value === null ? "" : String(value).replace(/`/g, "").trim();
}

function cleanIndustryStandardName(value) {
  return cleanCell(value)
    .replace(/\s*(?:行业索引分类|分类目录|所属目录|标准目录|标准分类目录)[:：].*$/u, "")
    .replace(/[。；;]\s*$/u, "")
    .trim();
}

function cleanIndustryCategory(value) {
  return cleanCell(value)
    .replace(/[。；;]\s*$/u, "")
    .replace(/[\\/／]+$/u, "")
    .trim();
}

function value(v) {
  return cleanCell(v);
}

function parseNumber(v) {
  const n = Number(String(v).replace(/[,+%]/g, ""));
  return Number.isFinite(n) ? n : null;
}

function firstMatch(text, regex) {
  const match = text.match(regex);
  return match ? match[1].trim() : "";
}

function firstDate(text) {
  return firstMatch(text, /(\d{4}-\d{2}-\d{2})/) || firstMatch(text, /(\d{8})/).replace(/^(\d{4})(\d{2})(\d{2})$/, "$1-$2-$3");
}

function normalizeName(value) {
  return cleanCell(value)
    .replace(/[\/\\]/g, "_")
    .replace(/、/g, "_")
    .replace(/\s+/g, "")
    .replace(/（/g, "(")
    .replace(/）/g, ")")
    .toLowerCase();
}

function canonicalIndustryKey(value) {
  return cleanCell(value)
    .replace(/^行业调研_/u, "")
    .replace(/_\d{4}-\d{2}-\d{2}(?:\.md)?$/u, "")
    .replace(/[.\u3002；;]+$/gu, "")
    .replace(/[\s_、,，/／\\()（）]+/gu, "")
    .toLowerCase();
}

function stableSlug(value) {
  return crypto.createHash("sha1").update(normalizeName(value)).digest("hex").slice(0, 14);
}

function relativePath(file) {
  return path.relative(PROJECT_ROOT, file).replace(/\\/g, "/");
}

function redactLocalPaths(text) {
  return text.replace(/D:\\drive\\Investment\\/gi, "Investment\\").replace(/D:\/drive\/Investment\//gi, "Investment/");
}

async function safeReadDir(dir) {
  try {
    return await fs.readdir(dir);
  } catch {
    return [];
  }
}

async function safeReadDirents(dir) {
  try {
    return await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

async function readText(file) {
  return (await fs.readFile(file, "utf8")).replace(/^\ufeff/, "");
}

async function writeJson(file, data) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
