import fs from "node:fs";
import path from "node:path";
import {
  formatLocalDate,
  normalizeProjectPath,
  projectRelativeToAbsolute,
  PROJECT_ROOT,
} from "../queue-store.mjs";

const MTIME_TOLERANCE_MS = 10_000;

export class LocalOutputValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "LocalOutputValidationError";
    this.localOutputValidation = true;
  }
}

export function companionOutputFile(domain, outputFile) {
  if (!domain.companionExtension) return "";
  const fileName = path.posix.basename(outputFile).replace(/\.md$/u, domain.companionExtension);
  return domain.companionOutputPrefix
    ? `${domain.companionOutputPrefix}${fileName}`
    : outputFile.replace(/\.md$/u, domain.companionExtension);
}

export function createOutputContract(item, domain) {
  const runDate = runDateFromItem(item);
  const expectedOutputFile = normalizeProjectPath(domain.expectedOutputFile?.(item, runDate));
  const expectedOutputDir = normalizeProjectPath(
    expectedOutputFile ? path.posix.dirname(expectedOutputFile) : domain.expectedOutputDir?.(item),
  ).replace(/\/+$/u, "");

  if (!expectedOutputFile && !expectedOutputDir) {
    throw new Error(`Domain ${domain.domain} did not provide an output file or directory.`);
  }
  if (expectedOutputFile) {
    validateOutputFilePath({ item, domain, outputFile: expectedOutputFile });
  }
  const expectedCompanionFile = companionOutputFile(domain, expectedOutputFile);
  if (expectedCompanionFile) {
    validateOutputFilePath({ item, domain, outputFile: expectedCompanionFile, companion: true });
  }

  return {
    projectRoot: PROJECT_ROOT,
    runDate,
    expectedOutputFile,
    expectedCompanionFile,
    expectedOutputDir: expectedOutputDir || ".",
  };
}

export function captureOutputSnapshot(outputContract, item) {
  const excluded = new Set([normalizeProjectPath(item.promptFile)].filter(Boolean));
  return snapshotDirectory(outputContract.expectedOutputDir, excluded);
}

export function validateLocalOutput(item, domain, outputContract, beforeSnapshot = null) {
  if (outputContract.expectedOutputFile) {
    if (outputContract.expectedCompanionFile) {
      validateOutputFile(item, domain, outputContract.expectedCompanionFile, true);
    } else {
      recoverExpectedOutputPath(item, domain, outputContract, beforeSnapshot);
    }
    return validateOutputFile(item, domain, outputContract.expectedOutputFile);
  }

  const excluded = new Set([normalizeProjectPath(item.promptFile)].filter(Boolean));
  const afterSnapshot = snapshotDirectory(outputContract.expectedOutputDir, excluded);
  const candidates = changedFiles(beforeSnapshot, afterSnapshot);
  if (candidates.length !== 1) {
    throw new LocalOutputValidationError(
      `file-run expected exactly one new or modified output in ${outputContract.expectedOutputDir}; found ${candidates.length}${candidates.length ? `: ${candidates.join(", ")}` : ""}`,
    );
  }
  return validateOutputFile(item, domain, candidates[0]);
}

function recoverExpectedOutputPath(item, domain, outputContract, beforeSnapshot) {
  const expectedAbsolute = outputFileToAbsolute(outputContract.expectedOutputFile);
  if (fs.existsSync(expectedAbsolute) || domain.domain === "file-run" || !(beforeSnapshot instanceof Map)) return;

  const afterSnapshot = snapshotDirectory(outputContract.expectedOutputDir, new Set());
  const candidates = changedFiles(beforeSnapshot, afterSnapshot).filter((candidate) => {
    try {
      validateOutputFilePath({ item, domain, outputFile: candidate });
      return true;
    } catch {
      return false;
    }
  });
  if (candidates.length !== 1) return;

  const candidate = candidates[0];
  fs.mkdirSync(path.dirname(expectedAbsolute), { recursive: true });
  fs.renameSync(outputFileToAbsolute(candidate), expectedAbsolute);
  outputContract.recoveredFrom = candidate;
}

function changedFiles(beforeSnapshot, afterSnapshot) {
  const changed = [];
  for (const [filePath, current] of afterSnapshot.entries()) {
    const previous = beforeSnapshot?.get(filePath);
    if (!previous || previous.size !== current.size || previous.mtimeMs !== current.mtimeMs) changed.push(filePath);
  }
  return changed;
}

function validateOutputFile(item, domain, outputFile, companion = false) {
  try {
    validateOutputFilePath({ item, domain, outputFile, companion });
    const absolutePath = outputFileToAbsolute(outputFile);
    if (!fs.existsSync(absolutePath)) throw new Error(`outputFile does not exist: ${outputFile}`);
    const stat = fs.statSync(absolutePath);
    if (!stat.isFile()) throw new Error(`outputFile is not a regular file: ${outputFile}`);
    if (stat.size <= 0) throw new Error(`outputFile is empty: ${outputFile}`);

    const startedAt = parseLocalDateTime(item.startedAt);
    if (startedAt && stat.mtimeMs + MTIME_TOLERANCE_MS < startedAt.getTime()) {
      throw new Error(`outputFile was not modified during this run: ${outputFile}`);
    }
    return outputFile;
  } catch (error) {
    if (error?.localOutputValidation) throw error;
    throw new LocalOutputValidationError(error?.message || String(error));
  }
}

export function outputFileToAbsolute(outputFile) {
  return projectRelativeToAbsolute(outputFile);
}

export function validateOutputFilePath({ item = null, domain, outputFile, originalOutputFile = outputFile, allowBackup = false, companion = false }) {
  if (!outputFile) throw new Error("outputFile is empty");
  if (path.isAbsolute(String(originalOutputFile).replace(/\//g, path.sep))) {
    throw new Error(`outputFile must be relative to ${PROJECT_ROOT}: ${originalOutputFile}`);
  }
  const outputPrefix = companion ? (domain.companionOutputPrefix || domain.outputPrefix) : domain.outputPrefix;
  if (outputPrefix && !outputFile.startsWith(outputPrefix)) {
    throw new Error(`outputFile must start with ${outputPrefix}: ${outputFile}`);
  }
  if (/[\\]/u.test(originalOutputFile)) {
    throw new Error(`outputFile must use forward slashes: ${originalOutputFile}`);
  }
  const parts = outputFile.split("/");
  if (parts.some((part) => part === "" || part === "." || part === "..")) {
    throw new Error(`outputFile contains an invalid path segment: ${outputFile}`);
  }
  const isBackupPath = /(^|\/)备份(\/|$)/u.test(outputFile);
  if (!domain.allowNonFormalOutputDirs && (/(^|\/)(tmp|研究方法)(\/|$)/u.test(outputFile) || (!allowBackup && isBackupPath))) {
    throw new Error(`outputFile points to a non-formal directory: ${outputFile}`);
  }

  const fileName = parts.at(-1) || "";
  if (companion && (!domain.companionExtension || path.posix.extname(fileName) !== domain.companionExtension)) {
    throw new Error(`Invalid companion output: ${outputFile}`);
  }
  const primaryFileName = companion ? `${fileName.slice(0, -domain.companionExtension.length)}.md` : fileName;
  if (!domain.outputFilePattern.test(primaryFileName)) {
    throw new Error(`outputFile filename does not match ${domain.domain} naming rule: ${fileName}`);
  }
  if (typeof domain.validateOutputFileForItem === "function" && !isBackupPath) {
    domain.validateOutputFileForItem({ item, outputFile, originalOutputFile, fileName, parts });
  }

  if (domain.allowedCategories?.size) {
    const relative = outputFile.slice(domain.outputPrefix.length);
    const category = relative.split("/")[0] || "";
    if (!domain.allowedCategories.has(category)) {
      throw new Error(`outputFile is outside allowed ${domain.domain} categories: ${outputFile}`);
    }
  }
}

function snapshotDirectory(projectDirectory, excluded) {
  const result = new Map();
  const root = projectDirectory === "." ? PROJECT_ROOT : projectRelativeToAbsolute(projectDirectory);
  if (!fs.existsSync(root)) return result;
  walk(root);
  return result;

  function walk(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) {
        walk(absolute);
      } else if (entry.isFile()) {
        const relative = normalizeProjectPath(path.relative(PROJECT_ROOT, absolute));
        if (excluded.has(relative)) continue;
        const stat = fs.statSync(absolute);
        result.set(relative, { size: stat.size, mtimeMs: stat.mtimeMs });
      }
    }
  }
}

function runDateFromItem(item) {
  return formatLocalDate(parseLocalDateTime(item?.startedAt) || new Date());
}

function parseLocalDateTime(value) {
  if (!value) return null;
  const parsed = new Date(String(value).replace(" ", "T"));
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed;
}
