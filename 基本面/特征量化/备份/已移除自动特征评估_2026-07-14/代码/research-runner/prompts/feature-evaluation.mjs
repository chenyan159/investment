import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";
import { normalizeHoldingPeriod } from "../domains/feature-contract.mjs";

export function buildFeatureEvaluationFormalPrompt(item, domain, outputContract) {
  const { featureId, featureName } = parseFeatureSubject(item.subject);
  const featureSubject = `${featureId}_${featureName}`;
  const holdingPeriod = getHoldingPeriod(item);
  if (!item?.scoreFile || !item?.scoreDate || !item?.holdingPeriod) {
    throw new Error(`feature-evaluation item must lock scoreFile, scoreDate, and holdingPeriod: ${item?.subject || ""}`);
  }
  const sourcePrompt = readUtf8(domain.promptPath)
    .replaceAll("{feature_subject}", featureSubject)
    .replaceAll("{feature_id}", featureId)
    .replaceAll("{feature_name}", featureName)
    .replaceAll("{return_window}", holdingPeriod)
    .replaceAll("{score_file}", String(item?.scoreFile || ""))
    .replaceAll("{score_date}", String(item?.scoreDate || ""));

  const lockContract = `
## 本次锁定输入

- score_file：\`${item.scoreFile}\`
- score_date：${item.scoreDate}
- holding_period：${holdingPeriod}
- feature_version：${item.featureVersion}
- score_tradable_timestamp：${item.scoreTradableTimestamp}

机器可读登记表必须额外包含 \`score_file\` 行，并使上述字段与锁定输入逐字一致。不得改用其他评分快照、形成日或持有期。
`;

  return `${sourcePrompt.trim()}\n\n${lockContract.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}

export function getHoldingPeriod(item) {
  return normalizeHoldingPeriod(item?.holdingPeriod || item?.returnWindow || "126d", "holdingPeriod");
}

export function parseFeatureSubject(subject) {
  const cleaned = String(subject || "").trim()
    .replace(/\.md$/iu, "")
    .replace(/_研究方案$/u, "")
    .replace(/_量化评分_\d{4}-\d{2}-\d{2}$/u, "");
  const match = cleaned.match(/^(N\d{2})_(.+)$/u);
  if (!match) return { featureId: cleaned || "Nxx", featureName: "特征" };
  return { featureId: match[1], featureName: match[2] };
}

export function safeFeatureFilePart(value, fallback) {
  const cleaned = String(value || "")
    .trim()
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, "_")
    .replace(/\s+/g, "_")
    .replace(/^_+|_+$/g, "");
  return (cleaned || fallback).slice(0, 100);
}
