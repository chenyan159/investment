import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const FUND_ROOT = path.resolve(__dirname, "..");
const PROJECT_ROOT = path.resolve(FUND_ROOT, "..");
const FEATURE_ROOT = path.join(FUND_ROOT, "特征量化");
const PLAN_ROOT = path.join(FEATURE_ROOT, "研究方案");
const EVAL_ROOT = path.join(FEATURE_ROOT, "特征评估");
const OUTPUT_FILE = path.join(FEATURE_ROOT, "有效指标清单_latest.json");

const HOLDING_DAYS = new Map([
  ["21d", 21],
  ["63d", 63],
  ["126d", 126],
  ["252d", 252],
]);
const ALLOWED_HOLDING_PERIODS = new Set(HOLDING_DAYS.keys());
const HASH_RE = /^[a-f0-9]{64}$/u;
const FAMILY_MEMBER_RE = /^(N\d{2})@([^@\s]+)@(21d|63d|126d|252d)$/u;

const POLICY = Object.freeze({
  methodology: "forward_only",
  identityFields: ["feature_id", "feature_version", "holding_period"],
  minMatureCohorts: 3,
  minSampleSize: 80,
  minMeanSpearmanIc: 0.05,
  minDirectionConsistency: 2 / 3,
  minSignificantCohortShare: 2 / 3,
  fdrQMax: 0.10,
  minIcir: 0.50,
  requireCompleteFrozenFdrFamily: true,
  requirePrimaryHorizon: true,
  requireNonOverlappingOosWindows: true,
  requireStrictTradableTimestampOrder: true,
  requirePositiveNeutralIc: true,
  requirePositiveNetSpread: true,
  rule: "同一特征版本与预注册主持有期内至少3个不重叠成熟前向形成期；形成时冻结cohort、评分快照、样本、收益口径和完整FDR family；入场严格晚于信号可交易时点；方向一致率和FDR显著期占比均不低于2/3；平均Spearman IC不低于0.05；ICIR不低于0.50；行业规模中性IC与扣费后Top-Bottom均为正。",
});

export async function main() {
  const today = todayIsoDate();
  const plans = await loadPlans();
  const records = deduplicateRecords(await loadEvaluationRecords());
  const alphaPlans = plans.filter((plan) => plan.layer === "alpha");
  const gatePlans = plans.filter((plan) => plan.layer === "gate");
  const completeFdrFamilies = attachBhQValues(records, today);
  const features = alphaPlans.map((plan) => summarizeFeature(plan, records, today));
  const qualifiedFeatures = features.filter((feature) => feature.status === "qualified");
  const effectiveSeriesIds = qualifiedFeatures.map((feature) => feature.effectiveIdentity);
  const effectiveFeatureIds = qualifiedFeatures.map((feature) => feature.id);
  const asOf = features.map((feature) => feature.oosEnd).filter(Boolean).sort().at(-1) || "";
  const activeAlphaIds = new Set(alphaPlans.map((plan) => plan.id));
  const activeRecords = records.filter((record) => activeAlphaIds.has(record.featureId));
  const rejectedCompleted = activeRecords.filter((record) => record.layer === "alpha"
    && record.status === "completed"
    && !isMatureAlphaRecord(record, today));

  const registry = {
    schemaVersion: 2,
    status: effectiveSeriesIds.length ? "qualified_features_available" : "awaiting_sufficient_forward_evidence",
    asOf,
    generatedAt: new Date().toISOString(),
    sourceRoot: "基本面/特征量化",
    policy: POLICY,
    activeArchitecture: {
      alphaFeatureCount: alphaPlans.length,
      gateCount: gatePlans.length,
      alphaFeatureIds: alphaPlans.map((plan) => plan.id),
      gateIds: gatePlans.map((plan) => plan.id),
    },
    effectiveFeatureIds,
    effectiveSeriesIds,
    effectiveFeatureCount: effectiveSeriesIds.length,
    features,
    gates: gatePlans.map((plan) => ({
      id: plan.id,
      name: plan.name,
      status: "not_alpha",
      use: "用于数据、可投资性或风险约束，不进入收益型有效特征名单。",
    })),
    audit: {
      parsedEvaluationRecords: records.length,
      activeEvaluationRecords: activeRecords.length,
      matureActiveRecords: activeRecords.filter((record) => isMatureAlphaRecord(record, today)).length,
      immatureActiveRecords: activeRecords.filter((record) => record.status === "immature").length,
      rejectedCompletedRecords: rejectedCompleted.length,
      completeFrozenFdrFamilies: completeFdrFamilies,
      rejectionReasons: countRejectionReasons(rejectedCompleted, today),
    },
  };

  await fs.writeFile(OUTPUT_FILE, `${JSON.stringify(registry, null, 2)}\n`, "utf8");
  console.log(`Wrote ${OUTPUT_FILE}`);
  console.log(`Active alpha=${alphaPlans.length}; gates=${gatePlans.length}; records=${records.length}; complete FDR families=${completeFdrFamilies}; qualified=${effectiveSeriesIds.length}; asOf=${asOf || "NA"}`);
  return registry;
}

async function loadPlans() {
  const names = await safeReadDir(PLAN_ROOT);
  const plans = names
    .map((name) => {
      const match = name.match(/^([NG]\d{2})_(.+)_研究方案\.md$/u);
      if (!match) return null;
      return { id: match[1], name: match[2], layer: match[1].startsWith("N") ? "alpha" : "gate" };
    })
    .filter(Boolean)
    .sort((a, b) => a.id.localeCompare(b.id));
  const duplicatedIds = plans.map((plan) => plan.id)
    .filter((id, index, ids) => ids.indexOf(id) !== index);
  if (duplicatedIds.length) throw new Error(`Duplicate feature plan IDs: ${[...new Set(duplicatedIds)].join(", ")}`);
  return plans;
}

async function loadEvaluationRecords() {
  const names = await safeReadDir(EVAL_ROOT);
  const records = [];
  for (const name of names) {
    const fileMeta = parseEvaluationFileName(name);
    if (!fileMeta) continue;
    const markdown = await fs.readFile(path.join(EVAL_ROOT, name), "utf8");
    const fields = parseRegistrationTable(markdown);
    if (!fields.size) continue;
    const featureId = field(fields, "feature_id");
    if (featureId !== fileMeta.featureId) continue;
    const scoreFile = field(fields, "score_file").replace(/\\/gu, "/");
    const scoreSnapshotHash = normalizeHash(field(fields, "score_snapshot_hash"));
    const actualScoreSnapshotHash = await hashScoreSnapshot(scoreFile);
    records.push({
      featureId,
      featureName: field(fields, "feature_name") || fileMeta.featureName,
      fileFeatureName: fileMeta.featureName,
      featureVersion: field(fields, "feature_version"),
      layer: field(fields, "layer"),
      status: field(fields, "status"),
      scoreFile,
      scoreAsOf: field(fields, "score_as_of"),
      fileFormationDate: fileMeta.formationDate,
      scoreTradableTimestamp: field(fields, "score_tradable_timestamp"),
      entryTimestamp: field(fields, "entry_timestamp"),
      oosStart: field(fields, "oos_start"),
      oosEnd: field(fields, "oos_end"),
      holdingPeriod: field(fields, "holding_period").toLowerCase(),
      returnWindowLabel: fileMeta.returnWindowLabel,
      tradingDays: numberField(fields, "trading_days"),
      n: numberField(fields, "n"),
      spearmanIc: numberField(fields, "spearman_ic"),
      neutralSpearmanIc: numberField(fields, "neutral_spearman_ic"),
      topBottomNetReturn: numberField(fields, "top_bottom_net_return"),
      quintileMonotonicity: numberField(fields, "quintile_monotonicity"),
      turnover: numberField(fields, "turnover"),
      transactionCost: numberField(fields, "transaction_cost"),
      permutationPValue: numberField(fields, "permutation_p_value"),
      dataQualityGate: field(fields, "data_quality_gate"),
      cohortId: field(fields, "cohort_id"),
      fdrFamilyId: field(fields, "fdr_family_id"),
      fdrFamilyMembers: parseFamilyMembers(field(fields, "fdr_family_members")),
      fdrFamilyHash: normalizeHash(field(fields, "fdr_family_hash")),
      scoreSnapshotId: field(fields, "score_snapshot_id"),
      scoreSnapshotHash,
      actualScoreSnapshotHash,
      universeHash: normalizeHash(field(fields, "universe_hash")),
      returnSeriesId: field(fields, "return_series_id"),
      returnMethod: field(fields, "return_method"),
      entryRule: field(fields, "entry_rule"),
      permutationSeed: field(fields, "permutation_seed"),
      isPrimaryHorizon: booleanField(fields, "is_primary_horizon"),
      evaluationDate: fileMeta.evaluationDate,
      sourceEvalFile: `基本面/特征量化/特征评估/${name}`,
      qValue: null,
    });
  }
  return records;
}

export function parseEvaluationFileName(name) {
  const match = String(name || "").match(/^([NG]\d{2})_(.+?)_特征评估_(21d|63d|126d|252d)_形成日(\d{4}-\d{2}-\d{2})_评估日(\d{4}-\d{2}-\d{2})\.md$/u);
  if (!match) return null;
  return {
    featureId: match[1],
    featureName: match[2],
    returnWindowLabel: match[3],
    formationDate: match[4],
    evaluationDate: match[5],
  };
}

function parseRegistrationTable(markdown) {
  const lines = markdown.replace(/^\ufeff/u, "").split(/\r?\n/u);
  const heading = lines.findIndex((line) => /^##\s+机器可读登记\s*$/u.test(line.trim()));
  if (heading < 0) return new Map();
  const fields = new Map();
  for (let i = heading + 1; i < lines.length; i += 1) {
    const line = lines[i].trim();
    if (/^##\s+/u.test(line)) break;
    if (!line.startsWith("|")) continue;
    const cells = line.replace(/^\|/u, "").replace(/\|$/u, "").split("|").map((cell) => cell.trim());
    if (cells.length < 2 || cells[0] === "字段" || /^[-:]+$/u.test(cells[0])) continue;
    fields.set(cells[0].toLowerCase(), cells[1]);
  }
  return fields;
}

function deduplicateRecords(records) {
  const latest = new Map();
  for (const record of records) {
    const key = [
      record.featureId,
      record.featureVersion,
      record.holdingPeriod,
      record.cohortId,
      record.fdrFamilyId,
      record.fdrFamilyHash,
      record.oosStart,
      record.oosEnd,
    ].join("|");
    const current = latest.get(key);
    if (!current || compareRecordRecency(record, current) >= 0) latest.set(key, record);
  }
  return [...latest.values()];
}

export function attachBhQValues(records, today = todayIsoDate()) {
  for (const record of records) record.qValue = null;
  const families = new Map();
  for (const record of records.filter((candidate) => isMatureAlphaRecord(candidate, today))) {
    const key = frozenFamilyCohortKey(record);
    if (!families.has(key)) families.set(key, []);
    families.get(key).push(record);
  }

  let completeFamilies = 0;
  for (const candidates of families.values()) {
    const expectedMembers = canonicalFamilyMembers(candidates[0].fdrFamilyMembers);
    if (!expectedMembers.length) continue;
    const latestByIdentity = new Map();
    for (const record of candidates) {
      const identity = seriesIdentity(record);
      if (!expectedMembers.includes(identity)) continue;
      const current = latestByIdentity.get(identity);
      if (!current || compareRecordRecency(record, current) >= 0) latestByIdentity.set(identity, record);
    }
    if (latestByIdentity.size !== expectedMembers.length
      || !expectedMembers.every((identity) => latestByIdentity.has(identity))) continue;
    const cohort = expectedMembers.map((identity) => latestByIdentity.get(identity));
    if (!cohort.every((record) => sameFrozenFamilyDefinition(record, candidates[0]))) continue;
    applyBenjaminiHochberg(cohort);
    completeFamilies += 1;
  }
  return completeFamilies;
}

function applyBenjaminiHochberg(cohort) {
  const sorted = [...cohort].sort((a, b) => a.permutationPValue - b.permutationPValue);
  let running = 1;
  for (let i = sorted.length - 1; i >= 0; i -= 1) {
    const raw = (sorted[i].permutationPValue * sorted.length) / (i + 1);
    running = Math.min(running, raw);
    sorted[i].qValue = Math.min(1, Math.max(0, running));
  }
}

function sameFrozenFamilyDefinition(record, anchor) {
  return record.fdrFamilyId === anchor.fdrFamilyId
    && record.fdrFamilyHash === anchor.fdrFamilyHash
    && canonicalFamilyMembers(record.fdrFamilyMembers).join("\n") === canonicalFamilyMembers(anchor.fdrFamilyMembers).join("\n")
    && frozenFamilyCohortKey(record) === frozenFamilyCohortKey(anchor);
}

function frozenFamilyCohortKey(record) {
  return [
    record.cohortId,
    record.fdrFamilyId,
    record.fdrFamilyHash,
    record.scoreAsOf,
    record.holdingPeriod,
    record.tradingDays,
    record.oosStart,
    record.oosEnd,
    record.entryTimestamp,
    record.universeHash,
    record.n,
    record.returnSeriesId,
    record.returnMethod,
    record.entryRule,
    record.permutationSeed,
  ].join("|");
}

export function summarizeFeature(plan, records, today = todayIsoDate()) {
  const observations = records.filter((record) => record.featureId === plan.id
    && record.fileFeatureName === plan.name
    && isIdentityObservation(record, today));
  const current = resolveCurrentIdentity(observations);
  const mature = records.filter((record) => record.featureId === plan.id
    && record.fileFeatureName === plan.name
    && isMatureAlphaRecord(record, today));
  const grouped = new Map();
  for (const record of mature) {
    const identity = seriesIdentity(record);
    if (!grouped.has(identity)) grouped.set(identity, []);
    grouped.get(identity).push(record);
  }
  const series = [...grouped.entries()].map(([identity, group]) => summarizeSeries(identity, group))
    .sort((a, b) => Number(b.identity === current.identity) - Number(a.identity === current.identity)
      || b.oosEnd.localeCompare(a.oosEnd));
  const selected = series.find((candidate) => candidate.identity === current.identity) || emptySeries(current.identity);
  const currentHasObservation = Boolean(current.identity);
  const status = current.conflict
    ? "identity_conflict"
    : selected.status === "qualified"
      ? "qualified"
      : currentHasObservation
        ? "observing"
        : "awaiting_forward_cohorts";
  return {
    id: plan.id,
    name: plan.name,
    ...selected,
    featureVersion: current.featureVersion || selected.featureVersion,
    holdingPeriod: current.holdingPeriod || selected.holdingPeriod,
    holdingPeriods: current.holdingPeriod ? [current.holdingPeriod] : [],
    effectiveIdentity: status === "qualified" ? current.identity : "",
    currentIdentity: current.identity,
    currentScoreAsOf: current.scoreAsOf,
    status,
    series,
  };
}

function resolveCurrentIdentity(records) {
  if (!records.length) return { identity: "", featureVersion: "", holdingPeriod: "", scoreAsOf: "", conflict: false };
  const latestScoreAsOf = records.map((record) => record.scoreAsOf).sort().at(-1);
  const latest = records.filter((record) => record.scoreAsOf === latestScoreAsOf);
  const identities = [...new Set(latest.map(seriesIdentity))];
  if (identities.length !== 1) {
    return { identity: "", featureVersion: "", holdingPeriod: "", scoreAsOf: latestScoreAsOf, conflict: true };
  }
  const record = latest.sort(compareRecordRecency).at(-1);
  return {
    identity: identities[0],
    featureVersion: record.featureVersion,
    holdingPeriod: record.holdingPeriod,
    scoreAsOf: latestScoreAsOf,
    conflict: false,
  };
}

function summarizeSeries(identity, records) {
  const cohorts = selectNonOverlappingCohorts(records);
  const nCohorts = cohorts.length;
  const meanIc = mean(cohorts.map((record) => record.spearmanIc));
  const neutralMeanIc = mean(cohorts.map((record) => record.neutralSpearmanIc));
  const meanNetSpread = mean(cohorts.map((record) => record.topBottomNetReturn));
  const meanTurnover = mean(cohorts.map((record) => record.turnover));
  const qValues = cohorts.map((record) => record.qValue).filter(Number.isFinite);
  const qValue = median(qValues);
  const completeFdrCoverage = nCohorts > 0 && qValues.length === nCohorts;
  const directionConsistency = nCohorts ? cohorts.filter((record) => record.spearmanIc > 0).length / nCohorts : null;
  const significantCohorts = cohorts.filter((record) => Number.isFinite(record.qValue) && record.qValue <= POLICY.fdrQMax).length;
  const significantCohortShare = nCohorts ? significantCohorts / nCohorts : null;
  const icir = informationRatio(cohorts.map((record) => record.spearmanIc));
  const dataQualityGate = nCohorts && cohorts.every((record) => record.dataQualityGate === "pass") ? "pass" : "insufficient";
  const qualified = nCohorts >= POLICY.minMatureCohorts
    && completeFdrCoverage
    && meanIc >= POLICY.minMeanSpearmanIc
    && directionConsistency >= POLICY.minDirectionConsistency
    && significantCohortShare >= POLICY.minSignificantCohortShare
    && icir !== null && icir >= POLICY.minIcir
    && neutralMeanIc > 0
    && meanNetSpread > 0
    && dataQualityGate === "pass";

  return {
    identity,
    featureVersion: cohorts[0]?.featureVersion || records[0]?.featureVersion || "",
    holdingPeriod: cohorts[0]?.holdingPeriod || records[0]?.holdingPeriod || "",
    status: qualified ? "qualified" : nCohorts ? "observing" : "awaiting_forward_cohorts",
    nCohorts,
    oosStart: cohorts.map((record) => record.oosStart).filter(Boolean).sort().at(0) || "",
    oosEnd: cohorts.map((record) => record.oosEnd).filter(Boolean).sort().at(-1) || "",
    holdingPeriods: [...new Set(cohorts.map((record) => record.holdingPeriod).filter(Boolean))].sort(),
    meanSpearmanIc: round(meanIc),
    meanNeutralSpearmanIc: round(neutralMeanIc),
    icir: round(icir),
    directionConsistency: round(directionConsistency),
    significantCohortShare: round(significantCohortShare),
    completeFdrCoverage,
    qValue: round(qValue),
    meanTopBottomNetReturn: round(meanNetSpread),
    turnover: round(meanTurnover),
    dataQualityGate,
    cohorts: [...cohorts]
      .sort((a, b) => a.oosStart.localeCompare(b.oosStart))
      .map((record) => ({
        cohortId: record.cohortId,
        fdrFamilyId: record.fdrFamilyId,
        fdrFamilyHash: record.fdrFamilyHash,
        scoreFile: record.scoreFile,
        scoreSnapshotId: record.scoreSnapshotId,
        scoreSnapshotHash: record.scoreSnapshotHash,
        scoreAsOf: record.scoreAsOf,
        scoreTradableTimestamp: record.scoreTradableTimestamp,
        entryTimestamp: record.entryTimestamp,
        oosStart: record.oosStart,
        oosEnd: record.oosEnd,
        holdingPeriod: record.holdingPeriod,
        tradingDays: record.tradingDays,
        n: record.n,
        spearmanIc: round(record.spearmanIc),
        neutralSpearmanIc: round(record.neutralSpearmanIc),
        topBottomNetReturn: round(record.topBottomNetReturn),
        turnover: round(record.turnover),
        pValue: round(record.permutationPValue),
        qValue: round(record.qValue),
        sourceEvalFile: record.sourceEvalFile,
      })),
  };
}

function emptySeries(identity = "") {
  const parts = parseSeriesIdentity(identity);
  return {
    identity,
    featureVersion: parts?.featureVersion || "",
    holdingPeriod: parts?.holdingPeriod || "",
    nCohorts: 0,
    oosStart: "",
    oosEnd: "",
    holdingPeriods: parts?.holdingPeriod ? [parts.holdingPeriod] : [],
    meanSpearmanIc: null,
    meanNeutralSpearmanIc: null,
    icir: null,
    directionConsistency: null,
    significantCohortShare: null,
    completeFdrCoverage: false,
    qValue: null,
    meanTopBottomNetReturn: null,
    turnover: null,
    dataQualityGate: "insufficient",
    cohorts: [],
    status: "awaiting_forward_cohorts",
  };
}

function selectNonOverlappingCohorts(records) {
  const sorted = [...records].sort((a, b) => a.oosEnd.localeCompare(b.oosEnd) || a.oosStart.localeCompare(b.oosStart));
  const selected = [];
  let lastEnd = "";
  for (const record of sorted) {
    if (lastEnd && record.oosStart <= lastEnd) continue;
    selected.push(record);
    lastEnd = record.oosEnd;
  }
  return selected;
}

export function isMatureAlphaRecord(record, today = todayIsoDate()) {
  return completedRecordValidationErrors(record, today).length === 0;
}

export function completedRecordValidationErrors(record, today = todayIsoDate()) {
  const errors = [];
  if (record.layer !== "alpha") errors.push("layer_not_alpha");
  if (record.status !== "completed") errors.push("status_not_completed");
  if (record.dataQualityGate !== "pass") errors.push("data_quality_not_pass");
  if (!/^N\d{2}$/u.test(String(record.featureId || ""))) errors.push("invalid_feature_id");
  if (!record.fileFeatureName || record.featureName !== record.fileFeatureName) errors.push("feature_name_mismatch");
  if (!record.featureVersion || /[@\s]/u.test(record.featureVersion)) errors.push("invalid_feature_version");
  if (!isIsoDate(record.fileFormationDate) || !isIsoDate(record.scoreAsOf)
    || record.fileFormationDate !== record.scoreAsOf) errors.push("formation_date_mismatch");
  if (!isIsoDate(record.evaluationDate) || record.evaluationDate > today) errors.push("invalid_or_future_evaluation_date");
  if (!isIsoDate(record.oosStart) || !isIsoDate(record.oosEnd)) errors.push("invalid_oos_date");
  if (isIsoDate(record.oosEnd) && isIsoDate(record.evaluationDate) && record.oosEnd > record.evaluationDate) errors.push("oos_not_mature_at_evaluation");
  if (isIsoDate(record.oosEnd) && record.oosEnd > today) errors.push("oos_end_in_future");
  if (!ALLOWED_HOLDING_PERIODS.has(record.holdingPeriod)) errors.push("invalid_holding_period");
  if (!Number.isInteger(record.tradingDays)
    || HOLDING_DAYS.get(record.holdingPeriod) !== record.tradingDays) errors.push("trading_days_mismatch");
  if (canonicalHoldingPeriod(record.returnWindowLabel) !== record.holdingPeriod) errors.push("filename_window_mismatch");
  if (record.isPrimaryHorizon !== true) errors.push("not_primary_horizon");
  if (!isIsoTimestamp(record.scoreTradableTimestamp)) errors.push("invalid_score_tradable_timestamp");
  if (!isIsoTimestamp(record.entryTimestamp)) errors.push("invalid_entry_timestamp");
  if (isIsoDate(record.scoreAsOf) && isIsoDate(record.oosStart) && record.scoreAsOf > record.oosStart) errors.push("score_after_oos_start");
  if (isIsoTimestamp(record.scoreTradableTimestamp) && isIsoDate(record.scoreAsOf)
    && record.scoreTradableTimestamp.slice(0, 10) < record.scoreAsOf) errors.push("tradable_before_score_as_of");
  if (isIsoTimestamp(record.entryTimestamp) && isIsoDate(record.oosStart)
    && record.entryTimestamp.slice(0, 10) !== record.oosStart) errors.push("entry_date_mismatch");
  if (isIsoTimestamp(record.entryTimestamp) && isIsoTimestamp(record.scoreTradableTimestamp)
    && Date.parse(record.entryTimestamp) <= Date.parse(record.scoreTradableTimestamp)) errors.push("entry_not_after_score_tradable");
  if (isIsoDate(record.oosStart) && isIsoDate(record.oosEnd) && record.oosStart > record.oosEnd) errors.push("oos_date_order");
  if (!Number.isInteger(record.n) || record.n < POLICY.minSampleSize) errors.push("sample_too_small");
  if (!inRange(record.spearmanIc, -1, 1)) errors.push("invalid_spearman_ic");
  if (!inRange(record.neutralSpearmanIc, -1, 1)) errors.push("invalid_neutral_spearman_ic");
  if (!Number.isFinite(record.topBottomNetReturn)) errors.push("invalid_top_bottom_return");
  if (!inRange(record.quintileMonotonicity, -1, 1)) errors.push("invalid_quintile_monotonicity");
  if (!inRange(record.turnover, 0, 1)) errors.push("invalid_turnover");
  if (!inRange(record.transactionCost, 0, 1)) errors.push("invalid_transaction_cost");
  if (!inRange(record.permutationPValue, 0, 1)) errors.push("invalid_permutation_p_value");
  validateFrozenIdentity(record, errors);
  return [...new Set(errors)];
}

function validateFrozenIdentity(record, errors) {
  if (!record.cohortId) errors.push("missing_cohort_id");
  if (!record.fdrFamilyId) errors.push("missing_fdr_family_id");
  const rawMembers = Array.isArray(record.fdrFamilyMembers) ? record.fdrFamilyMembers : [];
  const members = canonicalFamilyMembers(rawMembers);
  if (!rawMembers.length || members.length !== rawMembers.length
    || rawMembers.join("\n") !== members.join("\n")
    || !members.every((member) => FAMILY_MEMBER_RE.test(member))) errors.push("invalid_fdr_family_members");
  const memberFeatureIds = members.map((member) => parseSeriesIdentity(member)?.featureId).filter(Boolean);
  if (new Set(memberFeatureIds).size !== memberFeatureIds.length) errors.push("multiple_versions_for_one_feature_in_fdr_family");
  if (!HASH_RE.test(record.fdrFamilyHash)
    || (members.length && computeFamilyHash(members) !== record.fdrFamilyHash)) errors.push("fdr_family_hash_mismatch");
  if (members.length && !members.includes(seriesIdentity(record))) errors.push("feature_not_in_fdr_family");
  if (members.some((member) => parseSeriesIdentity(member)?.holdingPeriod !== record.holdingPeriod)) errors.push("mixed_holding_period_fdr_family");
  if (!record.scoreSnapshotId) errors.push("missing_score_snapshot_id");
  if (!HASH_RE.test(record.scoreSnapshotHash)) errors.push("invalid_score_snapshot_hash");
  if (!scoreFileMatchesRecord(record)) errors.push("score_file_identity_mismatch");
  if (!record.actualScoreSnapshotHash || record.actualScoreSnapshotHash !== record.scoreSnapshotHash) errors.push("score_snapshot_hash_mismatch");
  if (!HASH_RE.test(record.universeHash)) errors.push("invalid_universe_hash");
  if (!record.returnSeriesId) errors.push("missing_return_series_id");
  if (!record.returnMethod) errors.push("missing_return_method");
  if (!record.entryRule) errors.push("missing_entry_rule");
  if (!record.permutationSeed) errors.push("missing_permutation_seed");
}

function isIdentityObservation(record, today) {
  return record.layer === "alpha"
    && ["completed", "immature", "data_failed"].includes(record.status)
    && /^N\d{2}$/u.test(String(record.featureId || ""))
    && Boolean(record.fileFeatureName)
    && record.featureName === record.fileFeatureName
    && Boolean(record.featureVersion)
    && !/[@\s]/u.test(record.featureVersion)
    && isIsoDate(record.scoreAsOf)
    && isIsoDate(record.fileFormationDate)
    && record.scoreAsOf === record.fileFormationDate
    && isIsoDate(record.evaluationDate)
    && record.evaluationDate <= today
    && ALLOWED_HOLDING_PERIODS.has(record.holdingPeriod)
    && canonicalHoldingPeriod(record.returnWindowLabel) === record.holdingPeriod
    && record.isPrimaryHorizon === true;
}

export function seriesIdentity(record) {
  return `${record.featureId}@${record.featureVersion}@${record.holdingPeriod}`;
}

function parseSeriesIdentity(identity) {
  const match = String(identity || "").match(FAMILY_MEMBER_RE);
  return match ? { featureId: match[1], featureVersion: match[2], holdingPeriod: match[3] } : null;
}

export function canonicalFamilyMembers(members) {
  return [...new Set((Array.isArray(members) ? members : [])
    .map((member) => String(member || "").trim())
    .filter(Boolean))].sort();
}

export function computeFamilyHash(members) {
  return createHash("sha256").update(canonicalFamilyMembers(members).join("\n"), "utf8").digest("hex");
}

function parseFamilyMembers(value) {
  const text = String(value || "").trim();
  if (!text) return [];
  try {
    const parsed = JSON.parse(text);
    if (Array.isArray(parsed)) return parsed.map((member) => String(member).trim()).filter(Boolean);
  } catch {
    // Accept a concise comma-separated fallback for manually written reports.
  }
  return text.split(/[,，;；\s]+/u).map((member) => member.trim()).filter(Boolean);
}

function canonicalHoldingPeriod(label) {
  const normalized = String(label || "").trim().toLowerCase().replace(/\s+/gu, "");
  const aliases = new Map([
    ["21d", "21d"], ["21天", "21d"], ["1个月", "21d"],
    ["63d", "63d"], ["63天", "63d"], ["3个月", "63d"],
    ["126d", "126d"], ["126天", "126d"], ["6个月", "126d"],
    ["252d", "252d"], ["252天", "252d"], ["12个月", "252d"], ["1年", "252d"],
  ]);
  return aliases.get(normalized) || "";
}

function compareRecordRecency(a, b) {
  return `${a.evaluationDate}|${a.scoreAsOf}|${a.sourceEvalFile}`
    .localeCompare(`${b.evaluationDate}|${b.scoreAsOf}|${b.sourceEvalFile}`);
}

function countRejectionReasons(records, today) {
  const counts = new Map();
  for (const record of records) {
    for (const reason of completedRecordValidationErrors(record, today)) {
      counts.set(reason, (counts.get(reason) || 0) + 1);
    }
  }
  return Object.fromEntries([...counts.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

function informationRatio(values) {
  const clean = values.filter(Number.isFinite);
  if (clean.length < 2) return null;
  const avg = mean(clean);
  const variance = clean.reduce((sum, value) => sum + ((value - avg) ** 2), 0) / (clean.length - 1);
  const sd = Math.sqrt(variance);
  return sd > 0 ? avg / sd : null;
}

function mean(values) {
  const clean = values.filter(Number.isFinite);
  return clean.length ? clean.reduce((sum, value) => sum + value, 0) / clean.length : null;
}

function median(values) {
  const clean = values.filter(Number.isFinite).sort((a, b) => a - b);
  if (!clean.length) return null;
  const middle = Math.floor(clean.length / 2);
  return clean.length % 2 ? clean[middle] : (clean[middle - 1] + clean[middle]) / 2;
}

function round(value) {
  return Number.isFinite(value) ? Number(value.toFixed(6)) : null;
}

function inRange(value, minimum, maximum) {
  return Number.isFinite(value) && value >= minimum && value <= maximum;
}

function field(fields, key) {
  const value = String(fields.get(key) || "").trim();
  return /^(?:NA|null|-)$/iu.test(value) ? "" : value;
}

function numberField(fields, key) {
  const value = field(fields, key);
  if (!value) return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function booleanField(fields, key) {
  const value = field(fields, key).toLowerCase();
  if (["true", "1", "yes", "是"].includes(value)) return true;
  if (["false", "0", "no", "否"].includes(value)) return false;
  return null;
}

function normalizeHash(value) {
  return String(value || "").trim().toLowerCase().replace(/^sha256:/u, "");
}

function scoreFileMatchesRecord(record) {
  const prefix = "基本面/特征量化/量化评分/";
  if (!String(record.scoreFile || "").startsWith(prefix)) return false;
  const fileName = record.scoreFile.slice(prefix.length);
  if (!fileName || fileName.includes("/")) return false;
  const match = fileName.match(/^(N\d{2})_(.+)_量化评分_(\d{4}-\d{2}-\d{2})\.md$/u);
  return Boolean(match
    && match[1] === record.featureId
    && match[2] === record.fileFeatureName
    && match[3] === record.scoreAsOf);
}

async function hashScoreSnapshot(projectPath) {
  const normalized = String(projectPath || "").replace(/\\/gu, "/");
  const prefix = "基本面/特征量化/量化评分/";
  if (!normalized.startsWith(prefix) || normalized.split("/").some((part) => !part || part === "." || part === "..")) return "";
  const absolute = path.join(PROJECT_ROOT, ...normalized.split("/"));
  try {
    const content = await fs.readFile(absolute);
    return createHash("sha256").update(content).digest("hex");
  } catch {
    return "";
  }
}

export function isIsoDate(value) {
  const text = String(value || "");
  if (!/^\d{4}-\d{2}-\d{2}$/u.test(text)) return false;
  const parsed = new Date(`${text}T00:00:00.000Z`);
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === text;
}

function isIsoTimestamp(value) {
  const text = String(value || "");
  return /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})$/u.test(text)
    && isIsoDate(text.slice(0, 10))
    && Number.isFinite(Date.parse(text));
}

export function todayIsoDate(now = new Date()) {
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

async function safeReadDir(dir) {
  try {
    return await fs.readdir(dir);
  } catch {
    return [];
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
}
