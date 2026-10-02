import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  backupExistingFeatureQuantizationOutputs,
  expectedFeatureQuantizationOutputStem,
  parseFeatureQuantizationPlanEntries,
  rollbackFeatureQuantizationFormalRun,
  validateFeaturePlanSourceBoundary,
} from "../domains/feature-quantization.mjs";

test("same feature plan ID cannot exist under two names", () => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-plans-"));
  try {
    fs.writeFileSync(path.join(fixture, "N01_Old_研究方案.md"), featurePlanWithSourceBoundary("N01 Old"), "utf8");
    fs.writeFileSync(path.join(fixture, "N01_New_研究方案.md"), featurePlanWithSourceBoundary("N01 New"), "utf8");
    assert.throws(() => parseFeatureQuantizationPlanEntries(fixture), /Duplicate feature plan ID N01/);
  } finally {
    fs.rmSync(fixture, { recursive: true, force: true });
  }
});

test("feature plans must carry the complete local evidence allowlist and explicit prohibitions", () => {
  assert.doesNotThrow(() => validateFeaturePlanSourceBoundary(featurePlanWithSourceBoundary("N01 Good"), "good.md"));
  assert.throws(
    () => validateFeaturePlanSourceBoundary(
      featurePlanWithSourceBoundary("N01 Bad").replace("`基本面/行业调研/`", "`基本面/行业资料/`"),
      "bad.md",
    ),
    /missing allowed source path/,
  );
  assert.throws(
    () => validateFeaturePlanSourceBoundary(
      featurePlanWithSourceBoundary("N01 Bad").replace("禁止联网", "可以联网"),
      "bad-network.md",
    ),
    /must explicitly forbid network research/,
  );
});

test("quantization rollback removes only this run file and restores its prior version without touching history", () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-rollback-"));
  const outputDir = path.join(fixtureRoot, "scores");
  fs.mkdirSync(outputDir, { recursive: true });
  const item = { subject: "N01_AI可归因盈利暴露_研究方案" };
  const stem = expectedFeatureQuantizationOutputStem(item.subject);
  const expectedFileName = `${stem}_2026-07-12.md`;
  const historicalFileName = `${stem}_2026-06-04.md`;
  const expectedPath = path.join(outputDir, expectedFileName);
  const historicalPath = path.join(outputDir, historicalFileName);
  fs.writeFileSync(expectedPath, "prior expected\n", "utf8");
  fs.writeFileSync(historicalPath, "historical snapshot\n", "utf8");
  const outputContract = { expectedOutputFile: `基本面/特征量化/量化评分/${expectedFileName}` };
  try {
    const prepared = backupExistingFeatureQuantizationOutputs(item, outputContract, { rootDir: fixtureRoot, outputDir });
    assert.equal(fs.existsSync(expectedPath), false);
    assert.equal(fs.readFileSync(historicalPath, "utf8"), "historical snapshot\n");
    fs.writeFileSync(expectedPath, "failed new output\n", "utf8");

    const result = rollbackFeatureQuantizationFormalRun(item, prepared, outputContract, { rootDir: fixtureRoot, outputDir });
    assert.deepEqual(result.removed, ["scores/" + expectedFileName]);
    assert.equal(fs.readFileSync(expectedPath, "utf8"), "prior expected\n");
    assert.equal(fs.readFileSync(historicalPath, "utf8"), "historical snapshot\n");
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

function featurePlanWithSourceBoundary(title) {
  return `# ${title}

## 资料读取边界

除本方案文件本身外，研究证据只允许读取 \`基本面/公司调研/\`、\`基本面/行业调研/\` 和 \`金融资料/每日金融数据/\`。上述目录之外的 Investment 目录与文件一律禁止读取；禁止联网搜索或补充外部资料。
`;
}
