import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test, { after } from "node:test";

const root = fs.mkdtempSync(path.join(os.tmpdir(), "companion-output-"));
process.env.RESEARCH_RUNNER_PROJECT_ROOT = root;
process.env.RESEARCH_RUNNER_QUEUE_DIR = path.join(root, "tools");
const { companyComparisonDomain } = await import("../domains/company-comparison.mjs");
const { companyInvestmentDecisionDomain } = await import("../domains/company-investment-decision.mjs");
const { createOutputContract, captureOutputSnapshot, validateLocalOutput, validateOutputFilePath } = await import("../validators/output-validator.mjs");
const { buildOutputInstruction } = await import("../prompts/common.mjs");
const { backupExistingOutputs } = await import("../domains/output-backup.mjs");
const queue = await import("../queue-store.mjs");
after(() => fs.rmSync(root, { recursive: true, force: true }));

for (const domain of [companyComparisonDomain, companyInvestmentDecisionDomain]) {
  test(`${domain.domain}: exact MD and JSON required; content is not inspected`, () => {
    const item = { domain: domain.domain, subject: "TEST", startedAt: new Date().toISOString() };
    const contract = createOutputContract(item, domain);
    assert.equal(contract.expectedCompanionFile, contract.expectedOutputFile.replace(/\.md$/, ".json"));
    const md = path.join(root, contract.expectedOutputFile);
    const json = path.join(root, contract.expectedCompanionFile);
    fs.mkdirSync(path.dirname(md), { recursive: true });
    const snapshot = captureOutputSnapshot(contract, item);
    fs.writeFileSync(md, "report");
    assert.throws(() => validateLocalOutput(item, domain, contract, snapshot), /does not exist/);
    fs.writeFileSync(json, "");
    assert.throws(() => validateLocalOutput(item, domain, contract, snapshot), /empty/);
    fs.writeFileSync(json, "not parsed by the runner");
    fs.utimesSync(json, new Date(0), new Date(0));
    assert.throws(() => validateLocalOutput(item, domain, contract, snapshot), /not modified/);
    fs.utimesSync(json, new Date(), new Date());
    assert.equal(validateLocalOutput(item, domain, contract, snapshot), contract.expectedOutputFile);
    fs.renameSync(md, md.replace(/\.md$/, "_alternate.md"));
    assert.throws(() => validateLocalOutput(item, domain, contract, snapshot), /does not exist/);
    assert.equal(fs.existsSync(md), false);
    assert.throws(() => validateOutputFilePath({ domain, item, outputFile: contract.expectedCompanionFile }), /naming rule/);
    assert.throws(() => validateOutputFilePath({ domain, item, outputFile: contract.expectedCompanionFile.replace("TEST_", "OTHER_"), companion: true }), /must start with TEST_/);
    assert.throws(() => validateOutputFilePath({ domain, item, outputFile: "../result.json", companion: true }), /must start|invalid path/);
    const prompt = buildOutputInstruction(contract);
    assert.equal(prompt.split(contract.expectedOutputFile).length - 1, 1);
    assert.equal(prompt.split(contract.expectedCompanionFile).length - 1, 1);
    assert.ok(prompt.length < 350);
    fs.rmSync(path.dirname(md), { recursive: true, force: true });
  });

  test(`${domain.domain}: backs up and restores a pair; first JSON run restores MD-only state`, () => {
    const item = { domain: domain.domain, subject: "TEST", startedAt: "2026-10-11T09:00:00-07:00" };
    const contract = createOutputContract(item, domain);
    const md = path.join(root, contract.expectedOutputFile);
    const json = path.join(root, contract.expectedCompanionFile);
    fs.mkdirSync(path.dirname(md), { recursive: true });
    const other = path.join(path.dirname(md), "OTHER_keep.json");
    fs.writeFileSync(other, "unrelated");
    for (const hasJson of [false, true]) {
      fs.writeFileSync(md, "old MD");
      if (hasJson) fs.writeFileSync(json, "old JSON");
      const prepared = domain.prepareFormalRun(item, contract);
      assert.equal(prepared.files.length, hasJson ? 2 : 1);
      assert.equal(fs.existsSync(md), false);
      assert.equal(fs.existsSync(json), false);
      fs.writeFileSync(md, "new MD");
      fs.writeFileSync(json, "new JSON");
      domain.rollbackFormalRun(item, prepared, contract);
      assert.equal(fs.readFileSync(md, "utf8"), "old MD");
      assert.equal(fs.existsSync(json), hasJson);
      if (hasJson) assert.equal(fs.readFileSync(json, "utf8"), "old JSON");
      assert.equal(fs.readFileSync(other, "utf8"), "unrelated");
    }
    fs.rmSync(path.dirname(md), { recursive: true, force: true });
  });
}

test("a partial backup move restores files already moved", (t) => {
  const outputDir = path.join(root, "backup-failure", "results");
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, "a.md"), "MD");
  fs.writeFileSync(path.join(outputDir, "a.json"), "JSON");
  const rename = fs.renameSync;
  let moves = 0;
  const mocked = t.mock.method(fs, "renameSync", (from, to) => {
    if (path.dirname(from) === outputDir && ++moves === 2) throw new Error("injected move failure");
    return rename(from, to);
  });
  try {
    assert.throws(() => backupExistingOutputs({ rootDir: root, outputDir, backupKey: "a", matchFileName: () => true }), /injected move failure/);
    assert.equal(fs.readFileSync(path.join(outputDir, "a.md"), "utf8"), "MD");
    assert.equal(fs.readFileSync(path.join(outputDir, "a.json"), "utf8"), "JSON");
  } finally {
    mocked.mock.restore();
  }
});

function item(id, subject = "AAA", overrides = {}) {
  return { id, domain: "company-comparison", subject, status: "pending", attempts: 0, ...overrides };
}

test("same output owner is serialized; completion archives the companion", () => {
  queue.ensureQueueFiles();
  queue.writeActiveQueue([item("first"), item("duplicate", "aaa/alias"), item("other", "BBB")]);
  queue.writeDoneQueue([]);
  assert.equal(queue.claimNextQueueItem({ maxAttempts: 3 }).id, "first");
  assert.equal(queue.claimNextQueueItem({ maxAttempts: 3 }).id, "other");
  assert.equal(queue.claimNextQueueItem({ maxAttempts: 3 }), null);
  queue.markQueueItemDone("first", { outputFile: "report.md", companionFile: "report.json" });
  queue.archiveDoneItems();
  assert.equal(queue.readDoneQueue()[0].companionFile, "report.json");
  assert.equal(queue.claimNextQueueItem({ maxAttempts: 3 }).id, "duplicate");
});

test("claim, failure, interruption recovery and quota deferral clear companion records", () => {
  const stale = { companionFile: "stale.json", outputFile: "stale.md" };
  queue.writeActiveQueue([item("claim", "AAA", stale)]);
  assert.equal(queue.claimNextQueueItem({ maxAttempts: 3 }).companionFile, undefined);
  queue.writeActiveQueue([item("failure", "AAA", { ...stale, status: "running", attempts: 1 })]);
  queue.markQueueItemFailure("failure", "test", 3);
  assert.equal(queue.readActiveQueue()[0].companionFile, undefined);
  queue.writeActiveQueue([item("recover", "AAA", { ...stale, status: "running", attempts: 1 })]);
  queue.recoverRunningQueueItems({ maxAttempts: 3 });
  assert.equal(queue.readActiveQueue()[0].companionFile, undefined);
  queue.writeActiveQueue([item("quota", "AAA", { ...stale, status: "running", attempts: 1 })]);
  queue.deferQueueItemForQuota("quota", Date.now() + 60_000);
  assert.equal(queue.readActiveQueue()[0].companionFile, undefined);
});
