export function buildOutputInstruction(outputContract = {}) {
  if (outputContract.expectedCompanionFile) {
    return `\n## 本次输出\n\nMD：\`${outputContract.expectedOutputFile}\`\nJSON：\`${outputContract.expectedCompanionFile}\`\n两份均须交付，路径固定；字段按方案。临时材料放结果目录同级 tmp/，不另建正式文件。\n`;
  }
  const directoryRule = formalDirectoryInstruction(outputContract.expectedOutputFile || "");
  if (outputContract.expectedOutputFile) {
    return `\n## 本次输出\n\n将完整研究结果写入 \`${outputContract.expectedOutputFile}\`。不得更改该路径，也不得创建第二份正式报告。\n${directoryRule}`;
  }
  return `\n## 本次输出\n\n在 \`${outputContract.expectedOutputDir}\` 内只生成或更新一份完整研究结果；不得修改输入研究方案。\n`;
}

function formalDirectoryInstruction(outputFile) {
  const stages = [
    ["基本面/公司调研/结果/", "基本面/公司调研/tmp/"],
    ["基本面/行业调研/结果/", "基本面/行业调研/tmp/"],
    ["分析报告/公司情景投资决策/结果/", "分析报告/公司情景投资决策/tmp/"],
    ["分析报告/公司对比/结果/", "分析报告/公司对比/tmp/"],
    ["情绪面/公司情绪/", "情绪面/_work/"],
    ["基本面/特征量化/量化评分/", "基本面/特征量化/_work/"],
  ];
  const stage = stages.find(([prefix]) => outputFile.startsWith(prefix));
  if (!stage) return "";
  return `\n正式报告目录只存放正式报告，不得在其中建立备份、tmp、_work 或保存下载资料、脚本。临时材料写入 \`${stage[1]}\`；旧版备份由 runner 放在正式报告目录之外。读取上游报告时只从其正式结果目录选取，备份和临时目录不作为研究输入；索引只用于定位。\n`;
}
