import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { safeInside, readSource, parseCompanyIndex, parseIndustryIndex, writeJson, digest, renameWithRetry } from './lib/common.mjs';
import { buildStructured } from './lib/structured.mjs';
import { buildResearch } from './lib/research.mjs';
import { validateData } from './validate-data.mjs';

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.resolve(site, '../..');
const publicRoot = path.join(site, 'public');
const destination = safeInside(publicRoot, path.join(publicRoot, 'data'));
const staging = safeInside(site, path.join(site, '.build', `data-${process.pid}`));
const previous = safeInside(site, path.join(site, '.build', `previous-data-${process.pid}`));
const warnings = [], manifest = new Map();
await fs.mkdir(staging, { recursive: true });

try {
  const { text: companiesMarkdown } = await readSource(path.join(root, '基本面/公司调研/公司索引.md'), root, manifest);
  const { text: industriesMarkdown } = await readSource(path.join(root, '基本面/行业调研/行业索引.md'), root, manifest);
  const companyIndex = parseCompanyIndex(companiesMarkdown);
  const industryIndex = parseIndustryIndex(industriesMarkdown);
  const context = { root, output: staging, manifest, warnings };
  const scenarios = await buildStructured({ ...context, kind: 'scenario', directory: '公司情景投资决策' });
  const comparisons = await buildStructured({ ...context, kind: 'comparison', directory: '公司对比' });
  const research = await buildResearch({ ...context, companyIndex, industryIndex });
  const companyResearch = new Map(research.filter(r => r.summary.kind === 'company').map(r => [r.summary.ticker, r]));
  const tickers = [...new Set([...companyIndex.keys(), ...scenarios.keys(), ...comparisons.keys(), ...companyResearch.keys()])].sort();
  const companies = [];
  for (const ticker of tickers) {
    const scenario = scenarios.get(ticker), comparison = comparisons.get(ticker), report = companyResearch.get(ticker);
    const identity = companyIndex.get(ticker) ?? {
      ticker, name: report?.summary.name || ticker, sector: report?.summary.category || '未列入当前公司索引', tags: '', industries: [], notes: '当前公司索引未登记；保留正式报告供查阅。', indexed: false,
    };
    if (!identity.indexed) warnings.push(`${ticker} 未列入当前公司索引；正式报告保留供查阅，不视为当前登记投资样本。`);
    const summary = { ...identity, scenario: scenario?.summary ?? null, comparison: comparison?.summary ?? null, companyResearch: report?.summary ?? null, detailUrl: `data/companies/${encodeURIComponent(ticker)}.json` };
    await writeJson(staging, `companies/${ticker}.json`, { ...summary, scenario: scenario?.detail ?? null, comparison: comparison?.detail ?? null, companyResearch: report?.detail ?? null });
    companies.push(summary);
  }
  const dateRange = array => {
    const dates = array.filter(Boolean).sort();
    return { earliest: dates[0] ?? null, latest: dates.at(-1) ?? null };
  };
  const sourceEntries = [...manifest.values()].sort((a, b) => a.source.localeCompare(b.source, 'en'));
  const generatedAt = new Date().toISOString();
  const meta = {
    schemaVersion: 1, generatedAt, buildId: digest(JSON.stringify(sourceEntries)).slice(0, 16),
    counts: {
      companies: companies.length, indexedCompanies: companyIndex.size,
      scenarios: scenarios.size, pricedScenarios: [...scenarios.values()].filter(r => r.summary.priceApplicable).length,
      comparisons: [...comparisons.values()].filter(r => r.summary.structuredAvailable).length,
      comparisonReports: comparisons.size,
      peerComparisons: [...comparisons.values()].reduce((n, r) => n + r.summary.comparisons.length, 0),
      companyResearch: companyResearch.size,
      industries: research.filter(r => r.summary.kind === 'industry').length,
      backgrounds: research.filter(r => r.summary.kind === 'background').length,
      sourceFiles: sourceEntries.length,
    },
    dates: {
      scenarios: dateRange([...scenarios.values()].map(r => r.date)),
      comparisons: dateRange([...comparisons.values()].map(r => r.date)),
      companyResearch: dateRange([...companyResearch.values()].map(r => r.date)),
      industries: dateRange(research.filter(r => r.summary.kind === 'industry').map(r => r.date)),
      backgrounds: dateRange(research.filter(r => r.summary.kind === 'background').map(r => r.date)),
    },
    warnings: [...new Set(warnings)],
    sources: ['分析报告/公司情景投资决策', '分析报告/公司对比', '基本面/产业背景', '基本面/行业调研', '基本面/公司调研'],
    conventions: {
      referencePrice: '各报告自己的研究参考价与报价日期；非实时行情。',
      priceReturn: '(目标情景价格 ÷ 该报告参考价 − 1) × 100%，不含现金股息。',
      annualizedReturn: '((目标情景价格 ÷ 该报告参考价)^(365.25 ÷ 报价日至目标日天数) − 1) × 100%；非保证收益。',
      evidence: '证据等级描述经营假设支撑程度，不是情景发生概率。',
      comparison: '公司对比复核结果与原公司情景独立保留；不可将对比修正覆盖为原报告结论。',
      sourceBoundary: '只读取五个研究目录的正式结果、配套结构化数据及权威索引；不读取历史备份、队列、金融快照或研究方案。',
    },
  };
  await writeJson(staging, 'index.json', { schemaVersion: 1, generatedAt, meta, companies, research: research.map(r => r.summary) });
  await writeJson(staging, 'meta.json', meta);
  await writeJson(staging, 'source-manifest.json', { schemaVersion: 1, buildId: meta.buildId, generatedAt, sources: sourceEntries });
  const validation = await validateData(staging);
  // Recheck every source after building. If runner changed a paired MD/JSON during
  // generation, retain the last published data and ask for a fresh build.
  for (const entry of sourceEntries) {
    if (digest(await fs.readFile(path.join(root, entry.source))) !== entry.sha256) throw new Error(`Source changed during build: ${entry.source}`);
  }
  await fs.mkdir(publicRoot, { recursive: true });
  let movedOld = false;
  try {
    try { await renameWithRetry(destination, previous); movedOld = true; } catch (error) { if (error.code !== 'ENOENT') throw error; }
    await renameWithRetry(staging, destination);
  } catch (error) {
    if (movedOld) await renameWithRetry(previous, destination);
    throw error;
  }
  if (movedOld) await fs.rm(previous, { recursive: true, force: true });
  console.log(JSON.stringify({ ok: true, ...meta, validation }, null, 2));
} catch (error) {
  await fs.rm(staging, { recursive: true, force: true });
  throw error;
}
