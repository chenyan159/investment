import { bindResearchPlan, planForItem } from "../research-plan-store.mjs";
import fs from "node:fs";
import path from "node:path";
import { buildFileRunFormalPrompt } from "../prompts/file-run.mjs";
import {
  formatLocalDate,
  formatLocalIso,
  normalizeProjectPath,
  PROJECT_ROOT,
  safeIdPart,
} from "../queue-store.mjs";

export const fileRunDomain = {
  domain: "file-run",
  label: "文件运行",
  subjectHelp: "run id",
  requiresIndexedSubject: false,
  promptPath: PROJECT_ROOT,
  indexPath: PROJECT_ROOT,
  placeholder: "",
  outputPrefix: "",
  outputFilePattern: /^.+$/u,
  allowedCategories: new Set(),
  requiredPaths: [],
  allowNonFormalOutputDirs: true,
  checkRequired() {},
  expectedOutputFile(item) {
    return normalizeExpectedOutputFile(item.expectedOutputFile);
  },
  expectedOutputDir(item) {
    return normalizeExpectedOutputDir(item.expectedOutputDir);
  },
  buildFormalPrompt(item, outputContract) {
    return buildFileRunFormalPrompt(item, fileRunDomain, outputContract);
  },
  resolvePromptFilePath,
  parseIndexEntries() {
    return [];
  },
  resolveIndexEntry(subject) {
    const runId = normalizeRunId(subject);
    return runId ? { subject: runId, displayName: runId, category: "file-run" } : null;
  },
  createQueueItem(options) {
    return createFileRunQueueItem(options);
  },
  validateQueueItem(item, options = {}) {
    validateFileRunQueueItem(item, options);
  },
  validateOutputFileForItem({ item, outputFile }) {
    validateFileRunQueueItem(item, { checkPromptFileExists: false });
    const expectedFile = normalizeExpectedOutputFile(item.expectedOutputFile);
    if (expectedFile && outputFile !== expectedFile) {
      throw new Error(`file-run outputFile must equal expectedOutputFile ${expectedFile}: ${outputFile}`);
    }
    const expectedDir = normalizeExpectedOutputDir(item.expectedOutputDir);
    if (!pathIsInsideProjectDir(outputFile, expectedDir)) {
      throw new Error(`file-run outputFile must be inside expectedOutputDir ${expectedDir}: ${outputFile}`);
    }
  },
};

export function createFileRunQueueItem({
  runId = "",
  promptFile = "",
  expectedOutputDir = "",
  expectedOutputFile = "",
  subject = "",
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
  const normalizedRunId = normalizeRunId(runId || subject);
  if (!normalizedRunId) throw new Error("file-run queue item requires --run-id");
  if (!promptFile) throw new Error("file-run queue item requires --prompt-file");

  const normalizedPromptFile = normalizeProjectFile(promptFile, "promptFile");
  const plan = planForItem({ domain: "file-run", promptFile: normalizedPromptFile });
  const normalizedExpectedFile = normalizeExpectedOutputFile(expectedOutputFile);
  const defaultOutputDir = plan?.defaultOutputDir || normalizeProjectPath(path.posix.dirname(normalizedPromptFile)) || ".";
  const normalizedExpectedDir = normalizeExpectedOutputDir(
    expectedOutputDir || (normalizedExpectedFile ? path.posix.dirname(normalizedExpectedFile) : defaultOutputDir),
  );
  if (normalizedExpectedFile && !pathIsInsideProjectDir(normalizedExpectedFile, normalizedExpectedDir)) {
    throw new Error(`file-run expectedOutputFile must be inside expectedOutputDir ${normalizedExpectedDir}: ${normalizedExpectedFile}`);
  }

  const nowIso = formatLocalIso(new Date());
  const item = {
    id: id || `file-run-${safeIdPart(normalizedRunId)}-${safeIdPart(nowIso)}`,
    domain: "file-run",
    sourceDate,
    subject: normalizedRunId,
    displayName: displayName || normalizedRunId,
    category: category || "file-run",
    status,
    attempts,
    outputFile: normalizeProjectPath(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    runId: normalizedRunId,
    promptFile: normalizedPromptFile,
    expectedOutputDir: normalizedExpectedDir,
    expectedOutputFile: normalizedExpectedFile,
    ...extra,
  };
  bindResearchPlan(item);
  validateFileRunQueueItem(item);
  return item;
}

export function resolvePromptFilePath(promptFile) {
  return projectPathToAbsolute(normalizeProjectFile(promptFile, "promptFile"));
}

export function normalizeExpectedOutputDir(expectedOutputDir) {
  const raw = String(expectedOutputDir || "").trim();
  if (!raw) return "";
  return normalizeProjectEntry(raw, "expectedOutputDir", { directory: true });
}

export function normalizeExpectedOutputFile(expectedOutputFile) {
  const raw = String(expectedOutputFile || "").trim();
  if (!raw) return "";
  return normalizeProjectFile(raw, "expectedOutputFile");
}

export function validateFileRunQueueItem(item, { checkPromptFileExists = true } = {}) {
  const runId = normalizeRunId(item.runId || item.subject);
  if (!runId) throw new Error("file-run item is missing runId");
  if (!item.promptFile) throw new Error(`file-run ${runId} is missing promptFile`);
  if (!item.expectedOutputDir) throw new Error(`file-run ${runId} is missing expectedOutputDir`);

  const checked = bindResearchPlan({ ...item });
  const promptPath = resolvePromptFilePath(checked.promptFile);
  if (checkPromptFileExists && !fs.existsSync(promptPath)) {
    throw new Error(`file-run ${runId} promptFile does not exist: ${item.promptFile}`);
  }
  if (checkPromptFileExists && !fs.statSync(promptPath).isFile()) {
    throw new Error(`file-run ${runId} promptFile is not a file: ${item.promptFile}`);
  }

  const expectedDir = normalizeExpectedOutputDir(item.expectedOutputDir);
  const expectedFile = normalizeExpectedOutputFile(item.expectedOutputFile);
  const plan = planForItem(checked);
  if (plan?.outputRoot && expectedDir !== plan.outputRoot && !pathIsInsideProjectDir(expectedDir, plan.outputRoot)) {
    throw new Error(`file-run ${runId} expectedOutputDir must be inside research plan outputRoot ${plan.outputRoot}: ${expectedDir}`);
  }
  if (expectedFile && !pathIsInsideProjectDir(expectedFile, expectedDir)) {
    throw new Error(`file-run expectedOutputFile must be inside expectedOutputDir ${expectedDir}: ${expectedFile}`);
  }
}

function normalizeProjectFile(value, label) {
  const normalized = normalizeProjectEntry(value, label);
  if (!normalized || normalized === ".") throw new Error(`file-run ${label} must be a file path`);
  return normalized;
}

function normalizeProjectEntry(value, label, { directory = false } = {}) {
  const raw = String(value || "").trim();
  const nativePath = raw.replace(/\//g, path.sep);
  const absolute = path.isAbsolute(nativePath)
    ? path.resolve(nativePath)
    : path.resolve(PROJECT_ROOT, nativePath);
  const relative = path.relative(PROJECT_ROOT, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`file-run ${label} must be inside project root ${PROJECT_ROOT}: ${value}`);
  }
  const normalized = normalizeProjectPath(relative) || ".";
  return directory ? normalized.replace(/\/+$/u, "") || "." : normalized;
}

function projectPathToAbsolute(projectPath) {
  if (projectPath === ".") return PROJECT_ROOT;
  return path.join(PROJECT_ROOT, ...projectPath.split("/"));
}

function pathIsInsideProjectDir(filePath, directoryPath) {
  const file = normalizeProjectPath(filePath);
  const directory = normalizeProjectPath(directoryPath).replace(/\/+$/u, "") || ".";
  return directory === "." ? !file.startsWith("../") : file.startsWith(`${directory}/`);
}

function normalizeRunId(value) {
  return String(value || "").trim();
}
