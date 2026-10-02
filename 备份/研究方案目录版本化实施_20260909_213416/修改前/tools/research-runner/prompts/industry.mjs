import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";

export function buildIndustryFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readUtf8(domain.promptPath);
  const replaced = sourcePrompt.replaceAll(domain.placeholder, item.subject);
  const researchScope = domain.resolveIndexEntry?.(item.subject)?.researchScope;
  const scopeInstruction = researchScope
    ? `\n\n## 本专题研究范围提示\n\n${researchScope}\n\n此提示用于划清主责与相邻专题的交叉关系，不是行业事实或预设结论。可以质疑边界或探索更重要的机制，并说明理由。`
    : "";
  return `${replaced.trim()}${scopeInstruction}\n\n${buildOutputInstruction(outputContract)}`;
}
