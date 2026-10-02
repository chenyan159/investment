import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "../domains/output-backup.mjs";

test("integrated company-decision backup keeps formal results and backups as sibling directories", () => {
  const rootDir = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-backup-"));
  const outputDir = path.join(rootDir, "公司情景投资决策", "结果");
  const backupRootDir = path.join(rootDir, "公司情景投资决策", "备份");
  const fileName = "TEST_经营情景市场状态投资决策_2026-07-16.md";
  const outputFile = path.join(outputDir, fileName);

  try {
    fs.mkdirSync(outputDir, { recursive: true });
    fs.writeFileSync(outputFile, "old", "utf8");

    const prepared = backupExistingOutputs({
      rootDir,
      outputDir,
      backupRootDir,
      backupKey: "TEST",
      expectedFileName: fileName,
    });

    assert.equal(fs.existsSync(outputFile), false);
    assert.match(prepared.backupDir, /^公司情景投资决策\/备份\/TEST_/u);
    assert.equal(fs.existsSync(path.join(rootDir, ...prepared.files[0].to.split("/"))), true);

    fs.writeFileSync(outputFile, "new", "utf8");
    rollbackPreparedOutputs({
      rootDir,
      outputDir,
      backupRootDir,
      expectedFileName: fileName,
      prepareResult: prepared,
    });

    assert.equal(fs.readFileSync(outputFile, "utf8"), "old");
    assert.equal(fs.existsSync(path.join(outputDir, "备份")), false);
  } finally {
    fs.rmSync(rootDir, { recursive: true, force: true });
  }
});
