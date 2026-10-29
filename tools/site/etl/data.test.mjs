import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { safeInside, reportSections, reportSummary, parseCompanyIndex, assertPublicContent, digest } from './lib/common.mjs';
import { validateStructured, buildStructured } from './lib/structured.mjs';

function sample() {
  return {
    ticker: 'DEMO', research_date: '2026-10-22', information_cutoff: '2026-10-22T13:00:00-07:00',
    reference_price: { value: 100, date: '2026-10-22', currency: 'USD' }, target_date: '2030-10-22',
    scenarios: Object.fromEntries(['bear', 'base', 'bull', 'breakthrough'].map(key => [key, { dcf_price: [80, 80], business_price: [100, 120], target_price: [90, 150], evidence: 'medium' }])),
  };
}

test('null prices remain inapplicable rather than becoming a zero return', () => {
  const raw = sample();
  for (const scenario of Object.values(raw.scenarios)) scenario.dcf_price = scenario.business_price = scenario.target_price = null;
  assert.equal(validateStructured(raw, 'scenario').scenarios.base.target_price, null);
});

test('reversed intervals, zero reference prices and invalid evidence cannot publish', () => {
  const reversed = sample(); reversed.scenarios.base.target_price = [150, 100];
  assert.throws(() => validateStructured(reversed, 'scenario'), /Invalid base.target_price/);
  const badPrice = sample(); badPrice.reference_price.value = 0;
  assert.throws(() => validateStructured(badPrice, 'scenario'), /Invalid reference price/);
  const badEvidence = sample(); badEvidence.scenarios.bull.evidence = 0.6;
  assert.throws(() => validateStructured(badEvidence, 'scenario'), /evidence/);
});

test('comparison contract preserves insufficient evidence, unknown views and priority allocation', () => {
  const raw = sample();
  for (const scenario of Object.values(raw.scenarios)) scenario.review = 'adopt';
  raw.views = Object.fromEntries(['near_term_delivery', 'long_term_compounding', 'base_valuation', 'upside_potential', 'downside_resilience', 'relative_attractiveness'].map(key => [key, 'unknown']));
  raw.decision = { steady_allocation: 'priority_configure', offense_allocation: 'avoid', near_term_timing: 'wait_for_trigger' };
  raw.comparisons = [{ peer: 'PEER', relation: 'opportunity_cost', compounding_preference: 'insufficient', convexity_preference: 'insufficient', verdict: 'insufficient', reason: 'Evidence is insufficient.' }];
  assert.equal(validateStructured(raw, 'comparison'), raw);
  for (const key of ['compounding_preference', 'convexity_preference', 'verdict']) {
    const invalid = structuredClone(raw);
    invalid.comparisons[0][key] = 'unsupported';
    assert.throws(() => validateStructured(invalid, 'comparison'), /Invalid/);
  }
  const badView = structuredClone(raw); badView.views.base_valuation = 'unsupported';
  assert.throws(() => validateStructured(badView, 'comparison'), /Invalid view/);
  const badDecision = structuredClone(raw); badDecision.decision.steady_allocation = 'unsupported';
  assert.throws(() => validateStructured(badDecision, 'comparison'), /Invalid decision/);
});

test('output path checks reject the root itself and siblings', () => {
  const root = path.resolve(os.tmpdir(), 'ananta-boundary');
  assert.throws(() => safeInside(root, root));
  assert.throws(() => safeInside(root, path.join(root, '..', 'ananta-boundary-other', 'data')));
  assert.equal(safeInside(root, path.join(root, 'data')), path.join(root, 'data'));
});

test('report section ids are unique and fenced headings do not create sections', () => {
  const markdown = '# Report\r\n\r\nIntro\r\n\r\n## Same\r\n\r\n```js\r\n# fake\r\n```\r\n\r\n## Same\r\n\r\nBody';
  const sections = reportSections(markdown);
  assert.equal(sections.length, 3);
  assert.equal(new Set(sections.map(s => s.id)).size, 3);
  assert.ok(sections.every(s => s.title !== 'fake'));
});

test('a newer Markdown without companion JSON supersedes an older structured result explicitly', async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'ananta-data-'));
  const base = path.join(root, '分析报告', '公司情景投资决策');
  const output = path.join(root, 'site-output');
  await fs.mkdir(path.join(base, '结构化数据'), { recursive: true });
  await fs.mkdir(path.join(base, '结果'), { recursive: true });
  const oldName = 'DEMO_report_2026-10-22';
  const oldJson = path.join(base, '结构化数据', `${oldName}.json`);
  await fs.writeFile(oldJson, JSON.stringify(sample()));
  await fs.writeFile(path.join(base, '结果', `${oldName}.md`), '# Old result\n\nOriginal formal research.');
  await fs.writeFile(path.join(base, '结果', 'DEMO_report_2026-10-23.md'), '# New result\n\nLatest formal research without JSON.');
  const before = digest(await fs.readFile(oldJson));
  try {
    const reports = await buildStructured({ root, output, kind: 'scenario', directory: '公司情景投资决策', manifest: new Map(), warnings: [] });
    const latest = reports.get('DEMO');
    assert.equal(latest.date, '2026-10-23');
    assert.equal(latest.summary.structuredAvailable, false);
    assert.equal(latest.detail.raw, null);
    assert.equal(latest.summary.priceApplicable, false);
    assert.equal(digest(await fs.readFile(oldJson)), before, 'formal source was changed');
    assert.match(latest.detail.markdown, /New result/);
  } finally { await fs.rm(root, { recursive: true, force: true }); }
});

test('duplicate company identities and likely private keys are blocked', () => {
  assert.throws(() => parseCompanyIndex('| ABC | Alpha | `Sector/` |\n| ABC | Beta | `Sector/` |'), /Duplicate/);
  assert.throws(() => assertPublicContent('-----BEGIN PRIVATE KEY-----', 'fixture'), /private content/);
  assert.doesNotThrow(() => assertPublicContent('https://news.skhynix.com/en/sk-hynix-ships-samples-of-12-layer-next-gen-hbm4e-2/', 'public citation'));
});

test('research excerpts prefer substantive opening judgment over metadata and later source keyword matches', () => {
  const judgment = '公司的经济底座是已进入客户生产线的功能材料，当前更有证据支持交付和制造效率改善带来的成熟业务修复；新业务尚未成为主要利润来源。';
  const markdown = `# Company\r\n\r\n研究截止：2026年10月22日。金额全部采用美元，证券身份为普通股，资料采用最近季度报告及监管文件，本文不提供目标价格。\r\n\r\n## 一、当前判断与决定性边界\r\n\r\n**${judgment}**\r\n\r\n## 附录：来源底稿\r\n\r\n- L1：基本面/行业调研/结果/Example.md，核心判断用于技术边界以及合格供给核对，不应当作公司的核心结论。\r\n\r\n- DEF 14A：本次未找到适用代理文件，核心判断需要通过其他治理文件核对，不应当用其他公司的报告替代。`;
  assert.equal(reportSummary(markdown), judgment);
});
