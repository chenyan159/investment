import test from 'node:test';
import assert from 'node:assert/strict';
import { comparablePairs, distributionBins, sectorMedians, evidenceCounts, median } from '../src/overview-data.js';

function report(annualLow = 0, annualHigh = annualLow) {
  return {
    structuredAvailable: true,
    priceApplicable: true,
    research_date: '2024-01-01',
    reference_price: { value: 100, currency: 'USD', date: '2024-01-01' },
    target_date: '2028-01-01',
    scenarios: {
      base: { target_price: [100 * (1 + annualLow / 100) ** 4, 100 * (1 + annualHigh / 100) ** 4], evidence: 'medium' },
    },
  };
}

function company(ticker, original = report(), revised = report(10)) {
  return { ticker, name: ticker, sector: 'Test', scenario: original, comparison: revised };
}

test('revision points measure change in annualized range midpoint in percentage points', () => {
  const result = comparablePairs([company('ALPHA', report(), report(0, 20))]);
  assert.equal(result.pairs.length, 1);
  assert.equal(result.pairs[0].ticker, 'ALPHA');
  assert.ok(Math.abs(result.pairs[0].original) < 1e-9);
  // Mean of the two annualized endpoints is 10%; annualizing the mean target price is different.
  assert.ok(Math.abs(result.pairs[0].revised - 10) < 1e-9);
  assert.ok(Math.abs(result.pairs[0].delta - 10) < 1e-9);
  assert.equal(result.up, 1);
});

test('changing any price anchor or horizon excludes a company from revision attribution', () => {
  const cases = [
    ['CURRENCY', r => { r.reference_price.currency = 'EUR'; }],
    ['PRICE', r => { r.reference_price.value = 101; }],
    ['QUOTEDATE', r => { r.reference_price.date = '2024-01-02'; }],
    ['TARGETDATE', r => { r.target_date = '2029-01-01'; }],
  ];
  const companies = cases.map(([ticker, mutate]) => {
    const revised = report(10);
    mutate(revised);
    return company(ticker, report(), revised);
  });
  const result = comparablePairs([company('VALID'), ...companies]);
  assert.deepEqual(result.pairs.map(p => p.ticker), ['VALID']);
  assert.equal(result.total, 5);
  assert.equal(result.excluded, 4);
});

test('missing JSON or null scenario prices are excluded rather than treated as unchanged', () => {
  const noJson = { structuredAvailable: false, priceApplicable: false, reference_price: null, scenarios: {} };
  const unpriced = report(); unpriced.scenarios.base.target_price = null;
  const companies = [company('ATKR', unpriced, noJson), company('NULLPRICE', report(), unpriced), company('NOREPORT', report(), null)];
  const result = comparablePairs(companies);
  assert.equal(result.pairs.length, 0);
  assert.equal(result.total, 3);
  assert.equal(result.excluded, 3);
  assert.equal(result.up + result.down + result.unchanged, 0);
});

test('revision classification uses a small percentage-point tolerance, not a percent ratio', () => {
  const result = comparablePairs([
    company('UP', report(), report(0.11)),
    company('DOWN', report(), report(-0.11)),
    company('SMALLUP', report(), report(0.05)),
    company('SMALLDOWN', report(), report(-0.05)),
    company('FLAT', report(), report()),
  ]);
  assert.equal(result.up, 1);
  assert.equal(result.down, 1);
  assert.equal(result.unchanged, 3);
  assert.equal(result.pairs.length, result.up + result.down + result.unchanged);
});

test('exact positive and negative tolerance boundaries remain unchanged despite floating arithmetic', () => {
  const result = comparablePairs([
    company('BOUNDARYUP', report(), report(0.1)),
    company('BOUNDARYDOWN', report(), report(-0.1)),
  ]);
  assert.equal(result.up, 0);
  assert.equal(result.down, 0);
  assert.equal(result.unchanged, 2);
});

test('the selected operating scenario determines revision prices without falling back to base', () => {
  const original = report(), revised = report(10);
  original.scenarios.bull = { target_price: [100, 100], evidence: 'weak' };
  revised.scenarios.bull = { target_price: [100 * 0.9 ** 4, 100 * 0.9 ** 4], evidence: 'weak' };
  const result = comparablePairs([company('ALPHA', original, revised)], 'bull');
  assert.equal(result.pairs.length, 1);
  assert.ok(Math.abs(result.pairs[0].delta + 10) < 1e-9);
  assert.equal(result.down, 1);
  assert.equal(comparablePairs([company('ALPHA', original, revised)], 'breakthrough').pairs.length, 0);
});

test('comparison aggregates preserve the caller company order and source objects', () => {
  const input = [company('ZETA'), company('ALPHA', report(), report(-10))];
  const frozen = JSON.stringify(input);
  comparablePairs(input);
  assert.equal(JSON.stringify(input), frozen);
});

test('distribution bins are left-closed and count both sides on the same sample', () => {
  const values = [-20.01, -20, 0, 10, 20, 40];
  const bins = distributionBins(values.map(value => ({ original: value, revised: value })));
  assert.deepEqual(bins.map(bin => bin.original), [1, 1, 1, 1, 1, 1]);
  assert.deepEqual(bins.map(bin => bin.revised), [1, 1, 1, 1, 1, 1]);
  assert.equal(bins.reduce((sum, bin) => sum + bin.original, 0), values.length);
  assert.equal(bins.reduce((sum, bin) => sum + bin.revised, 0), values.length);
});

test('industry comparison uses an unweighted median rather than an outlier-sensitive average', () => {
  const input = [
    { sector: 'A', original: 0, revised: 1 },
    { sector: 'A', original: 10, revised: 5 },
    { sector: 'A', original: 1000, revised: 7 },
    { sector: 'B', original: -4, revised: -6 },
    { sector: 'B', original: 2, revised: 4 },
  ];
  const result = sectorMedians(input);
  assert.deepEqual(result.find(s => s.sector === 'A'), { sector: 'A', count: 3, original: 10, revised: 5 });
  assert.deepEqual(result.find(s => s.sector === 'B'), { sector: 'B', count: 2, original: -1, revised: -1 });
  assert.equal(median([null, undefined, NaN]), null);
});

test('evidence comparison keeps paired reports even without prices and separates missing evidence', () => {
  const unpriced = report(); unpriced.scenarios.base.target_price = null;
  unpriced.scenarios.base.evidence = 'strong';
  const revised = report(); revised.scenarios.base.target_price = null;
  revised.scenarios.base.evidence = 'medium';
  const missing = report(); delete missing.scenarios.base.evidence;
  const reportOnly = { structuredAvailable: false, scenarios: {} };
  const result = evidenceCounts([
    company('PRICENULL', unpriced, revised),
    company('EVIDENCEMISSING', missing, revised),
    company('REPORTONLY', report(), reportOnly),
  ]);
  assert.equal(result.total, 2);
  assert.equal(result.excluded, 1);
  assert.equal(result.original.strong, 1);
  assert.equal(result.original.missing, 1);
  assert.equal(result.revised.medium, 2);
  assert.equal(Object.values(result.original).reduce((a, b) => a + b, 0), result.total);
  assert.equal(Object.values(result.revised).reduce((a, b) => a + b, 0), result.total);
});
