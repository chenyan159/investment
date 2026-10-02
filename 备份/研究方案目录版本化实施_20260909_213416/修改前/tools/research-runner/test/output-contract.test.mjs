import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { companyDomain } from "../domains/company.mjs";
import { createFileRunQueueItem, fileRunDomain } from "../domains/file-run.mjs";
import { DOMAIN_ADAPTERS } from "../domains/index.mjs";
import { buildOutputInstruction } from "../prompts/common.mjs";
import {
  ANALYSIS_ROOT,
  FUNDAMENTAL_ROOT,
  normalizeProjectPath,
  PROJECT_ROOT,
} from "../queue-store.mjs";
import {
  captureOutputSnapshot,
  createOutputContract,
  validateLocalOutput,
} from "../validators/output-validator.mjs";

test("project root is Investment and standard domain output paths are Investment-relative", () => {
  assert.equal(FUNDAMENTAL_ROOT, path.join(PROJECT_ROOT, "基本面"));
  assert.equal(ANALYSIS_ROOT, path.join(PROJECT_ROOT, "分析报告"));
  const item = companyDomain.createQueueItem({
    subject: "TEST",
    displayName: "Test Company",
    category: "AI服务器_存储_EMS",
    startedAt: "2026-07-12 12:00:00",
  });
  const contract = createOutputContract(item, companyDomain);
  assert.equal(contract.runDate, "2026-07-12");
  assert.equal(
    contract.expectedOutputFile,
    "基本面/公司调研/AI服务器_存储_EMS/TEST_Test_Company_公司调研_2026-07-12.md",
  );
});

test("legacy company output paths normalize to the Investment-relative schema", () => {
  const item = companyDomain.createQueueItem({
    subject: "TEST",
    category: "AI服务器_存储_EMS",
    outputFile: "公司调研/AI服务器_存储_EMS/TEST_Test_公司调研_2026-07-12.md",
  });
  assert.equal(item.outputFile, "基本面/公司调研/AI服务器_存储_EMS/TEST_Test_公司调研_2026-07-12.md");
});

test("every indexed standard-domain prompt injects its exact local output path exactly once", () => {
  for (const [name, domain] of Object.entries(DOMAIN_ADAPTERS)) {
    if (name === "file-run") continue;
    const entries = domain.parseIndexEntries();
    assert.ok(entries.length > 0, `${name} has index entries for the contract test`);
    for (const entry of entries) {
      const item = domain.createQueueItem({
        subject: entry.subject,
        startedAt: "2026-07-12 12:00:00",
      });
      const contract = createOutputContract(item, domain);
      assert.ok(
        contract.expectedOutputFile.startsWith("基本面/")
          || contract.expectedOutputFile.startsWith("分析报告/")
          || contract.expectedOutputFile.startsWith("情绪面/"),
        `${name}/${entry.subject} output is Investment-relative`,
      );
      const prompt = domain.buildFormalPrompt(
        item,
        contract,
      );
      const occurrences = prompt.split(contract.expectedOutputFile).length - 1;
      assert.equal(occurrences, 1, `${name}/${entry.subject} prompt has one authoritative output path`);
    }
  }
});

test("production domains use file-only local output validation", () => {
  for (const [name, domain] of Object.entries(DOMAIN_ADAPTERS)) {
    assert.equal(
      typeof domain.validateOutputContentForItem,
      "undefined",
      `${name} must not register content validation in the local output validator`,
    );
  }
});

test("retired company-evaluation is not an active domain", () => {
  assert.equal(DOMAIN_ADAPTERS["company-evaluation"], undefined);
});

test("the appended prompt contains only the concise output contract", () => {
  assert.equal(
    buildOutputInstruction({ expectedOutputFile: "基本面/结果.md" }),
    "\n## 本次输出\n\n将完整研究结果写入 `基本面/结果.md`。不得更改该路径，也不得创建第二份正式报告。\n",
  );
  assert.equal(
    buildOutputInstruction({ expectedOutputDir: "基本面/结果" }),
    "\n## 本次输出\n\n在 `基本面/结果` 内只生成或更新一份完整研究结果；不得修改输入研究方案。\n",
  );
});

test("research plans leave filesystem output routing to the runner", () => {
  const standardPlans = [
    "基本面/公司调研/研究方法/调研方案.md",
    "基本面/行业调研/研究方法/行业调研方案.md",
    "分析报告/公司对比/研究方案.md",
    "分析报告/公司情景投资决策/研究方案.md",
    "情绪面/研究方法/研究方案.md",
  ];
  const filesystemRule = /把报告写入|正式输出目录固定为|输出目录固定为|推荐输出文件名：|结果写入 `D:\\drive\\Investment\\情绪面\\公司情绪\\`/u;
  for (const relativePath of standardPlans) {
    const source = fs.readFileSync(path.join(PROJECT_ROOT, ...relativePath.split("/")), "utf8");
    assert.doesNotMatch(source, filesystemRule, relativePath);
    assert.doesNotMatch(source, /research[- ]?runner|runner|入队|队列工具/iu, relativePath);
  }

  const featurePlansDir = path.join(FUNDAMENTAL_ROOT, "特征量化", "研究方案");
  const featurePlans = fs.readdirSync(featurePlansDir).filter((name) => /^[NG]\d{2}_.+_研究方案\.md$/u.test(name));
  assert.equal(featurePlans.length, 19);
  for (const name of featurePlans) {
    const source = fs.readFileSync(path.join(featurePlansDir, name), "utf8");
    assert.doesNotMatch(source, /结果写入：\s*`基本面\/特征量化\/量化评分\//u, name);
    assert.doesNotMatch(source, /research[- ]?runner|runner|入队|队列工具/iu, name);
    assert.match(source, /^##\s+.*(?:输出|产出|门槛结论|覆盖层结论)/mu, name);
    assert.match(source, /(?:全公司|全部公司|每家公司|全样本|股票池|全部可识别证券)/u, name);
  }
});

test("file-run defaults its output directory to the prompt file directory", () => {
  const relativeDir = "tools/research-runner/test/file-run-default";
  const absoluteDir = path.join(PROJECT_ROOT, ...relativeDir.split("/"));
  const promptPath = path.join(absoluteDir, "plan.md");
  fs.mkdirSync(absoluteDir, { recursive: true });
  fs.writeFileSync(promptPath, "# test plan\n", "utf8");
  try {
    const item = createFileRunQueueItem({ runId: "default-dir", promptFile: normalizeProjectPath(path.relative(PROJECT_ROOT, promptPath)) });
    assert.equal(item.expectedOutputDir, relativeDir);
    assert.equal(item.expectedOutputFile, "");
  } finally {
    fs.rmSync(absoluteDir, { recursive: true, force: true });
  }
});

test("exact local validation ignores document content and accepts repeated table fields", () => {
  const relativeDir = "tools/research-runner/test/local-output-exact";
  const absoluteDir = path.join(PROJECT_ROOT, ...relativeDir.split("/"));
  const outputFile = `${relativeDir}/result.md`;
  fs.mkdirSync(absoluteDir, { recursive: true });
  const domain = {
    domain: "test-exact",
    outputPrefix: `${relativeDir}/`,
    outputFilePattern: /^result\.md$/u,
    allowedCategories: new Set(),
    allowNonFormalOutputDirs: true,
    expectedOutputFile: () => outputFile,
    validateOutputContentForItem() {
      throw new Error("content validation must not run");
    },
  };
  const item = { domain: domain.domain, subject: "test", startedAt: "2020-01-01 00:00:00" };
  try {
    const contract = createOutputContract(item, domain);
    fs.writeFileSync(
      path.join(absoluteDir, "result.md"),
      [
        "# result",
        "",
        "| ticker | company | source_id |",
        "|---|---|---|",
        "| AAA | Alpha | S1 |",
        "",
        "| ticker | storage_platform | source_id |",
        "|---|---|---|",
        "| BBB | storage_platform | S2 |",
        "",
      ].join("\n"),
      "utf8",
    );
    assert.equal(validateLocalOutput(item, domain, contract), outputFile);
  } finally {
    fs.rmSync(absoluteDir, { recursive: true, force: true });
  }
});

test("exact local validation normalizes one matching fresh filename deviation", () => {
  const relativeDir = "tools/research-runner/test/local-output-recovery";
  const absoluteDir = path.join(PROJECT_ROOT, ...relativeDir.split("/"));
  const expectedOutputFile = `${relativeDir}/result.md`;
  fs.mkdirSync(absoluteDir, { recursive: true });
  const domain = {
    domain: "test-recovery",
    outputPrefix: `${relativeDir}/`,
    outputFilePattern: /^result(?:-alternate)?\.md$/u,
    allowedCategories: new Set(),
    allowNonFormalOutputDirs: true,
    expectedOutputFile: () => expectedOutputFile,
  };
  const item = { domain: domain.domain, subject: "test", startedAt: "2020-01-01 00:00:00" };
  try {
    const contract = createOutputContract(item, domain);
    const before = captureOutputSnapshot(contract, item);
    fs.writeFileSync(path.join(absoluteDir, "result-alternate.md"), "# result\n", "utf8");
    assert.equal(validateLocalOutput(item, domain, contract, before), expectedOutputFile);
    assert.equal(contract.recoveredFrom, `${relativeDir}/result-alternate.md`);
    assert.equal(fs.existsSync(path.join(absoluteDir, "result.md")), true);
    assert.equal(fs.existsSync(path.join(absoluteDir, "result-alternate.md")), false);
  } finally {
    fs.rmSync(absoluteDir, { recursive: true, force: true });
  }
});

test("directory-mode file-run accepts exactly one changed output", () => {
  const relativeDir = "tools/research-runner/test/local-output-directory";
  const absoluteDir = path.join(PROJECT_ROOT, ...relativeDir.split("/"));
  const promptFile = `${relativeDir}/plan.md`;
  fs.mkdirSync(absoluteDir, { recursive: true });
  fs.writeFileSync(path.join(absoluteDir, "plan.md"), "# plan\n", "utf8");
  const item = createFileRunQueueItem({ runId: "directory-mode", promptFile, startedAt: "2020-01-01 00:00:00" });
  try {
    const contract = createOutputContract(item, fileRunDomain);
    const before = captureOutputSnapshot(contract, item);
    fs.writeFileSync(path.join(absoluteDir, "result.md"), "# result\n", "utf8");
    assert.equal(validateLocalOutput(item, fileRunDomain, contract, before), `${relativeDir}/result.md`);
  } finally {
    fs.rmSync(absoluteDir, { recursive: true, force: true });
  }
});
