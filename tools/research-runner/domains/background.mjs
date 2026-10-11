import fs from "node:fs";
import path from "node:path";
import { buildBackgroundFormalPrompt } from "../prompts/background.mjs";
import {
  formatLocalDate,
  formatLocalIso,
  FUNDAMENTAL_ROOT,
  normalizeProjectPath,
  PROJECT_ROOT,
  safeIdPart,
} from "../queue-store.mjs";
import { backupExistingOutputs, rollbackPreparedOutputs } from "./output-backup.mjs";
import { safeOutputNamePart } from "./output-path.mjs";

// 产业背景：研究方案/<专题>/ 下各一套方案；结果/ 只放每个专题、每个会议系列的最新一份；旧版移入 备份/。
export const BACKGROUND_ROOT = path.join(FUNDAMENTAL_ROOT, "产业背景");
export const BACKGROUND_PLAN_ROOT = path.join(BACKGROUND_ROOT, "研究方案");
export const BACKGROUND_RESULT_DIR = path.join(BACKGROUND_ROOT, "结果");
export const BACKGROUND_BACKUP_DIR = path.join(BACKGROUND_ROOT, "备份");
export const CONFERENCE_TOPIC = "会议调研";

const OUTPUT_PREFIX = "基本面/产业背景/结果/";
const PLAN_FILE_PATTERN = /^研究方案_\d{8}_\d{6}\.md$/u;
const DATE_SUFFIX = /_\d{4}-\d{2}-\d{2}\.md$/u;
const CONFERENCE_FILE_PATTERN = /^会议调研_(.+)_((?:19|20)\d{2})_(\d{4}-\d{2}-\d{2})\.md$/u;

export const backgroundDomain = {
  domain: "background",
  label: "产业背景",
  subjectHelp: "background topic, or conference series plus year",
  requiresIndexedSubject: true,
  promptPath: BACKGROUND_PLAN_ROOT,
  indexPath: BACKGROUND_PLAN_ROOT,
  placeholder: "",
  outputPrefix: OUTPUT_PREFIX,
  outputFilePattern: /^.+_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(),
  requiredPaths: [BACKGROUND_PLAN_ROOT, BACKGROUND_RESULT_DIR],
  expectedOutputFile(item, runDate) {
    return `${OUTPUT_PREFIX}${backgroundOutputFileName(backgroundEntryForItem(item), runDate)}`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildBackgroundFormalPrompt(item, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupBackgroundOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackBackgroundRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return listBackgroundTopics().map((topic) => resolveBackgroundSubject(topic));
  },
  resolveIndexEntry(subject) {
    return resolveBackgroundSubject(subject);
  },
  createQueueItem(options) {
    return createBackgroundQueueItem(options);
  },
  validateQueueItem(item) {
    backgroundEntryForItem(item);
  },
  validateOutputFileForItem({ item, fileName }) {
    if (!item) return;
    const entry = backgroundEntryForItem(item);
    if (!isSameSubjectOutput(entry, fileName)) {
      throw new Error(`background outputFile does not belong to ${item.subject}: ${fileName}`);
    }
  },
};

export function listBackgroundTopics(planRoot = BACKGROUND_PLAN_ROOT) {
  if (!fs.existsSync(planRoot)) return [];
  return fs.readdirSync(planRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && entry.name !== CONFERENCE_TOPIC)
    .filter((entry) => fs.readdirSync(path.join(planRoot, entry.name)).some((name) => PLAN_FILE_PATTERN.test(name)))
    .map((entry) => entry.name)
    .sort((a, b) => a.localeCompare(b, "zh-CN"));
}

export function parseConferenceSubject(subject) {
  const match = /^(.*\S)[\s_]+((?:19|20)\d{2})$/u.exec(String(subject || "").trim());
  if (!match) return null;
  const series = match[1].replace(/[\s_]+/gu, " ").trim();
  return series ? { series, year: match[2] } : null;
}

export function conferenceSeriesKey(series) {
  return String(series || "").toLowerCase().replace(/[\s_\-—–·.,:：()（）/／]+/gu, "");
}

export function resolveBackgroundSubject(subject, planRoot = BACKGROUND_PLAN_ROOT) {
  const raw = String(subject || "").trim();
  if (!raw) return null;
  if (listBackgroundTopics(planRoot).includes(raw)) {
    return { subject: raw, displayName: raw, category: "背景专题", kind: "topic", topic: raw };
  }
  const conference = parseConferenceSubject(raw);
  if (!conference || !fs.existsSync(path.join(planRoot, CONFERENCE_TOPIC))) return null;
  const name = `${conference.series} ${conference.year}`;
  return {
    subject: name,
    displayName: name,
    category: CONFERENCE_TOPIC,
    kind: "conference",
    topic: CONFERENCE_TOPIC,
    series: conference.series,
    year: conference.year,
  };
}

export function backgroundEntryForItem(item) {
  if (item?.backgroundKind === "conference" && item.conferenceSeries && item.conferenceYear) {
    return { kind: "conference", topic: CONFERENCE_TOPIC, series: item.conferenceSeries, year: item.conferenceYear };
  }
  if (item?.backgroundKind === "topic" && item.backgroundTopic) {
    return { kind: "topic", topic: item.backgroundTopic };
  }
  const entry = resolveBackgroundSubject(item?.subject);
  if (!entry) {
    throw new Error(`background subject must be a topic under 基本面/产业背景/研究方案/ or "<会议系列> <年份>": ${item?.subject || ""}`);
  }
  return entry;
}

export function backgroundOutputFileName(entry, runDate) {
  if (entry.kind === "conference") {
    return `${CONFERENCE_TOPIC}_${safeOutputNamePart(entry.series)}_${entry.year}_${runDate}.md`;
  }
  return `${safeOutputNamePart(entry.topic)}_${runDate}.md`;
}

export function isSameSubjectOutput(entry, fileName) {
  const name = String(fileName || "");
  if (entry.kind === "conference") {
    const match = CONFERENCE_FILE_PATTERN.exec(name);
    return Boolean(match) && conferenceSeriesKey(match[1]) === conferenceSeriesKey(entry.series);
  }
  return DATE_SUFFIX.test(name) && name.replace(DATE_SUFFIX, "") === safeOutputNamePart(entry.topic);
}

export function listConferenceResults(resultDir = BACKGROUND_RESULT_DIR) {
  if (!fs.existsSync(resultDir)) return [];
  return fs.readdirSync(resultDir)
    .map((file) => ({ file, match: CONFERENCE_FILE_PATTERN.exec(file) }))
    .filter(({ match }) => match)
    .map(({ file, match }) => ({ file, series: match[1].replace(/_/gu, " "), year: match[2], date: match[3] }))
    .sort((a, b) => a.series.localeCompare(b.series, "en", { sensitivity: "base" }) || a.year.localeCompare(b.year));
}

export function newerConferenceEdition(entry, resultDir = BACKGROUND_RESULT_DIR) {
  if (entry.kind !== "conference") return "";
  const newer = listConferenceResults(resultDir)
    .find((row) => conferenceSeriesKey(row.series) === conferenceSeriesKey(entry.series) && Number(row.year) > Number(entry.year));
  return newer?.file || "";
}

export function createBackgroundQueueItem({
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
  planRoot = BACKGROUND_PLAN_ROOT,
  resultDir = BACKGROUND_RESULT_DIR,
} = {}) {
  const entry = resolveBackgroundSubject(subject, planRoot);
  if (!entry) {
    throw new Error(`background subject must be a topic under 基本面/产业背景/研究方案/ or "<会议系列> <年份>": ${subject || ""}`);
  }
  const newer = newerConferenceEdition(entry, resultDir);
  if (newer) throw new Error(`结果中已有该会议系列更新的一届，不能用旧届替换：${newer}`);

  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `background-${safeIdPart(entry.subject)}-${safeIdPart(nowIso)}`,
    domain: "background",
    sourceDate,
    subject: entry.subject,
    displayName: displayName || entry.displayName,
    category: category || entry.category,
    status,
    attempts,
    outputFile: normalizeProjectPath(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    backgroundKind: entry.kind,
    backgroundTopic: entry.topic,
    ...(entry.kind === "conference" ? { conferenceSeries: entry.series, conferenceYear: entry.year } : {}),
    ...extra,
  };
}

export function backupBackgroundOutputs(item, outputContract = {}, {
  rootDir = PROJECT_ROOT,
  resultDir = BACKGROUND_RESULT_DIR,
  backupDir = BACKGROUND_BACKUP_DIR,
} = {}) {
  const entry = backgroundEntryForItem(item);
  const newer = newerConferenceEdition(entry, resultDir);
  if (newer) throw new Error(`结果中已有该会议系列更新的一届，不能用旧届替换：${newer}`);
  return backupExistingOutputs({
    rootDir,
    outputDir: resultDir,
    backupRootDir: backupDir,
    backupKey: backupKeyFor(entry),
    expectedFileName: path.posix.basename(outputContract.expectedOutputFile || ""),
    matchFileName: (fileName) => isSameSubjectOutput(entry, fileName),
  });
}

export function rollbackBackgroundRun(item, prepareResult = {}, outputContract = {}, {
  rootDir = PROJECT_ROOT,
  resultDir = BACKGROUND_RESULT_DIR,
  backupDir = BACKGROUND_BACKUP_DIR,
} = {}) {
  const entry = backgroundEntryForItem(item);
  return rollbackPreparedOutputs({
    rootDir,
    outputDir: resultDir,
    backupRootDir: backupDir,
    expectedFileName: path.posix.basename(outputContract.expectedOutputFile || ""),
    prepareResult,
    newFileNameMatcher: (fileName) => isSameSubjectOutput(entry, fileName),
  });
}

function backupKeyFor(entry) {
  return entry.kind === "conference"
    ? `${CONFERENCE_TOPIC}_${safeOutputNamePart(entry.series)}`
    : safeOutputNamePart(entry.topic);
}
