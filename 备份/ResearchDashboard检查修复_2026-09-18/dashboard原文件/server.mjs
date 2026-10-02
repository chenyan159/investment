import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { randomBytes } from "node:crypto";

import {
  DASHBOARD_HOST,
  DASHBOARD_PORT,
  IDLE_EXIT_MS,
  PUBLIC_DIR,
  QUOTA_REFRESH_MS,
  STATE_REFRESH_MS,
} from "./config.mjs";
import { QuotaService } from "./quota-service.mjs";
import {
  forceStopRunner,
  setRunnerConcurrency,
  startRunner,
  validateQueue,
} from "./runner-control.mjs";
import { buildDashboardSnapshot } from "./snapshot.mjs";

const token = randomBytes(32).toString("base64url");
const quotaService = new QuotaService();
const startedAt = new Date();
let lastClientSeenAt = Date.now();
let shuttingDown = false;

const server = http.createServer(async (request, response) => {
  try {
    applySecurityHeaders(response);
    const url = new URL(request.url || "/", `http://${request.headers.host || `${DASHBOARD_HOST}:${DASHBOARD_PORT}`}`);

    if (request.method === "GET" && url.pathname === "/api/health") {
      return json(response, 200, {
        ok: true,
        pid: process.pid,
        startedAt: startedAt.toISOString(),
        idleExitMinutes: IDLE_EXIT_MS ? IDLE_EXIT_MS / 60_000 : 0,
      });
    }

    if (request.method === "GET" && url.pathname === "/api/status") {
      markClientSeen();
      return json(response, 200, buildDashboardSnapshot({ quota: quotaService.current() }));
    }

    if (request.method === "GET" && url.pathname === "/api/quota") {
      markClientSeen();
      const quota = await quotaService.refresh({ force: url.searchParams.get("refresh") === "1" });
      return json(response, 200, { quota, refreshMs: QUOTA_REFRESH_MS });
    }

    if (request.method === "POST" && url.pathname.startsWith("/api/actions/")) {
      await requireControlRequest(request);
      markClientSeen();
      const body = await readJsonBody(request);
      if (url.pathname === "/api/actions/validate") {
        const result = await validateQueue();
        return json(response, result.ok ? 200 : 422, result);
      }
      if (url.pathname === "/api/actions/start") {
        const result = await startRunner({ concurrency: body.concurrency });
        return json(response, 200, result);
      }
      if (url.pathname === "/api/actions/concurrency") {
        return json(response, 200, setRunnerConcurrency(body.concurrency));
      }
      if (url.pathname === "/api/actions/force-stop") {
        return json(response, 200, await forceStopRunner({ confirm: body.confirm }));
      }
      if (url.pathname === "/api/actions/shutdown-dashboard") {
        json(response, 200, { stopping: true, runnerUnaffected: true });
        setTimeout(() => stopServer("requested_by_ui"), 100).unref();
        return;
      }
      return json(response, 404, { error: "Unknown action." });
    }

    if (request.method !== "GET" && request.method !== "HEAD") {
      return json(response, 405, { error: "Method not allowed." });
    }
    return serveStatic(url.pathname, response, request.method === "HEAD");
  } catch (error) {
    const statusCode = Number(error?.statusCode) || 500;
    return json(response, statusCode, {
      error: error?.message || String(error),
      details: error?.details || null,
    });
  }
});

server.on("error", (error) => {
  if (error.code === "EADDRINUSE") {
    console.error(`Dashboard port ${DASHBOARD_PORT} is already in use.`);
  } else {
    console.error(error);
  }
  process.exitCode = 1;
});

server.listen(DASHBOARD_PORT, DASHBOARD_HOST, () => {
  console.log(`Research Runner Dashboard: http://${DASHBOARD_HOST}:${DASHBOARD_PORT}`);
  void quotaService.refresh();
});

if (IDLE_EXIT_MS > 0) {
  const idleTimer = setInterval(() => {
    if (Date.now() - lastClientSeenAt >= IDLE_EXIT_MS) stopServer("idle_timeout");
  }, Math.min(60_000, Math.max(5_000, IDLE_EXIT_MS / 3)));
  idleTimer.unref();
}

process.on("SIGINT", () => stopServer("SIGINT"));
process.on("SIGTERM", () => stopServer("SIGTERM"));

function markClientSeen() {
  lastClientSeenAt = Date.now();
}

function stopServer(reason) {
  if (shuttingDown) return;
  shuttingDown = true;
  console.log(`Stopping dashboard (${reason}); research runner is unaffected.`);
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 2_000).unref();
}

async function requireControlRequest(request) {
  const contentType = String(request.headers["content-type"] || "").toLowerCase();
  if (!contentType.startsWith("application/json")) {
    const error = new Error("Control requests must use application/json.");
    error.statusCode = 415;
    throw error;
  }
  if (request.headers["x-dashboard-token"] !== token) {
    const error = new Error("Invalid dashboard control token.");
    error.statusCode = 403;
    throw error;
  }
  const origin = String(request.headers.origin || "");
  const expected = `http://${request.headers.host}`;
  if (!origin || origin !== expected) {
    const error = new Error("Invalid control request origin.");
    error.statusCode = 403;
    throw error;
  }
}

function readJsonBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.setEncoding("utf8");
    request.on("data", (chunk) => {
      body += chunk;
      if (body.length > 64 * 1024) {
        const error = new Error("Request body is too large.");
        error.statusCode = 413;
        reject(error);
        request.destroy();
      }
    });
    request.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        const error = new Error("Request body is not valid JSON.");
        error.statusCode = 400;
        reject(error);
      }
    });
    request.on("error", reject);
  });
}

function serveStatic(requestPath, response, headOnly) {
  const relative = requestPath === "/" ? "index.html" : requestPath.replace(/^\/+/, "");
  const target = path.resolve(PUBLIC_DIR, relative);
  const insidePublic = target === PUBLIC_DIR || target.startsWith(`${PUBLIC_DIR}${path.sep}`);
  if (!insidePublic || !fs.existsSync(target) || !fs.statSync(target).isFile()) {
    return json(response, 404, { error: "Not found." });
  }
  const extension = path.extname(target).toLowerCase();
  const contentType = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
  }[extension] || "application/octet-stream";
  let body = fs.readFileSync(target);
  if (extension === ".html") {
    body = Buffer.from(body.toString("utf8").replaceAll("__DASHBOARD_TOKEN__", token), "utf8");
    response.setHeader("Cache-Control", "no-store");
  } else {
    response.setHeader("Cache-Control", "no-cache");
  }
  response.writeHead(200, { "Content-Type": contentType, "Content-Length": body.length });
  response.end(headOnly ? undefined : body);
}

function json(response, statusCode, value) {
  if (response.writableEnded) return;
  const body = Buffer.from(JSON.stringify(value), "utf8");
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": body.length,
    "Cache-Control": "no-store",
  });
  response.end(body);
}

function applySecurityHeaders(response) {
  response.setHeader("Content-Security-Policy", "default-src 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'");
  response.setHeader("Referrer-Policy", "no-referrer");
  response.setHeader("X-Content-Type-Options", "nosniff");
  response.setHeader("X-Frame-Options", "DENY");
  response.setHeader("Cross-Origin-Resource-Policy", "same-origin");
  response.setHeader("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()");
}

export { server };
