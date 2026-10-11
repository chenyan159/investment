import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { findPreviousReports } from "../../../分析报告/公司对比/生成站点数据.mjs";

test("comparison history uses the external backup root and file times, not migration directory times", async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "comparison-history-"));
  try {
    const backup = path.join(root, "备份");
    for (const [folder, date, reportTime, directoryTime] of [
      ["old", "2026-09-01", "2026-09-01", "2026-10-11"],
      ["new", "2026-10-01", "2026-10-01", "2026-10-10"],
    ]) {
      const dir = path.join(backup, folder);
      await fs.mkdir(dir, { recursive: true });
      const file = path.join(dir, `TEST_逐家公司投资思路对比_${date}.md`);
      await fs.writeFile(file, "report");
      await fs.utimes(file, new Date(reportTime), new Date(reportTime));
      await fs.utimes(dir, new Date(directoryTime), new Date(directoryTime));
    }
    const reports = await findPreviousReports(new Set(["TEST"]), backup);
    assert.equal(reports.length, 1);
    assert.equal(reports[0].reportDate, "2026-10-01");
    assert.deepEqual(await findPreviousReports(new Set(["TEST"]), path.join(root, "missing")), []);
  } finally {
    await fs.rm(root, { recursive: true, force: true });
  }
});
