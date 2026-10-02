import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";
import { featureIdentityFromStem } from "../domains/feature-contract.mjs";

export function buildFeatureQuantizationFormalPrompt(item, domain, outputContract) {
  const entry = domain.resolveIndexEntry(item.subject);
  if (!entry) throw new Error(`feature-quantization plan not found: ${item.subject}`);
  const identity = featureIdentityFromStem(entry.subject);
  const versionField = identity.featureId.startsWith("G") ? "gate_version" : "feature_version";
  const metadataContract = `
## 机器可读评分元数据

正式结果必须包含以下两列表。字段名不得改写或重复；\`as_of_date\` 固定为本次截面日期；\`${versionField}\` 使用能够区分方法版本的非空稳定标识；\`score_tradable_timestamp\` 必须是带时区的 ISO-8601 时间。

| 字段 | 值 |
|---|---|
| feature_id | ${identity.featureId} |
| feature_name | ${identity.featureName} |
| ${versionField} | 非空稳定版本标识 |
| as_of_date | ${outputContract.runDate} |
| score_tradable_timestamp | 带时区的 ISO-8601 时间，且不得早于 as_of_date |
`;
  return `${readUtf8(entry.planPath).trim()}\n\n${metadataContract.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
