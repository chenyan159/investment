import { buildOutputInstruction } from "./common.mjs";
import { readResearchPlan } from "../research-plan-store.mjs";

export function buildCompanySentimentFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readResearchPlan(item);
  const replaced = sourcePrompt.replaceAll(domain.placeholder, item.subject);
  return `${replaced.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
