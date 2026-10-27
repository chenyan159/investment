import path from 'node:path';
import { filesUnder, readSource, dateFromName, latestBy, reportId, reportTitle, reportSummary, reportSections, writeJson, slash } from './common.mjs';

export async function buildResearch({ root, output, manifest, warnings, companyIndex, industryIndex }) {
  const documents = [];
  const normalizedName = name => name.replace(/[\s/_]+/g, '').toLocaleLowerCase();
  const industryNames = new Map();
  for (const entry of industryIndex.values()) {
    const key = normalizedName(entry.name);
    if (industryNames.has(key)) throw new Error(`Ambiguous normalized industry index: ${entry.name}`);
    industryNames.set(key, entry);
  }
  for (const [kind, directory] of [['background', '产业背景'], ['industry', '行业调研'], ['company', '公司调研']]) {
    const results = path.join(root, '基本面', directory, '结果');
    const candidates = [];
    for (const file of await filesUnder(results)) {
      const { text: markdown, source } = await readSource(file, root, manifest);
      const filename = path.basename(file, '.md');
      const date = dateFromName(file);
      if (!date) throw new Error(`Formal research report has no dated filename: ${source}`);
      const ticker = kind === 'company' ? filename.split('_')[0] : null;
      if (ticker && !/^[A-Z][A-Z0-9.-]*$/.test(ticker)) throw new Error(`Unrecognized company report filename: ${source}`);
      const fileSubject = kind === 'company' ? ticker : filename.replace(/_\d{4}-\d{2}-\d{2}$/, '').replace(/^行业调研_/, '');
      const industry = kind === 'industry' ? industryNames.get(normalizedName(fileSubject)) : null;
      const subject = industry?.name ?? fileSubject;
      const relative = slash(path.relative(results, file));
      const folder = relative.includes('/') ? relative.split('/')[0] : '';
      const category = kind === 'background' ? (filename.startsWith('会议调研_') ? '会议调研' : '产业背景专题') : folder;
      if (kind === 'industry' && !industryIndex.has(subject)) warnings.push(`行业报告「${subject}」未在当前行业索引定位，仍按正式结果保留。`);
      const id = reportId(kind, `${kind}/${subject}`);
      const summary = {
        id, kind, title: reportTitle(markdown, subject), subject, date, category, ticker,
        name: ticker ? companyIndex.get(ticker)?.name ?? filename.split('_').slice(1, -2).join(' ') : subject,
        summary: reportSummary(markdown), source,
        scope: industry?.scope ?? '',
        detailUrl: `data/research/${id}.json`, reportUrl: null,
      };
      candidates.push({ key: subject, date, summary, detail: { ...summary, markdown, sections: reportSections(markdown) } });
    }
    documents.push(...latestBy(candidates, item => item.key, item => item.date, warnings, directory).values());
  }
  for (const document of documents) {
    await writeJson(output, `research/${document.summary.id}.json`, document.detail);
  }
  return documents.sort((a, b) => b.date.localeCompare(a.date) || a.summary.title.localeCompare(b.summary.title, 'zh-CN'));
}
