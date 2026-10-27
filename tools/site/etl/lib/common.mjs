import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

export const SCENARIOS = ['bear', 'base', 'bull', 'breakthrough'];
export const slash = value => value.split(path.sep).join('/');
export const digest = value => crypto.createHash('sha256').update(value).digest('hex');
export const reportId = (kind, source) => `${kind}-${digest(source).slice(0, 16)}`;
export const dateFromName = name => name.match(/(\d{4}-\d{2}-\d{2})(?=\.[^.]+$)/)?.[1] ?? null;
export const publicPath = (...parts) => slash(path.join(...parts));

export function safeInside(root, candidate) {
  const base = path.resolve(root);
  const target = path.resolve(candidate);
  if (target === base || !target.startsWith(`${base}${path.sep}`)) {
    throw new Error(`Refusing path outside ${base}: ${target}`);
  }
  return target;
}

export async function filesUnder(root, extension = '.md') {
  const out = [];
  for (const entry of await fs.readdir(root, { withFileTypes: true })) {
    if (entry.isSymbolicLink()) throw new Error(`Source symlink is not permitted: ${path.join(root, entry.name)}`);
    if (entry.isDirectory()) {
      if (/^(备份|tmp|_work|研究方案|站点数据)$/u.test(entry.name)) throw new Error(`Unexpected non-formal directory in results: ${entry.name}`);
      out.push(...await filesUnder(path.join(root, entry.name), extension));
    } else if (entry.isFile() && entry.name.endsWith(extension)) out.push(path.join(root, entry.name));
  }
  return out.sort((a, b) => a.localeCompare(b, 'en'));
}

export function plainText(markdown) {
  return markdown
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/<[^>]*>/g, ' ')
    .replace(/[*_`#]/g, '')
    .replace(/\s+/g, ' ').trim();
}

export function reportTitle(markdown, fallback) {
  return plainText(markdown.match(/^#\s+(.+)$/m)?.[1] ?? fallback);
}

export function reportSummary(markdown, max = 420) {
  const candidates = [];
  const conclusionHeading = /当前(?:判断|结论|投资|决策)|核心(?:判断|结论|摘要)|总体判断|投资判断|结论先行|执行摘要|研究摘要|核心发现|主要结论/;
  const metadataStart = /^(?:研究(?:截止|日期|日[：:、])|信息截止|数据截止|截止(?:日期|时间)|报价(?:日期|时点)|证券(?:身份|口径)|口径(?:先行|说明|约定)|金额(?:除|单位)|除(?:另|特别|特殊)注|本文(?:采用|使用|以|是|不以|的)|本(?:报告|次研究)(?:采用|使用|以|读取)|(?:资料|数据|价格|信息|来源)[来源出自：:]{1,4}|(?:L|S|R)\d+[：:]|(?:DEF\s*14A|EX-10)[，：:])/i;
  for (const [sectionIndex, section] of reportSections(markdown).entries()) {
    const hasConclusionHeading = conclusionHeading.test(section.title);
    if (!hasConclusionHeading && /来源|证据目录|底稿|取证|参考文献|附录|资料清单|免责声明/.test(section.title)) continue;
    const paragraphs = section.markdown.split(/\r?\n\s*\r?\n/).map(s => s.trim());
    for (const [paragraphIndex, paragraph] of paragraphs.entries()) {
      if (/^(#|\||```|>)/.test(paragraph)) continue;
      const text = plainText(paragraph);
      if (text.length < 45 || metadataStart.test(text)) continue;
      if (/(?:基本面|分析报告|金融资料)[\\/](?:结果|行业调研|公司调研|产业背景)|[A-Z]:[\\/]|^\[[A-Z]?\d+\]:\s*https?:/.test(text)) continue;
      const list = /^(?:[-*+]\s|\d+[.、]\s?)/.test(paragraph);
      const directConclusion = /^(?:当前(?:判断|结论|投资|决策)|核心(?:判断|结论)|总体判断|投资判断|结论先行)[：:]/.test(text);
      const score = (hasConclusionHeading ? 200 : 0) + (directConclusion ? 120 : 0)
        + (/摘要|结论|判断/.test(section.title) ? 20 : 0) - (list ? 50 : 0)
        - Math.min(sectionIndex, 100) - paragraphIndex * 2;
      candidates.push({ text, score });
    }
  }
  // Excerpts are copied from one actual prose paragraph. Never synthesize a
  // conclusion from a source list or treat a late keyword mention as a summary.
  const text = candidates.sort((a, b) => b.score - a.score)[0]?.text ?? '';
  return text.length > max ? `${text.slice(0, max)}…` : text;
}

export function reportSections(markdown) {
  const lines = markdown.split(/\r?\n/);
  const sections = [];
  let start = 0, current = { id: 'section-0', title: '报告开篇', level: 1 };
  let fenced = false;
  for (let i = 0; i < lines.length; i++) {
    if (/^```/.test(lines[i])) fenced = !fenced;
    const match = !fenced && lines[i].match(/^(#{1,6})\s+(.+)$/);
    if (!match) continue;
    if (i > start) sections.push({ ...current, markdown: lines.slice(start, i).join('\n').trim() });
    current = { id: `section-${sections.length}`, title: plainText(match[2]), level: match[1].length };
    start = i;
  }
  sections.push({ ...current, markdown: lines.slice(start).join('\n').trim() });
  return sections.filter(s => s.markdown);
}

// Abort publication on likely credentials. Public research text remains unmodified.
export function assertPublicContent(text, source) {
  const forbidden = [
    /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
    /\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{30,}\b/,
    /\bsk-proj-[A-Za-z0-9_-]{40,}\b/,
    /\bsk-[A-Za-z0-9]{40,}\b/,
    /\bAKIA[0-9A-Z]{16}\b/,
    /[?&](?:access_token|api_key|auth_token|token)=[A-Za-z0-9_-]{24,}/i,
    /\b(?:C|D):[\\/]Users[\\/][^\s)\]]+/i,
  ];
  if (forbidden.some(pattern => pattern.test(text))) throw new Error(`Possible private content found; manual review required: ${source}`);
}

export async function readSource(file, root, manifest) {
  const bytes = await fs.readFile(file);
  const text = bytes.toString('utf8').replace(/^\uFEFF/, '');
  const source = slash(path.relative(root, file));
  assertPublicContent(text, source);
  manifest.set(source, { source, bytes: bytes.length, sha256: digest(bytes) });
  return { text, source };
}

export async function writeJson(root, relative, value) {
  const destination = safeInside(root, path.join(root, relative));
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, JSON.stringify(value), 'utf8');
}

// Windows scanners/watchers can briefly retain a directory handle. Retry the
// same atomic operation; never fall back to deleting the active output first.
export async function renameWithRetry(from, to) {
  for (let attempt = 0; ; attempt++) {
    try { await fs.rename(from, to); return; }
    catch (error) {
      if (!['EPERM', 'EACCES', 'EBUSY'].includes(error.code) || attempt >= 6) throw error;
      await new Promise(resolve => setTimeout(resolve, Math.min(150 * (2 ** attempt), 1200)));
    }
  }
}

export function tableRows(markdown) {
  return markdown.split(/\r?\n/).filter(line => /^\s*\|/.test(line)).map(line => line.trim().replace(/^\||\|$/g, '').split(/(?<!\\)\|/).map(cell => cell.trim().replace(/`/g, '')));
}

export function parseCompanyIndex(markdown) {
  const map = new Map();
  for (const cells of tableRows(markdown)) {
    const [ticker, name, directory, tags = '', industries = '', notes = ''] = cells;
    if (!/^[A-Z][A-Z0-9.-]*$/.test(ticker) || !directory?.endsWith('/')) continue;
    if (map.has(ticker)) throw new Error(`Duplicate company index ticker: ${ticker}`);
    map.set(ticker, { ticker, name, sector: directory.replace(/\/$/, ''), tags, industries: industries.split(/[；;]/).map(x => x.trim()).filter(Boolean), notes, indexed: true });
  }
  if (!map.size) throw new Error('Company index did not contain any recognized rows');
  return map;
}

export function parseIndustryIndex(markdown) {
  const map = new Map();
  for (const cells of tableRows(markdown)) {
    const [name, directory, scope = ''] = cells;
    if (!directory?.endsWith('/') || !name) continue;
    map.set(name, { name, category: directory.replace(/\/$/, ''), scope });
  }
  return map;
}

export function latestBy(items, key, date, warnings, label) {
  const chosen = new Map();
  for (const item of items) {
    const id = key(item), previous = chosen.get(id);
    if (!previous) chosen.set(id, item);
    else {
      if (date(item) === date(previous)) throw new Error(`Ambiguous same-date ${label}: ${id}`);
      if (date(item) > date(previous)) chosen.set(id, item);
      warnings.push(`${label} ${id} 存在多个正式版本；仅展示日期最新的一份。`);
    }
  }
  return chosen;
}
