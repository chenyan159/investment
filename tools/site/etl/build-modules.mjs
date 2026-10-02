import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import { buildData, validateModuleArtifact } from "./build-data.mjs";

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, "..");
const PROJECT_ROOT = path.resolve(SITE_ROOT, "..", "..");
const ANALYSIS_ROOT = path.join(PROJECT_ROOT, "分析报告");

export const MODULES = [
  {
    id: "companyComparisons",
    label: "公司对比",
    script: path.join(ANALYSIS_ROOT, "公司对比", "生成站点数据.mjs"),
    outputRoot: path.join(ANALYSIS_ROOT, "公司对比", "站点数据"),
  },
  {
    id: "scenarioDecisions",
    label: "情景决策",
    script: path.join(ANALYSIS_ROOT, "公司情景投资决策", "生成站点数据.mjs"),
    outputRoot: path.join(ANALYSIS_ROOT, "公司情景投资决策", "站点数据"),
  },
  {
    id: "rankings",
    label: "公司排序",
    script: path.join(ANALYSIS_ROOT, "公司排序", "生成站点数据.mjs"),
    outputRoot: path.join(ANALYSIS_ROOT, "公司排序", "站点数据"),
  },
  {
    id: "technicalResearch",
    label: "技术面",
    script: path.join(PROJECT_ROOT, "技术面", "生成站点数据.mjs"),
    outputRoot: path.join(PROJECT_ROOT, "技术面", "站点数据"),
  },
  {
    id: "dailyNews",
    label: "每日新闻",
    script: path.join(__dirname, "build-daily-news.mjs"),
    outputRoot: path.join(SITE_ROOT, "public", "data", "daily-news"),
  },
];

export async function buildSiteData({ modules = MODULES } = {}) {
  const moduleBuilds = await buildModules({ modules });
  await buildData({ moduleBuilds });
  printSummary(moduleBuilds);
  return moduleBuilds;
}

export async function buildModules({ modules = MODULES, run = runIsolatedModule } = {}) {
  const moduleBuilds = {};
  for (const module of modules) {
    moduleBuilds[module.id] = await run(module);
  }
  return moduleBuilds;
}

export async function buildOneModule(id) {
  const module = MODULES.find((candidate) => candidate.id === id);
  if (!module) throw new Error(`未知站点数据模块：${id}`);
  const result = await runIsolatedModule(module);
  printSummary({ [id]: result });
  return result;
}

export async function runIsolatedModule(
  module,
  {
    execute = executeModule,
    validate = validateModuleArtifact,
    now = () => new Date().toISOString(),
  } = {},
) {
  const attemptedAt = now();
  const stagingRoot = siblingWorkRoot(module, "staging");
  await fs.rm(stagingRoot, { recursive: true, force: true });

  try {
    const output = await execute(module, stagingRoot);
    if (output?.stdout?.trim()) console.log(`[${module.label}]\n${output.stdout.trim()}`);
    if (output?.stderr?.trim()) console.warn(`[${module.label}]\n${output.stderr.trim()}`);
    const artifact = await validate(module.id, stagingRoot);
    await promoteDirectory(stagingRoot, module.outputRoot, module);
    console.log(`[${module.label}] fresh${artifact.dataDate ? ` · ${artifact.dataDate}` : ""}`);
    return {
      label: module.label,
      status: "fresh",
      attemptedAt,
      generatedAt: artifact.generatedAt || "",
      dataDate: artifact.dataDate || "",
    };
  } catch (error) {
    await fs.rm(stagingRoot, { recursive: true, force: true });
    let fallback;
    try {
      fallback = await validate(module.id, module.outputRoot, { allowHistoricalCohort: true });
    } catch (fallbackError) {
      throw new Error(
        `${module.label}生成失败，且没有可用的上一版站点数据：${publicError(error)}；上一版校验：${publicError(fallbackError)}`,
        { cause: error },
      );
    }
    const message = publicError(error);
    console.warn(`[${module.label}] stale · 沿用 ${fallback.dataDate || fallback.generatedAt || "上一版"} · ${message}`);
    return {
      label: module.label,
      status: "stale",
      attemptedAt,
      generatedAt: fallback.generatedAt || "",
      dataDate: fallback.dataDate || "",
      error: message,
    };
  }
}

async function executeModule(module, stagingRoot) {
  return execFileAsync(process.execPath, [module.script], {
    cwd: path.dirname(module.script),
    env: {
      ...process.env,
      PROJECT_ANANTA_OUTPUT_ROOT: stagingRoot,
    },
    maxBuffer: 16 * 1024 * 1024,
    windowsHide: true,
  });
}

async function promoteDirectory(stagingRoot, outputRoot, module) {
  const backupRoot = siblingWorkRoot(module, "backup");
  await fs.rm(backupRoot, { recursive: true, force: true });
  const hadCurrent = await pathExists(outputRoot);

  if (hadCurrent) await fs.rename(outputRoot, backupRoot);
  try {
    await fs.rename(stagingRoot, outputRoot);
  } catch (error) {
    if (hadCurrent && (await pathExists(backupRoot))) await fs.rename(backupRoot, outputRoot);
    throw error;
  }

  if (hadCurrent) {
    await fs.rm(backupRoot, { recursive: true, force: true }).catch((error) => {
      console.warn(`[${module.label}] 无法清理已替换的临时备份：${publicError(error)}`);
    });
  }
}

function siblingWorkRoot(module, kind) {
  const parent = path.dirname(module.outputRoot);
  const base = path.basename(module.outputRoot);
  const nonce = crypto.randomBytes(6).toString("hex");
  return path.join(parent, `.${base}-${module.id}-${kind}-${process.pid}-${nonce}`);
}

async function pathExists(target) {
  return fs.stat(target).then(() => true).catch(() => false);
}

function publicError(error) {
  return String(error?.stderr || error?.message || error || "未知错误")
    .replace(/[A-Z]:[\\/][^\r\n]*/giu, "[本地路径已省略]")
    .replace(/\s+/gu, " ")
    .trim()
    .slice(0, 240);
}

function printSummary(moduleBuilds) {
  const summary = Object.entries(moduleBuilds)
    .map(([id, result]) => `${id}=${result.status}${result.dataDate ? `(${result.dataDate})` : ""}`)
    .join(", ");
  console.log(`Module builds: ${summary}`);
}

if (path.resolve(process.argv[1] || "") === __filename) {
  const selectedModule = process.argv.find((value) => value.startsWith("--module="))?.slice("--module=".length);
  const task = selectedModule ? buildOneModule(selectedModule) : buildSiteData();
  task.catch((error) => {
    console.error(error.stack || error.message || error);
    process.exitCode = 1;
  });
}
