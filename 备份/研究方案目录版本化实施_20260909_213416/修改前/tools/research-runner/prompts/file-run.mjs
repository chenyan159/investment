import { buildOutputInstruction } from "./common.mjs";
import { readUtf8 } from "../queue-store.mjs";

export function buildFileRunFormalPrompt(item, domain, outputContract) {
  const sourcePrompt = readUtf8(domain.resolvePromptFilePath(item.promptFile));
  return `${sourcePrompt.trim()}\n\n${buildOutputInstruction(outputContract)}`;
}
