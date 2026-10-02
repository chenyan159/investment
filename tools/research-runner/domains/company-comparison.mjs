import { resolveCurrentPlan } from "../research-plan-store.mjs";
import path from "node:path";
import {
  buildCompanyComparisonFormalPrompt,
} from "../prompts/company-comparison.mjs";
import {
  COMPANY_CATEGORIES,
  parseCompanyIndexEntries,
  resolveCompanyIndexEntry,
} from "./company.mjs";
import {
  ANALYSIS_ROOT,
  formatLocalDate,
  formatLocalIso,
  FUNDAMENTAL_ROOT,
  normalizeProjectPath,
  PROJECT_ROOT,
  safeIdPart,
} from "../queue-store.mjs";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "./output-backup.mjs";
import { primarySubject, safeOutputNamePart } from "./output-path.mjs";

export const COMPANY_COMPARISON_PLAN_DIR = path.join(ANALYSIS_ROOT, "公司对比", "研究方案");
export const COMPANY_COMPARISON_OUTPUT_DIR = path.join(ANALYSIS_ROOT, "公司对比", "结果");

export const companyComparisonDomain = {
  domain: "company-comparison",
  label: "公司对比",
  subjectHelp: "ticker",
  requiresIndexedSubject: true,
  get promptPath() { return resolveCurrentPlan(COMPANY_COMPARISON_PLAN_DIR); },
  indexPath: path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
  placeholder: "【公司股票代号A】",
  outputPrefix: "分析报告/公司对比/结果/",
  outputFilePattern: /^.+_逐家公司投资思路对比_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  companyCategories: new Set(COMPANY_CATEGORIES),
  requiredPaths: [
    COMPANY_COMPARISON_PLAN_DIR,
    path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
    path.join(ANALYSIS_ROOT, "公司情景投资决策", "结果"),
  ],
  expectedOutputFile(item, runDate) {
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    return `分析报告/公司对比/结果/${ticker}_逐家公司投资思路对比_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildCompanyComparisonFormalPrompt(item, companyComparisonDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingCompanyComparisonOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackCompanyComparisonFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseCompanyIndexEntries(companyComparisonDomain.indexPath);
  },
  resolveIndexEntry(subject) {
    return resolveCompanyIndexEntry(companyComparisonDomain.indexPath, subject);
  },
  createQueueItem(options) {
    return createCompanyComparisonQueueItem(options);
  },
  validateOutputFileForItem({ item, fileName }) {
    const primary = primarySubject(item?.subject);
    if (!primary) throw new Error("company-comparison output validation requires item.subject");
    if (!fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)) {
      throw new Error(`company-comparison outputFile filename must start with ${primary}_: ${fileName}`);
    }
  },
};

export function createCompanyComparisonQueueItem({
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
  if (!subject) throw new Error("company-comparison queue item requires --subject or --ticker");
  const entry = companyComparisonDomain.resolveIndexEntry(subject);
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `company-comparison-${safeIdPart(subject)}-${safeIdPart(nowIso)}`,
    domain: "company-comparison",
    sourceDate,
    subject,
    displayName: displayName || entry?.displayName || "",
    category: category || entry?.category || "",
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

export function backupExistingCompanyComparisonOutputs(item, outputContract = {}) {
  const primary = primarySubject(item?.subject);
  if (!primary) return { backupDir: "", files: [] };

  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: COMPANY_COMPARISON_OUTPUT_DIR,
    backupKey: primary,
    expectedFileName,
    matchFileName: (fileName) => fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyComparisonDomain.outputFilePattern.test(fileName),
  });
}

export function rollbackCompanyComparisonFormalRun(item, prepareResult = {}, outputContract = {}) {
  const primary = primarySubject(item?.subject);
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: COMPANY_COMPARISON_OUTPUT_DIR,
    expectedFileName,
    prepareResult,
    newFileNameMatcher: (fileName) => primary
      && fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyComparisonDomain.outputFilePattern.test(fileName),
  });
}
