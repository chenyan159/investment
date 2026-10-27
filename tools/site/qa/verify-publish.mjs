import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

// Read-only verification. Never deploys, edits DNS, or starts research jobs.
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const docs = path.join(root, 'docs');
const origin = process.argv.find(x => x.startsWith('--origin='))?.slice(9);
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
async function filesAt(dir) {
  const result = [];
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`Unexpected symlink: ${target}`);
    if (entry.isDirectory()) result.push(...await filesAt(target));
    else result.push(target);
  }
  return result;
}
const files = await filesAt(docs);
const html = await fs.readFile(path.join(docs, 'index.html'), 'utf8');
if ((await fs.readFile(path.join(docs, 'CNAME'), 'utf8')).trim() !== 'projectananta.com') {
  throw new Error('CNAME must remain projectananta.com');
}
const jsonFiles = files.filter(x => x.endsWith('.json'));
for (const file of jsonFiles) JSON.parse(await fs.readFile(file, 'utf8'));
const references = [...html.matchAll(/(?:src|href)="(\.\/assets\/[^"?#]+)"/g)].map(x => x[1].replace(/^\.\//, ''));
for (const ref of references) await fs.access(path.join(docs, ref));
const summary = { jsonFiles: jsonFiles.length, assets: references.length, cname: 'projectananta.com', local: 'passed' };
if (origin) {
  const index = JSON.parse(await fs.readFile(path.join(docs, 'data/index.json'), 'utf8'));
  const company = index.companies.find(item => item.ticker === 'NVDA') ?? index.companies[0];
  const samplePaths = [company?.detailUrl, index.research[0]?.detailUrl].filter(Boolean).map(value => value.split('?')[0]);
  const paths = ['index.html', 'data/meta.json', 'data/index.json', ...references, ...samplePaths];
  const results = await Promise.all(paths.map(async relative => {
    const local = await fs.readFile(path.join(docs, relative));
    const url = new URL(relative === 'index.html' ? './' : relative, `${origin.replace(/\/$/, '')}/`);
    url.searchParams.set('verify', Date.now().toString());
    const response = await fetch(url, { signal: AbortSignal.timeout(30000), cache: 'no-store' });
    if (!response.ok) throw new Error(`${relative}: HTTP ${response.status}`);
    const remote = Buffer.from(await response.arrayBuffer());
    if (sha(local) !== sha(remote)) throw new Error(`${relative}: deployed content differs from local build`);
    return relative;
  }));
  summary.live = { origin, verified: results, mismatchCount: 0 };
}
console.log(JSON.stringify(summary, null, 2));
