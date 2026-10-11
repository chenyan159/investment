import { buildOutputInstruction } from "./common.mjs";
import { readResearchPlan } from "../research-plan-store.mjs";

export function buildBackgroundFormalPrompt(item, outputContract) {
  let sourcePrompt = readResearchPlan(item);
  if (item.backgroundKind === "conference") {
    sourcePrompt = sourcePrompt
      .replaceAll("【会议名称】", item.conferenceSeries)
      .replaceAll("【会议年份】", item.conferenceYear);
  }
  return `${sourcePrompt.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
