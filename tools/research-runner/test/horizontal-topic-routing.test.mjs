import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { RESEARCH_PLANS, bindResearchPlan, PLAN_PROJECT_ROOT, readResearchPlan } from "../research-plan-store.mjs";
import { createFileRunQueueItem, fileRunDomain, validateFileRunQueueItem } from "../domains/file-run.mjs";
import { createOutputContract } from "../validators/output-validator.mjs";

const topics = RESEARCH_PLANS.filter(p => p.outputRoot);

test("all six horizontal plans bind and build prompts with background output defaults", () => {
  assert.equal(topics.length, 6);
  for (const plan of topics) {
    const item = createFileRunQueueItem({ runId: `routing-${plan.id}`, promptFile: plan.directory });
    assert.equal(item.planId, plan.id);
    assert.equal(item.expectedOutputDir, plan.defaultOutputDir);
    const contract = createOutputContract(item, fileRunDomain);
    const prompt = fileRunDomain.buildFormalPrompt(item, contract);
    assert.ok(prompt.includes(contract.expectedOutputDir));
    assert.ok(prompt.includes(readResearchPlan(item).trim()));
    assert.ok(fs.existsSync(path.resolve(PLAN_PROJECT_ROOT, contract.expectedOutputDir)));
    const alias = createFileRunQueueItem({ runId: `alias-${plan.id}`, promptFile: plan.directoryAliases[0] });
    assert.equal(alias.planSha256, item.planSha256);
    assert.equal(alias.expectedOutputDir, item.expectedOutputDir);
  }
});

test("topic outputs cannot escape background; ordinary file-run remains unrestricted", () => {
  for (const plan of topics) {
    for (const directory of [plan.directory, "备份", "基本面/行业调研/产业背景旁边", "基本面/行业调研/产业背景/../结果"]) {
      assert.throws(() => createFileRunQueueItem({ runId: plan.id, promptFile: plan.directory, expectedOutputDir: directory }), /outputRoot/);
    }
    const item = createFileRunQueueItem({ runId: plan.id, promptFile: plan.directory, expectedOutputFile: `${plan.defaultOutputDir}/fixture.md` });
    fileRunDomain.validateOutputFileForItem({ item, outputFile: item.expectedOutputFile });
    assert.throws(() => validateFileRunQueueItem({ ...item, expectedOutputFile: "", expectedOutputDir: "备份" }), /outputRoot/);
  }
  const ordinary = createFileRunQueueItem({ runId: "ordinary", promptFile: "AGENTS.md", expectedOutputDir: "备份" });
  assert.equal(ordinary.expectedOutputDir, "备份");
  assert.equal(ordinary.planId, undefined);
});

test("moved bound snapshots retain version and hash, including superseded conference entry", () => {
  for (const plan of topics) {
    const item = bindResearchPlan({ domain: "file-run", promptFile: plan.directory });
    const before = { ...item };
    for (const key of ["promptFile", "planSnapshotFile", "planEntryFile"]) item[key] = item[key].replace(plan.directory, plan.directoryAliases[0]);
    bindResearchPlan(item);
    assert.equal(item.planVersion, before.planVersion);
    assert.equal(item.planSha256, before.planSha256);
    assert.equal(item.planSnapshotFile, before.planSnapshotFile);
    assert.throws(() => bindResearchPlan({ ...item, planSha256: "wrong" }), /hash mismatch/);
  }
  const conference = topics.find(p => p.id === "conference");
  const old = bindResearchPlan({ domain: "file-run", promptFile: `${conference.directoryAliases[0]}/研究方案_20260910_230757.md` });
  assert.equal(old.planVersion, "20260910_230757");
  assert.ok(readResearchPlan(old).includes("如任务指定输出文件"));
});
