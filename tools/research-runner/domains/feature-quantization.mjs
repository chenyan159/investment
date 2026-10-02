import fs from "node:fs";
import path from "node:path";
import {
  buildFeatureQuantizationFormalPrompt,
} from "../prompts/feature-quantization.mjs";
import {
  formatLocalDate,
  formatLocalIso,
  FUNDAMENTAL_ROOT,
  normalizeProjectPath,
  PROJECT_ROOT,
  readUtf8,
  safeIdPart,
} from "../queue-store.mjs";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "./output-backup.mjs";
import {
  featureIdentityFromStem,
} from "./feature-contract.mjs";

export const FEATURE_QUANTIZATION_PLANS_DIR = path.join(FUNDAMENTAL_ROOT, "特征量化", "研究方案");
export const FEATURE_QUANTIZATION_OUTPUT_DIR = path.join(FUNDAMENTAL_ROOT, "特征量化", "量化评分");
export const FEATURE_PLAN_ALLOWED_SOURCE_PATHS = Object.freeze([
  "基本面/公司调研/",
  "基本面/行业调研/",
  "金融资料/每日金融数据/",
]);

export const featureQuantizationDomain = {
  domain: "feature-quantization",
  label: "特征量化",
  subjectHelp: "feature plan stem",
  requiresIndexedSubject: true,
  promptPath: FEATURE_QUANTIZATION_PLANS_DIR,
  indexPath: FEATURE_QUANTIZATION_PLANS_DIR,
  placeholder: "",
  outputPrefix: "基本面/特征量化/量化评分/",
  outputFilePattern: /^[NG]\d{2}_.+_量化评分_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  requiredPaths: [
    FEATURE_QUANTIZATION_PLANS_DIR,
  ],
  checkRequired() {
    const entries = parseFeatureQuantizationPlanEntries();
    if (!entries.length) {
      throw new Error(`No feature-quantization plan Markdown files found in: ${FEATURE_QUANTIZATION_PLANS_DIR}`);
    }
  },
  expectedOutputFile(item, runDate) {
    return `基本面/特征量化/量化评分/${expectedFeatureQuantizationOutputStem(item.subject)}_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildFeatureQuantizationFormalPrompt(item, featureQuantizationDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingFeatureQuantizationOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackFeatureQuantizationFormalRun(item, prepareResult, outputContract);
  },
  validateOutputFileForItem({ item, outputFile }) {
    validateFeatureQuantizationOutputFileForItem({ item, outputFile });
  },
  validateQueueItem(item) {
    const entry = resolveFeatureQuantizationPlanEntry(item?.subject);
    if (!entry || entry.subject !== item.subject) {
      throw new Error(`feature-quantization item does not match the current plan ID/name: ${item?.subject || ""}`);
    }
  },
  parseIndexEntries() {
    return parseFeatureQuantizationPlanEntries();
  },
  resolveIndexEntry(subject) {
    return resolveFeatureQuantizationPlanEntry(subject);
  },
  createQueueItem(options) {
    return createFeatureQuantizationQueueItem(options);
  },
};

export function parseFeatureQuantizationPlanEntries(plansDir = FEATURE_QUANTIZATION_PLANS_DIR) {
  if (!fs.existsSync(plansDir)) return [];
  const entries = fs.readdirSync(plansDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && /^[NG]\d{2}_.+_研究方案\.md$/u.test(entry.name))
    .sort((a, b) => a.name.localeCompare(b.name, "zh-Hans-CN"))
    .map((entry) => {
      const planPath = path.join(plansDir, entry.name);
      const planContent = readUtf8(planPath);
      validateFeaturePlanSourceBoundary(planContent, entry.name);
      const stem = entry.name.replace(/\.md$/u, "");
      return {
        subject: stem,
        displayName: extractPlanTitle(planContent) || stem,
        category: "研究方案",
        planFile: normalizeProjectPath(path.relative(PROJECT_ROOT, planPath)),
        planPath,
      };
    });
  const byId = new Map();
  for (const entry of entries) {
    const identity = featureIdentityFromStem(entry.subject);
    const previous = byId.get(identity?.featureId);
    if (previous) {
      throw new Error(`Duplicate feature plan ID ${identity.featureId}: ${previous.subject}, ${entry.subject}`);
    }
    byId.set(identity?.featureId, entry);
  }
  return entries;
}

export function validateFeaturePlanSourceBoundary(content, source = "feature plan") {
  const text = String(content || "");
  if (!/^##\s+资料读取边界\s*$/mu.test(text)) {
    throw new Error(`${source} is missing the 资料读取边界 section`);
  }
  for (const allowedPath of FEATURE_PLAN_ALLOWED_SOURCE_PATHS) {
    if (!text.includes(`\`${allowedPath}\``)) {
      throw new Error(`${source} is missing allowed source path: ${allowedPath}`);
    }
  }
  if (!/上述目录之外的 Investment 目录与文件一律禁止读取/u.test(text)) {
    throw new Error(`${source} must explicitly forbid all non-allowlisted Investment paths`);
  }
  if (!/禁止联网(?:搜索)?/u.test(text)) {
    throw new Error(`${source} must explicitly forbid network research`);
  }
  if (!/禁止[^。\n]*外部资料/u.test(text)) {
    throw new Error(`${source} must explicitly forbid external sources`);
  }
  return true;
}

export function resolveFeatureQuantizationPlanEntry(subject) {
  const wanted = normalizePlanSubject(subject);
  const entries = parseFeatureQuantizationPlanEntries();
  const exact = entries.find((entry) => normalizePlanSubject(entry.subject) === wanted || normalizePlanSubject(entry.displayName) === wanted);
  if (exact) return exact;
  const wantedId = featureIdentityFromStem(wanted)?.featureId || wanted.match(/^[NG]\d{2}/u)?.[0] || "";
  return wantedId ? entries.find((entry) => featureIdentityFromStem(entry.subject)?.featureId === wantedId) || null : null;
}

export function createFeatureQuantizationQueueItem({
  subject,
  displayName = "",
  category = "",
  sourceDate = formatLocalDate(new Date()),
  status = "pending",
  id = "",
  outputFile = "",
  startedAt = "",
  finishedAt = "",
  attempts = 0,
  note = "",
  extra = {},
} = {}) {
  if (!subject) throw new Error("feature-quantization queue item requires --subject");
  const entry = resolveFeatureQuantizationPlanEntry(subject);
  const normalizedSubject = entry?.subject || subject;
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `feature-quantization-${safeIdPart(normalizedSubject)}-${safeIdPart(nowIso)}`,
    domain: "feature-quantization",
    sourceDate,
    subject: normalizedSubject,
    displayName: displayName || entry?.displayName || normalizedSubject,
    category: category || entry?.category || "研究方案",
    status,
    attempts,
    outputFile: normalizeProjectPath(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    planFile: entry?.planFile || "",
    ...extra,
  };
}

export function expectedFeatureQuantizationOutputStem(subject) {
  const entry = resolveFeatureQuantizationPlanEntry(subject);
  const subjectStem = (entry?.subject || String(subject || ""))
    .trim()
    .replace(/\.md$/iu, "")
    .replace(/_研究方案$/u, "");
  if (!/^[NG]\d{2}_.+/u.test(subjectStem)) {
    throw new Error(`Cannot infer feature output stem from subject: ${subject}`);
  }
  return `${subjectStem}_量化评分`;
}

export function validateFeatureQuantizationOutputFileForItem({ item, outputFile }) {
  if (!item?.subject) return;
  const expectedStem = expectedFeatureQuantizationOutputStem(item.subject);
  const fileName = normalizeProjectPath(outputFile).split("/").pop() || "";
  const pattern = new RegExp(`^${escapeRegExp(expectedStem)}_\\d{4}-\\d{2}-\\d{2}\\.md$`, "u");
  if (!pattern.test(fileName)) {
    throw new Error(`outputFile must match current feature ${expectedStem}_YYYY-MM-DD.md: ${fileName}`);
  }
}

export function backupExistingFeatureQuantizationOutputs(item, outputContract = {}, paths = {}) {
  const expectedStem = expectedFeatureQuantizationOutputStem(item.subject);
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return backupExistingOutputs({
    rootDir: paths.rootDir || PROJECT_ROOT,
    outputDir: paths.outputDir || FEATURE_QUANTIZATION_OUTPUT_DIR,
    backupKey: expectedStem,
    expectedFileName,
    matchFileName: () => false,
  });
}

export function rollbackFeatureQuantizationFormalRun(item, prepareResult = {}, outputContract = {}, paths = {}) {
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return rollbackPreparedOutputs({
    rootDir: paths.rootDir || PROJECT_ROOT,
    outputDir: paths.outputDir || FEATURE_QUANTIZATION_OUTPUT_DIR,
    expectedFileName,
    prepareResult,
    newFileNameMatcher: () => false,
  });
}

function normalizePlanSubject(value) {
  return String(value || "")
    .trim()
    .replace(/\.md$/iu, "")
    .replace(/\s+/g, "");
}

function extractPlanTitle(content) {
  const firstTitle = String(content || "")
    .split(/\r?\n/)
    .find((line) => line.trim().startsWith("# "));
  return firstTitle ? firstTitle.replace(/^#\s*/u, "").trim() : "";
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
