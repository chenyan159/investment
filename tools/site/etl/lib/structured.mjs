import path from 'node:path';
import { SCENARIOS, filesUnder, readSource, dateFromName, latestBy, reportTitle, reportSummary, reportSections, writeJson } from './common.mjs';

const EVIDENCE = new Set(['strong', 'medium', 'weak', 'insufficient']);
const VIEWS = ['near_term_delivery', 'long_term_compounding', 'base_valuation', 'upside_potential', 'downside_resilience', 'relative_attractiveness'];
const DECISIONS = { steady_allocation: ['avoid', 'conditional_wait', 'preferred_participate', 'priority_configure'], offense_allocation: ['small_option_bet', 'avoid', 'high_priority_offense'], near_term_timing: ['build_now', 'wait_for_trigger', 'avoid'] };

export function validateStructured(raw, kind, source = '') {
  const fail = message => { throw new Error(`${source}: ${message}`); };
  if (!/^[A-Z][A-Z0-9.-]*$/.test(raw.ticker)) fail('Invalid ticker');
  for (const key of ['research_date', 'target_date']) if (!/^\d{4}-\d{2}-\d{2}$/.test(raw[key]) || !Number.isFinite(Date.parse(raw[key]))) fail(`Invalid ${key}`);
  if (!raw.information_cutoff || !Number.isFinite(Date.parse(raw.information_cutoff))) fail('Missing information cutoff');
  const ref = raw.reference_price;
  if (!ref || typeof ref.value !== 'number' || !Number.isFinite(ref.value) || ref.value <= 0 || !/^[A-Z]{3}$/.test(ref.currency) || !/^\d{4}-\d{2}-\d{2}$/.test(ref.date)) fail('Invalid reference price');
  if (Date.parse(raw.target_date) <= Date.parse(ref.date)) fail('Target date must be after reference date');
  for (const scenario of SCENARIOS) {
    const item = raw.scenarios?.[scenario];
    if (!item || !EVIDENCE.has(item.evidence)) fail(`Invalid ${scenario} evidence`);
    for (const field of ['business_price', 'target_price', ...(kind === 'scenario' ? ['dcf_price'] : [])]) {
      const range = item[field];
      if (range === null) continue;
      if (!Array.isArray(range) || range.length !== 2 || range.some(x => typeof x !== 'number' || !Number.isFinite(x) || x < 0) || range[0] > range[1]) fail(`Invalid ${scenario}.${field}`);
    }
    if (kind === 'comparison' && !['adopt', 'revise', 'reestimate'].includes(item.review)) fail(`Invalid ${scenario}.review`);
  }
  if (kind === 'comparison') {
    for (const key of VIEWS) if (!['positive', 'mixed', 'negative', 'unknown'].includes(raw.views?.[key])) fail(`Invalid view ${key}`);
    for (const [key, choices] of Object.entries(DECISIONS)) if (!choices.includes(raw.decision?.[key])) fail(`Invalid decision ${key}`);
    if (!Array.isArray(raw.comparisons)) fail('Missing comparisons');
    const peers = new Set();
    for (const peer of raw.comparisons) {
      if (!peer.peer || peers.has(peer.peer) || peer.peer === raw.ticker || !peer.reason) fail('Invalid or duplicate comparison peer');
      peers.add(peer.peer);
      for (const key of ['compounding_preference', 'convexity_preference']) if (!['target_preferred', 'peer_preferred', 'comparable', 'both_avoid', 'insufficient'].includes(peer[key])) fail(`Invalid ${key}`);
      if (!['target_preferred', 'peer_preferred', 'comparable', 'split_by_mandate', 'both_avoid', 'insufficient'].includes(peer.verdict)) fail('Invalid comparison verdict');
    }
  }
  return raw;
}

export async function buildStructured({ root, output, kind, directory, manifest, warnings }) {
  const base = path.join(root, '分析报告', directory);
  const documents = [];
  const pairedFiles = new Set();
  for (const jsonFile of await filesUnder(path.join(base, '结构化数据'), '.json')) {
    const { text, source: jsonSource } = await readSource(jsonFile, root, manifest);
    const raw = validateStructured(JSON.parse(text), kind, jsonSource);
    if (dateFromName(jsonFile) !== raw.research_date || !path.basename(jsonFile).startsWith(`${raw.ticker}_`)) throw new Error(`JSON filename identity mismatch: ${jsonSource}`);
    const markdownFile = path.join(base, '结果', path.basename(jsonFile).replace(/\.json$/, '.md'));
    pairedFiles.add(markdownFile);
    const { text: markdown, source } = await readSource(markdownFile, root, manifest);
    const priceApplicable = Object.values(raw.scenarios).some(s => Array.isArray(s.target_price));
    const summary = {
      ...raw,
      title: reportTitle(markdown, raw.ticker),
      summary: reportSummary(markdown),
      source, jsonSource,
      reportUrl: null,
      rawUrl: `data/structured/${kind}/${encodeURIComponent(raw.ticker)}.json`,
      structuredAvailable: true,
      priceApplicable,
      priceNote: priceApplicable ? '情景价格为报告研究假设，参考价不是实时行情；证据等级不等于概率。' : '报告未提供可用情景价格；请阅读证券状态与适用边界。',
    };
    documents.push({ ticker: raw.ticker, date: raw.research_date, summary, detail: { ...summary, markdown, sections: reportSections(markdown), raw } });
  }
  // Pick the latest formal Markdown, never an older JSON just because it exists.
  // Report-only formal results remain readable with explicit missing-data status.
  for (const markdownFile of await filesUnder(path.join(base, '结果'), '.md')) {
    if (pairedFiles.has(markdownFile)) continue;
    const ticker = path.basename(markdownFile).split('_')[0];
    const date = dateFromName(markdownFile);
    if (!/^[A-Z][A-Z0-9.-]*$/.test(ticker) || !date) throw new Error(`Unrecognized formal report identity: ${markdownFile}`);
    const { text: markdown, source } = await readSource(markdownFile, root, manifest);
    const summary = {
      ticker, research_date: date, information_cutoff: null, reference_price: null, target_date: null,
      scenarios: {}, ...(kind === 'comparison' ? { views: {}, decision: {}, comparisons: [] } : {}),
      title: reportTitle(markdown, ticker), summary: reportSummary(markdown), source, jsonSource: null,
      reportUrl: null, rawUrl: null,
      structuredAvailable: false, priceApplicable: false,
      priceNote: '该正式报告没有同名配套 JSON，仅展示原文，不推定价格或比较结论。',
    };
    documents.push({ ticker, date, summary, detail: { ...summary, markdown, sections: reportSections(markdown), raw: null } });
    warnings.push(`${ticker} ${directory} ${date} 缺少同名配套 JSON；保留原文，结构化图表不适用。`);
  }
  const chosen = latestBy(documents, d => d.ticker, d => d.date, warnings, kind);
  for (const { detail } of chosen.values()) {
    if (detail.raw) await writeJson(output, `structured/${kind}/${detail.ticker}.json`, detail.raw);
    if (!detail.priceApplicable) warnings.push(`${detail.ticker} ${directory} 的情景价格不适用，保留 null，不计入回报图表。`);
  }
  return chosen;
}
