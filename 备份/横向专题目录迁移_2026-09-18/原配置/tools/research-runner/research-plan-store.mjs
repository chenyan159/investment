import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

const toolDir = path.dirname(fileURLToPath(import.meta.url));
export const PLAN_PROJECT_ROOT = path.resolve(process.env.RESEARCH_RUNNER_PROJECT_ROOT || path.join(toolDir, "../.."));
export const RESEARCH_PLANS = JSON.parse(fs.readFileSync(path.join(toolDir, "research-plans.json"), "utf8"));
const pattern = /^研究方案_(\d{8}_\d{6})\.md$/u;
const relative = (file, root) => path.relative(root, file).replaceAll("\\", "/");
export const planHash = (content) => createHash("sha256").update(content).digest("hex");

export function resolveCurrentPlan(directory, root = PLAN_PROJECT_ROOT) {
  const dir = path.resolve(root, directory);
  const files = fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.isFile() && pattern.test(e.name));
  if (files.length !== 1) throw new Error(`Expected exactly one current research plan in ${dir}; found ${files.length}`);
  return path.join(dir, files[0].name);
}

export function planForItem(item, root = PLAN_PROJECT_ROOT) {
  if (item.domain !== "file-run") return RESEARCH_PLANS.find(p => p.id === item.domain);
  if (!item.promptFile) return undefined;
  const file = path.resolve(root, item.promptFile);
  return RESEARCH_PLANS.find(p => file === path.resolve(root, p.legacy)
    || file === path.resolve(root, p.directory)
    || (file.startsWith(path.resolve(root, p.directory) + path.sep) && pattern.test(path.basename(file))));
}

export function bindResearchPlan(item, root = PLAN_PROJECT_ROOT) {
  if (item.planSnapshotFile) {
    const body = fs.readFileSync(path.resolve(root, item.planSnapshotFile));
    if (planHash(body) !== item.planSha256) throw new Error(`Research plan hash mismatch: ${item.planSnapshotFile}`);
    return item;
  }
  const plan = planForItem(item, root);
  if (!plan) return item;
  const requested = item.domain === "file-run" && pattern.test(path.basename(item.promptFile || ""))
    ? path.resolve(root, item.promptFile) : resolveCurrentPlan(plan.directory, root);
  const version = pattern.exec(path.basename(requested))[1];
  const snapshot = path.resolve(root, plan.directory, version, path.basename(requested));
  const body = fs.readFileSync(requested);
  const hash = planHash(body);
  if (planHash(fs.readFileSync(snapshot)) !== hash) throw new Error(`Research plan snapshot differs: ${snapshot}`);
  Object.assign(item, {
    planId: plan.id, planVersion: version, planEntryFile: relative(requested, root),
    planSnapshotFile: relative(snapshot, root), planSha256: hash, planBoundAt: new Date().toISOString(),
  });
  if (item.domain === "file-run") item.promptFile = item.planSnapshotFile;
  return item;
}

export function readResearchPlan(item) {
  bindResearchPlan(item);
  const file = item.planSnapshotFile || item.promptFile;
  return fs.readFileSync(path.resolve(PLAN_PROJECT_ROOT, file), "utf8").replace(/^\uFEFF/u, "");
}

export function researchPlanMetadata(item) {
  return Object.fromEntries(["planId", "planVersion", "planEntryFile", "planSnapshotFile", "planSha256", "planBoundAt"]
    .filter(key => item[key]).map(key => [key, item[key]]));
}
