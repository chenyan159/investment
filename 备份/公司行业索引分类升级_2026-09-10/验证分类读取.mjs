import fs from "node:fs/promises";
import path from "node:path";
import assert from "node:assert/strict";
import { fileURLToPath, pathToFileURL } from "node:url";

const out = path.dirname(fileURLToPath(import.meta.url));
const root = "D:/drive/Investment";
const siteRoot = path.join(root, "tools/site");
const sourcePath = path.join(siteRoot, "etl/build-data.mjs");
const mirrorPath = path.join(out, "验证用ETL模块.mjs");
const scratch = path.join(out, "读取兼容性验证输出");
let source = await fs.readFile(sourcePath, "utf8");
source = source.replace('const SITE_ROOT = path.resolve(__dirname, "..");', "const SITE_ROOT = " + JSON.stringify(siteRoot) + ";");
source = source.replace('const PUBLIC_DATA = path.join(SITE_ROOT, "public", "data");', "const PUBLIC_DATA = " + JSON.stringify(scratch) + ";");
source += "\nexport { parseCompanyIndex, parseIndustryIndex, buildIndustryReports, buildCompanies };\n";
await fs.writeFile(mirrorPath, source, "utf8");
const etl = await import(pathToFileURL(mirrorPath).href);
const companies = await etl.parseCompanyIndex();
const industries = await etl.parseIndustryIndex();
assert.equal(companies.length, 218);
assert.equal(industries.length, 91);
assert.equal(industries.filter((row) => row.topicType === "横向专题").length, 1);
const reportMap = await etl.buildIndustryReports(industries);
const companyRows = await etl.buildCompanies(companies, reportMap, new Map(), industries);
assert.equal(companyRows.length, 218);
assert.equal(companyRows.filter((row) => row.hasReport).length, 193);
const byTicker = new Map(companyRows.map((row) => [row.ticker, row]));
const byName = new Map(industries.map((row) => [row.name, row]));
for (const ticker of ["CGNX", "SYM", "TTMI", "ROK", "ASTS", "NET"]) {
  const row = byTicker.get(ticker);
  assert.equal(row.hasReport, false);
  assert.ok(row.relatedIndustrySlugs.length > 0, ticker + " must retain links to pending industry topics");
}
const robotTopic = byName.get("人形机器人与关键执行部件");
assert.ok(byTicker.get("TSLA").relatedIndustrySlugs.includes(robotTopic.slug));
const semiCategory = "半导体与电子制造_设备_材料_测试";
const renamedReports = [...reportMap.values()].filter((row) => row.indexCategory === semiCategory);
assert.equal(renamedReports.length, 19);
assert.ok(renamedReports.every((row) => row.category === semiCategory));
const result = {
  companyIndexRows: companies.length,
  companyReports: companyRows.filter((row) => row.hasReport).length,
  industryIndexRows: industries.length,
  horizontalTopics: 1,
  renamedIndustryReportCategories: renamedReports.length,
  pendingIndustryLinksPreserved: true,
  outputScope: scratch,
  formalSiteDataWritten: false,
};
await fs.writeFile(path.join(out, "分类读取验证.json"), JSON.stringify(result, null, 2) + "\n", "utf8");
console.log(JSON.stringify(result));
