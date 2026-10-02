import { createHash } from "node:crypto";
import fs from "node:fs";
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
  readUtf8,
  safeIdPart,
} from "../queue-store.mjs";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "./output-backup.mjs";
import { primarySubject, safeOutputNamePart } from "./output-path.mjs";

export const COMPANY_INVESTMENT_DECISION_PLAN_PATH = path.join(
  ANALYSIS_ROOT,
  "公司情景投资决策",
  "研究方案.md",
);
export const COMPANY_INVESTMENT_DECISION_OUTPUT_DIR = path.join(
  ANALYSIS_ROOT,
  "公司情景投资决策",
  "结果",
);
export const COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX = "分析报告/公司情景投资决策/结果/";
export const COMPANY_INVESTMENT_DECISION_BATCHES_PATH = path.join(
  PROJECT_ROOT,
  "tools",
  "research-runner",
  "company-investment-decision.batches.json",
);

const COMPANY_INDEX_PATH = path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md");
const MARKET_SNAPSHOT_PREFIX = "金融资料/市场状态/";
const MARKET_SNAPSHOT_FILE_PATTERN = /_(\d{4}-\d{2}-\d{2})\.md$/u;
const SHA256_PATTERN = /^[0-9A-F]{64}$/u;
const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/u;
const REQUIRED_MARKET_SNAPSHOT_MARKERS = Object.freeze([
  "快照身份与使用边界",
  "五块市场记分板",
  "宽度与参与",
  "信用与融资",
  "波动率与市场功能",
  "利率与折现率",
  "盈利预期修正",
  "主状态",
  "唯一相邻状态",
  "总体证据强度",
]);
const batchManifestCache = new Map();
const marketSnapshotCache = new Map();

export const companyInvestmentDecisionDomain = {
  domain: "company-investment-decision",
  label: "公司经营评估与情景投资决策",
  subjectHelp: "ticker",
  requiresIndexedSubject: true,
  promptPath: COMPANY_INVESTMENT_DECISION_PLAN_PATH,
  indexPath: COMPANY_INDEX_PATH,
  placeholder: "【公司股票代号】",
  outputPrefix: COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX,
  outputFilePattern: /^.+_经营情景市场状态投资决策_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  companyCategories: new Set(COMPANY_CATEGORIES),
  requiredPaths: [
    COMPANY_INVESTMENT_DECISION_PLAN_PATH,
    COMPANY_INDEX_PATH,
    COMPANY_INVESTMENT_DECISION_BATCHES_PATH,
  ],
  expectedOutputFile(item, runDate) {
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    return `${COMPANY_INVESTMENT_DECISION_OUTPUT_PREFIX}${ticker}_经营情景市场状态投资决策_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract, options = {}) {
    const marketSnapshot = options.marketSnapshot
      || resolveCompanyInvestmentDecisionMarketSnapshot(item);
    return buildCompanyInvestmentDecisionFormalPrompt(
      item,
      companyInvestmentDecisionDomain,
      outputContract,
      marketSnapshot,
    );
  },
  prepareFormalRun(item, outputContract) {
    return prepareCompanyInvestmentDecisionFormalRun(item, outputContract);
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
  validateQueueItem(item) {
    resolveCompanyInvestmentDecisionMarketSnapshot(item);
  },
  validateOutputFileForItem({ item, fileName }) {
    const primary = primarySubject(item?.subject);
    if (!primary) throw new Error("company-investment-decision output validation requires item.subject");
    if (!fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)) {
      throw new Error(`company-investment-decision outputFile filename must start with ${primary}_: ${fileName}`);
    }
  },
};

export function resolveCompanyInvestmentDecisionMarketSnapshot(item, {
  projectRoot = PROJECT_ROOT,
  batchesPath = COMPANY_INVESTMENT_DECISION_BATCHES_PATH,
  useCache = true,
} = {}) {
  const sourceDate = String(item?.sourceDate || "").trim();
  const subject = primarySubject(item?.subject).toUpperCase();
  if (!subject) throw new Error("company-investment-decision market snapshot requires item.subject");
  if (!DATE_PATTERN.test(sourceDate)) {
    throw new Error(`company-investment-decision ${subject} sourceDate must use YYYY-MM-DD: ${sourceDate || "(empty)"}`);
  }

  const manifest = readAndValidateBatchManifest(batchesPath, { useCache });
  const matches = manifest.batches.filter((batch) => (
    batch.sourceDate === sourceDate && batch.subjects.includes(subject)
  ));
  if (!matches.length) {
    throw new Error(`company-investment-decision ${subject}/${sourceDate} is not bound to a shared market snapshot batch in ${batchesPath}`);
  }
  if (matches.length !== 1) {
    throw new Error(`company-investment-decision ${subject}/${sourceDate} matches multiple shared market snapshot batches in ${batchesPath}`);
  }

  const batch = matches[0];
  const cacheKey = `${path.resolve(batchesPath)}\u0000${batch.batchId}`;
  const cached = useCache ? marketSnapshotCache.get(cacheKey) : null;
  if (cached) return cached;

  const snapshotFile = normalizeMarketSnapshotFile(batch.snapshotFile);
  const snapshotDate = snapshotFile.match(MARKET_SNAPSHOT_FILE_PATTERN)?.[1] || "";
  if (snapshotDate !== batch.sourceDate) {
    throw new Error(`shared market snapshot filename date must equal batch sourceDate ${batch.sourceDate}: ${snapshotFile}`);
  }

  const snapshotPath = path.join(projectRoot, ...snapshotFile.split("/"));
  if (!fs.existsSync(snapshotPath)) {
    throw new Error(`shared market snapshot does not exist: ${snapshotFile}`);
  }
  const stat = fs.statSync(snapshotPath);
  if (!stat.isFile()) throw new Error(`shared market snapshot is not a regular file: ${snapshotFile}`);
  if (stat.size <= 0) throw new Error(`shared market snapshot is empty: ${snapshotFile}`);

  const bytes = fs.readFileSync(snapshotPath);
  const content = bytes.toString("utf8");
  const actualSha256 = createHash("sha256").update(bytes).digest("hex").toUpperCase();
  if (actualSha256 !== batch.sha256) {
    throw new Error(`shared market snapshot SHA-256 mismatch for ${snapshotFile}: expected ${batch.sha256}, actual ${actualSha256}`);
  }
  if (!content.includes(batch.sourceDate)) {
    throw new Error(`shared market snapshot does not contain its batch sourceDate ${batch.sourceDate}: ${snapshotFile}`);
  }
  for (const marker of REQUIRED_MARKET_SNAPSHOT_MARKERS) {
    if (!content.includes(marker)) {
      throw new Error(`shared market snapshot is missing required marker ${marker}: ${snapshotFile}`);
    }
  }

  const snapshot = Object.freeze({
    batchId: batch.batchId,
    sourceDate: batch.sourceDate,
    marketScope: batch.marketScope,
    snapshotFile,
    sha256: actualSha256,
    content,
  });
  if (useCache) marketSnapshotCache.set(cacheKey, snapshot);
  return snapshot;
}

export function prepareCompanyInvestmentDecisionFormalRun(item, outputContract = {}, {
  resolveMarketSnapshot = resolveCompanyInvestmentDecisionMarketSnapshot,
  backupOutputs = backupExistingCompanyInvestmentDecisionOutputs,
} = {}) {
  resolveMarketSnapshot(item);
  return backupOutputs(item, outputContract);
}

function readAndValidateBatchManifest(batchesPath, { useCache }) {
  const resolvedPath = path.resolve(batchesPath);
  const cached = useCache ? batchManifestCache.get(resolvedPath) : null;
  if (cached) return cached;
  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`company-investment-decision batch manifest does not exist: ${resolvedPath}`);
  }

  let parsed;
  try {
    parsed = JSON.parse(readUtf8(resolvedPath));
  } catch (error) {
    throw new Error(`invalid company-investment-decision batch manifest ${resolvedPath}: ${error.message}`);
  }
  if (parsed?.schemaVersion !== 1 || !Array.isArray(parsed?.batches) || !parsed.batches.length) {
    throw new Error(`company-investment-decision batch manifest must contain schemaVersion=1 and a non-empty batches array: ${resolvedPath}`);
  }

  const seenBatchIds = new Set();
  const seenBindings = new Set();
  const batches = parsed.batches.map((rawBatch, index) => {
    const label = `batch manifest entry ${index + 1}`;
    const batchId = String(rawBatch?.batchId || "").trim();
    const sourceDate = String(rawBatch?.sourceDate || "").trim();
    const marketScope = String(rawBatch?.marketScope || "").trim();
    const snapshotFile = normalizeMarketSnapshotFile(rawBatch?.snapshotFile);
    const sha256 = String(rawBatch?.sha256 || "").trim().toUpperCase();
    const subjects = Array.isArray(rawBatch?.subjects)
      ? rawBatch.subjects.map((value) => String(value || "").trim().toUpperCase()).filter(Boolean)
      : [];

    if (!batchId) throw new Error(`${label} is missing batchId`);
    if (seenBatchIds.has(batchId)) throw new Error(`${label} duplicates batchId ${batchId}`);
    seenBatchIds.add(batchId);
    if (!DATE_PATTERN.test(sourceDate)) throw new Error(`${label} sourceDate must use YYYY-MM-DD: ${sourceDate || "(empty)"}`);
    if (!marketScope) throw new Error(`${label} is missing marketScope`);
    if (!subjects.length) throw new Error(`${label} must contain at least one subject`);
    if (new Set(subjects).size !== subjects.length) throw new Error(`${label} contains duplicate subjects`);
    if (!SHA256_PATTERN.test(sha256)) throw new Error(`${label} sha256 must contain 64 hexadecimal characters`);

    for (const subject of subjects) {
      const bindingKey = `${sourceDate}\u0000${subject}`;
      if (seenBindings.has(bindingKey)) {
        throw new Error(`${label} duplicates the ${subject}/${sourceDate} shared market snapshot binding`);
      }
      seenBindings.add(bindingKey);
    }
    return Object.freeze({ batchId, sourceDate, marketScope, snapshotFile, sha256, subjects: Object.freeze(subjects) });
  });

  const manifest = Object.freeze({ schemaVersion: 1, batches: Object.freeze(batches) });
  if (useCache) batchManifestCache.set(resolvedPath, manifest);
  return manifest;
}

function normalizeMarketSnapshotFile(value) {
  const raw = String(value || "").trim();
  if (!raw) throw new Error("shared market snapshot binding is missing snapshotFile");
  const nativePath = raw.replace(/\//g, path.sep);
  if (path.isAbsolute(nativePath)) {
    throw new Error(`shared market snapshot path must be Investment-relative: ${raw}`);
  }
  if (/\\/u.test(raw)) throw new Error(`shared market snapshot path must use forward slashes: ${raw}`);

  const snapshotFile = normalizeProjectPath(raw);
  const parts = snapshotFile.split("/");
  if (parts.some((part) => !part || part === "." || part === "..")) {
    throw new Error(`shared market snapshot path contains an invalid segment: ${raw}`);
  }
  if (!snapshotFile.startsWith(MARKET_SNAPSHOT_PREFIX)) {
    throw new Error(`shared market snapshot must be under ${MARKET_SNAPSHOT_PREFIX}: ${snapshotFile}`);
  }
  if (parts.some((part) => ["备份", "tmp", "_work"].includes(part))) {
    throw new Error(`shared market snapshot must be a formal file, not backup or working material: ${snapshotFile}`);
  }
  if (!MARKET_SNAPSHOT_FILE_PATTERN.test(path.posix.basename(snapshotFile))) {
    throw new Error(`shared market snapshot filename must end with _YYYY-MM-DD.md: ${snapshotFile}`);
  }
  return snapshotFile;
}

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
