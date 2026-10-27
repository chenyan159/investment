import test from 'node:test';
import assert from 'node:assert/strict';
import { returnRange, annualRange, midpoint } from '../src/lib.js';

test('price gains and annualized gains use different units over four years', () => {
  const report = { reference_price: { value: 100, date: '2024-01-01' }, target_date: '2028-01-01', scenarios: { base: { target_price: [100, 200] } } };
  assert.deepEqual(returnRange(report), [0, 100]);
  const annual = annualRange(report);
  assert.equal(annual[0], 0);
  assert.ok(Math.abs(annual[1] - 18.9207115) < 0.00001);
});

test('unpriced securities do not become zero-return investment samples', () => {
  const report = { reference_price: { value: null, date: '2026-10-22' }, target_date: '2029-12-31', scenarios: { base: { target_price: null } } };
  assert.deepEqual(returnRange(report), []);
  assert.deepEqual(annualRange(report), []);
  assert.equal(midpoint([]), null);
});

test('a revised comparison uses its own reference price', () => {
  const original = { reference_price: { value: 100 }, scenarios: { base: { target_price: [150, 200] } } };
  const reviewed = { reference_price: { value: 125 }, scenarios: { base: { target_price: [150, 200] } } };
  assert.deepEqual(returnRange(original), [50, 100]);
  assert.ok(Math.abs(returnRange(reviewed)[0] - 20) < 1e-10);
  assert.ok(Math.abs(returnRange(reviewed)[1] - 60) < 1e-10);
});

test('an expired or absent target date cannot generate annualized gains', () => {
  const report = { reference_price: { value: 100, date: '2026-10-22' }, target_date: '2026-10-22', scenarios: { base: { target_price: [120, 150] } } };
  assert.deepEqual(annualRange(report), []);
});
