import fs from "node:fs";
import path from "node:path";
import {
  buildFeatureEvaluationFormalPrompt,
  getHoldingPeriod,
  parseFeatureSubject,
  safeFeatureFilePart,
} from "../prompts/feature-evaluation.mjs";
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
import {
  FEATURE_QUANTIZATION_PLANS_DIR,
  parseFeatureQuantizationPlanEntries,
} from "./feature-quantization.mjs";
import {
  featureIdentityFromStem,
  normalizeHoldingPeriod,
  parseMachineFields,
  requiredMachineField,
  validateIsoDate,
  validateZonedIsoTimestamp,
} from "./feature-contract.mjs";

export const FEATURE_EVALUATION_PLAN_PATH = path.join(FUNDAMENTAL_ROOT, "特征量化", "特征评估", "研究方案", "特征评估.md");
export const FEATURE_QUANTIZATION_OUTPUT_DIR = path.join(FUNDAMENTAL_ROOT, "特征量化", "量化评分");
export const FEATURE_EVALUATION_OUTPUT_DIR = path.join(FUNDAMENTAL_ROOT, "特征量化", "特征评估");
export const FEATURE_EVALUATION_RETURN_DIR = path.join(FUNDAMENTAL_ROOT, "日度资料", "区间涨跌");

export const featureEvaluationDomain = {
  domain: "feature-evaluation",
  label: "特征评估",
  subjectHelp: "feature stem",
  requiresIndexedSubject: true,
  promptPath: FEATURE_EVALUATION_PLAN_PATH,
  indexPath: FEATURE_QUANTIZATION_OUTPUT_DIR,
  placeholder: "",
  outputPrefix: "基本面/特征量化/特征评估/",
  outputFilePattern: /^N\d{2}_.+_特征评估_(?:21d|63d|126d|252d)_形成日\d{4}-\d{2}-\d{2}_评估日\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  requiredPaths: [
    FEATURE_EVALUATION_PLAN_PATH,
    FEATURE_QUANTIZATION_OUTPUT_DIR,
    FEATURE_EVALUATION_RETURN_DIR,
  ],
  checkRequired() {
    const entries = parseFeatureEvaluationEntries();
    if (!entries.length) {
      throw new Error(`No feature quantization outputs found in: ${FEATURE_QUANTIZATION_OUTPUT_DIR}`);
    }
  },
  expectedOutputFile(item, runDate) {
    const { featureId, featureName } = parseFeatureSubject(item.subject);
    const featureStem = `${safeFeatureFilePart(featureId, "Nxx")}_${safeFeatureFilePart(featureName, "特征")}`;
    const holdingPeriod = getHoldingPeriod(item);
    const scoreDate = scoreDateForItem(item);
    return `基本面/特征量化/特征评估/${featureStem}_特征评估_${holdingPeriod}_形成日${scoreDate}_评估日${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildFeatureEvaluationFormalPrompt(item, featureEvaluationDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingFeatureEvaluationOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackFeatureEvaluationFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseFeatureEvaluationEntries();
  },
  resolveIndexEntry(subject) {
    return resolveFeatureEvaluationEntry(subject);
  },
  createQueueItem(options) {
    return createFeatureEvaluationQueueItem(options);
  },
  validateOutputFileForItem({ item, outputFile, fileName }) {
    const relative = outputFile.slice(featureEvaluationDomain.outputPrefix.length);
    if (!relative || relative.includes("/")) {
      throw new Error(`feature-evaluation outputFile must be directly under 基本面/特征量化/特征评估/: ${outputFile}`);
    }
    const expectedPrefix = expectedFeatureEvaluationOutputPrefix(item);
    if (!fileName.startsWith(expectedPrefix)) {
      throw new Error(`feature-evaluation outputFile filename must start with ${expectedPrefix}: ${fileName}`);
    }
  },
  validateOutputContentForItem({ item, outputFile, content }) {
    validateFeatureEvaluationOutputContentForItem({ item, outputFile, content });
  },
  validateQueueItem(item) {
    validateFeatureEvaluationQueueItem(item);
  },
};

export function parseFeatureEvaluationEntries(
  scoreDir = FEATURE_QUANTIZATION_OUTPUT_DIR,
  plansDir = FEATURE_QUANTIZATION_PLANS_DIR,
) {
  if (!fs.existsSync(scoreDir)) return [];
  const currentAlphaPlans = new Map(parseFeatureQuantizationPlanEntries(plansDir)
    .filter((plan) => plan.subject.startsWith("N"))
    .map((plan) => {
      const identity = featureIdentityFromStem(plan.subject);
      return [identity.featureId, identity];
    }));
  const entries = [];
  for (const entry of fs.readdirSync(scoreDir, { withFileTypes: true })) {
    if (!entry.isFile()) continue;
    const match = entry.name.match(/^(N\d{2}_.+)_量化评分_(\d{4}-\d{2}-\d{2})\.md$/u);
    if (!match) continue;
    const featureSubject = match[1];
    const date = match[2];
    const identity = featureIdentityFromStem(featureSubject);
    const currentIdentity = currentAlphaPlans.get(identity?.featureId);
    if (!identity || !currentIdentity || currentIdentity.featureSubject !== identity.featureSubject) continue;
    const scorePath = path.join(scoreDir, entry.name);
    const scoreFile = normalizeProjectPath(path.relative(PROJECT_ROOT, scorePath));
    const metadata = parseLockedScoreMetadata({
      content: fs.readFileSync(scorePath, "utf8"),
      featureSubject,
      scoreDate: date,
    });
    entries.push({
      subject: `${featureSubject}_量化评分_${date}`,
      featureSubject,
      displayName: `${featureSubject} @ ${date}`,
      category: "特征评估",
      scoreDate: date,
      scoreFile,
      featureVersion: metadata.featureVersion,
      scoreTradableTimestamp: metadata.scoreTradableTimestamp,
    });
  }
  return entries.sort((a, b) => a.featureSubject.localeCompare(b.featureSubject, "zh-Hans-CN") || a.scoreDate.localeCompare(b.scoreDate));
}

export function resolveFeatureEvaluationEntry(subject) {
  const entries = parseFeatureEvaluationEntries();
  const literal = String(subject || "").trim().replace(/\.md$/iu, "");
  const exact = entries.find((entry) => entry.subject === literal || entry.displayName === literal);
  if (exact) return exact;
  const wanted = normalizeFeatureSubject(subject);
  const matching = entries.filter((entry) => normalizeFeatureSubject(entry.featureSubject) === wanted
    || normalizeFeatureSubject(entry.displayName) === wanted
    || normalizeFeatureSubject(entry.subject) === wanted);
  if (matching.length) return matching.sort((a, b) => b.scoreDate.localeCompare(a.scoreDate))[0];
  if (/^N\d{2}$/u.test(wanted)) {
    return entries.filter((entry) => normalizeFeatureSubject(entry.featureSubject).startsWith(`${wanted}_`))
      .sort((a, b) => b.scoreDate.localeCompare(a.scoreDate))[0] || null;
  }
  return null;
}

export function createFeatureEvaluationQueueItem({
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
  scoreFile = "",
  scoreDate = "",
  holdingPeriod = "",
  returnWindow = "",
  extra = {},
} = {}) {
  if (!subject) throw new Error("feature-evaluation queue item requires --subject");
  const normalizedScoreFile = normalizeProjectPath(scoreFile);
  const entry = normalizedScoreFile
    ? parseFeatureEvaluationEntries().find((candidate) => candidate.scoreFile === normalizedScoreFile)
    : resolveFeatureEvaluationEntry(subject);
  if (!entry) throw new Error(`feature-evaluation score snapshot does not match the current N plan ID/name: ${subject}`);
  const normalizedSubject = entry.subject;
  const normalizedHoldingPeriod = normalizeHoldingPeriod(holdingPeriod || returnWindow || "126d", "holdingPeriod");
  if (scoreDate && scoreDate !== entry.scoreDate) {
    throw new Error(`feature-evaluation scoreDate does not match scoreFile: ${scoreDate} != ${entry.scoreDate}`);
  }
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `feature-evaluation-${safeIdPart(normalizedSubject)}-${safeIdPart(normalizedHoldingPeriod)}-${safeIdPart(nowIso)}`,
    domain: "feature-evaluation",
    sourceDate,
    subject: normalizedSubject,
    displayName: displayName || entry?.displayName || normalizedSubject,
    category: category || entry?.category || "特征评估",
    status,
    attempts,
    outputFile: normalizeProjectPath(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    ...extra,
    scoreFile: entry.scoreFile,
    scoreDate: entry.scoreDate,
    holdingPeriod: normalizedHoldingPeriod,
    featureVersion: entry.featureVersion,
    scoreTradableTimestamp: entry.scoreTradableTimestamp,
  };
}

export function backupExistingFeatureEvaluationOutputs(item, outputContract = {}) {
  const expectedPrefix = expectedFeatureEvaluationOutputPrefix(item);
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: FEATURE_EVALUATION_OUTPUT_DIR,
    backupKey: `${parseFeatureSubject(item.subject).featureId}_${scoreDateForItem(item)}_${getHoldingPeriod(item)}`,
    expectedFileName,
    matchFileName: (fileName) => fileName.startsWith(expectedPrefix)
      && featureEvaluationDomain.outputFilePattern.test(fileName),
  });
}

export function rollbackFeatureEvaluationFormalRun(item, prepareResult = {}, outputContract = {}) {
  const expectedFileName = outputContract.expectedOutputFile?.split("/").pop() || "";
  const expectedPrefix = expectedFeatureEvaluationOutputPrefix(item);
  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir: FEATURE_EVALUATION_OUTPUT_DIR,
    expectedFileName,
    prepareResult,
    newFileNameMatcher: (fileName) => fileName.startsWith(expectedPrefix)
      && featureEvaluationDomain.outputFilePattern.test(fileName),
  });
}

function expectedFeatureEvaluationOutputPrefix(item) {
  const { featureId, featureName } = parseFeatureSubject(item.subject);
  const holdingPeriod = getHoldingPeriod(item);
  return `${safeFeatureFilePart(featureId, "Nxx")}_${safeFeatureFilePart(featureName, "特征")}_特征评估_${holdingPeriod}_形成日${scoreDateForItem(item)}_评估日`;
}

export function validateFeatureEvaluationQueueItem(item) {
  const holdingPeriod = getHoldingPeriod(item);
  const scoreFile = normalizeProjectPath(item?.scoreFile);
  const scoreDate = scoreDateForItem(item);
  if (!scoreFile) throw new Error(`feature-evaluation item is missing scoreFile: ${item?.subject || ""}`);
  if (item?.holdingPeriod && item.holdingPeriod !== holdingPeriod) {
    throw new Error(`feature-evaluation holdingPeriod must be canonical: ${item.holdingPeriod}`);
  }
  const entry = parseFeatureEvaluationEntries().find((candidate) => candidate.scoreFile === scoreFile);
  if (!entry) throw new Error(`feature-evaluation scoreFile is not a current valid N snapshot: ${scoreFile}`);
  if (entry.subject !== item.subject) {
    throw new Error(`feature-evaluation subject does not match scoreFile: ${item.subject} != ${entry.subject}`);
  }
  if (entry.scoreDate !== scoreDate) {
    throw new Error(`feature-evaluation scoreDate does not match scoreFile: ${scoreDate} != ${entry.scoreDate}`);
  }
  if (item.featureVersion && item.featureVersion !== entry.featureVersion) {
    throw new Error(`feature-evaluation featureVersion does not match scoreFile: ${item.featureVersion} != ${entry.featureVersion}`);
  }
  if (item.scoreTradableTimestamp && item.scoreTradableTimestamp !== entry.scoreTradableTimestamp) {
    throw new Error("feature-evaluation scoreTradableTimestamp does not match scoreFile");
  }
  return { ...entry, holdingPeriod };
}

export function validateFeatureEvaluationOutputContentForItem({ item, content, lockedEntry = null }) {
  const locked = lockedEntry || validateFeatureEvaluationQueueItem(item);
  const identity = featureIdentityFromStem(locked.featureSubject);
  const fields = parseMachineFields(content);
  const expected = {
    feature_id: identity.featureId,
    feature_name: identity.featureName,
    feature_version: locked.featureVersion,
    score_file: locked.scoreFile,
    score_as_of: locked.scoreDate,
    score_tradable_timestamp: locked.scoreTradableTimestamp,
    holding_period: locked.holdingPeriod,
  };
  for (const [name, expectedValue] of Object.entries(expected)) {
    const actual = requiredMachineField(fields, name);
    const normalizedActual = name === "score_file" ? normalizeProjectPath(actual) : actual;
    if (normalizedActual !== expectedValue) {
      throw new Error(`evaluation machine-readable field ${name} does not match locked task: ${normalizedActual} != ${expectedValue}`);
    }
  }
  if (requiredMachineField(fields, "layer") !== "alpha") {
    throw new Error("evaluation machine-readable field layer must be alpha for N features");
  }
  const status = requiredMachineField(fields, "status");
  if (!new Set(["completed", "immature", "data_failed"]).has(status)) {
    throw new Error(`evaluation machine-readable field status is invalid: ${status}`);
  }
  validateIsoDate(requiredMachineField(fields, "oos_start"), "oos_start");
  validateIsoDate(requiredMachineField(fields, "oos_end"), "oos_end");
  const scoreTradableTimestamp = validateZonedIsoTimestamp(
    requiredMachineField(fields, "score_tradable_timestamp"),
    "score_tradable_timestamp",
  );
  const entryTimestamp = validateZonedIsoTimestamp(requiredMachineField(fields, "entry_timestamp"), "entry_timestamp");
  if (new Date(entryTimestamp).getTime() <= new Date(scoreTradableTimestamp).getTime()) {
    throw new Error("entry_timestamp must be strictly later than score_tradable_timestamp");
  }
}

export function parseLockedScoreMetadata({ content, featureSubject, scoreDate }) {
  const identity = featureIdentityFromStem(featureSubject);
  if (!identity || !identity.featureId.startsWith("N")) {
    throw new Error(`score snapshot is not an N feature: ${featureSubject}`);
  }
  const fields = parseMachineFields(content);
  const featureId = requiredMachineField(fields, "feature_id");
  const featureName = requiredMachineField(fields, "feature_name");
  const featureVersion = requiredMachineField(fields, "feature_version");
  const asOfDate = validateIsoDate(requiredMachineField(fields, "as_of_date"), "as_of_date");
  const scoreTradableTimestamp = validateZonedIsoTimestamp(
    requiredMachineField(fields, "score_tradable_timestamp"),
    "score_tradable_timestamp",
  );
  if (`${featureId}_${featureName}` !== identity.featureSubject) {
    throw new Error(`score metadata feature identity does not match filename: ${featureId}_${featureName} != ${identity.featureSubject}`);
  }
  if (asOfDate !== scoreDate) throw new Error(`score metadata as_of_date does not match filename: ${asOfDate} != ${scoreDate}`);
  if (scoreTradableTimestamp.slice(0, 10) < asOfDate) {
    throw new Error(`score_tradable_timestamp cannot precede as_of_date: ${scoreTradableTimestamp} < ${asOfDate}`);
  }
  return { featureVersion, scoreTradableTimestamp };
}

function scoreDateForItem(item) {
  const date = String(item?.scoreDate || "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/u.test(date)) {
    throw new Error(`feature-evaluation item is missing a valid scoreDate: ${item?.subject || ""}`);
  }
  return date;
}

function normalizeFeatureSubject(value) {
  return String(value || "")
    .trim()
    .replace(/\.md$/iu, "")
    .replace(/_研究方案$/u, "")
    .replace(/_量化评分_\d{4}-\d{2}-\d{2}$/u, "")
    .replace(/\s+/g, "");
}
