import fs from 'node:fs';
import { fileRunDomain } from '../../tools/research-runner/domains/file-run.mjs';
import { buildFileRunFormalPrompt } from '../../tools/research-runner/prompts/file-run.mjs';

const cases=JSON.parse(fs.readFileSync(new URL('./入口预检用例.json',import.meta.url),'utf8'));
const checked=[];
for (const c of cases) {
  const item=fileRunDomain.createQueueItem(c);
  fileRunDomain.validateQueueItem(item);
  const compiled=buildFileRunFormalPrompt(item,fileRunDomain,item);
  const original=fs.readFileSync(fileRunDomain.resolvePromptFilePath(item.promptFile),'utf8');
  if (!compiled.startsWith(original.trim())) throw new Error(`Prompt lost: ${item.promptFile}`);
  if (!compiled.includes('2026-09-07')) throw new Error(`Version absent: ${item.promptFile}`);
  const bodyEnd=compiled.indexOf('## 本次输出');
  if (bodyEnd<original.trim().length) throw new Error('Unexpected output override');
  checked.push({prompt:item.promptFile,run_id:item.runId,compiled_characters:compiled.length,ok:true});
}
fs.writeFileSync(new URL('./运行入口预检.json',import.meta.url),JSON.stringify({checked,queue_written:false,research_started:false,scope:'Existing file-run creation, validation and prompt assembly, in memory only.'},null,2));
console.log(JSON.stringify({entries:checked.length,ok:true,queue_written:false}));
