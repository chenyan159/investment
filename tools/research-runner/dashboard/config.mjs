import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  DONE_QUEUE_PATH,
  PROJECT_ROOT,
  QUEUE_CONTROL_PATH,
  QUEUE_PATH,
} from "../queue-store.mjs";

export const DASHBOARD_DIR = path.dirname(fileURLToPath(import.meta.url));
export const RUNNER_DIR = path.resolve(DASHBOARD_DIR, "..");
export const PUBLIC_DIR = path.join(DASHBOARD_DIR, "public");
export const LOCK_PATH = path.join(RUNNER_DIR, "runner.lock");
export const LOG_PATH = path.join(RUNNER_DIR, "logs", "current.jsonl");

export { DONE_QUEUE_PATH, PROJECT_ROOT, QUEUE_CONTROL_PATH, QUEUE_PATH };

export const DASHBOARD_HOST = "127.0.0.1";
export const DASHBOARD_PORT = parseInteger(
  process.env.RESEARCH_DASHBOARD_PORT,
  4319,
  { min: 1, max: 65535 },
);
export { DEFAULT_CONCURRENCY as DEFAULT_RUNNER_CONCURRENCY } from "../runtime-config.mjs";
export const MAX_RUNNER_CONCURRENCY = 128;
export const STATE_REFRESH_MS = 5_000;
export const QUOTA_REFRESH_MS = 60_000;
export const IDLE_EXIT_MS = parseInteger(
  process.env.RESEARCH_DASHBOARD_IDLE_MINUTES,
  15,
  { min: 0, max: 1440 },
) * 60_000;
export const RECENT_ITEM_LIMIT = 8;
export const RECENT_COMPLETED_LIMIT = 30;
export const RECENT_ANOMALY_LIMIT = 8;
export const RUNNING_VISIBLE_ROW_LIMIT = 10;


function parseInteger(raw, fallback, { min, max }) {
  if (raw === undefined || raw === null || String(raw).trim() === "") return fallback;
  const value = Number(raw);
  if (!Number.isInteger(value) || value < min || value > max) return fallback;
  return value;
}
