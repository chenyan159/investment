export function buildOutputInstruction(outputContract = {}) {
  if (outputContract.expectedOutputFile) {
    return `\n## 本次输出\n\n将完整研究结果写入 \`${outputContract.expectedOutputFile}\`。不得更改该路径，也不得创建第二份正式报告。\n`;
  }
  return `\n## 本次输出\n\n在 \`${outputContract.expectedOutputDir}\` 内只生成或更新一份完整研究结果；不得修改输入研究方案。\n`;
}
