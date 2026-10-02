import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";

export function buildCompanySentimentFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readUtf8(domain.promptPath);
  const replaced = sourcePrompt.replaceAll(domain.placeholder, item.subject);
  return `${replaced.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
