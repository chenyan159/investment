// Pure display calculations. Inputs remain formal reports; no research is modified.
export const REVISION_TOLERANCE = 0.1;
export function classifyRevision(delta) {return delta > REVISION_TOLERANCE + 1e-9 ? 'up' : delta < -REVISION_TOLERANCE - 1e-9 ? 'down' : 'unchanged';}
export const DISTRIBUTION_BOUNDS = [-20, 0, 10, 20, 40];
export const DISTRIBUTION_LABELS = ['低于 −20%', '−20% 至 0%', '0% 至 10%', '10% 至 20%', '20% 至 40%', '40% 及以上'];

function annualMidpoint(report, scenario) {
  const reference = report?.reference_price?.value;
  const range = report?.scenarios?.[scenario]?.target_price;
  const start = Date.parse(report?.reference_price?.date);
  const end = Date.parse(report?.target_date);
  const years = (end - start) / (365.25 * 86400000);
  if (typeof reference !== 'number' || !Number.isFinite(reference) || reference <= 0 || !(years > 0) || !Number.isFinite(years)) return null;
  if (!Array.isArray(range) || range.length !== 2 || !range.every(value => typeof value === 'number' && Number.isFinite(value) && value >= 0) || range[1] < range[0]) return null;
  const annual = range.map(value => (Math.pow(value / reference, 1 / years) - 1) * 100);
  return annual.every(Number.isFinite) ? (annual[0] + annual[1]) / 2 : null;
}

export function comparablePairs(companies = [], scenario = 'base') {
  const pairs = [];
  for (const company of companies) {
    const a = company.scenario, b = company.comparison;
    if (!a || !b || a.structuredAvailable === false || b.structuredAvailable === false) continue;
    if (!a.reference_price?.currency || a.reference_price.currency !== b.reference_price?.currency || a.reference_price.value !== b.reference_price.value || a.reference_price.date !== b.reference_price.date || a.target_date !== b.target_date) continue;
    const original = annualMidpoint(a, scenario), revised = annualMidpoint(b, scenario);
    if (original === null || revised === null) continue;
    pairs.push({ company, ticker: company.ticker, name: company.name, sector: company.sector || '未分类', original, revised, delta: revised - original });
  }
  return { pairs, total: companies.length, excluded: companies.length - pairs.length, up: pairs.filter(p => classifyRevision(p.delta) === 'up').length, down: pairs.filter(p => classifyRevision(p.delta) === 'down').length, unchanged: pairs.filter(p => classifyRevision(p.delta) === 'unchanged').length };
}

export function median(values = []) {
  const sorted = values.filter(v => typeof v === 'number' && Number.isFinite(v)).sort((a, b) => a - b);
  if (!sorted.length) return null;
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

export function distributionBins(pairs = []) {
  const bins = DISTRIBUTION_LABELS.map(label => ({ label, original: 0, revised: 0 }));
  for (const pair of pairs) for (const key of ['original', 'revised']) {
    const value = pair[key];
    if (typeof value !== 'number' || !Number.isFinite(value)) continue;
    const found = DISTRIBUTION_BOUNDS.findIndex(bound => value < bound);
    bins[found < 0 ? bins.length - 1 : found][key]++;
  }
  return bins;
}

export function sectorMedians(pairs = []) {
  const groups = new Map();
  for (const pair of pairs) { if (!groups.has(pair.sector)) groups.set(pair.sector, []); groups.get(pair.sector).push(pair); }
  return [...groups].map(([sector, rows]) => ({ sector, count: rows.length, original: median(rows.map(r => r.original)), revised: median(rows.map(r => r.revised)) })).sort((a,b) => a.sector.localeCompare(b.sector, 'zh-CN'));
}

export function evidenceCounts(companies = [], scenario = 'base') {
  const sample = companies.filter(c => c.scenario && c.comparison && c.scenario.structuredAvailable !== false && c.comparison.structuredAvailable !== false);
  const keys = ['strong', 'medium', 'weak', 'insufficient', 'missing'];
  const counts = { original: Object.fromEntries(keys.map(k => [k, 0])), revised: Object.fromEntries(keys.map(k => [k, 0])) };
  for (const company of sample) for (const [side, source] of [['original', 'scenario'], ['revised', 'comparison']]) {
    const value = company[source]?.scenarios?.[scenario]?.evidence;
    counts[side][keys.includes(value) ? value : 'missing']++;
  }
  return { ...counts, total: sample.length, excluded: companies.length - sample.length, keys };
}
