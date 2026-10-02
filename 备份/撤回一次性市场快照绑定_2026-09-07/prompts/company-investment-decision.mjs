import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";

export function buildCompanyInvestmentDecisionFormalPrompt(
  item,
  domain,
  outputContract,
  marketSnapshot,
) {
  const sourcePrompt = readUtf8(domain.promptPath);
  const replaced = sourcePrompt
    .replaceAll(domain.placeholder, item.subject)
    .replaceAll("<公司股票代号>", item.subject);
  return `${replaced.trim()}\n\n${buildSharedMarketSnapshotInstruction(marketSnapshot)}\n\n${buildOutputInstruction(outputContract)}`;
}

function buildSharedMarketSnapshotInstruction(marketSnapshot) {
  if (!marketSnapshot?.content) {
    throw new Error("company-investment-decision prompt requires a validated shared market snapshot");
  }
  return `## 本批次唯一共享市场快照（执行器硬约束）

- 批次 ID：\`${marketSnapshot.batchId}\`
- 研究截止日：\`${marketSnapshot.sourceDate}\`
- 市场范围：${marketSnapshot.marketScope}
- 快照文件：\`${marketSnapshot.snapshotFile}\`
- SHA-256：\`${marketSnapshot.sha256}\`

执行器已读取并固定下面这份快照。必须原样复用其中的快照身份、五块记分板、主状态、唯一相邻状态和总体证据强度；不得联网重建、重新分类或按目标公司选择更有利的市场列。公司特有信息只能用于板块轮动修正、估值敏感度和经营情景，不能改变共享市场状态。批量执行已经具备可复核快照，因此研究方案中“无法获得共享快照时写为边界 / 未锁定”的降级规则不适用于本次任务。若快照与其他资料冲突，以本快照的市场状态分类为准，并只记录冲突而不改写分类。

报告第 1 节“研究快照”必须逐项回显上面的批次 ID、快照文件、SHA-256，以及快照正文中的快照 ID、公司价格与估值锚路径和锚点时刻。不得用目标公司报告中的其他盘中价格替换统一价格锚；任何一项身份字段缺失或不一致都视为本报告未完成。

<shared_market_snapshot>
${marketSnapshot.content.trim()}
</shared_market_snapshot>`;
}
