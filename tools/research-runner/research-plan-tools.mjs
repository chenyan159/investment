#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { PLAN_PROJECT_ROOT, RESEARCH_PLANS, resolveCurrentPlan } from "./research-plan-store.mjs";

const [command, ...args] = process.argv.slice(2);
if (command !== "publish") throw new Error("Usage: publish (--plan-id=ID | --plan-dir=DIR) --source=FILE --reason=TEXT [--timestamp=yyyymmdd_hhmmss]");
const options = Object.fromEntries(args.map(arg => {
  const i = arg.indexOf("=");
  if (!arg.startsWith("--") || i < 0) throw new Error(`Invalid argument: ${arg}`);
  return [arg.slice(2, i), arg.slice(i + 1)];
}));
const plan = options["plan-dir"]
  ? planForDirectory(options["plan-dir"])
  : RESEARCH_PLANS.find(p => p.id === options["plan-id"]);
if (!plan || !options.source || !options.reason?.trim()) throw new Error("plan-id or plan-dir, source and reason are required");
const stamp = options.timestamp || new Intl.DateTimeFormat("sv-SE", {
  timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false,
}).format(new Date()).replaceAll("-", "").replace(" ", "_").replaceAll(":", "");
if (!/^\d{8}_\d{6}$/u.test(stamp)) throw new Error("Invalid timestamp");
const old = currentPlanOrNull(plan);
const content = fs.readFileSync(path.resolve(PLAN_PROJECT_ROOT, options.source));
if (!content.toString("utf8").trim()) throw new Error("Empty research plan");
const dir = path.resolve(PLAN_PROJECT_ROOT, plan.directory);
const archive = path.join(dir, stamp);
const name = `研究方案_${stamp}.md`;
if (fs.existsSync(archive) || fs.existsSync(path.join(dir, name))) throw new Error(`Version already exists: ${stamp}`);
fs.mkdirSync(archive, { recursive: true });
fs.writeFileSync(path.join(archive, name), content, { flag: "wx" });
fs.writeFileSync(path.join(archive, "修改记录以及效果.md"), `# 修改记录以及效果\n\n- 版本：${stamp}\n- 上一版：${old ? path.basename(old) : "（首个版本）"}\n- 修改原因：${options.reason}\n- 修改内容：待补充。\n- 预期效果：待补充。\n- 运行记录：尚未运行。\n- 实际效果：待运行后追加。\n`);
fs.copyFileSync(path.join(archive, name), path.join(dir, name), fs.constants.COPYFILE_EXCL);
if (old) fs.unlinkSync(old);
console.log(JSON.stringify({ planId: plan.id, version: stamp, planFile: path.join(dir, name), archive }));

// --plan-dir 可直接指定方案目录（例如产业背景的新专题）；已登记目录仍按登记信息处理。
function planForDirectory(directory) {
  const absolute = path.resolve(PLAN_PROJECT_ROOT, directory);
  const relative = path.relative(PLAN_PROJECT_ROOT, absolute);
  if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) throw new Error(`plan-dir must be inside the project: ${directory}`);
  const registered = RESEARCH_PLANS.find(p => path.resolve(PLAN_PROJECT_ROOT, p.directory) === absolute);
  return registered || { id: relative.replaceAll("\\", "/"), directory: relative.replaceAll("\\", "/"), unregistered: true };
}

// 未登记的新目录允许没有现行方案（发布首个版本）；已登记方案仍要求恰好一份。
function currentPlanOrNull(plan) {
  const dir = path.resolve(PLAN_PROJECT_ROOT, plan.directory);
  if (plan.unregistered && (!fs.existsSync(dir) || !fs.readdirSync(dir).some(name => /^研究方案_\d{8}_\d{6}\.md$/u.test(name)))) return null;
  return resolveCurrentPlan(plan.directory);
}
