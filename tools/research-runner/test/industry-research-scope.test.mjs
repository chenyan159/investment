import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { industryDomain, parseIndustryIndexEntries } from "../domains/industry.mjs";
import { createOutputContract } from "../validators/output-validator.mjs";

test("industry index accepts legacy rows and carries optional research scope", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "industry-scope-"));
  const file = path.join(dir, "index.md");
  try {
    fs.writeFileSync(file, [
      "| 行业名称 | 目录 | 研究范围提示 |",
      "|---|---|---|",
      "| 旧专题 | `AI服务器_存储_芯片/` |",
      "| 新专题 | `AI应用_软件_数据平台/` | 客户付费，区分系统和应用。 |",
    ].join("\n"));
    assert.deepEqual(parseIndustryIndexEntries(file), [
      { subject: "旧专题", displayName: "旧专题", category: "AI服务器_存储_芯片", researchScope: "" },
      { subject: "新专题", displayName: "新专题", category: "AI应用_软件_数据平台", researchScope: "客户付费，区分系统和应用。" },
    ]);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test("every indexed industry routes to an allowed category without generating reports", () => {
  const entries = industryDomain.parseIndexEntries();
  assert.equal(new Set(entries.map((entry) => entry.subject)).size, entries.length);
  for (const entry of entries) {
    assert.ok(industryDomain.allowedCategories.has(entry.category), entry.subject);
    const item = industryDomain.createQueueItem({
      subject: entry.subject,
      sourceDate: "2026-09-05",
      startedAt: "2026-09-05 12:00:00",
    });
    const contract = createOutputContract(item, industryDomain);
    assert.ok(contract.expectedOutputFile.startsWith(`基本面/行业调研/结果/${entry.category}/`));
    assert.ok(industryDomain.outputFilePattern.test(path.posix.basename(contract.expectedOutputFile)));
  }
});

test("new application topics are indexed and their actual formal prompt includes the specific scope", () => {
  const subjects = [
    "企业AI与Agent工作流软件",
    "AI创作与文档生产软件",
    "数据平台、数据库与AI数据软件",
    "网络安全、身份权限与AI治理",
    "广告推荐、搜索与数字分发",
  ];
  for (const subject of subjects) {
    const entry = industryDomain.resolveIndexEntry(subject);
    assert.equal(entry.category, "AI应用_软件_数据平台");
    assert.ok(entry.researchScope.length > 0);
    const item = industryDomain.createQueueItem({ subject, sourceDate: "2026-09-05", startedAt: "2026-09-05 12:00:00" });
    const contract = createOutputContract(item, industryDomain);
    const prompt = industryDomain.buildFormalPrompt(item, contract);
    assert.ok(prompt.includes(entry.researchScope));
    assert.ok(prompt.includes(subject));
    assert.ok(prompt.includes(contract.expectedOutputFile));
    assert.ok(!prompt.includes("【行业名称】"));
    assert.match(prompt, /可以质疑边界/u);
  }
});

test("existing subjects without a scope still build a complete formal prompt", () => {
  const entry = industryDomain.parseIndexEntries().find((item) => !item.researchScope);
  assert.ok(entry);
  const item = industryDomain.createQueueItem({ subject: entry.subject, sourceDate: "2026-09-05", startedAt: "2026-09-05 12:00:00" });
  const contract = createOutputContract(item, industryDomain);
  const prompt = industryDomain.buildFormalPrompt(item, contract);
  assert.ok(prompt.includes(entry.subject));
  assert.ok(prompt.includes(contract.expectedOutputFile));
  assert.doesNotMatch(prompt, /本专题研究范围提示|undefined/u);
});
