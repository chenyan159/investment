import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(fs.readFileSync(path.join(dir, '核验数据.json'), 'utf8'));
const prices = {SOMMY:20, PSIX:40.49, ET:21.5, SPACEX:147.95, GOOGL:338.46, MU:1016.59, CRWV:89.36, SNDK:1740, AVGO:357.9, CRDO:170.57};
const dividends = (ticker, scenario, horizon) => {
  if (ticker === 'AVGO') return [1.3, 2.6, 7.8][horizon];
  if (ticker === 'GOOGL') return [.44, .88, 2.64][horizon];
  if (ticker === 'MU') return [.3, .6, 1.8][horizon];
  if (ticker === 'SOMMY') return [[4,8,26],[8,16,56],[8,16,66],[8,16,72]][scenario][horizon]*5/155;
  if (ticker === 'ET') {
    const annual = scenario === 0 ? 1 : 1.38;
    const growth = [0.01,0.03,0.04,0.05][scenario];
    return [.3425+annual/4, .3425+3*annual/4, .3425+annual+annual*(1+growth)+.75*annual*(1+growth)**2][horizon];
  }
  return 0;
};
const results = [];
for (const table of data.tables) {
  for (let i=0; i<table.details.length; i++) {
    const row = table.details[i];
    if (row.prices.length !== 2 || row.returns.length < 1) continue;
    const reported = row.returns.length === 1 ? [row.returns[0],row.returns[0]] : row.returns.slice(0,2);
    const div = dividends(table.ticker, Math.floor(i/3), i%3);
    const actual = row.prices.map(p => (p+div)/prices[table.ticker]*100-100);
    const errors = actual.map((x,j) => Math.abs(x-reported[j]));
    // Reported exit values and returns are both rounded. Allow price precision plus return rounding.
    const precision = table.ticker === 'SNDK' ? .5 : ['SOMMY','PSIX','ET','CRWV'].includes(table.ticker) ? .005 : .05;
    const tolerance = .050001 + precision/prices[table.ticker]*100;
    results.push({ticker:table.ticker, line:row.line, scenario:Math.floor(i/3), horizon:[6,12,36][i%3], price:prices[table.ticker],dividend:div, exits:row.prices, reported, recalculated:actual, errors, tolerance, passes:errors.every(e=>e<=tolerance)});
  }
}
const stats = {cells:results.length, endpoints:2*results.length, passingCells:results.filter(x=>x.passes).length, maximumErrorPercentagePoints:Math.max(...results.flatMap(x=>x.errors)), exceptions:results.filter(x=>!x.passes)};
fs.writeFileSync(path.join(dir,'回报算术核验.json'),JSON.stringify({scope:'Recalculate total return from published current price, target value and modeled cumulative dividends only; this does not verify valuation assumptions, full models, or source authenticity.',stats,results},null,2));
console.log(JSON.stringify(stats,null,2));
