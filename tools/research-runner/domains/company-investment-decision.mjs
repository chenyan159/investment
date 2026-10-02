import { resolveCurrentPlan } from "../research-plan-store.mjs";
import path from "node:path";
import {
  buildCompanyInvestmentDecisionFormalPrompt,
} from "../prompts/company-investment-decision.mjs";
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

export const COMPANY_INVESTMENT_DECISION_PLAN_DIR = path.join(ANALYSIS_ROOT, "公司情景投资决策", "研究方案");
export const COMPANY_INVESTMENT_DECISION_OUTPUT_DIR = path.join(
  ANALYSIS_ROOT,
  "公司情景投资决策",
  "结果",
);
export const COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX = "分析报告/公司情景投资决策/结果/";
const COMPANY_INDEX_PATH = path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md");
export const companyInvestmentDecisionDomain = {
  domain: "company-investment-decision",
  label: "公司经营评估与情景投资决策",
  subjectHelp: "ticker",
  requiresIndexedSubject: true,
  get promptPath() { return resolveCurrentPlan(COMPANY_INVESTMENT_DECISION_PLAN_DIR); },
  indexPath: COMPANY_INDEX_PATH,
  placeholder: "【公司股票代号】",
  outputPrefix: COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX,
  outputFilePattern: /^.+_经营情景市场状态投资决策_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  companyCategories: new Set(COMPANY_CATEGORIES),
  requiredPaths: [
    COMPANY_INVESTMENT_DECISION_PLAN_DIR,
    COMPANY_INDEX_PATH,
  ],
  expectedOutputFile(item, runDate) {
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    return `${COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX}${ticker}_经营情景市场状态投资决策_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildCompanyInvestmentDecisionFormalPrompt(
      item,
      companyInvestmentDecisionDomain,
      outputContract,
    );
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingCompanyInvestmentDecisionOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackCompanyInvestmentDecisionFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseCompanyIndexEntries(companyInvestmentDecisionDomain.indexPath);
  },
  resolveIndexEntry(subject) {
    return resolveCompanyIndexEntry(companyInvestmentDecisionDomain.indexPath, subject);
  },
  createQueueItem(options) {
    return createCompanyInvestmentDecisionQueueItem(options);
  },
  validateOutputFileForItem({ item, fileName }) {
    const primary = primarySubject(item?.subject);
    if (!primary) throw new Error("company-investment-decision output validation requires item.subject");
    if (!fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)) {
      throw new Error(`company-investment-decision outputFile filename must start with ${primary}_: ${fileName}`);
    }
  },
};

export function createCompanyInvestmentDecisionQueueItem({
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
  if (!subject) throw new Error("company-investment-decision queue item requires --subject or --ticker");
  const entry = companyInvestmentDecisionDomain.resolveIndexEntry(subject);
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `company-investment-decision-${safeIdPart(subject)}-${safeIdPart(nowIso)}`,
    domain: "company-investment-decision",
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

export function backupExistingCompanyInvestmentDecisionOutputs(item, outputContract = {}) {
  const primary = primarySubject(item?.subject);
  if (!primary) return { backupDir: "", files: [] };

  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: COMPANY_INVESTMENT_DECISION_OUTPUT_DIR,
    backupKey: primary,
    expectedFileName,
    matchFileName: (fileName) => fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyInvestmentDecisionDomain.outputFilePattern.test(fileName),
  });
}

export function rollbackCompanyInvestmentDecisionFormalRun(item, prepareResult = {}, outputContract = {}) {
  const primary = primarySubject(item?.subject);
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: COMPANY_INVESTMENT_DECISION_OUTPUT_DIR,
    expectedFileName,
    prepareResult,
    newFileNameMatcher: (fileName) => primary
      && fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyInvestmentDecisionDomain.outputFilePattern.test(fileName),
  });
}
