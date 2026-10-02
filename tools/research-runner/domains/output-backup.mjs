import fs from "node:fs";
import path from "node:path";
import {
  formatLocalIso,
  normalizeProjectPath,
  PROJECT_ROOT,
  safeIdPart,
} from "../queue-store.mjs";

export function backupExistingOutputs({
  rootDir = PROJECT_ROOT,
  outputDir,
  backupRootDir = "",
  backupKey,
  expectedFileName = "",
  matchFileName = () => false,
} = {}) {
  if (!outputDir) return { backupDir: "", files: [] };
  fs.mkdirSync(outputDir, { recursive: true });

  const matchingFiles = fs.readdirSync(outputDir, { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .filter((fileName) => fileName === expectedFileName || matchFileName(fileName));

  if (!matchingFiles.length) return { backupDir: "", files: [] };

  const resolvedBackupRootDir = backupRootDir || path.join(outputDir, "备份");
  const backupDir = path.join(resolvedBackupRootDir, `${safeIdPart(backupKey || "output")}_${safeIdPart(formatLocalIso(new Date()))}`);
  fs.mkdirSync(backupDir, { recursive: true });

  const files = [];
  for (const fileName of matchingFiles) {
    const sourcePath = path.join(outputDir, fileName);
    const targetPath = uniqueBackupPath(path.join(backupDir, fileName));
    fs.renameSync(sourcePath, targetPath);
    files.push({
      from: normalizeProjectPath(path.relative(rootDir, sourcePath)),
      to: normalizeProjectPath(path.relative(rootDir, targetPath)),
    });
  }

  return {
    backupDir: normalizeProjectPath(path.relative(rootDir, backupDir)),
    files,
  };
}

export function rollbackPreparedOutputs({
  rootDir = PROJECT_ROOT,
  outputDir,
  backupRootDir = "",
  expectedFileName = "",
  newFileNameMatcher = () => false,
  prepareResult = {},
} = {}) {
  const removed = [];
  const restored = [];

  if (outputDir && fs.existsSync(outputDir)) {
    const newFiles = fs.readdirSync(outputDir, { withFileTypes: true })
      .filter((entry) => entry.isFile())
      .map((entry) => entry.name)
      .filter((fileName) => fileName === expectedFileName || newFileNameMatcher(fileName));

    for (const fileName of newFiles) {
      const possibleNewOutput = path.join(outputDir, fileName);
      fs.rmSync(possibleNewOutput, { force: true });
      removed.push(normalizeProjectPath(path.relative(rootDir, possibleNewOutput)));
    }
  }

  const files = Array.isArray(prepareResult?.files) ? [...prepareResult.files].reverse() : [];
  for (const file of files) {
    const backupPath = path.join(rootDir, ...normalizeProjectPath(file.to).split("/"));
    const restorePath = path.join(rootDir, ...normalizeProjectPath(file.from).split("/"));
    if (!fs.existsSync(backupPath)) continue;
    if (fs.existsSync(restorePath)) {
      throw new Error(`Cannot restore backup because target already exists: ${file.from}`);
    }
    fs.mkdirSync(path.dirname(restorePath), { recursive: true });
    fs.renameSync(backupPath, restorePath);
    restored.push({ from: file.to, to: file.from });
  }

  if (prepareResult?.backupDir && outputDir) {
    const backupDir = path.join(rootDir, ...normalizeProjectPath(prepareResult.backupDir).split("/"));
    removeEmptyDirectoriesUpTo(backupDir, backupRootDir || path.join(outputDir, "备份"));
  }

  return { removed, files: restored };
}

function uniqueBackupPath(targetPath) {
  if (!fs.existsSync(targetPath)) return targetPath;
  const parsed = path.parse(targetPath);
  for (let index = 2; index < 1000; index += 1) {
    const candidate = path.join(parsed.dir, `${parsed.name}_${index}${parsed.ext}`);
    if (!fs.existsSync(candidate)) return candidate;
  }
  throw new Error(`Could not create unique backup path for: ${targetPath}`);
}

function removeEmptyDirectoriesUpTo(startDir, stopDir) {
  let current = startDir;
  const stop = path.resolve(stopDir);
  while (path.resolve(current).startsWith(stop)) {
    if (!fs.existsSync(current)) return;
    try {
      fs.rmdirSync(current);
    } catch {
      return;
    }
    if (path.resolve(current) === stop) return;
    current = path.dirname(current);
  }
}
