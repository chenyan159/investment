import fs from 'node:fs';
import { resolveCompanyInvestmentDecisionMarketSnapshot } from '../../../tools/research-runner/domains/company-investment-decision.mjs';

const root = 'D:/drive/Investment';
const manifest = JSON.parse(fs.readFileSync(`${root}/tools/research-runner/company-investment-decision.batches.json`, 'utf8'));
const rows = [];
for (const batch of manifest.batches) {
  for (const subject of batch.subjects) {
    const resolved = resolveCompanyInvestmentDecisionMarketSnapshot({subject, sourceDate: batch.sourceDate}, {useCache: false});
    rows.push({subject, sourceDate:batch.sourceDate, batchId:resolved.batchId, sha256:resolved.sha256, passed:true});
  }
}
let unbound;
try {
  resolveCompanyInvestmentDecisionMarketSnapshot({subject:'MU', sourceDate:'2026-09-05'}, {useCache:false});
  unbound={subject:'MU',sourceDate:'2026-09-05',rejected:false};
} catch (e) {
  unbound={subject:'MU',sourceDate:'2026-09-05',rejected:true,message:e.message};
}
const result={scope:'Read-only production resolver; no queue creation, formal preparation or research execution.',rows,unbound};
fs.writeFileSync(`${root}/备份/流程审计与研究方案改进_2026-09-05/data/decisions_snapshot_live_check.json`,JSON.stringify(result,null,2));
console.log(JSON.stringify({boundPassed:rows.length,unbound},null,2));
