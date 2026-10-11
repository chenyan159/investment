import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test, { after } from "node:test";

// Import real adapters against an isolated project, never the live research files.
const root = fs.mkdtempSync(path.join(os.tmpdir(), "six-stage-backups-"));
const previousRoot = process.env.RESEARCH_RUNNER_PROJECT_ROOT;
process.env.RESEARCH_RUNNER_PROJECT_ROOT = root;
const { companyDomain } = await import("../domains/company.mjs");
const { industryDomain } = await import("../domains/industry.mjs");
const { companyComparisonDomain } = await import("../domains/company-comparison.mjs");
const { companyInvestmentDecisionDomain } = await import("../domains/company-investment-decision.mjs");
const { companySentimentDomain } = await import("../domains/company-sentiment.mjs");
const { featureQuantizationDomain } = await import("../domains/feature-quantization.mjs");
const { buildOutputInstruction } = await import("../prompts/common.mjs");
if (previousRoot === undefined) delete process.env.RESEARCH_RUNNER_PROJECT_ROOT;
else process.env.RESEARCH_RUNNER_PROJECT_ROOT = previousRoot;
after(() => fs.rmSync(root, { recursive: true, force: true }));

for (const adapter of [companyDomain, industryDomain]) {
  fs.mkdirSync(path.dirname(adapter.indexPath), { recursive: true });
  fs.writeFileSync(adapter.indexPath, "| 股票代号 | 公司名称 | 目录 |\n|---|---|---|\n");
}

const cases = [
  [companyDomain, "基本面/公司调研/结果/企业软件_数据平台", "基本面/公司调研/备份/企业软件_数据平台", "TEST_测试_公司调研", { subject: "TEST", category: "企业软件_数据平台" }],
  [industryDomain, "基本面/行业调研/结果/AI服务器_存储_芯片", "基本面/行业调研/备份/AI服务器_存储_芯片", "行业调研_测试行业", { subject: "测试行业", category: "AI服务器_存储_芯片" }],
  [companyComparisonDomain, "分析报告/公司对比/结果", "分析报告/公司对比/备份", "TEST_逐家公司投资思路对比", { subject: "TEST" }],
  [companyInvestmentDecisionDomain, "分析报告/公司情景投资决策/结果", "分析报告/公司情景投资决策/备份", "TEST_经营情景市场状态投资决策", { subject: "TEST" }],
  [companySentimentDomain, "情绪面/公司情绪", "情绪面/备份/公司情绪", "TEST_测试_公司情绪", { subject: "TEST" }],
  [featureQuantizationDomain, "基本面/特征量化/量化评分", "基本面/特征量化/备份", "N01_AI可归因盈利暴露_量化评分", { subject: "N01_AI可归因盈利暴露_研究方案" }],
];

for (const [adapter, resultPath, backupPath, stem, item] of cases) {
  test(`${adapter.domain}: actual adapter backs up outside results and restores failed reruns`, () => {
    const resultDir = path.join(root, resultPath);
    const backupDir = path.join(root, backupPath);
    fs.mkdirSync(resultDir, { recursive: true });
    fs.mkdirSync(backupDir, { recursive: true });
    const fileName = `${stem}_2026-10-11.md`;
    const oldName = `${stem}_2026-10-08.md`;
    const failedName = `${stem}_2026-10-12.md`;
    const contract = { expectedOutputFile: `${resultPath}/${fileName}` };
    fs.writeFileSync(path.join(resultDir, fileName), "prior same-day report");
    fs.writeFileSync(path.join(resultDir, oldName), "older formal report");
    fs.writeFileSync(path.join(resultDir, "OTHER_2026-10-11.md"), "unrelated report");
    fs.writeFileSync(path.join(backupDir, "keep.md"), "existing history");

    const prepared = adapter.prepareFormalRun(item, contract);
    assert.ok(prepared.backupDir.startsWith(`${backupPath}/`), prepared.backupDir);
    assert.equal(fs.existsSync(path.join(resultDir, fileName)), false);
    const isFeature = adapter.domain === "feature-quantization";
    assert.equal(fs.existsSync(path.join(resultDir, oldName)), isFeature);
    assert.equal(prepared.files.length, isFeature ? 1 : 2);
    assert.equal(fs.existsSync(path.join(resultDir, "备份")), false);
    fs.writeFileSync(path.join(resultDir, fileName), "failed new report");
    if (!isFeature) fs.writeFileSync(path.join(resultDir, failedName), "failed extra report");

    adapter.rollbackFormalRun(item, prepared, contract);
    assert.equal(fs.readFileSync(path.join(resultDir, fileName), "utf8"), "prior same-day report");
    assert.equal(fs.readFileSync(path.join(resultDir, oldName), "utf8"), "older formal report");
    assert.equal(fs.readFileSync(path.join(resultDir, "OTHER_2026-10-11.md"), "utf8"), "unrelated report");
    assert.equal(fs.readFileSync(path.join(backupDir, "keep.md"), "utf8"), "existing history");
    assert.equal(fs.existsSync(path.join(root, prepared.backupDir)), false);
    assert.equal(fs.existsSync(path.join(resultDir, failedName)), false);

    const instruction = buildOutputInstruction(contract);
    assert.ok(instruction.includes("不得在其中建立备份、tmp、_work"));
    assert.ok(instruction.includes("备份和临时目录不作为研究输入"));
  });
}
