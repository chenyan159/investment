import { buildOutputInstruction } from "./common.mjs";
import { readResearchPlan } from "../research-plan-store.mjs";

export function buildFileRunFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readResearchPlan(item);
  return `${sourcePrompt.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
