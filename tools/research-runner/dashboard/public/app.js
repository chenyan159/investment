const token = document.querySelector('meta[name="dashboard-token"]').content;
const state = { snapshot: null, busy: false };

const statusLabels = {
  running: ["运行中", "good"],
  stopped: ["已停止", ""],
  stale_lock: ["Stale Lock", "bad"],
  quota_paused: ["Quota Paused", "warn"],
  concurrency_zero: ["并发为 0", "warn"],
  stopping: ["正在退出", "warn"],
};

const problemLabels = {
  missing: "文件缺失",
  empty: "空文件",
  h1_count: "H1 数量异常",
  placeholder: "存在占位符",
  outside_project: "位于项目外",
  duplicate_path: "重复路径",
  duplicate_content: "重复内容",
  not_file: "目标不是文件",
};

document.querySelector("#refresh-button").addEventListener("click", () => refreshAll(true));
document.querySelector("#validate-button").addEventListener("click", () => runAction("validate", {}));
document.querySelector("#runner-toggle-button").addEventListener("click", () => void toggleRunner());
document.querySelector("#concurrency-button").addEventListener("click", () => runConcurrencyAction("concurrency", 0));
document.querySelector("#shutdown-dashboard-button").addEventListener("click", async () => {
  if (!window.confirm("只关闭 Dashboard 服务？正在运行的 research runner 不受影响。")) return;
  await runAction("shutdown-dashboard", {});
  showNotice("Dashboard 已收到关闭请求；runner 不受影响。");
});

document.addEventListener("visibilitychange", () => {
  if (!document.hidden) void refreshAll(false);
});
window.addEventListener("resize", () => {
  const running = state.snapshot?.running;
  if (running) sizeRunningTable(running.items?.length || 0, state.snapshot?.display?.runningVisibleRowLimit || 10);
});

setInterval(() => void refreshStatus(), 5_000);
setInterval(() => void refreshQuota(), 60_000);
void refreshAll(true);

async function refreshAll(forceQuota) {
  await Promise.all([refreshStatus(), refreshQuota(forceQuota)]);
}

async function refreshStatus() {
  setRefreshState("loading");
  try {
    const response = await fetch("/api/status", { cache: "no-store" });
    if (!response.ok) throw new Error(`状态请求失败：HTTP ${response.status}`);
    state.snapshot = await response.json();
    render(state.snapshot);
    setRefreshState("ok", state.snapshot.generatedAt);
    hideError();
  } catch (error) {
    setRefreshState("error");
    showError(error.message || String(error));
  }
}

async function refreshQuota(force = false, renderAfter = true) {
  try {
    const response = await fetch(`/api/quota${force ? "?refresh=1" : ""}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`Quota 请求失败：HTTP ${response.status}`);
    await response.json();
    if (renderAfter && state.snapshot) await refreshStatus();
  } catch (error) {
    showError(error.message || String(error));
  }
}

async function runAction(action, body) {
  if (state.busy) return;
  state.busy = true;
  setButtonsDisabled(true);
  showActionOutput(`${action} 执行中…`);
  try {
    const response = await fetch(`/api/actions/${action}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-dashboard-token": token,
      },
      body: JSON.stringify(body),
    });
    const result = await response.json();
    showActionOutput(JSON.stringify(result, null, 2));
    if (!response.ok) throw new Error(result.error || `${action} 失败`);
    showNotice(actionMessage(action, result));
    if (action !== "shutdown-dashboard") await refreshAll(action === "start");
  } catch (error) {
    showError(error.message || String(error));
  } finally {
    state.busy = false;
    setButtonsDisabled(false);
  }
}

async function runConcurrencyAction(action, minimum) {
  try {
    await runAction(action, { concurrency: inputConcurrency(minimum) });
  } catch (error) {
    showError(error.message || String(error));
  }
}

async function toggleRunner() {
  const runner = state.snapshot?.runner;
  if (!runner) {
    showError("尚未取得 Runner 状态，请刷新后重试。");
    return;
  }
  if (!runner.pidAlive) {
    await runConcurrencyAction("start", 1);
    return;
  }
  if (!window.confirm("强制停止会终止 runner 进程树，但不会修改 queue 状态。确定继续吗？")) return;
  if (!window.confirm("再次确认：下一次启动将由 runner 自行恢复 stale running。")) return;
  await runAction("force-stop", { confirm: "STOP" });
}

function render(snapshot) {
  renderRunner(snapshot.runner);
  renderQueue(snapshot.queue);
  renderRunning(snapshot.running, snapshot.display?.runningVisibleRowLimit || 10);
  renderCompleted(snapshot.completed);
  renderForecast(snapshot.eta, snapshot.quota);
  renderAnomalies(snapshot.anomalies);
  renderPathHealth(snapshot.pathHealth);
  renderQuota(snapshot.quota);
}

function renderRunner(runner) {
  const [label, tone] = statusLabels[runner.status] || [runner.status || "未知", "warn"];
  const status = document.querySelector("#runner-status");
  status.textContent = label;
  status.className = `status-pill ${tone}`.trim();
  setText("runner-pid", runner.pid ? `PID ${runner.pid}` : "无 PID");
  const detail = runner.pidAlive
    ? `并发 ${valueOrDash(runner.concurrency)} · 已运行 ${formatDurationSeconds(runner.uptimeSeconds)}`
    : `并发设置 ${valueOrDash(runner.concurrency)} · runner 当前未运行`;
  setText("runner-detail", detail);
  setText("runner-model", `启动配置：${runner.configuredModel || "—"} · 默认 ${runner.defaultReasoningEffort || "—"} · SDK ${runner.sdkVersion || "—"}`);
  const input = document.querySelector("#concurrency-input");
  if (document.activeElement !== input && Number.isInteger(runner.concurrency)) input.value = runner.concurrency;
  renderRunnerToggle(runner);
}

function renderRunnerToggle(runner) {
  const button = document.querySelector("#runner-toggle-button");
  const running = Boolean(runner?.pidAlive);
  button.textContent = state.busy ? "处理中…" : running ? "强制停止 Runner" : "启动 Runner";
  button.classList.toggle("button-primary", !running);
  button.classList.toggle("button-danger", running);
  button.disabled = state.busy || !runner;
  button.setAttribute("aria-label", running ? "强制停止 Runner" : "启动 Runner");
}

function renderQueue(queue) {
  setText("queue-active", formatNumber(queue.active));
  setText("queue-detail", `${queue.running} running · ${queue.pending} pending · ${queue.retryPending} retry · ${queue.failed} failed`);
  setText("queue-progress-label", `本轮 ${queue.currentRunCompleted} / ${queue.currentRunTotal} · ${queue.progressPercent}%`);
  document.querySelector("#queue-progress").style.width = `${clamp(queue.progressPercent, 0, 100)}%`;
  renderStatChips("queue-status-stats", [
    ["Running", queue.running], ["Pending", queue.pending], ["Retry", queue.retryPending],
    ["Failed", queue.failed], ["Unarchived done", queue.unarchivedDone],
  ]);
  renderTable("domain-table-body", queue.domains, [
    (row) => row.domain,
    (row) => formatNumber(row.total),
    (row) => formatNumber(row.byStatus.running || 0),
    (row) => formatNumber(row.byStatus.pending || 0),
    (row) => formatNumber(row.byStatus.retry_pending || 0),
    (row) => formatNumber(row.byStatus.failed || 0),
  ]);
  setText("active-tasks-summary", `共 ${queue.active} 项 · 按队列顺序`);
  renderTable("active-tasks-table-body", queue.items || [], [
    (row) => primaryCell(row.displayName || row.subject, row.subject),
    (row) => row.domain,
    (row) => queueStatusLabel(row.status),
    (row) => row.reasoningEffort || "—",
    (row) => formatPlanVersion(row.planVersion),
  ]);
  toggle("active-tasks-empty", !queue.items?.length);
}

function queueStatusLabel(status) {
  return ({ pending: "待运行", running: "运行中", retry_pending: "待重试", failed: "失败", done: "已完成" })[status] || status || "未记录";
}

function formatPlanVersion(version) {
  return version || "未记录";
}

function renderRunning(running, visibleRowLimit) {
  const rows = running.items || [];
  setText("running-summary", `最新 ${Math.min(rows.length, visibleRowLimit)} 条在上 · 共 ${running.count}`);
  renderStatChips("running-stats", [
    ["Running", running.count],
    ["平均已运行", formatMinutes(running.averageElapsedMinutes)],
    ["最长已运行", formatMinutes(running.maxElapsedMinutes)],
    ["Attempt > 1", running.retrying],
  ]);
  renderTable("running-table-body", rows, [
    (row) => primaryCell(row.displayName || row.subject, row.subject),
    (row) => row.domain,
    (row) => formatPlanVersion(row.planVersion),
    (row) => formatMinutes(row.elapsedMinutes),
    (row) => formatNumber(row.attempts),
    (row) => row.reasoningEffort || "—",
  ]);
  sizeRunningTable(rows.length, visibleRowLimit);
  toggle("running-empty", running.count === 0);
}

function sizeRunningTable(rowCount, visibleRowLimit) {
  const wrap = document.querySelector("#running-table-wrap");
  const rows = [...document.querySelectorAll("#running-table-body tr")];
  const isScrollable = rowCount > visibleRowLimit;
  wrap.classList.toggle("is-scrollable", isScrollable);
  wrap.tabIndex = isScrollable ? 0 : -1;
  wrap.setAttribute("aria-label", isScrollable
    ? `运行中任务列表，最新 ${visibleRowLimit} 条可见，可向下滚动查看全部 ${rowCount} 条`
    : `运行中任务列表，共 ${rowCount} 条`);
  wrap.style.maxHeight = "none";
  if (!isScrollable) return;
  const headerHeight = wrap.querySelector("thead")?.getBoundingClientRect().height || 0;
  const rowsHeight = rows.slice(0, visibleRowLimit)
    .reduce((total, row) => total + row.getBoundingClientRect().height, 0);
  const scrollbarHeight = Math.max(0, wrap.offsetHeight - wrap.clientHeight);
  wrap.style.maxHeight = `${Math.ceil(headerHeight + rowsHeight + scrollbarHeight + 1)}px`;
}

function renderCompleted(completed) {
  setText("completed-count", formatNumber(completed.currentRun));
  const averageMinutes = completed.duration?.average;
  setText("completed-detail", `${formatMinutes(averageMinutes)} 平均 · ${formatTokens(completed.totalTokens)} tokens`);
  setText("completed-summary", `展示最近 ${Math.min(completed.latest.length, 8)} · archive ${formatNumber(completed.archiveTotal)}`);
  renderStatChips("completed-stats", [
    ["本轮完成", completed.currentRun],
    ["平均", formatMinutes(completed.duration?.average)],
    ["Median", formatMinutes(completed.duration?.median)],
    ["P90", formatMinutes(completed.duration?.p90)],
    ["Worker time", formatMinutes(completed.totalWorkerMinutes)],
    ["首试成功", completed.firstAttempt],
    ["有重试", completed.retried],
    ["总 tokens", formatTokens(completed.totalTokens)],
  ]);
  renderTable("completed-table-body", completed.latest, [
    (row) => primaryCell(row.displayName || row.subject, formatDate(row.finishedAt)),
    (row) => row.domain,
    (row) => formatPlanVersion(row.planVersion),
    (row) => formatMinutes(row.durationMinutes),
    (row) => formatNumber(row.attempts),
    (row) => formatTokens(row.totalTokens),
  ]);
  toggle("completed-empty", completed.latest.length === 0);
}

function renderForecast(eta, quota) {
  if (eta.available && !eta.complete) {
    setText("eta-mean", formatDate(eta.meanFinishAt));
    setText("eta-p90", formatDate(eta.p90FinishAt));
    setText("forecast-note", `预计剩余 ${formatTokens(eta.estimatedRemainingTokens)} tokens · ${eta.basis}`);
  } else if (eta.complete) {
    setText("eta-mean", "队列已完成");
    setText("eta-p90", "队列已完成");
    setText("forecast-note", "当前没有可执行的剩余任务。");
  } else {
    setText("eta-mean", "暂不可用");
    setText("eta-p90", "暂不可用");
    setText("forecast-note", eta.reason === "concurrency_zero_or_unknown" ? "并发为 0 或未知，无法估算完成时间。" : eta.reason === "model_history_unavailable" ? `暂无 ${eta.model} 对应推理强度的耗时样本，完成时间暂不可估算。` : "等待足够数据。");
  }
  setText("quota-threshold-label", `预计触及已用 ${quota.thresholdPercent ?? 95}% 暂停阈值`);
  setText("quota-projected", quota.available && Number.isFinite(quota.projectedAtFinishRemainingPercent)
    ? `${quota.projectedAtFinishRemainingPercent}%`
    : quota.available ? "未校准" : "暂不可用");
  setText("quota-threshold-time", quota.available && quota.estimatedThresholdAt
    ? formatDate(quota.estimatedThresholdAt)
    : quota.blocked ? "已达到暂停阈值" : quota.available ? "暂不可估算" : "暂不可用");
}

function renderQuota(quota) {
  if (!quota.available) {
    setText("quota-remaining", quota.loading ? "读取中" : "不可用");
    setText("quota-detail", quota.error || "等待 quota 数据");
    document.querySelector("#quota-meter").style.width = "0%";
    return;
  }
  setText("quota-remaining", Number.isFinite(quota.primaryRemainingPercent) ? `${quota.primaryRemainingPercent}%` : "未知");
  document.querySelector("#quota-meter").style.width = `${clamp(quota.primaryRemainingPercent, 0, 100)}%`;
  setText("quota-detail", `已用 ${Number.isFinite(quota.primaryUsedPercent) ? quota.primaryUsedPercent + "%" : "未知"} · ${quota.resetCredits ?? "—"} 次重置 · ${formatDate(quota.resetsAt)} 重置`);
}

function renderAnomalies(anomalies) {
  setText("anomaly-summary", `最新 ${Math.min(anomalies.latest.length, 8)} / ${anomalies.total}`);
  const kinds = Object.entries(anomalies.byKind || {}).sort((a, b) => b[1] - a[1]);
  renderStatChips("anomaly-stats", [
    ["Total", anomalies.total], ["Errors", anomalies.errors], ["Warnings", anomalies.warnings], ...kinds,
  ]);
  const list = document.querySelector("#anomaly-list");
  list.replaceChildren(...anomalies.latest.map((entry) => {
    const item = document.createElement("li");
    const title = document.createElement("div");
    title.className = "event-title";
    const event = document.createElement("span");
    event.textContent = entry.event || "未命名事件";
    const time = document.createElement("time");
    time.textContent = formatDate(entry.timestamp);
    title.append(event, time);
    const meta = document.createElement("div");
    meta.className = "event-meta";
    meta.textContent = [entry.level, entry.id, entry.details].filter(Boolean).join(" · ");
    item.append(title, meta);
    return item;
  }));
  toggle("anomaly-empty", anomalies.total === 0);
}

function renderPathHealth(pathHealth) {
  const status = document.querySelector("#path-health-status");
  status.textContent = pathHealth.clean ? "Clean" : "Needs attention";
  status.className = `status-pill ${pathHealth.clean ? "good" : "bad"}`;
  renderStatChips("path-stats", [
    ["Checked", pathHealth.checked], ["Missing", pathHealth.missing], ["Empty", pathHealth.empty],
    ["Bad H1", pathHealth.badH1], ["Placeholder", pathHealth.placeholderFiles],
    ["Dup path", pathHealth.duplicatePaths], ["Dup content", pathHealth.duplicateContent],
    ["Artifacts", pathHealth.artifacts],
  ]);
  const list = document.querySelector("#path-problem-list");
  list.replaceChildren(...pathHealth.latestProblems.map((problem) => {
    const item = document.createElement("li");
    const title = document.createElement("div");
    title.className = "event-title";
    const subject = document.createElement("span");
    subject.textContent = problem.subject || problem.id;
    const labels = document.createElement("span");
    labels.textContent = problem.problems.map((value) => problemLabels[value] || value).join("、");
    title.append(subject, labels);
    const meta = document.createElement("div");
    meta.className = "event-meta";
    meta.textContent = problem.outputFile || "无输出路径";
    item.append(title, meta);
    return item;
  }));
  toggle("path-empty", pathHealth.latestProblems.length === 0);
}

function renderStatChips(targetId, pairs) {
  const target = document.querySelector(`#${targetId}`);
  target.replaceChildren(...pairs.map(([label, value]) => {
    const chip = document.createElement("div");
    chip.className = "stat-chip";
    const name = document.createElement("span");
    name.textContent = label;
    const strong = document.createElement("strong");
    strong.textContent = value ?? "—";
    chip.append(name, strong);
    return chip;
  }));
}

function renderTable(targetId, rows, columns) {
  const body = document.querySelector(`#${targetId}`);
  body.replaceChildren(...rows.map((row) => {
    const tr = document.createElement("tr");
    for (const getValue of columns) {
      const td = document.createElement("td");
      const value = getValue(row);
      if (value instanceof Node) td.append(value);
      else td.textContent = value ?? "—";
      tr.append(td);
    }
    return tr;
  }));
}

function primaryCell(primary, secondary) {
  const wrap = document.createElement("span");
  wrap.className = "table-primary";
  wrap.textContent = primary || "—";
  if (secondary) {
    const small = document.createElement("span");
    small.className = "table-secondary";
    small.textContent = secondary;
    wrap.append(small);
  }
  return wrap;
}

function inputConcurrency(minimum) {
  const input = document.querySelector("#concurrency-input");
  const value = Number(input.value);
  if (!Number.isInteger(value) || value < minimum || value > 128) {
    throw new Error(`并发必须是 ${minimum}–128 的整数。`);
  }
  return value;
}

function setButtonsDisabled(disabled) {
  document.querySelectorAll(".controls-row button").forEach((button) => { button.disabled = disabled; });
  if (!disabled) renderRunnerToggle(state.snapshot?.runner);
}

function setRefreshState(mode, timestamp) {
  const dot = document.querySelector("#refresh-dot");
  dot.className = `refresh-dot ${mode === "ok" ? "live" : mode === "error" ? "error" : ""}`.trim();
  if (timestamp) setText("last-refresh", `更新于 ${formatDate(timestamp, true)}`);
  else if (mode === "loading") setText("last-refresh", "正在刷新");
  else if (mode === "error") setText("last-refresh", "刷新失败");
}

function showActionOutput(value) {
  const output = document.querySelector("#action-output");
  output.textContent = value;
  output.classList.remove("hidden");
}

function actionMessage(action, result) {
  if (action === "validate") return `Validate 完成：${result.summary?.errors ?? "—"} errors，${result.summary?.warnings ?? "—"} warnings。`;
  if (action === "start") return result.started ? `Runner 已启动，PID ${result.pid}。` : `Runner 已快速退出：${result.message || "queue 可能为空"}`;
  if (action === "concurrency") return `目标并发已设置为 ${result.concurrency}。`;
  if (action === "force-stop") return result.stopped ? `Runner PID ${result.pid} 已停止。` : `Runner 未停止：${result.reason || "未知原因"}`;
  return `${action} 完成。`;
}

function showError(message) {
  const banner = document.querySelector("#error-banner");
  banner.textContent = message;
  banner.classList.remove("hidden");
}

function hideError() { document.querySelector("#error-banner").classList.add("hidden"); }

function showNotice(message) {
  const banner = document.querySelector("#notice-banner");
  banner.textContent = message;
  banner.classList.remove("hidden");
  setTimeout(() => banner.classList.add("hidden"), 8_000);
}

function setText(id, value) { document.querySelector(`#${id}`).textContent = value ?? "—"; }
function toggle(id, visible) { document.querySelector(`#${id}`).classList.toggle("hidden", !visible); }
function valueOrDash(value) { return value === null || value === undefined ? "—" : value; }
function clamp(value, min, max) { return Math.max(min, Math.min(max, Number(value) || 0)); }
function formatNumber(value) { return Number.isFinite(Number(value)) ? new Intl.NumberFormat("zh-CN").format(Number(value)) : "—"; }

function formatMinutes(value) {
  if (!Number.isFinite(Number(value))) return "—";
  const minutes = Number(value);
  if (minutes < 60) return `${minutes.toFixed(minutes < 10 ? 1 : 0)}m`;
  return `${Math.floor(minutes / 60)}h ${Math.round(minutes % 60)}m`;
}

function formatDurationSeconds(value) {
  if (!Number.isFinite(Number(value))) return "—";
  return formatMinutes(Number(value) / 60);
}

function formatTokens(value) {
  const tokens = Number(value);
  if (!Number.isFinite(tokens)) return "—";
  if (tokens >= 1_000_000_000) return `${(tokens / 1_000_000_000).toFixed(2)}B`;
  if (tokens >= 1_000_000) return `${(tokens / 1_000_000).toFixed(1)}M`;
  if (tokens >= 1_000) return `${(tokens / 1_000).toFixed(1)}K`;
  return formatNumber(tokens);
}

function formatDate(value, includeSeconds = false) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit",
    second: includeSeconds ? "2-digit" : undefined,
    hour12: false,
  }).format(date);
}
