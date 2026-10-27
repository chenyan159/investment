import test from 'node:test';
import assert from 'node:assert/strict';
import { atlasPoints, leaderRows, scatterMeta } from '../src/company-atlas-data.js';

const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} != ${expected}`);
const prices = (low, high = low) => [100 * (1 + low / 100) ** 4, 100 * (1 + high / 100) ** 4];
function report() {
  return {
    structuredAvailable: true, priceApplicable: true,
    reference_price: { value: 100, date: '2024-01-01', currency: 'USD' },
    target_date: '2028-01-01',
    scenarios: {
      bear: { target_price: prices(-20, -10), evidence: 'strong' },
      base: { target_price: prices(0, 20), evidence: 'medium' },
      bull: { target_price: prices(30, 50), evidence: 'weak' },
      breakthrough: { target_price: prices(60, 100), evidence: 'insufficient' },
    },
    decision: { steady_allocation: 'preferred_participate', offense_allocation: 'high_priority_offense' },
  };
}
function company(ticker = 'TEST') { return { ticker, name: ticker, scenario: report(), comparison: report() }; }
const tickers = rows => rows.map(row => row.ticker);

test('ranking averages annualized endpoints, not target prices, and uses percent units', () => {
  const result = leaderRows([company()]);
  assert.equal(result.eligible, 1);
  close(result.rows[0].values[0], 0);
  close(result.rows[0].values[1], 20);
  close(result.rows[0].score, 10);
  const wrong = (((prices(0, 20)[0] + prices(0, 20)[1]) / 200) ** 0.25 - 1) * 100;
  assert.ok(Math.abs(result.rows[0].score - wrong) > 1);
});

test('scatter axes retain separate return, interval width and categorical units', () => {
  const input = [company()];
  const risk = atlasPoints(input, 'comparison', 'risk_return')[0];
  close(risk.x, -15); close(risk.y, 10);
  const upside = atlasPoints(input, 'comparison', 'base_upside')[0];
  close(upside.x, 10); close(upside.y, 40);
  const width = atlasPoints(input, 'comparison', 'range_return')[0];
  close(width.x, 20); close(width.y, 10);
  assert.equal(scatterMeta('range_return').xUnit, 'pp');
  assert.equal(scatterMeta('range_return').yUnit, 'percent');
  assert.equal(scatterMeta('risk_return').xUnit, 'percent');
  assert.equal(scatterMeta('evidence_return').xUnit, 'category');
});

test('null, incomplete and reversed intervals are excluded rather than zero filled', () => {
  for (const range of [null, [100], [null, 100], [100, null], [200, 100], [100, Infinity], [-1, 100], ['100', 200]]) {
    const item = company(); item.comparison.scenarios.base.target_price = range;
    assert.equal(leaderRows([item]).eligible, 0, JSON.stringify(range));
    assert.equal(atlasPoints([item], 'comparison', 'range_return').length, 0);
  }
});

test('two equal endpoints and zero downside target remain legitimate report values', () => {
  const item = company(); item.comparison.scenarios.base.target_price = [100, 100];
  close(leaderRows([item]).rows[0].score, 0);
  item.comparison.scenarios.base.target_price = [0, 100];
  assert.deepEqual(leaderRows([item]).rows[0].values, [-100, 0]);
});

test('invalid calendar dates and nonpositive horizons cannot create annualized values', () => {
  for (const [field, value] of [['target_date', '2028-02-30'], ['target_date', 'not-a-date'], ['target_date', '2024-01-01'], ['target_date', '2023-01-01'], ['target_date', '2028-1-1'], ['date', '2024-02-30'], ['date', null]]) {
    const item = company();
    if (field === 'date') item.comparison.reference_price.date = value;
    else item.comparison[field] = value;
    assert.equal(leaderRows([item]).eligible, 0, `${field}=${value}`);
    assert.equal(atlasPoints([item]).length, 0);
  }
});

test('invalid reference prices, inapplicable prices and report-only records stay excluded', () => {
  for (const value of [null, 0, -1, Infinity, '100']) {
    const item = company(); item.comparison.reference_price.value = value;
    assert.equal(leaderRows([item]).eligible, 0);
  }
  for (const flag of ['structuredAvailable', 'priceApplicable']) {
    const item = company(); item.comparison[flag] = false;
    assert.equal(leaderRows([item]).eligible, 0);
    assert.equal(atlasPoints([item]).length, 0);
  }
  const item = company(); item.comparison = null;
  assert.equal(leaderRows([item]).eligible, 0);
});

test('source selection is explicit and does not substitute the other report', () => {
  const item = company(); item.scenario.scenarios.base.target_price = prices(40);
  close(leaderRows([item], { source: 'scenario' }).rows[0].score, 40);
  close(leaderRows([item], { source: 'comparison' }).rows[0].score, 10);
  item.comparison = null;
  assert.equal(leaderRows([item], { source: 'comparison' }).eligible, 0);
  assert.equal(atlasPoints([item], 'comparison').length, 0);
});

test('each operating dimension ranks its own scenario without fallback to base', () => {
  const item = company();
  for (const [dimension, expected] of [['bear', -15], ['base', 10], ['bull', 40], ['breakthrough', 80]]) {
    close(leaderRows([item], { dimension }).rows[0].score, expected);
  }
  delete item.comparison.scenarios.bull;
  assert.equal(leaderRows([item], { dimension: 'bull' }).eligible, 0);
  assert.equal(atlasPoints([item], 'comparison', 'base_upside').length, 0);
  assert.equal(atlasPoints([item], 'comparison', 'range_return').length, 1);
});

test('steady and offense are exact reviewed decision filters, not numeric labels', () => {
  const preferred = company('PREFERRED');
  const conditional = company('CONDITIONAL');
  conditional.comparison.decision = { steady_allocation: 'conditional_wait', offense_allocation: 'small_option_bet' };
  conditional.comparison.scenarios.base.target_price = prices(200);
  const avoid = company('AVOID');
  avoid.comparison.decision = { steady_allocation: 'avoid', offense_allocation: 'avoid' };
  const missing = company('MISSING'); delete missing.comparison.decision;
  const input = [conditional, avoid, preferred, missing];
  const steady = leaderRows(input, { dimension: 'steady' });
  const offense = leaderRows(input, { dimension: 'offense' });
  assert.deepEqual(tickers(steady.rows), ['PREFERRED']); close(steady.rows[0].score, 10);
  assert.deepEqual(tickers(offense.rows), ['PREFERRED']); close(offense.rows[0].score, 80);
  assert.equal(steady.total, 4); assert.equal(steady.eligible, 1);
  for (const dimension of ['steady', 'offense']) {
    const result = leaderRows(input, { source: 'scenario', dimension });
    assert.equal(result.rows.length, 0); assert.equal(result.eligible, 0); assert.equal(result.total, 4);
  }
});

test('ties use stable ticker order and the limit does not alter eligible coverage', () => {
  const input = [company('ZZZ'), company('AAA'), company('MMM')];
  const result = leaderRows(input, { limit: 2 });
  assert.deepEqual(tickers(result.rows), ['AAA', 'MMM']);
  assert.equal(result.eligible, 3); assert.equal(result.total, 3);
  assert.deepEqual(tickers(leaderRows(input.toReversed(), { limit: 3 }).rows), ['AAA', 'MMM', 'ZZZ']);
});

test('scatter and ranking preserve input array order and report content', () => {
  const input = [company('ZZZ'), company('AAA')];
  const before = JSON.stringify(input);
  for (const mode of ['risk_return', 'base_upside', 'range_return', 'evidence_return']) atlasPoints(input, 'comparison', mode);
  for (const dimension of ['base', 'steady', 'offense']) leaderRows(input, { dimension });
  assert.equal(JSON.stringify(input), before);
});

test('evidence is categorical and missing evidence is never invented as strong', () => {
  const grades = ['weak', 'medium', 'strong', 'insufficient', undefined];
  const input = grades.map((grade, index) => {
    const item = company(`T${index}`); item.comparison.scenarios.base.evidence = grade; return item;
  });
  const result = atlasPoints(input, 'comparison', 'evidence_return');
  assert.deepEqual(result.map(point => point.x), [0, 1, 2, 3, 3]);
  assert.equal(result.length, 5);
});

test('unknown selectors produce no silently substituted results', () => {
  const input = [company()];
  assert.equal(atlasPoints(input, 'unknown').length, 0);
  assert.equal(atlasPoints(input, 'comparison', 'unknown').length, 0);
  assert.equal(leaderRows(input, { source: 'unknown' }).rows.length, 0);
  assert.equal(leaderRows(input, { dimension: 'unknown' }).rows.length, 0);
});
