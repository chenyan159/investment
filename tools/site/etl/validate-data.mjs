import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { SCENARIOS, safeInside, filesUnder, digest } from './lib/common.mjs';
import { validateStructured } from './lib/structured.mjs';

export async function validateData(directory) {
  const dataRoot = path.resolve(directory);
  const load = async relative => JSON.parse(await fs.readFile(safeInside(dataRoot, path.join(dataRoot, relative)), 'utf8'));
  const index = await load('index.json'), meta = await load('meta.json'), manifest = await load('source-manifest.json');
  assert.equal(index.schemaVersion, 1);
  assert.deepEqual(index.meta, meta);
  assert.equal(meta.buildId, manifest.buildId);
  assert.equal(meta.buildId, digest(JSON.stringify(manifest.sources)).slice(0, 16));
  const permittedSources = /^(分析报告\/(公司情景投资决策|公司对比)\/(结果|结构化数据)\/|基本面\/(产业背景|行业调研|公司调研)\/结果\/|基本面\/(公司调研\/公司索引|行业调研\/行业索引)\.md$)/u;
  for (const entry of manifest.sources) assert.ok(permittedSources.test(entry.source), `Unexpected source ${entry.source}`);
  const tickers = new Set();
  let scenarioCount = 0, comparisonCount = 0, comparisonReports = 0, peerCount = 0;
  for (const company of index.companies) {
    assert.ok(!tickers.has(company.ticker), `Duplicate ticker ${company.ticker}`);
    tickers.add(company.ticker);
    const detail = await load(`companies/${company.ticker}.json`);
    assert.equal(detail.ticker, company.ticker);
    for (const kind of ['scenario', 'comparison']) {
      const report = detail[kind];
      assert.equal(Boolean(company[kind]), Boolean(report));
      if (!report) continue;
      if (report.structuredAvailable) {
        validateStructured(report.raw, kind, report.source);
        assert.equal(report.raw.ticker, company.ticker);
        assert.deepEqual(report.scenarios, report.raw.scenarios);
        assert.deepEqual(company[kind].scenarios, report.raw.scenarios);
        assert.deepEqual(await load(`structured/${kind}/${company.ticker}.json`), report.raw);
      } else {
        assert.equal(report.raw, null);
        assert.equal(report.priceApplicable, false);
        assert.deepEqual(report.scenarios, {});
      }
      assert.ok(report.markdown.length > 200, `Unexpectedly empty ${kind} report: ${company.ticker}`);
      assert.ok(report.sections.length > 0);
      for (const scenario of report.structuredAvailable ? SCENARIOS : []) {
        const prices = report.scenarios[scenario].target_price;
        if (prices !== null) assert.ok(prices.every(price => Number.isFinite(price / report.reference_price.value - 1)));
      }
      assert.equal(report.reportUrl, null, 'Markdown downloads are generated from the complete body in the browser');
      if (kind === 'scenario') scenarioCount++;
      else { comparisonReports++; if (report.structuredAvailable) comparisonCount++; peerCount += report.comparisons.length; }
    }
  }
  const ids = new Set();
  for (const summary of index.research) {
    assert.ok(!ids.has(summary.id)); ids.add(summary.id);
    const report = await load(`research/${summary.id}.json`);
    assert.equal(report.title, summary.title);
    assert.equal(report.source, summary.source);
    assert.ok(report.markdown.length > 200);
    assert.ok(report.sections.length > 0);
    assert.equal(report.reportUrl, null);
  }
  assert.equal(meta.counts.companies, tickers.size);
  assert.equal(meta.counts.scenarios, scenarioCount);
  assert.equal(meta.counts.comparisons, comparisonCount);
  assert.equal(meta.counts.comparisonReports, comparisonReports);
  assert.equal(meta.counts.peerComparisons, peerCount);
  for (const [kind, key] of [['company', 'companyResearch'], ['industry', 'industries'], ['background', 'backgrounds']]) assert.equal(meta.counts[key], index.research.filter(r => r.kind === kind).length);
  const files = await filesUnder(dataRoot, '.json');
  for (const file of files) JSON.parse(await fs.readFile(file, 'utf8'));
  return { jsonFiles: files.length, companies: tickers.size, researchReports: ids.size, peerComparisons: peerCount };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const directory = process.argv.find(arg => arg.startsWith('--dir='))?.slice(6) ?? path.join(site, 'public/data');
  console.log(JSON.stringify({ ok: true, ...await validateData(path.resolve(directory)) }, null, 2));
}
