import { resolveCurrentPlan } from "../research-plan-store.mjs";
import path from "node:path";
import { buildIndustryFormalPrompt } from "../prompts/industry.mjs";
import {
  categoryFromOutputFile,
  FUNDAMENTAL_ROOT,
  formatLocalDate,
  formatLocalIso,
  normalizeProjectPath,
  parseMarkdownTableRows,
  PROJECT_ROOT,
  readUtf8,
  safeIdPart,
} from "../queue-store.mjs";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "./output-backup.mjs";
import { safeOutputNamePart } from "./output-path.mjs";

export const INDUSTRY_CATEGORIES = [
  "AI园区电力_机电_冷却",
  "AI服务器_存储_芯片",
  "AI网络_光互联_铜互联",
  "晶圆制造_设备_材料_测试",
  "机器人_硬件_零部件",
  "商业航天_火箭_卫星",
  "AI应用_软件_数据平台",
];

export const industryDomain = {
  domain: "industry",
  label: "行业调研",
  subjectHelp: "industry topic",
  requiresIndexedSubject: true,
  get promptPath() { return resolveCurrentPlan(path.join(FUNDAMENTAL_ROOT, "行业调研", "研究方法", "行业调研", "研究方案")); },
  indexPath: path.join(FUNDAMENTAL_ROOT, "行业调研", "行业索引.md"),
  placeholder: "【行业名称】",
  outputPrefix: "基本面/行业调研/",
  outputFilePattern: /^行业调研_.+_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(INDUSTRY_CATEGORIES),
  requiredPaths: [
    path.join(FUNDAMENTAL_ROOT, "行业调研", "研究方法", "行业调研", "研究方案"),
    path.join(FUNDAMENTAL_ROOT, "行业调研", "行业索引.md"),
  ],
  expectedOutputFile(item, runDate) {
    const entry = industryDomain.resolveIndexEntry(item?.subject || "");
    const category = cleanCategory(item?.category || entry?.category || "");
    if (!category) throw new Error(`industry output category is missing: ${item?.subject || ""}`);
    const subject = safeOutputNamePart(item?.subject, "行业");
    return `基本面/行业调研/${category}/行业调研_${subject}_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildIndustryFormalPrompt(item, industryDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingIndustryOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackIndustryFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseIndustryIndexEntries(industryDomain.indexPath);
  },
  resolveIndexEntry(subject) {
    return resolveIndustryIndexEntry(industryDomain.indexPath, subject);
  },
  createQueueItem(options) {
    return createIndustryQueueItem(options);
  },
  validateOutputFileForItem({ item, fileName }) {
    const actualKey = canonicalIndustryKey(industryNameFromOutputFileName(fileName));
    const expectedKey = canonicalIndustryKey(item?.subject);
    if (!expectedKey || actualKey !== expectedKey) {
      throw new Error(`industry outputFile filename does not match ${item?.subject || "current subject"}: ${fileName}`);
    }
  },
};

export function parseIndustryIndexEntries(indexPath = industryDomain.indexPath) {
  return parseMarkdownTableRows(readUtf8(indexPath), "行业名称")
    .filter((cells) => cells.length >= 2)
    .map((cells) => ({
      subject: cells[0].trim(),
      displayName: cells[0].trim(),
      category: cleanCategory(cells[1]),
      researchScope: (cells[2] || "").trim(),
    }))
    .filter((entry) => entry.subject && entry.category);
}

export function resolveIndustryIndexEntry(indexPath, subject) {
  const wanted = normalizeSubject(subject);
  return parseIndustryIndexEntries(indexPath).find((entry) => normalizeSubject(entry.subject) === wanted) || null;
}

export function createIndustryQueueItem({
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
  if (!subject) throw new Error("industry queue item requires --subject");
  const entry = industryDomain.resolveIndexEntry(subject);
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `industry-${safeIdPart(subject)}-${safeIdPart(nowIso)}`,
    domain: "industry",
    sourceDate,
    subject,
    displayName: displayName || entry?.displayName || subject,
    category: category || entry?.category || categoryFromOutputFile(outputFile),
    status,
    attempts,
    outputFile: normalizeProjectPath(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    ...extra,
  };
}

export function backupExistingIndustryOutputs(item, outputContract = {}) {
  const outputDir = industryOutputDir(item);
  const expectedKey = canonicalIndustryKey(item?.subject);
  if (!outputDir || !expectedKey) return { backupDir: "", files: [] };

  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    backupKey: item.subject,
    expectedFileName: outputContract.expectedOutputFile?.split("/").pop() || "",
    matchFileName: (fileName) => industryDomain.outputFilePattern.test(fileName)
      && canonicalIndustryKey(industryNameFromOutputFileName(fileName)) === expectedKey,
  });
}

export function rollbackIndustryFormalRun(item, prepareResult = {}, outputContract = {}) {
  const outputDir = industryOutputDir(item);
  const expectedPrefix = industryOutputPrefix(item);
  if (!outputDir || !expectedPrefix) return { removed: [], files: [] };

  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    expectedFileName: outputContract.expectedOutputFile?.split("/").pop() || "",
    prepareResult,
    newFileNameMatcher: (fileName) => fileName.startsWith(expectedPrefix)
      && industryDomain.outputFilePattern.test(fileName),
  });
}

function industryOutputDir(item) {
  const entry = industryDomain.resolveIndexEntry(item?.subject || "");
  const category = cleanCategory(item?.category || entry?.category || "");
  if (!category) return "";
  return path.join(FUNDAMENTAL_ROOT, "行业调研", category);
}

function industryOutputPrefix(item) {
  const subject = String(item?.subject || "").trim();
  return subject ? `行业调研_${subject}_` : "";
}

function industryNameFromOutputFileName(fileName) {
  return String(fileName || "")
    .replace(/\.md$/u, "")
    .replace(/^行业调研_/u, "")
    .replace(/_\d{4}-\d{2}-\d{2}$/u, "");
}

function canonicalIndustryKey(value) {
  return String(value || "")
    .trim()
    .replace(/^行业调研_/u, "")
    .replace(/_\d{4}-\d{2}-\d{2}(?:\.md)?$/u, "")
    .replace(/[\s_\-—–、,，/／\\()（）]+/gu, "")
    .toLowerCase();
}

function normalizeSubject(value) {
  return String(value || "").trim().replace(/\s+/g, "");
}

function cleanCategory(value) {
  return String(value || "").replace(/`/g, "").replace(/[\\/]\s*$/, "").trim();
}
