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
  additionalOutputDirs = [],
  backupRootDir = "",
  backupKey,
  expectedFileName = "",
  matchFileName = () => false,
} = {}) {
  if (!outputDir) return { backupDir: "", files: [] };
  const resolvedBackupRootDir = resolveBackupRoot(outputDir, backupRootDir);
  const outputDirs = [outputDir, ...additionalOutputDirs];
  const matchingFiles = [];
  for (const directory of outputDirs) {
    resolveBackupRoot(directory, resolvedBackupRootDir);
    fs.mkdirSync(directory, { recursive: true });
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      if (entry.isFile() && (entry.name === expectedFileName || matchFileName(entry.name))) {
        matchingFiles.push(path.join(directory, entry.name));
      }
    }
  }

  if (!matchingFiles.length) return { backupDir: "", files: [] };

  const backupDir = path.join(resolvedBackupRootDir, `${safeIdPart(backupKey || "output")}_${safeIdPart(formatLocalIso(new Date()))}`);
  fs.mkdirSync(backupDir, { recursive: true });

  const files = [];
  try {
    for (const sourcePath of matchingFiles) {
      const fileName = path.basename(sourcePath);
      const targetPath = uniqueBackupPath(path.join(backupDir, fileName));
      fs.renameSync(sourcePath, targetPath);
      files.push({
        from: normalizeProjectPath(path.relative(rootDir, sourcePath)),
        to: normalizeProjectPath(path.relative(rootDir, targetPath)),
      });
    }
  } catch (error) {
    const restoreErrors = [];
    for (const file of [...files].reverse()) {
      try {
        fs.renameSync(path.join(rootDir, file.to), path.join(rootDir, file.from));
      } catch (restoreError) {
        restoreErrors.push(restoreError);
      }
    }
    removeEmptyDirectoriesUpTo(backupDir, resolvedBackupRootDir);
    if (restoreErrors.length) throw new AggregateError([error, ...restoreErrors], `Backup restore failed; retained files in ${backupDir}`);
    throw error;
  }

  return {
    backupDir: normalizeProjectPath(path.relative(rootDir, backupDir)),
    files,
  };
}

export function rollbackPreparedOutputs({
  rootDir = PROJECT_ROOT,
  outputDir,
  additionalOutputDirs = [],
  backupRootDir = "",
  expectedFileName = "",
  newFileNameMatcher = () => false,
  prepareResult = {},
} = {}) {
  const removed = [];
  const restored = [];
  const resolvedBackupRootDir = outputDir ? resolveBackupRoot(outputDir, backupRootDir) : "";

  for (const directory of [outputDir, ...additionalOutputDirs].filter(Boolean)) {
    if (!fs.existsSync(directory)) continue;
    const newFiles = fs.readdirSync(directory, { withFileTypes: true })
      .filter((entry) => entry.isFile())
      .map((entry) => entry.name)
      .filter((fileName) => fileName === expectedFileName || newFileNameMatcher(fileName));

    for (const fileName of newFiles) {
      const possibleNewOutput = path.join(directory, fileName);
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
    removeEmptyDirectoriesUpTo(backupDir, resolvedBackupRootDir);
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
  while (isWithin(stop, current)) {
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

function resolveBackupRoot(outputDir, backupRootDir) {
  const backup = path.resolve(backupRootDir || path.join(path.dirname(outputDir), "备份"));
  if (isWithin(outputDir, backup) || isWithin(backup, outputDir)) {
    throw new Error("Backup directory must be separate from the formal output directory");
  }
  return backup;
}

function isWithin(parent, child) {
  const relative = path.relative(path.resolve(parent), path.resolve(child));
  return relative === "" || (!path.isAbsolute(relative) && relative !== ".." && !relative.startsWith(`..${path.sep}`));
}
