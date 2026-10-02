import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { buildModules, runIsolatedModule } from "./build-modules.mjs";

async function withTempDir(callback) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "project-ananta-modules-"));
  try {
    await callback(root);
  } finally {
    await fs.rm(root, { recursive: true, force: true });
  }
}

async function writeArtifact(root, payload) {
  await fs.mkdir(root, { recursive: true });
  await fs.writeFile(path.join(root, "current.json"), `${JSON.stringify(payload)}\n`, "utf8");
}

async function validateFixture(_id, root) {
  const payload = JSON.parse(await fs.readFile(path.join(root, "current.json"), "utf8"));
  if (!payload.valid) throw new Error("fixture artifact invalid");
  return {
    generatedAt: payload.generatedAt,
    dataDate: payload.dataDate,
  };
}

function fixtureModule(root) {
  return {
    id: "fixture",
    label: "测试模块",
    script: path.join(root, "unused.mjs"),
    outputRoot: path.join(root, "artifact"),
  };
}

test("successful module build atomically replaces the previous artifact", async () => {
  await withTempDir(async (root) => {
    const module = fixtureModule(root);
    await writeArtifact(module.outputRoot, {
      valid: true,
      generatedAt: "2026-07-22T00:00:00.000Z",
      dataDate: "2026-07-22",
    });

    const result = await runIsolatedModule(module, {
      execute: async (_module, stagingRoot) => {
        await writeArtifact(stagingRoot, {
          valid: true,
          generatedAt: "2026-07-23T00:00:00.000Z",
          dataDate: "2026-07-23",
        });
      },
      validate: validateFixture,
      now: () => "2026-07-23T01:00:00.000Z",
    });

    assert.equal(result.status, "fresh");
    assert.equal(result.dataDate, "2026-07-23");
    const current = JSON.parse(await fs.readFile(path.join(module.outputRoot, "current.json"), "utf8"));
    assert.equal(current.dataDate, "2026-07-23");
    assert.deepEqual((await fs.readdir(root)).filter((name) => name.startsWith(".artifact-")), []);
  });
});

test("failed module command keeps the last known good artifact and reports stale", async () => {
  await withTempDir(async (root) => {
    const module = fixtureModule(root);
    const validationOptions = [];
    await writeArtifact(module.outputRoot, {
      valid: true,
      generatedAt: "2026-07-22T00:00:00.000Z",
      dataDate: "2026-07-22",
    });

    const result = await runIsolatedModule(module, {
      execute: async (_module, stagingRoot) => {
        await writeArtifact(stagingRoot, { valid: false });
        throw new Error("synthetic command failure");
      },
      validate: async (id, artifactRoot, options) => {
        validationOptions.push(options);
        return validateFixture(id, artifactRoot);
      },
    });

    assert.equal(result.status, "stale");
    assert.equal(result.dataDate, "2026-07-22");
    assert.match(result.error, /synthetic command failure/u);
    assert.deepEqual(validationOptions, [{ allowHistoricalCohort: true }]);
    const current = JSON.parse(await fs.readFile(path.join(module.outputRoot, "current.json"), "utf8"));
    assert.equal(current.dataDate, "2026-07-22");
  });
});

test("invalid newly generated artifact falls back without replacing the current version", async () => {
  await withTempDir(async (root) => {
    const module = fixtureModule(root);
    await writeArtifact(module.outputRoot, {
      valid: true,
      generatedAt: "2026-07-22T00:00:00.000Z",
      dataDate: "2026-07-22",
    });

    const result = await runIsolatedModule(module, {
      execute: async (_module, stagingRoot) => {
        await writeArtifact(stagingRoot, {
          valid: false,
          generatedAt: "2026-07-23T00:00:00.000Z",
          dataDate: "2026-07-23",
        });
      },
      validate: validateFixture,
    });

    assert.equal(result.status, "stale");
    assert.match(result.error, /fixture artifact invalid/u);
    const current = JSON.parse(await fs.readFile(path.join(module.outputRoot, "current.json"), "utf8"));
    assert.equal(current.dataDate, "2026-07-22");
  });
});

test("module failure is fatal only when no valid previous artifact exists", async () => {
  await withTempDir(async (root) => {
    const module = fixtureModule(root);
    await assert.rejects(
      runIsolatedModule(module, {
        execute: async () => {
          throw new Error("synthetic first-run failure");
        },
        validate: validateFixture,
      }),
      /没有可用的上一版站点数据/u,
    );
  });
});

test("a stale module does not prevent later independent modules from running", async () => {
  const calls = [];
  const modules = [
    { id: "first", label: "第一模块" },
    { id: "second", label: "第二模块" },
  ];
  const results = await buildModules({
    modules,
    run: async (module) => {
      calls.push(module.id);
      return {
        label: module.label,
        status: module.id === "first" ? "stale" : "fresh",
        attemptedAt: "2026-07-23T00:00:00.000Z",
        generatedAt: "2026-07-22T00:00:00.000Z",
        dataDate: "2026-07-22",
      };
    },
  });

  assert.deepEqual(calls, ["first", "second"]);
  assert.equal(results.first.status, "stale");
  assert.equal(results.second.status, "fresh");
});
