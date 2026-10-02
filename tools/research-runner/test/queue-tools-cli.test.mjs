import assert from "node:assert/strict";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(testDir, "..");
const queueToolsPath = path.join(projectDir, "queue-tools.mjs");

test("queue tools no longer expose or accept --include-done", () => {
  const help = spawnSync(process.execPath, [queueToolsPath, "--help"], {
    cwd: projectDir,
    encoding: "utf8",
  });
  assert.equal(help.status, 0);
  assert.doesNotMatch(help.stdout, /--include-done/u);

  const removedOption = spawnSync(process.execPath, [queueToolsPath, "validate", "--include-done"], {
    cwd: projectDir,
    encoding: "utf8",
  });
  assert.notEqual(removedOption.status, 0);
  assert.match(removedOption.stderr, /Unknown argument: --include-done/u);
});
