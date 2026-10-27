// Display-only calculations over one chosen report. Values are percentages,
// not fractions. No probability, composite score, or cross-report fallback.
const SOURCES = new Set(['scenario', 'comparison']);
const SCENARIOS = new Set(['bear', 'base', 'bull', 'breakthrough']);
const MODES = new Set(['risk_return', 'base_upside', 'range_return', 'evidence_return']);
const DAY = 86400000;

function calendarDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const time = Date.parse(`${value}T00:00:00.000Z`);
  return Number.isFinite(time) && new Date(time).toISOString().slice(0, 10) === value ? time : null;
}

function annualEndpoints(report, scenario) {
  if (!report || report.structuredAvailable === false || report.priceApplicable === false) return null;
  const reference = report.reference_price?.value;
  const prices = report.scenarios?.[scenario]?.target_price;
  const start = calendarDate(report.reference_price?.date);
  const target = calendarDate(report.target_date);
  if (typeof reference !== 'number' || !Number.isFinite(reference) || reference <= 0 || start === null || target === null || target <= start) return null;
  if (!Array.isArray(prices) || prices.length !== 2 || prices.some(value => typeof value !== 'number' || !Number.isFinite(value) || value < 0) || prices[0] > prices[1]) return null;
  const years = (target - start) / (365.25 * DAY);
  const values = prices.map(value => (Math.pow(value / reference, 1 / years) - 1) * 100);
  return values.every(Number.isFinite) ? values : null;
}

function midpoint(values) { return values[0] / 2 + values[1] / 2; }
function evidenceOf(report, scenario) { return report.scenarios?.[scenario]?.evidence || 'missing'; }
function byTicker(a, b) { return a.ticker < b.ticker ? -1 : a.ticker > b.ticker ? 1 : 0; }

export function atlasPoints(companies = [], source = 'comparison', mode = 'risk_return') {
  if (!Array.isArray(companies) || !SOURCES.has(source) || !MODES.has(mode)) return [];
  const points = [];
  for (const company of companies) {
    if (!company || typeof company.ticker !== 'string') continue;
    const report = company[source];
    const range = annualEndpoints(report, 'base');
    if (!range) continue;
    const evidence = evidenceOf(report, 'base');
    let x, y;
    if (mode === 'risk_return') {
      const bear = annualEndpoints(report, 'bear');
      if (!bear) continue;
      x = midpoint(bear); y = midpoint(range);
    } else if (mode === 'base_upside') {
      const bull = annualEndpoints(report, 'bull');
      if (!bull) continue;
      x = midpoint(range); y = midpoint(bull);
    } else if (mode === 'range_return') {
      x = range[1] - range[0]; y = midpoint(range);
    } else {
      x = evidence === 'weak' ? 0 : evidence === 'medium' ? 1 : evidence === 'strong' ? 2 : 3;
      y = midpoint(range);
    }
    if (Number.isFinite(x) && Number.isFinite(y)) points.push({ company, ticker: company.ticker, name: company.name || company.ticker, x, y, evidence, range, report });
  }
  return points;
}

export function scatterMeta(mode = 'risk_return') {
  const descriptions = {
    risk_return: {
      title: '下行情景与基准回报',
      description: '每个点是一家公司。横轴为悲观情景年化价格回报区间的端点中值，纵轴为基准情景端点中值；越向右表示悲观模型下的回报越高。',
      xLabel: '悲观情景年化中值', yLabel: '基准情景年化中值', xUnit: 'percent', yUnit: 'percent', categorical: false,
    },
    base_upside: {
      title: '基准回报与乐观空间',
      description: '比较每家公司的基准与乐观情景年化价格回报。中值是两个年化端点的算术平均，不是概率加权预期收益。',
      xLabel: '基准情景年化中值', yLabel: '乐观情景年化中值', xUnit: 'percent', yUnit: 'percent', categorical: false,
    },
    range_return: {
      title: '基准区间宽度与回报',
      description: '横轴是基准情景年化回报上限减下限，单位为百分点；区间宽度描述报告给出的估值范围，不代表统计波动率或置信区间。',
      xLabel: '基准年化区间宽度', yLabel: '基准情景年化中值', xUnit: 'pp', yUnit: 'percent', categorical: false,
    },
    evidence_return: {
      title: '经营证据与基准回报',
      description: '按基准情景的经营证据等级分组观察具体公司回报。弱、中、强与证据不足是类别，不是连续分数，也不是情景发生概率。',
      xLabel: '基准情景证据等级', yLabel: '基准情景年化中值', xUnit: 'category', yUnit: 'percent', categorical: true,
    },
  };
  return descriptions[mode] ?? descriptions.risk_return;
}

export function leaderRows(companies = [], { source = 'comparison', dimension = 'base', limit = 10 } = {}) {
  const total = Array.isArray(companies) ? companies.length : 0;
  const empty = { rows: [], eligible: 0, total };
  if (!Array.isArray(companies) || !SOURCES.has(source)) return empty;
  const decisionDimension = dimension === 'steady' || dimension === 'offense';
  if ((!SCENARIOS.has(dimension) && !decisionDimension) || (decisionDimension && source !== 'comparison')) return empty;
  const scenario = dimension === 'steady' ? 'base' : dimension === 'offense' ? 'breakthrough' : dimension;
  const rows = [];
  for (const company of companies) {
    if (!company || typeof company.ticker !== 'string') continue;
    const report = company[source];
    if (dimension === 'steady' && report?.decision?.steady_allocation !== 'preferred_participate') continue;
    if (dimension === 'offense' && report?.decision?.offense_allocation !== 'high_priority_offense') continue;
    const values = annualEndpoints(report, scenario);
    if (!values) continue;
    rows.push({ company, ticker: company.ticker, name: company.name || company.ticker, values, score: midpoint(values), evidence: evidenceOf(report, scenario), report });
  }
  rows.sort((a, b) => b.score - a.score || byTicker(a, b));
  const count = limit === Infinity ? rows.length : Number.isFinite(limit) ? Math.max(0, Math.floor(limit)) : 10;
  return { rows: rows.slice(0, count), eligible: rows.length, total };
}
