import path from "node:path";
import {
  buildCompanySentimentFormalPrompt,
} from "../prompts/company-sentiment.mjs";
import {
  COMPANY_CATEGORIES,
  parseCompanyIndexEntries,
  resolveCompanyIndexEntry,
} from "./company.mjs";
import {
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

export const companySentimentDomain = {
  domain: "company-sentiment",
  label: "公司情绪",
  subjectHelp: "ticker",
  requiresIndexedSubject: true,
  promptPath: path.join(PROJECT_ROOT, "情绪面", "研究方法", "研究方案.md"),
  indexPath: path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
  placeholder: "【股票代号】",
  outputPrefix: "情绪面/公司情绪/",
  outputFilePattern: /^.+_公司情绪_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  companyCategories: new Set(COMPANY_CATEGORIES),
  requiredPaths: [
    path.join(PROJECT_ROOT, "情绪面", "研究方法", "研究方案.md"),
    path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
  ],
  expectedOutputFile(item, runDate) {
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    const name = safeOutputNamePart(item?.displayName, "公司");
    return `情绪面/公司情绪/${ticker}_${name}_公司情绪_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildCompanySentimentFormalPrompt(item, companySentimentDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingCompanySentimentOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackCompanySentimentFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseCompanyIndexEntries(companySentimentDomain.indexPath);
  },
  resolveIndexEntry(subject) {
    return resolveCompanyIndexEntry(companySentimentDomain.indexPath, subject);
  },
  createQueueItem(options) {
    return createCompanySentimentQueueItem(options);
  },
  validateOutputFileForItem({ item, fileName }) {
    const primary = primarySubject(item?.subject);
    if (!primary) throw new Error("company-sentiment output validation requires item.subject");
    if (!fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)) {
      throw new Error(`company-sentiment outputFile filename must start with ${primary}_: ${fileName}`);
    }
  },
};

export function backupExistingCompanySentimentOutputs(item, outputContract = {}) {
  const outputDir = path.join(PROJECT_ROOT, "情绪面", "公司情绪");
  const primary = primarySubject(item?.subject);
  if (!primary) return { backupDir: "", files: [] };

  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    backupKey: primary,
    expectedFileName,
    matchFileName: (fileName) => fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companySentimentDomain.outputFilePattern.test(fileName),
  });
}

export function rollbackCompanySentimentFormalRun(item, prepareResult = {}, outputContract = {}) {
  const outputDir = path.join(PROJECT_ROOT, "情绪面", "公司情绪");
  const primary = primarySubject(item?.subject);
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    expectedFileName,
    prepareResult,
    newFileNameMatcher: (fileName) => primary
      && fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companySentimentDomain.outputFilePattern.test(fileName),
  });
}

export function createCompanySentimentQueueItem({
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
  if (!subject) throw new Error("company-sentiment queue item requires --subject or --ticker");
  const entry = companySentimentDomain.resolveIndexEntry(subject);
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `company-sentiment-${safeIdPart(subject)}-${safeIdPart(nowIso)}`,
    domain: "company-sentiment",
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
