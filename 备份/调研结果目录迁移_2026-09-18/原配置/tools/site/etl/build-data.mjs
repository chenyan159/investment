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
const COMPANY_COMPARISON_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "company-comparison");
const SCENARIO_DECISION_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "scenario-decision");
const INDUSTRY_REPORT_DIR = path.join(PUBLIC_DATA, "reports", "industry");

const FUND_ROOT = path.join(PROJECT_ROOT, "基本面");
const ANALYSIS_ROOT = path.join(PROJECT_ROOT, "分析报告");
const FINANCIAL_MATERIALS_ROOT = path.join(PROJECT_ROOT, "金融资料");
const COMPANY_ROOT = path.join(FUND_ROOT, "公司调研");
const INDUSTRY_ROOT = path.join(FUND_ROOT, "行业调研");
const COMPANY_SORTING_ROOT = path.join(ANALYSIS_ROOT, "公司排序");
const COMPANY_SORTING_SITE_DATA_ROOT = path.join(COMPANY_SORTING_ROOT, "站点数据");
const COMPANY_COMPARISON_ROOT = path.join(ANALYSIS_ROOT, "公司对比");
const COMPANY_COMPARISON_SITE_DATA_ROOT = path.join(COMPANY_COMPARISON_ROOT, "站点数据");
const SCENARIO_DECISION_ROOT = path.join(ANALYSIS_ROOT, "公司情景投资决策");
const SCENARIO_DECISION_SITE_DATA_ROOT = path.join(SCENARIO_DECISION_ROOT, "站点数据");
const TECHNICAL_ROOT = path.join(PROJECT_ROOT, "技术面");
const TECHNICAL_SITE_DATA_ROOT = path.join(TECHNICAL_ROOT, "站点数据");
const FEATURE_QUANT_ROOT = path.join(FUND_ROOT, "特征量化");
const FEATURE_PLAN_ROOT = path.join(FEATURE_QUANT_ROOT, "研究方案");
const FEATURE_ROOT = path.join(FEATURE_QUANT_ROOT, "量化评分");
const FEATURE_PLAN_FILE_PATTERN = /^([NG]\d{2})_([\s\S]+)_研究方案\.md$/u;
const FEATURE_SCORE_FILE_PATTERN = /^([NG]\d{2})_([\s\S]+)_量化评分_(\d{4}-\d{2}-\d{2})\.md$/u;
const DEFAULT_ALPHA_FEATURE_IDS = Array.from({ length: 16 }, (_, index) => `N${String(index + 1).padStart(2, "0")}`);
const DEFAULT_GATE_IDS = Array.from({ length: 3 }, (_, index) => `G${String(index + 1).padStart(2, "0")}`);
const TICKER_ALIASES = new Map([
  ["PSTG", "P"],
]);
const MODULE_LABELS = {
  companyComparisons: "公司对比",
  scenarioDecisions: "情景决策",
  rankings: "公司排序",
  technicalResearch: "技术面",
  dailyNews: "每日新闻",
};
const FINANCE_ROOT = path.join(FINANCIAL_MATERIALS_ROOT, "每日金融数据");
const DAILY_NEWS_SITE_DATA_ROOT = path.join(PUBLIC_DATA, "daily-news");

const companyToIndustryCategory = {
  "AI计算芯片_EDA_IP_custom_ASIC": "AI服务器_存储_芯片",
  "AI服务器_存储_EMS": "AI服务器_存储_芯片",
  "AI网络_光互联_连接器": "AI网络_光互联_铜互联",
  "电子材料_化学品_基板_PCB": "半导体与电子制造_设备_材料_测试",
  "晶圆制造_前道设备": "半导体与电子制造_设备_材料_测试",
  "封测_检测_计量_光罩": "半导体与电子制造_设备_材料_测试",
  "功率半导体_电源管理_传感器": "AI园区电力_机电_冷却",
  "配电_电源系统_电气设备": "AI园区电力_机电_冷却",
  "电力_发电_能源_储能": "AI园区电力_机电_冷却",
  "热管理_流体_水处理": "AI园区电力_机电_冷却",
  "工程建设_机电安装": "AI园区电力_机电_冷却",
  "机器人_工业自动化_智能硬件": "工业自动化_机器人_感知",
  "航空航天_卫星_高可靠系统": "商业航天_火箭_卫星",
  "云算力_IDC_边缘云": "AI服务器_存储_芯片",
  "企业软件_数据平台": "AI应用_软件_数据平台",
  "网络安全_身份权限_治理": "AI应用_软件_数据平台",
};

export async function buildData({ moduleBuilds = {} } = {}) {
  await prepareOutput();
  const companyIndex = await parseCompanyIndex();
  const industryIndex = await parseIndustryIndex();
  const industryReports = await buildIndustryReports(industryIndex);
  const companies = await buildCompanies(companyIndex, industryReports, industryIndex);
  const companyComparisons = await buildCompanyComparisons(companyIndex, {
    allowHistoricalCohort: moduleBuilds.companyComparisons?.status === "stale",
  });
  const scenarioDecisions = await buildScenarioDecisions(companyIndex, {
    allowHistoricalCohort: moduleBuilds.scenarioDecisions?.status === "stale",
  });
  const technicalResearch = await buildTechnicalResearch();
  const rankings = await buildRankings(companyIndex, {
    allowHistoricalCohort: moduleBuilds.rankings?.status === "stale",
  });
  const features = await buildFeatures(companies);
  const dailyNews = await loadDailyNews();
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
    scenarioDecisions,
    technicalResearch,
    moduleBuilds,
  });
  const meta = buildMeta({
    companies,
    industries,
    rankings,
    features,
    quality,
    latestFinancialDate,
    dailyNews,
    companyComparisons,
    scenarioDecisions,
    technicalResearch,
    moduleBuilds,
  });

  await writeJson(path.join(PUBLIC_DATA, "meta.json"), meta);
  await writeJson(path.join(PUBLIC_DATA, "companies.json"), companies);
  await writeJson(path.join(PUBLIC_DATA, "industries.json"), industries);
  await writeJson(path.join(PUBLIC_DATA, "rankings.json"), rankings);
  await writeJson(path.join(PUBLIC_DATA, "company-comparisons.json"), companyComparisons);
  await writeJson(path.join(PUBLIC_DATA, "scenario-decisions.json"), scenarioDecisions);
  await writeJson(path.join(PUBLIC_DATA, "technical-research.json"), technicalResearch);
  await writeJson(path.join(PUBLIC_DATA, "features.json"), features);
  await writeJson(path.join(PUBLIC_DATA, "quality.json"), quality);
  await writeJson(path.join(PUBLIC_DATA, "daily-news.json"), dailyNews);

  console.log(`Wrote site data to ${PUBLIC_DATA}`);
  console.log(
    `Companies: ${companies.length}, comparisons: ${companyComparisons.companies.length}, scenario decisions: ${scenarioDecisions.companies.length}, technical factors: ${technicalResearch.factorCount}, industries: ${industries.length}, features: ${features.features.length}, daily news: ${dailyNews.items.length}`,
  );
}

let companyIndexForValidation;

export async function validateModuleArtifact(id, siteDataRoot, { allowHistoricalCohort = false } = {}) {
  const companyIndex = async () => {
    companyIndexForValidation ||= parseCompanyIndex();
    return companyIndexForValidation;
  };

  let payload;
  if (id === "companyComparisons") {
    payload = await buildCompanyComparisons(await companyIndex(), {
      siteDataRoot,
      copyReports: false,
      allowHistoricalCohort,
    });
  } else if (id === "scenarioDecisions") {
    payload = await buildScenarioDecisions(await companyIndex(), {
      siteDataRoot,
      copyReports: false,
      allowHistoricalCohort,
    });
  } else if (id === "rankings") {
    payload = await buildRankings(await companyIndex(), { siteDataRoot, allowHistoricalCohort });
  } else if (id === "technicalResearch") {
    payload = await buildTechnicalResearch({ siteDataRoot });
  } else if (id === "dailyNews") {
    payload = await loadDailyNews({ siteDataRoot });
  } else {
    throw new Error(`未知站点数据模块：${id}`);
  }

  return {
    generatedAt: payload.generatedAt || "",
    dataDate:
      payload.latestDate ||
      payload.reportDateLabel ||
      payload.reportDate ||
      payload.currentEvaluation?.priceAsOf ||
      "",
  };
}

async function prepareOutput() {
  await fs.mkdir(PUBLIC_DATA, { recursive: true });
  await fs.mkdir(COMPANY_REPORT_DIR, { recursive: true });
  await fs.mkdir(COMPANY_COMPARISON_REPORT_DIR, { recursive: true });
  await fs.mkdir(SCENARIO_DECISION_REPORT_DIR, { recursive: true });
  await fs.mkdir(INDUSTRY_REPORT_DIR, { recursive: true });
  await cleanJsonDir(COMPANY_REPORT_DIR);
  await cleanJsonDir(COMPANY_COMPARISON_REPORT_DIR);
  await cleanJsonDir(SCENARIO_DECISION_REPORT_DIR);
  await cleanJsonDir(INDUSTRY_REPORT_DIR);
  await fs.rm(path.join(PUBLIC_DATA, "reports", "company-evaluation"), { recursive: true, force: true });
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
    businessTags: cleanCell(row["业务标签"]),
    relatedIndustryNames: cleanCell(row["关联行业"]).split("；").map((name) => name.trim()).filter(Boolean),
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
    topicType: cleanCell(row["专题类型"]) || "行业",
    slug: stableSlug(cleanCell(row["行业名称"])),
  }));
}

async function buildCompanies(indexRows, industryReports, industryIndex = []) {
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
  const indexedIndustries = new Map(industryIndex.map((row) => [canonicalIndustryKey(row.name), row]));
  for (const industry of industryIndex.length ? industryIndex : industryReports.values()) {
    if (!industryByCategory.has(industry.category)) industryByCategory.set(industry.category, []);
    industryByCategory.get(industry.category).push(industry.slug);
  }

  const companies = [];
  for (const row of indexRows) {
    const reportPath = reportsByTicker.get(row.ticker);
    const relatedIndustryCategory = companyToIndustryCategory[row.category];
    const relatedIndustrySlugs = row.relatedIndustryNames?.length
      ? [...new Set(row.relatedIndustryNames.map((name) => indexedIndustries.get(canonicalIndustryKey(name))?.slug || industryReports.get(canonicalIndustryKey(name))?.slug).filter(Boolean))]
      : relatedIndustryCategory ? industryByCategory.get(relatedIndustryCategory) || [] : [];
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
      businessTags: row.businessTags || "",
      relatedIndustrySlugs,
      hasReport: Boolean(report),
      report,
    });
  }
  return companies;
}

async function buildCompanyComparisons(
  indexRows,
  { siteDataRoot = COMPANY_COMPARISON_SITE_DATA_ROOT, copyReports = true, allowHistoricalCohort = false } = {},
) {
  const payload = JSON.parse(await readText(path.join(siteDataRoot, "current.json")));
  const payloadCompanies = Array.isArray(payload.companies) ? payload.companies : [];
  const currentCompanyCount = indexRows.length;
  const artifactCompanyCount = Number(payload.companyCount);
  const artifactCompanyCountValid = Number.isInteger(artifactCompanyCount) && artifactCompanyCount > 0;
  const expectedCompanyCount = allowHistoricalCohort && artifactCompanyCountValid
    ? artifactCompanyCount
    : currentCompanyCount;
  const expectedDirectedRows = expectedCompanyCount * (expectedCompanyCount - 1);
  const expectedPairCount = expectedDirectedRows / 2;
  const expectedTickers = new Set(indexRows.map((row) => row.ticker));
  const actualTickers = new Set(payloadCompanies.map((row) => row.ticker));
  const missing = [...expectedTickers].filter((ticker) => !actualTickers.has(ticker));
  const extra = [...actualTickers].filter((ticker) => !expectedTickers.has(ticker));
  const reportCopies = [];

  const errors = [];
  if (!payload.quality?.complete) errors.push("上游站点数据未标记为完整");
  if (!artifactCompanyCountValid) errors.push(`公司数不是有效正整数：${payload.companyCount}`);
  if (payload.companyCount !== expectedCompanyCount || payloadCompanies.length !== expectedCompanyCount || actualTickers.size !== expectedCompanyCount) {
    errors.push(`公司数应为 ${expectedCompanyCount}，实际 ${payload.companyCount}/${payloadCompanies.length}/${actualTickers.size}`);
  }
  if (payload.rowCount !== expectedDirectedRows) errors.push(`定向记录应为 ${expectedDirectedRows}，实际 ${payload.rowCount}`);
  if (payload.pairCount !== expectedPairCount) errors.push(`公司对应为 ${expectedPairCount}，实际 ${payload.pairCount}`);
  if (missing.length && !allowHistoricalCohort) errors.push(`缺失公司：${missing.join(", ")}`);
  if (extra.length) errors.push(`额外公司：${extra.join(", ")}`);

  for (const row of payloadCompanies) {
    const source = path.join(siteDataRoot, "companies", `${row.ticker}.json`);
    const detail = JSON.parse(await readText(source));
    if (detail.pairs?.length !== expectedCompanyCount - 1) {
      errors.push(`${row.ticker} 明细应有 ${expectedCompanyCount - 1} 个对手，实际 ${detail.pairs?.length || 0}`);
      continue;
    }
    reportCopies.push({ source, target: path.join(PUBLIC_DATA, row.dataFile) });
  }

  if (errors.length) {
    throw new Error(`公司横评站点数据校验失败：\n- ${errors.slice(0, 30).join("\n- ")}`);
  }
  if (copyReports) {
    for (const { source, target } of reportCopies) {
      await fs.mkdir(path.dirname(target), { recursive: true });
      await fs.copyFile(source, target);
    }
  }
  const coverageComplete = missing.length === 0 && extra.length === 0;
  return {
    ...payload,
    missing,
    quality: {
      ...payload.quality,
      sourceComplete: Boolean(payload.quality?.complete),
      coverageComplete,
      complete: Boolean(payload.quality?.complete) && coverageComplete,
    },
  };
}

async function buildScenarioDecisions(
  indexRows,
  { siteDataRoot = SCENARIO_DECISION_SITE_DATA_ROOT, copyReports = true, allowHistoricalCohort = false } = {},
) {
  const payload = JSON.parse(await readText(path.join(siteDataRoot, "current.json")));
  const payloadCompanies = Array.isArray(payload.companies) ? payload.companies : [];
  const currentCompanyCount = indexRows.length;
  const artifactCompanyCount = Number(payload.companyCount);
  const artifactCompanyCountValid = Number.isInteger(artifactCompanyCount) && artifactCompanyCount > 0;
  const expectedCompanyCount = allowHistoricalCohort && artifactCompanyCountValid
    ? artifactCompanyCount
    : currentCompanyCount;
  const expectedCellCount = expectedCompanyCount * 20;
  const expectedTickers = new Set(indexRows.map((row) => row.ticker));
  const actualTickers = new Set(payloadCompanies.map((row) => row.ticker));
  const missing = [...expectedTickers].filter((ticker) => !actualTickers.has(ticker));
  const extra = [...actualTickers].filter((ticker) => !expectedTickers.has(ticker));
  const errors = [];
  const reportCopies = [];

  if (payload.schemaVersion !== 1 || payload.source !== "companyScenarioDecisionSiteData") {
    errors.push(`站点数据契约版本或来源不支持：${payload.schemaVersion}/${payload.source}`);
  }
  if (!payload.quality?.complete) errors.push("上游公司情景投资决策站点数据未标记为完整");
  if (!artifactCompanyCountValid) errors.push(`公司数不是有效正整数：${payload.companyCount}`);
  if (
    payload.sourceRoot !== "分析报告/公司情景投资决策" ||
    payload.resultRoot !== "分析报告/公司情景投资决策/结果"
  ) {
    errors.push(`上游目录边界不符合约定：${payload.sourceRoot}/${payload.resultRoot}`);
  }
  if (payload.companyCount !== expectedCompanyCount || payloadCompanies.length !== expectedCompanyCount || actualTickers.size !== expectedCompanyCount) {
    errors.push(`公司数应为 ${expectedCompanyCount}，实际 ${payload.companyCount}/${payloadCompanies.length}/${actualTickers.size}`);
  }
  if (payload.cellCount !== expectedCellCount) errors.push(`矩阵格子应为 ${expectedCellCount}，实际 ${payload.cellCount}`);
  if (payload.scenarioGrid?.length !== 20) errors.push(`全局情景矩阵应有20格，实际 ${payload.scenarioGrid?.length || 0}`);
  if (payload.operatingScenarios?.length !== 4 || payload.marketStates?.length !== 5) {
    errors.push(`经营/市场状态契约应为4×5，实际 ${payload.operatingScenarios?.length || 0}×${payload.marketStates?.length || 0}`);
  }
  if (missing.length && !allowHistoricalCohort) errors.push(`缺失公司：${missing.join(", ")}`);
  if (extra.length) errors.push(`额外公司：${extra.join(", ")}`);

  for (const row of payloadCompanies) {
    if (row.matrix?.cellCount !== 20) errors.push(`${row.ticker} 摘要矩阵应有20格，实际 ${row.matrix?.cellCount || 0}`);
    if (!row.current?.operatingScenario || !row.current?.marketState || !row.current?.adviceKey) {
      errors.push(`${row.ticker} 当前定位字段不完整`);
    }
    const source = path.join(siteDataRoot, "companies", `${row.ticker}.json`);
    const detail = JSON.parse(await readText(source));
    if (detail.ticker !== row.ticker || detail.cells?.length !== 20) {
      errors.push(`${row.ticker} 明细身份或矩阵不完整：${detail.ticker}/${detail.cells?.length || 0}`);
      continue;
    }
    reportCopies.push({ source, target: path.join(PUBLIC_DATA, row.dataFile) });
  }

  if (errors.length) {
    throw new Error(`公司情景投资决策站点数据校验失败：\n- ${errors.slice(0, 40).join("\n- ")}`);
  }
  if (copyReports) {
    for (const { source, target } of reportCopies) {
      await fs.mkdir(path.dirname(target), { recursive: true });
      await fs.copyFile(source, target);
    }
  }
  const coverageComplete = missing.length === 0 && extra.length === 0;
  return {
    ...payload,
    missing,
    quality: {
      ...payload.quality,
      sourceComplete: Boolean(payload.quality?.complete),
      coverageComplete,
      complete: Boolean(payload.quality?.complete) && coverageComplete,
    },
  };
}

async function buildTechnicalResearch({ siteDataRoot = TECHNICAL_SITE_DATA_ROOT } = {}) {
  const payload = JSON.parse(await readText(path.join(siteDataRoot, "current.json")));
  const expectedFactorIds = Array.from({ length: 18 }, (_, index) => `MF${String(index + 1).padStart(3, "0")}`);
  const factorIds = (payload.factors || []).map((factor) => factor.id);
  const actualFactorIds = new Set(factorIds);
  const missing = expectedFactorIds.filter((id) => !actualFactorIds.has(id));
  const extra = [...actualFactorIds].filter((id) => !expectedFactorIds.includes(id));
  const errors = [];

  if (payload.schemaVersion !== 1 || payload.source !== "technicalResearchSiteData") {
    errors.push(`站点数据契约版本或来源不支持：${payload.schemaVersion}/${payload.source}`);
  }
  if (!payload.quality?.complete) errors.push("上游技术面站点数据未标记为完整");
  if (payload.sourceRoot !== "技术面/因子研究" || payload.resultRoot !== "技术面/站点数据") {
    errors.push(`上游目录边界不符合约定：${payload.sourceRoot}/${payload.resultRoot}`);
  }
  if (payload.factorCount !== 18 || payload.factors?.length !== 18 || actualFactorIds.size !== 18) {
    errors.push(`因子数应为 18，实际 ${payload.factorCount}/${payload.factors?.length || 0}/${actualFactorIds.size}`);
  }
  if (payload.marketCount !== 5 || payload.scope?.markets?.length !== 5) {
    errors.push(`市场数应为 5，实际 ${payload.marketCount}/${payload.scope?.markets?.length || 0}`);
  }
  if (payload.horizonCount !== 5 || payload.scope?.horizons?.join("/") !== "10/21/63/126/252") {
    errors.push(`窗口契约不完整：${payload.scope?.horizons?.join("/") || "空"}`);
  }
  if (missing.length) errors.push(`缺失因子：${missing.join(", ")}`);
  if (extra.length) errors.push(`额外因子：${extra.join(", ")}`);

  const familyFactorIds = (payload.families || []).flatMap((family) => family.factorIds || []);
  const familyCountByFactor = Object.fromEntries(expectedFactorIds.map((id) => [id, familyFactorIds.filter((value) => value === id).length]));
  const familyCoverageErrors = Object.entries(familyCountByFactor).filter(([, count]) => count !== 1);
  if (familyCoverageErrors.length) {
    errors.push(`因子家族映射必须一对一：${familyCoverageErrors.map(([id, count]) => `${id}=${count}`).join(", ")}`);
  }

  for (const factor of payload.factors || []) {
    if (!factor.markdown?.startsWith("# ")) errors.push(`${factor.id} 缺少完整 Markdown 报告`);
    if (!factor.sourceFile?.startsWith("技术面/因子研究/")) errors.push(`${factor.id} 来源路径越界：${factor.sourceFile}`);
    if (Object.keys(factor.outlook || {}).sort().join("/") !== "10/126/21/252/63") {
      errors.push(`${factor.id} 五窗口摘要不完整`);
    }
  }

  if (errors.length) throw new Error(`技术面站点数据校验失败：\n- ${errors.slice(0, 40).join("\n- ")}`);
  return payload;
}

async function buildIndustryReports(indexRows) {
  const indexedByName = new Map(indexRows.map((row) => [canonicalIndustryKey(row.name), row]));
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
        category: indexedByName.get(canonical)?.category || category,
        topicType: indexedByName.get(canonical)?.topicType || "行业",
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

async function buildRankings(
  companyIndex,
  { siteDataRoot = COMPANY_SORTING_SITE_DATA_ROOT, allowHistoricalCohort = false } = {},
) {
  const payload = JSON.parse(await readText(path.join(siteDataRoot, "current.json")));
  const errors = [];
  const runs = payload.runs || {};
  const order = payload.order || [];
  const runEntries = Object.entries(runs);
  const expectedTickers = new Set(companyIndex.map((row) => canonicalTicker(row.ticker)));
  const methodIds = new Set(runEntries.map(([, run]) => run.methodId));
  const effectivenessIds = new Set((payload.effectiveness?.methods || []).map((row) => row.methodId));
  const missingAcrossRuns = new Set();

  if (payload.schemaVersion !== 3 || payload.source !== "companySortingSiteData") {
    errors.push(`站点数据契约版本或来源不支持：${payload.schemaVersion}/${payload.source}`);
  }
  if (!payload.validation?.complete) errors.push("上游公司排序站点数据未标记为完整");
  if (order.length !== runEntries.length || new Set(order).size !== order.length) {
    errors.push(`榜单顺序与榜单对象不一致：${order.length}/${runEntries.length}`);
  }
  if (order.some((key) => !runs[key])) errors.push("榜单顺序包含不存在的榜单键");
  if (!runs[payload.defaultRunKey]) errors.push(`默认榜单不存在：${payload.defaultRunKey}`);
  if (runEntries.length !== payload.validation?.listCount) {
    errors.push(`公开榜单数不一致：${runEntries.length}/${payload.validation?.listCount}`);
  }
  if (methodIds.size !== payload.validation?.methodCount || effectivenessIds.size !== methodIds.size) {
    errors.push(`公开方法数或效果记录数不一致：${methodIds.size}/${effectivenessIds.size}/${payload.validation?.methodCount}`);
  }
  if (
    payload.publicationPolicy?.publishedMethodCount !== payload.validation?.methodCount ||
    payload.publicationPolicy?.publishedListCount !== payload.validation?.listCount
  ) {
    errors.push("发布策略计数与站点数据校验计数不一致");
  }

  for (const [key, run] of runEntries) {
    const rows = run.rows || [];
    const ranks = new Set(rows.map((row) => Number(row.rank)));
    const tickers = new Set(rows.map((row) => canonicalTicker(row.ticker)).filter(Boolean));
    const missing = [...expectedTickers].filter((ticker) => !tickers.has(ticker));
    const extra = [...tickers].filter((ticker) => !expectedTickers.has(ticker));
    for (const ticker of missing) missingAcrossRuns.add(ticker);
    if (
      run.key !== key ||
      rows.length !== payload.validation.expectedRowsPerList ||
      ranks.size !== payload.validation.expectedRowsPerList ||
      tickers.size !== payload.validation.expectedRowsPerList ||
      extra.length ||
      (missing.length && !allowHistoricalCohort)
    ) {
      errors.push(
        `${key} 榜单无效：rows=${rows.length}, ranks=${ranks.size}, tickers=${tickers.size}, missing=${missing.length}, extra=${extra.length}`,
      );
    }
  }

  if (errors.length) {
    throw new Error(`公司排序站点数据校验失败：\n- ${errors.slice(0, 30).join("\n- ")}`);
  }
  const missing = [...missingAcrossRuns].sort();
  const coverageComplete = missing.length === 0;
  return {
    ...payload,
    missing,
    validation: {
      ...payload.validation,
      sourceComplete: Boolean(payload.validation?.complete),
      coverageComplete,
      complete: Boolean(payload.validation?.complete) && coverageComplete,
    },
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
  const planDefinitions = await readFeaturePlanDefinitions();
  const definitionById = new Map(planDefinitions.map((definition) => [definition.id, definition]));
  const discoveredAlphaIds = planDefinitions.filter((definition) => definition.layer === "alpha").map((definition) => definition.id);
  const discoveredGateIds = planDefinitions.filter((definition) => definition.layer === "gate").map((definition) => definition.id);
  const alphaFeatureIds = discoveredAlphaIds.length ? discoveredAlphaIds : DEFAULT_ALPHA_FEATURE_IDS;
  const gateIds = discoveredGateIds.length ? discoveredGateIds : DEFAULT_GATE_IDS;
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

  for (const id of activeIds) {
    const layer = id.startsWith("N") ? "alpha" : "gate";
    const definition = definitionById.get(id);
    const scoreFile = latestByFeature.get(id);
    const featureName = definition?.name || scoreFile?.featureName || id;
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
      planPath: definition?.sourcePath || "",
      rowCount: rows.length,
      hasScores: Boolean(scoreFile && rows.length),
      concept: definition?.concept || "",
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
    featureGroups: {
      alpha: alphaFeatureIds,
      gates: gateIds,
    },
    alphaFeatureIds,
    gateIds,
    scoreFileCount: latestByFeature.size,
    parseProblems,
  };
}

async function readFeaturePlanDefinitions() {
  const names = (await safeReadDir(FEATURE_PLAN_ROOT)).filter((name) => FEATURE_PLAN_FILE_PATTERN.test(name));
  const definitions = await Promise.all(names.map(async (name) => {
    const match = name.match(FEATURE_PLAN_FILE_PATTERN);
    const file = path.join(FEATURE_PLAN_ROOT, name);
    const content = await readText(file);
    return {
      id: match[1],
      name: match[2],
      layer: match[1].startsWith("N") ? "alpha" : "gate",
      concept: extractFeatureConcept(content),
      sourcePath: relativePath(file),
    };
  }));
  return definitions.sort((a, b) => a.id.localeCompare(b.id));
}

function extractFeatureConcept(markdown) {
  const lines = String(markdown || "").split(/\r?\n/u);
  const headingIndex = lines.findIndex((line) => /^##\s+.*(?:研究命题|研究目标与哲学)/u.test(line.trim()));
  if (headingIndex < 0) return "";
  for (let index = headingIndex + 1; index < lines.length; index += 1) {
    const line = lines[index].trim();
    if (!line) continue;
    if (line.startsWith("#")) return "";
    return line;
  }
  return "";
}

async function loadDailyNews({ siteDataRoot = DAILY_NEWS_SITE_DATA_ROOT } = {}) {
  const payload = JSON.parse(await readText(path.join(siteDataRoot, "current.json")));
  const items = Array.isArray(payload.items) ? payload.items : [];
  const dates = items.map((item) => item.date);
  const errors = [];

  if (payload.schemaVersion !== 1 || payload.source !== "dailyNewsSiteData") {
    errors.push(`站点数据契约版本或来源不支持：${payload.schemaVersion}/${payload.source}`);
  }
  if (!items.length) errors.push("没有可发布的每日 AI 新闻");
  if (new Set(dates).size !== dates.length) errors.push("每日 AI 新闻日期不唯一");
  if (dates.join("/") !== [...dates].sort().reverse().join("/")) errors.push("每日 AI 新闻未按日期倒序排列");
  if (payload.latestDate !== dates[0] || payload.oldestDate !== dates.at(-1)) {
    errors.push(`新闻日期边界不一致：${payload.latestDate}/${payload.oldestDate}`);
  }

  for (const item of items) {
    if (!/^\d{4}-\d{2}-\d{2}$/u.test(item.date || "") || !item.title || !item.markdown) {
      errors.push(`${item.date || "未知日期"} 的标题或正文不完整`);
    }
    if (!item.sourcePath?.startsWith("金融资料/最新AI新闻/新闻稿/")) {
      errors.push(`${item.date || "未知日期"} 的来源路径越界：${item.sourcePath || "空"}`);
    }
    if (/[A-Z]:[\\/]/u.test(item.markdown || "")) {
      errors.push(`${item.date || "未知日期"} 的公开正文包含本地绝对路径`);
    }
    if (item.audio) {
      const expectedPrefix = "data/daily-news/audio/";
      if (!item.audio.url?.startsWith(expectedPrefix)) {
        errors.push(`${item.date || "未知日期"} 的音频 URL 越界：${item.audio.url || "空"}`);
      } else {
        const audioFile = path.join(siteDataRoot, "audio", path.basename(item.audio.url));
        const stat = await fs.stat(audioFile).catch(() => null);
        if (!stat?.isFile() || stat.size <= 0) errors.push(`${item.date || "未知日期"} 的音频文件缺失或为空`);
      }
    }
  }

  if (errors.length) throw new Error(`每日 AI 新闻站点数据校验失败：\n- ${errors.slice(0, 30).join("\n- ")}`);
  return payload;
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
  scenarioDecisions,
  technicalResearch,
  moduleBuilds,
}) {
  const alerts = [];
  for (const [id, result] of Object.entries(moduleBuilds || {})) {
    if (result.status !== "stale") continue;
    const version = result.dataDate || result.generatedAt || "上一版";
    alerts.push({
      severity: "warn",
      type: `module-stale-${id}`,
      title: `${MODULE_LABELS[id] || id}沿用上一版站点数据`,
      message: `本次独立生成失败；当前展示 ${version} 的最近有效版本。${result.error ? ` ${result.error}` : ""}`.trim(),
    });
  }
  const companyReportMissing = companies.filter((company) => !company.hasReport);
  if (companyReportMissing.length) {
    alerts.push({
      severity: "warn",
      type: "company-report-missing",
      title: "公司索引中存在未匹配正式报告",
      message: companyReportMissing.map((c) => c.ticker).join(", "),
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
      message: "公司排序站点数据 current.json 没有生成可用公开榜单。",
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
      message: "未从 金融资料/最新AI新闻/新闻稿 匹配到可发布文件。",
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

  if (scenarioDecisions.quality?.warningCount) {
    alerts.push({
      severity: "info",
      type: "scenario-decision-na-cells",
      title: "部分公司情景格子无法可靠估值",
      message: scenarioDecisions.quality.warnings.join("；"),
    });
  }
  if (scenarioDecisions.missing?.length) {
    alerts.push({
      severity: "warn",
      type: "scenario-decision-missing",
      title: "公司情景投资决策未覆盖全部公司",
      message: `缺失 ${scenarioDecisions.missing.length} 家：${scenarioDecisions.missing.join(", ")}`,
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
      industryIndexCount: industryIndex.length,
      industryReportUnique: industries.filter((industry) => industry.hasReport).length,
      featureDefinitionCount: features.features.length,
      featureFileCount: features.scoreFileCount,
      alphaFeatureCount: features.alphaFeatureIds.length,
      gateCount: features.gateIds.length,
      companyComparisonCount: companyComparisons.companyCount,
      companyComparisonRowCount: companyComparisons.rowCount,
      companyComparisonDate: companyComparisons.reportDate,
      scenarioDecisionCount: scenarioDecisions.companyCount,
      scenarioDecisionCellCount: scenarioDecisions.cellCount,
      scenarioDecisionEstimableCellCount: scenarioDecisions.estimableCellCount,
      scenarioDecisionDate: scenarioDecisions.reportDate,
      technicalFactorCount: technicalResearch.factorCount,
      technicalMarketCount: technicalResearch.marketCount,
      technicalHorizonCount: technicalResearch.horizonCount,
      technicalReportDate: technicalResearch.reportDate,
      dailyNewsCount: dailyNews.items.length,
      rankingMethodCount: rankings.validation?.methodCount || 0,
      rankingListCount: rankings.validation?.listCount || 0,
      rankingExpectedListCount: rankings.validation?.expectedListCount || 0,
      rankingRegisteredMethodCount: rankings.validation?.registeredMethodCount || 0,
      rankingRegisteredListCount: rankings.validation?.registeredListCount || 0,
      rankingEvaluationId: rankings.currentEvaluation?.id || "",
      rankingRuns: Object.fromEntries(Object.entries(rankings.runs).map(([key, run]) => [key, run.rowCount])),
      rawIndustryReportCount: industryReports.size,
      moduleBuilds: Object.fromEntries(Object.entries(moduleBuilds || {}).map(([id, result]) => [id, result.status])),
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

function buildMeta({
  companies,
  industries,
  rankings,
  features,
  quality,
  latestFinancialDate,
  dailyNews,
  companyComparisons,
  scenarioDecisions,
  technicalResearch,
  moduleBuilds,
}) {
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
    industryCount: industries.length,
    industryReportCount: industries.filter((industry) => industry.hasReport).length,
    featureCount: features.features.length,
    featureScoreFileCount: features.scoreFileCount,
    alphaFeatureCount: features.alphaFeatureIds.length,
    gateCount: features.gateIds.length,
    latestRankingDate: rankingDates.at(-1) || "",
    rankingMethodCount: rankings.validation?.methodCount || 0,
    rankingListCount: rankings.validation?.listCount || 0,
    rankingRegisteredMethodCount: rankings.validation?.registeredMethodCount || 0,
    rankingRegisteredListCount: rankings.validation?.registeredListCount || 0,
    currentRankingEvaluationId: rankings.currentEvaluation?.id || "",
    currentRankingEvidenceType: rankings.currentEvaluation?.evidenceType || "",
    currentRankingPriceAsOf: rankings.currentEvaluation?.priceAsOf || "",
    latestCompanyComparisonDate: companyComparisons.reportDate,
    companyComparisonCount: companyComparisons.companyCount,
    companyComparisonRowCount: companyComparisons.rowCount,
    latestScenarioDecisionDate: scenarioDecisions.reportDate,
    scenarioDecisionCount: scenarioDecisions.companyCount,
    scenarioDecisionCellCount: scenarioDecisions.cellCount,
    scenarioDecisionEstimableCellCount: scenarioDecisions.estimableCellCount,
    latestTechnicalResearchDate: technicalResearch.reportDate,
    technicalFactorCount: technicalResearch.factorCount,
    technicalMarketCount: technicalResearch.marketCount,
    technicalHorizonCount: technicalResearch.horizonCount,
    latestFinancialDate,
    latestDailyNewsDate: dailyNews.latestDate,
    dailyNewsCount: dailyNews.items.length,
    qualityAlertCount: quality.alerts.length,
    moduleBuilds,
  };
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
  return text.replace(/D:\\(?:drive\\)?Investment\\/gi, "Investment\\").replace(/D:\/(?:drive\/)?Investment\//gi, "Investment/");
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

if (path.resolve(process.argv[1] || "") === __filename) {
  buildData().catch((error) => {
    console.error(error.stack || error.message || error);
    process.exitCode = 1;
  });
}
