import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { buildCompanyComparisonFormalPrompt } from "../prompts/company-comparison.mjs";
import { PROJECT_ROOT } from "../queue-store.mjs";

test("comparison prompt resolves both ticker placeholders and preserves the selected comparison set", () => {
  const dir = fs.mkdtempSync(path.join(PROJECT_ROOT, "分析报告/公司对比/tmp/prompt-test-"));
  try {
    const source = "# 研究对象：【公司股票代号】\n参数：【公司股票代号A】 / <公司A股票代号>\n自主选取 6—12 家比较公司，不设机械的凑数配额。\n";
    const file = path.join(dir, "plan.md");
    fs.writeFileSync(file, source);
    const output = "分析报告/公司对比/结果/MU_逐家公司投资思路对比_2026-10-09.md";
    const prompt = buildCompanyComparisonFormalPrompt(
      { domain: "file-run", subject: "MU", promptFile: file },
      { placeholder: "【公司股票代号A】" },
      { expectedOutputFile: output },
    );
    assert.ok(prompt.startsWith("# 研究对象：MU\n参数：MU / MU\n自主选取 6—12 家比较公司，不设机械的凑数配额。"));
    assert.doesNotMatch(prompt, /【公司股票代号A?】|<公司A股票代号>/u);
    assert.equal(prompt.split(output).length - 1, 1);
  } finally {
    const checked = path.resolve(dir);
    const allowed = path.resolve(PROJECT_ROOT, "分析报告/公司对比/tmp") + path.sep;
    assert.ok(checked.startsWith(allowed));
    fs.rmSync(checked, { recursive: true, force: true });
  }
});
