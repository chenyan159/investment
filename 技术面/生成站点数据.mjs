import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const TECH_ROOT = path.dirname(fileURLToPath(import.meta.url));
const PUBLICATION_FILE = path.join(TECH_ROOT, "站点发布.json");
const REPORT_ROOT = path.join(TECH_ROOT, "因子研究");
const DEFAULT_OUTPUT_ROOT = path.join(TECH_ROOT, "站点数据");
const OUTPUT_ROOT = process.env.PROJECT_ANANTA_OUTPUT_ROOT?.trim()
  ? path.resolve(process.env.PROJECT_ANANTA_OUTPUT_ROOT)
  : DEFAULT_OUTPUT_ROOT;
const OUTPUT_FILE = path.join(OUTPUT_ROOT, "current.json");
const EXPECTED_FACTOR_IDS = Array.from({ length: 18 }, (_, index) => `MF${String(index + 1).padStart(3, "0")}`);

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function reportDateFromFile(name) {
  return name.match(/研究结果_(\d{4}-\d{2}-\d{2})\.md$/u)?.[1] || "";
}

function firstHeading(markdown, fallback) {
  return markdown.match(/^#\s+(.+)$/mu)?.[1]?.trim() || fallback;
}

async function latestReportForFactor(factorId, names) {
  const matches = names
    .filter((name) => name.startsWith(`${factorId}_`) && /_研究结果_\d{4}-\d{2}-\d{2}\.md$/u.test(name))
    .sort((a, b) => reportDateFromFile(a).localeCompare(reportDateFromFile(b)) || a.localeCompare(b, "zh-CN"));
  const name = matches.at(-1);
  if (!name) throw new Error(`${factorId} 未找到正式研究结果`);
  const markdown = await fs.readFile(path.join(REPORT_ROOT, name), "utf8");
  if (!markdown.includes(factorId)) throw new Error(`${name} 正文未包含因子编号 ${factorId}`);
  return {
    sourceFile: `技术面/因子研究/${name}`,
    reportDate: reportDateFromFile(name),
    reportTitle: firstHeading(markdown, path.basename(name, ".md")),
    reportHash: sha256(markdown),
    markdown,
  };
}

async function main() {
  const publicationText = await fs.readFile(PUBLICATION_FILE, "utf8");
  const publication = JSON.parse(publicationText);
  const errors = [];

  if (publication.schemaVersion !== 1 || publication.source !== "technicalResearchPublication") {
    errors.push(`不支持的发布配置：${publication.schemaVersion}/${publication.source}`);
  }

  const factors = publication.factors || [];
  const factorIds = factors.map((factor) => factor.id);
  const uniqueFactorIds = new Set(factorIds);
  if (factors.length !== 18 || uniqueFactorIds.size !== 18) errors.push(`因子应为 18 个且编号唯一，实际 ${factors.length}/${uniqueFactorIds.size}`);
  const missing = EXPECTED_FACTOR_IDS.filter((id) => !uniqueFactorIds.has(id));
  const extra = [...uniqueFactorIds].filter((id) => !EXPECTED_FACTOR_IDS.includes(id));
  if (missing.length) errors.push(`发布配置缺少：${missing.join(", ")}`);
  if (extra.length) errors.push(`发布配置含额外编号：${extra.join(", ")}`);

  const familyIds = new Set((publication.families || []).map((family) => family.id));
  for (const factor of factors) {
    if (!familyIds.has(factor.familyId)) errors.push(`${factor.id} 引用了不存在的家族 ${factor.familyId}`);
    const horizons = Object.keys(factor.outlook || {}).map(Number).sort((a, b) => a - b);
    if (JSON.stringify(horizons) !== JSON.stringify(publication.scope?.horizons || [])) {
      errors.push(`${factor.id} 时间窗口不完整：${horizons.join("/")}`);
    }
  }
  for (const family of publication.families || []) {
    const unknown = (family.factorIds || []).filter((id) => !uniqueFactorIds.has(id));
    if (unknown.length) errors.push(`${family.id} 含未知因子：${unknown.join(", ")}`);
  }
  if (publication.scope?.markets?.length !== 5 || publication.scope?.horizons?.length !== 5) {
    errors.push("市场或时间窗口不是 5×5 契约");
  }
  if (errors.length) throw new Error(`技术面站点发布配置校验失败：\n- ${errors.join("\n- ")}`);

  const reportNames = (await fs.readdir(REPORT_ROOT)).filter((name) => name.toLowerCase().endsWith(".md"));
  const enrichedFactors = [];
  for (const factor of factors) {
    const report = await latestReportForFactor(factor.id, reportNames);
    enrichedFactors.push({ ...factor, ...report });
  }

  const reportDates = [...new Set(enrichedFactors.map((factor) => factor.reportDate))].sort();
  if (reportDates.at(-1) !== publication.reportDate) {
    throw new Error(`发布日期 ${publication.reportDate} 与最新报告日期 ${reportDates.at(-1)} 不一致`);
  }

  const sourceHash = sha256(
    [sha256(publicationText), ...enrichedFactors.map((factor) => `${factor.id}:${factor.reportHash}`)].join("\n"),
  );
  const payload = {
    schemaVersion: 1,
    source: "technicalResearchSiteData",
    generatedAt: new Date().toISOString(),
    reportDate: publication.reportDate,
    asOf: publication.asOf,
    sourceRoot: "技术面/因子研究",
    resultRoot: "技术面/站点数据",
    sourceHash,
    factorCount: enrichedFactors.length,
    marketCount: publication.scope.markets.length,
    horizonCount: publication.scope.horizons.length,
    scope: publication.scope,
    summary: publication.summary,
    marketOutlook: publication.marketOutlook,
    riskForecasts: publication.riskForecasts,
    currentSignals: publication.currentSignals,
    families: publication.families,
    factors: enrichedFactors,
    quality: {
      complete: true,
      expectedFactorCount: 18,
      factorCount: enrichedFactors.length,
      missing,
      extra,
      reportDates,
    },
  };

  assertOutputRoot();
  if (!OUTPUT_FILE.startsWith(`${OUTPUT_ROOT}${path.sep}`)) throw new Error(`拒绝写入技术面站点数据目录之外：${OUTPUT_FILE}`);
  await fs.mkdir(OUTPUT_ROOT, { recursive: true });
  await fs.writeFile(OUTPUT_FILE, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`技术面站点数据：${enrichedFactors.length} 因子 × ${payload.marketCount} 市场 × ${payload.horizonCount} 窗口`);
  console.log(`写入 ${OUTPUT_FILE}`);
}

function assertOutputRoot() {
  const resolved = path.resolve(OUTPUT_ROOT);
  const expected = path.resolve(DEFAULT_OUTPUT_ROOT);
  const isStaging = path.basename(resolved).startsWith(".站点数据-");
  if (path.dirname(resolved) !== path.resolve(TECH_ROOT) || (resolved !== expected && !isStaging)) {
    throw new Error(`拒绝写入非预期目录：${resolved}`);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
