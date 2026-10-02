import test from "node:test";
import assert from "node:assert/strict";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execute = promisify(execFile);
const dashboard = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const projectRoot = path.resolve(dashboard, "../../..");

async function withHealth(health, callback) {
  const server = http.createServer((request, response) => {
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify(health));
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  try {
    await callback(server.address().port);
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
}

function launch(port) {
  return execute("pwsh", ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", path.join(dashboard, "launch-dashboard.ps1"), "-NoBrowser"], {
    env: { ...process.env, RESEARCH_DASHBOARD_PORT: String(port) },
    timeout: 15000,
  });
}

test("launcher reuses only this dashboard and workspace", { skip: process.platform !== "win32" }, async () => {
  await withHealth({ ok: true, service: "research-runner-dashboard", projectRoot }, async port => {
    const result = await launch(port);
    assert.match(result.stdout, new RegExp(`http://127.0.0.1:${port}`));
  });
});

test("launcher rejects a foreign healthy service without opening it", { skip: process.platform !== "win32" }, async () => {
  await withHealth({ ok: true }, async port => {
    await assert.rejects(launch(port), error => /occupied by a different service or workspace/.test(error.stderr));
  });
});

test("launcher rejects a dashboard pointing at another workspace", { skip: process.platform !== "win32" }, async () => {
  await withHealth({ ok: true, service: "research-runner-dashboard", projectRoot: path.join(projectRoot, "different") }, async port => {
    await assert.rejects(launch(port), error => /occupied by a different service or workspace/.test(error.stderr));
  });
});
