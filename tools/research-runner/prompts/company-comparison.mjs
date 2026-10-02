import { buildOutputInstruction } from "./common.mjs";
import { readResearchPlan } from "../research-plan-store.mjs";

export function buildCompanyComparisonFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readResearchPlan(item);
  const replaced = sourcePrompt
    .replaceAll(domain.placeholder, item.subject)
    .replaceAll("<公司A股票代号>", item.subject);
  return `${replaced.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
