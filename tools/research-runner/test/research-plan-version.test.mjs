import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { RESEARCH_PLANS, PLAN_PROJECT_ROOT, bindResearchPlan, resolveCurrentPlan, planHash } from "../research-plan-store.mjs";

const toolDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const version = "20260909_100000";
function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "research-plan-"));
  const plan = RESEARCH_PLANS.find(p => p.id === "conference");
  const dir = path.join(root, plan.directory);
  fs.mkdirSync(path.join(dir, version), { recursive: true });
  const name = `研究方案_${version}.md`;
  fs.writeFileSync(path.join(dir, name), "# first version\n");
  fs.copyFileSync(path.join(dir, name), path.join(dir, version, name));
  return { root, plan, dir, name };
}

test("all eleven live entries have matching archive bytes and their two documents", () => {
  assert.equal(RESEARCH_PLANS.length, 11);
  for (const plan of RESEARCH_PLANS) {
    const item = bindResearchPlan({ domain: "file-run", promptFile: plan.directory });
    assert.equal(item.planId, plan.id);
    assert.equal(planHash(fs.readFileSync(resolveCurrentPlan(plan.directory))), item.planSha256);
    assert.ok(fs.existsSync(path.join(PLAN_PROJECT_ROOT, plan.directory, "README.md")));
    assert.ok(fs.existsSync(path.join(PLAN_PROJECT_ROOT, plan.directory, item.planVersion, "修改记录以及效果.md")));
  }
});

test("publisher changes current entry while an already bound task keeps its version", () => {
  const { root, plan, dir, name } = fixture();
  try {
    const old = bindResearchPlan({ domain: "file-run", promptFile: plan.directory }, root);
    fs.writeFileSync(path.join(root, "candidate.md"), "# second version\n");
    const args = [path.join(toolDir, "research-plan-tools.mjs"), "publish", "--plan-id=conference", "--source=candidate.md", "--reason=clearer scope", "--timestamp=20260909_110000"];
    const result = spawnSync(process.execPath, args, { env: { ...process.env, RESEARCH_RUNNER_PROJECT_ROOT: root }, encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    assert.ok(!fs.existsSync(path.join(dir, name)));
    assert.equal(bindResearchPlan(old, root).planVersion, version);
    assert.equal(bindResearchPlan({ domain: "file-run", promptFile: plan.directory }, root).planVersion, "20260909_110000");
    assert.match(fs.readFileSync(path.join(dir, "20260909_110000", "修改记录以及效果.md"), "utf8"), /clearer scope/);
    const duplicate = spawnSync(process.execPath, args, { env: { ...process.env, RESEARCH_RUNNER_PROJECT_ROOT: root }, encoding: "utf8" });
    assert.notEqual(duplicate.status, 0);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test("ambiguous entries and changed snapshot bytes are rejected", () => {
  const { root, plan, dir } = fixture();
  try {
    const item = bindResearchPlan({ domain: "file-run", promptFile: plan.directory }, root);
    fs.writeFileSync(path.join(root, item.planSnapshotFile), "changed");
    assert.throws(() => bindResearchPlan(item, root), /hash mismatch/);
    fs.writeFileSync(path.join(dir, "研究方案_20260909_110000.md"), "other");
    assert.throws(() => resolveCurrentPlan(plan.directory, root), /exactly one/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test("ordinary file-run tasks receive no managed-plan fields", () => {
  const item = { domain: "file-run", promptFile: "ordinary.md" };
  assert.deepEqual(bindResearchPlan(item), { domain: "file-run", promptFile: "ordinary.md" });
});

test("real CLI enqueue and queue completion preserve the bound version and actual prompt metadata", () => {
  const { root, plan } = fixture();
  try {
    const env = { ...process.env, RESEARCH_RUNNER_PROJECT_ROOT: root, RESEARCH_RUNNER_QUEUE_DIR: path.join(root, "queue") };
    const result = spawnSync(process.execPath, [path.join(toolDir, "queue-tools.mjs"), "add-file-run", "--run-id=version-test", `--prompt-file=${plan.directory}`, "--expected-output-file=基本面/行业调研/产业背景/顶级会议信息/report.md"], { env, encoding: "utf8" });
    assert.equal(result.status, 0, result.stderr);
    const queued = JSON.parse(fs.readFileSync(path.join(root, "queue/queue.jsonl"), "utf8"));
    assert.equal(queued.planVersion, version);
    const script = `import {bindActiveResearchPlans, recordResearchPlanRun, markQueueItemDone, archiveDoneItems} from './queue-store.mjs';
      bindActiveResearchPlans(); recordResearchPlanRun(${JSON.stringify(queued.id)}, {actualPromptFile:'prompt.md',actualPromptSha256:'test-hash'});
      markQueueItemDone(${JSON.stringify(queued.id)}, {outputFile:'基本面/行业调研/产业背景/顶级会议信息/report.md'}); archiveDoneItems();`;
    const completion = spawnSync(process.execPath, ["--input-type=module", "-e", script], { env, cwd: toolDir, encoding: "utf8" });
    assert.equal(completion.status, 0, completion.stderr);
    const done = JSON.parse(fs.readFileSync(path.join(root, "queue/queue.done.jsonl"), "utf8"));
    assert.equal(done.planSha256, queued.planSha256);
    assert.equal(done.planVersion, version);
    assert.equal(done.actualPromptFile, "prompt.md");
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
