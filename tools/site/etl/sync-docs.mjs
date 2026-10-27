import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { safeInside, renameWithRetry } from './lib/common.mjs';
import { validateData } from './validate-data.mjs';

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = safeInside(site, path.join(site, 'dist'));
const docs = safeInside(site, path.join(site, 'docs'));
const staging = safeInside(site, path.join(site, '.build', `docs-${process.pid}`));
const previous = safeInside(site, path.join(site, '.build', `previous-docs-${process.pid}`));

const html = await fs.readFile(path.join(dist, 'index.html'), 'utf8');
if (!html.includes('<html') || !html.includes('<script')) throw new Error('Built index.html is incomplete');
const cname = (await fs.readFile(path.join(dist, 'CNAME'), 'utf8')).trim();
if (cname !== 'projectananta.com') throw new Error('Refusing to publish an unexpected custom domain');
await validateData(path.join(dist, 'data'));
await fs.mkdir(path.dirname(staging), { recursive: true });
await fs.cp(dist, staging, { recursive: true, errorOnExist: true, force: false });
// GitHub Pages serves underscore-containing files without processing research Markdown.
await fs.writeFile(path.join(staging, '.nojekyll'), '');
let movedOld = false;
try {
  try { await renameWithRetry(docs, previous); movedOld = true; } catch (error) { if (error.code !== 'ENOENT') throw error; }
  await renameWithRetry(staging, docs);
} catch (error) {
  if (movedOld) await renameWithRetry(previous, docs);
  await fs.rm(staging, { recursive: true, force: true });
  throw error;
}
if (movedOld) await fs.rm(previous, { recursive: true, force: true });
console.log(`Published bundle prepared: ${docs}; domain ${cname}; data validated.`);
