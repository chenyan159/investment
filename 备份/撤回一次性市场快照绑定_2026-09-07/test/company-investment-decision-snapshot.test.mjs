import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  prepareCompanyInvestmentDecisionFormalRun,
  resolveCompanyInvestmentDecisionMarketSnapshot,
} from "../domains/company-investment-decision.mjs";
import { buildCompanyInvestmentDecisionFormalPrompt } from "../prompts/company-investment-decision.mjs";

const PRODUCTION_SUBJECTS = Object.freeze([
  "TEL", "CMI", "AVGO", "AMKR", "CARR", "HPE", "NVDA", "TSM",
  "META", "EME", "POWL", "MKSI", "NVT", "MU", "ALAB", "CRDO",
  "LITE", "ANET", "GEV", "BE", "STX", "WDC", "NBIS", "CRWV",
]);

test("production decision batch pins all 24 subjects to the same shared market snapshot", () => {
  const snapshots = PRODUCTION_SUBJECTS.map((subject) => (
    resolveCompanyInvestmentDecisionMarketSnapshot({ subject, sourceDate: "2026-08-19" })
  ));
  const first = snapshots[0];
  assert.equal(first.batchId, "cid-us-2026-08-19-24");
  assert.equal(first.snapshotFile, "金融资料/市场状态/美国股票市场状态快照_2026-08-19.md");
  assert.equal(first.sha256, "5F4AD0D0CC460D63450B7A192390E99836CABCC284916A7499A547503EE77663");
  for (const snapshot of snapshots.slice(1)) assert.strictEqual(snapshot, first);
});

test("decision prompt injects one authoritative snapshot block and disables batch fallback", () => {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), "decision-prompt-test-"));
  const promptPath = path.join(fixtureRoot, "plan.md");
  fs.writeFileSync(promptPath, "# plan for 【公司股票代号】\n", "utf8");
  try {
    const snapshot = {
      batchId: "test-batch",
      sourceDate: "2026-08-19",
      marketScope: "test market scope",
      snapshotFile: "金融资料/市场状态/测试市场状态快照_2026-08-19.md",
      sha256: "A".repeat(64),
      content: "UNIQUE-SNAPSHOT-BODY",
    };
    const prompt = buildCompanyInvestmentDecisionFormalPrompt(
      { subject: "TEL" },
      { promptPath, placeholder: "【公司股票代号】" },
      { expectedOutputFile: "分析报告/公司情景投资决策/结果/TEL_test.md" },
      snapshot,
    );
    assert.match(prompt, /# plan for TEL/u);
    assert.equal(prompt.split(snapshot.snapshotFile).length - 1, 1);
    assert.equal(prompt.split(snapshot.sha256).length - 1, 1);
    assert.equal(prompt.split(snapshot.content).length - 1, 1);
    assert.match(prompt, /不得联网重建、重新分类/u);
    assert.match(prompt, /降级规则不适用于本次任务/u);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test("snapshot resolver accepts a valid isolated manifest", () => {
  const fixture = createFixture();
  try {
    const snapshot = resolveCompanyInvestmentDecisionMarketSnapshot(
      { subject: "TEL", sourceDate: "2026-08-19" },
      { projectRoot: fixture.root, batchesPath: fixture.manifestPath, useCache: false },
    );
    assert.equal(snapshot.batchId, "fixture-batch");
    assert.equal(snapshot.snapshotFile, fixture.snapshotFile);
    assert.equal(snapshot.sha256, fixture.sha256);
    assert.equal(snapshot.content, fixture.content);
  } finally {
    fixture.cleanup();
  }
});

test("snapshot resolver rejects missing, stale, modified, malformed, and multiply-bound inputs", async (t) => {
  await t.test("missing snapshot", () => {
    const fixture = createFixture({ writeSnapshot: false });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /shared market snapshot does not exist/u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("stale filename date", () => {
    const fixture = createFixture({ snapshotFile: "金融资料/市场状态/测试市场状态快照_2026-08-18.md" });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /filename date must equal batch sourceDate 2026-08-19/u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("SHA mismatch", () => {
    const fixture = createFixture({ manifestSha256: "0".repeat(64) });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /SHA-256 mismatch/u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("path outside formal market-state root", () => {
    const fixture = createFixture({ snapshotFile: "金融资料/每日金融数据/测试市场状态快照_2026-08-19.md" });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /must be under 金融资料\/市场状态\//u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("required marker missing", () => {
    const fixture = createFixture({ content: validSnapshotContent().replace("盈利预期修正", "") });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /missing required marker 盈利预期修正/u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("duplicate subject and date binding", () => {
    const fixture = createFixture({ duplicateBinding: true });
    try {
      assert.throws(
        () => resolveFixture(fixture),
        /duplicates the TEL\/2026-08-19 shared market snapshot binding/u,
      );
    } finally {
      fixture.cleanup();
    }
  });

  await t.test("unbound or expired sourceDate", () => {
    const fixture = createFixture();
    try {
      assert.throws(
        () => resolveFixture(fixture, { subject: "TEL", sourceDate: "2026-08-20" }),
        /is not bound to a shared market snapshot batch/u,
      );
    } finally {
      fixture.cleanup();
    }
  });
});

test("formal preparation validates the snapshot before touching existing outputs", () => {
  let backupCalls = 0;
  assert.throws(
    () => prepareCompanyInvestmentDecisionFormalRun(
      { subject: "TEL", sourceDate: "2026-08-19" },
      { expectedOutputFile: "unused.md" },
      {
        resolveMarketSnapshot() {
          throw new Error("snapshot preflight failed");
        },
        backupOutputs() {
          backupCalls += 1;
          return {};
        },
      },
    ),
    /snapshot preflight failed/u,
  );
  assert.equal(backupCalls, 0);
});

function resolveFixture(fixture, item = { subject: "TEL", sourceDate: "2026-08-19" }) {
  return resolveCompanyInvestmentDecisionMarketSnapshot(item, {
    projectRoot: fixture.root,
    batchesPath: fixture.manifestPath,
    useCache: false,
  });
}

function createFixture({
  snapshotFile = "金融资料/市场状态/测试市场状态快照_2026-08-19.md",
  content = validSnapshotContent(),
  manifestSha256 = "",
  writeSnapshot = true,
  duplicateBinding = false,
} = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "decision-snapshot-test-"));
  const snapshotPath = path.join(root, ...snapshotFile.split("/"));
  if (writeSnapshot) {
    fs.mkdirSync(path.dirname(snapshotPath), { recursive: true });
    fs.writeFileSync(snapshotPath, content, "utf8");
  }
  const bytes = Buffer.from(content, "utf8");
  const sha256 = createHash("sha256").update(bytes).digest("hex").toUpperCase();
  const batch = {
    batchId: "fixture-batch",
    sourceDate: "2026-08-19",
    marketScope: "fixture market",
    subjects: ["TEL", "META"],
    snapshotFile,
    sha256: manifestSha256 || sha256,
  };
  const batches = duplicateBinding
    ? [batch, { ...batch, batchId: "duplicate-fixture-batch", subjects: ["TEL"] }]
    : [batch];
  const manifestPath = path.join(root, "company-investment-decision.batches.json");
  fs.writeFileSync(manifestPath, `${JSON.stringify({ schemaVersion: 1, batches }, null, 2)}\n`, "utf8");
  return {
    root,
    manifestPath,
    snapshotFile,
    content,
    sha256,
    cleanup() {
      fs.rmSync(root, { recursive: true, force: true });
    },
  };
}

function validSnapshotContent() {
  return `# 测试市场状态快照（2026-08-19）

## 快照身份与使用边界

主状态；唯一相邻状态；总体证据强度。

## 五块市场记分板

宽度与参与；信用与融资；波动率与市场功能；利率与折现率；盈利预期修正。
`;
}
