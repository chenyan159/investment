import fs from "node:fs";
import { COMPANY_CATEGORIES, companyDomain } from "./domains/company.mjs";
import { INDUSTRY_CATEGORIES, industryDomain } from "./domains/industry.mjs";
import { formatLocalDate, FUNDAMENTAL_ROOT } from "./queue-store.mjs";

export function updateIndexForQueueAdd(domain, options) {
  if (domain === "company") return updateCompanyIndex(options);
  if (domain === "industry") return updateIndustryIndex(options);
  throw new Error("--update-index is only supported for add-company and add-industry");
}

function updateCompanyIndex({ subject, displayName = "", category = "", dryRun = false } = {}) {
  const ticker = String(subject || "").trim();
  if (!ticker) throw new Error("company index update requires --ticker or --subject");

  const entries = companyDomain.parseIndexEntries();
  const existing = companyDomain.resolveIndexEntry(ticker);
  const cleanInputCategory = cleanCategory(category);
  const cleanInputName = String(displayName || "").trim();

  if (existing) {
    if (cleanInputName && cleanInputName !== existing.displayName) {
      throw new Error(`company already exists in index with different display name: ${existing.displayName}`);
    }
    if (cleanInputCategory && cleanInputCategory !== existing.category) {
      throw new Error(`company already exists in index with different category: ${existing.category}`);
    }
    return {
      changed: false,
      indexPath: companyDomain.indexPath,
      subject: existing.subject,
      displayName: existing.displayName,
      category: existing.category,
      reason: "already indexed",
    };
  }

  if (!cleanInputName) throw new Error("new company index entry requires --display-name");
  if (!cleanInputCategory) throw new Error("new company index entry requires --category");
  assertAllowedCategory("company", cleanInputCategory, COMPANY_CATEGORIES);

  const nextEntry = {
    subject: ticker,
    displayName: cleanInputName,
    category: cleanInputCategory,
  };
  const nextEntries = [...entries, nextEntry];
  const body = renderCompanyIndex(nextEntries);
  if (!dryRun) fs.writeFileSync(companyDomain.indexPath, body, "utf8");

  return {
    changed: true,
    dryRun,
    indexPath: companyDomain.indexPath,
    subject: nextEntry.subject,
    displayName: nextEntry.displayName,
    category: nextEntry.category,
    reason: dryRun ? "would add company index entry" : "added company index entry",
  };
}

function updateIndustryIndex({ subject, category = "", dryRun = false } = {}) {
  const industryName = String(subject || "").trim();
  if (!industryName) throw new Error("industry index update requires --subject");

  const entries = industryDomain.parseIndexEntries();
  const existing = industryDomain.resolveIndexEntry(industryName);
  const cleanInputCategory = cleanCategory(category);

  if (existing) {
    if (cleanInputCategory && cleanInputCategory !== existing.category) {
      throw new Error(`industry already exists in index with different category: ${existing.category}`);
    }
    return {
      changed: false,
      indexPath: industryDomain.indexPath,
      subject: existing.subject,
      displayName: existing.displayName,
      category: existing.category,
      reason: "already indexed",
    };
  }

  if (!cleanInputCategory) throw new Error("new industry index entry requires --category");
  assertAllowedCategory("industry", cleanInputCategory, INDUSTRY_CATEGORIES);

  const nextEntry = {
    subject: industryName,
    displayName: industryName,
    category: cleanInputCategory,
  };
  const nextEntries = [...entries, nextEntry];
  const body = renderIndustryIndex(nextEntries);
  if (!dryRun) fs.writeFileSync(industryDomain.indexPath, body, "utf8");

  return {
    changed: true,
    dryRun,
    indexPath: industryDomain.indexPath,
    subject: nextEntry.subject,
    displayName: nextEntry.displayName,
    category: nextEntry.category,
    reason: dryRun ? "would add industry index entry" : "added industry index entry",
  };
}

function renderCompanyIndex(entries) {
  const orderedEntries = orderEntriesByCategory(entries, COMPANY_CATEGORIES);
  const counts = countByCategory(orderedEntries, COMPANY_CATEGORIES);
  const today = formatLocalDate(new Date());

  const lines = [
    `# ${orderedEntries.length}家公司股票代号、公司名称和分类目录`,
    "",
    `生成日期：${today}`,
    "",
    `来源：\`${FUNDAMENTAL_ROOT}\\公司调研\\结果\` 下 ${COMPANY_CATEGORIES.length} 个正式分类目录内的公司调研 Markdown 文件，以及新增待调研公司。`,
    "",
    "生成口径：每个正式分类目录直属 `.md` 公司调研文件或索引中新增待调研项算一家公司；股票代号、公司名称和所属分类目录从当前文件名、所在目录或人工指定目录抽取；`研究方法/`、`tmp/`、`评估备份/`、各类 `备份/` 子目录、根目录对比评估文件和 `AGENTS.md` 不计入公司数量。",
    "",
    "## 目录统计",
    "",
    ...COMPANY_CATEGORIES.map((categoryName) => `- ${categoryName}：${counts.get(categoryName) || 0} 家`),
    "",
    "## 索引表",
    "",
    "下表目录列相对于本调研目录的 `结果/`；分类名称保持不变。",
    "",
    "| 股票代号 | 公司名称 | 目录 | 业务标签 | 关联行业 | 交易身份与登记备注 |",
    "|---|---|---|---|---|---|",
    ...orderedEntries.map((entry) => "| " + [tableCell(entry.subject), tableCell(entry.displayName), "`" + tableCell(entry.category) + "/`", tableCell(entry.businessTags), tableCell(entry.industrySubjects), tableCell(entry.listingNote)].join(" | ") + " |"),
    "",
  ];

  return `${lines.join("\n")}`;
}

function renderIndustryIndex(entries) {
  const orderedEntries = orderEntriesByCategory(entries, INDUSTRY_CATEGORIES);
  const counts = countByCategory(orderedEntries, INDUSTRY_CATEGORIES);
  const today = formatLocalDate(new Date());

  const lines = [
    "# " + orderedEntries.length + "个行业与横向专题名称和分类目录",
    "",
    `生成日期：${today}`,
    "",
    `来源：\`${FUNDAMENTAL_ROOT}\\行业调研\\结果\` 下 ${INDUSTRY_CATEGORIES.length} 个正式分类目录内的行业调研 Markdown 文件，以及新增待调研行业。`,
    "",
    "生成口径：每个正式分类目录直属 `.md` 行业调研文件或索引中新增待调研项算一个行业；行业名称和所属分类目录从当前文件名、所在目录或人工指定目录抽取；`研究方法/`、`产业背景/`、`顶级conference纪要/`、各类 `备份/` 子目录、根目录专题文件、`AGENTS.md` 和 `desktop.ini` 不计入行业数量。",
    "",
    "## 目录统计",
    "",
    ...INDUSTRY_CATEGORIES.map((categoryName) => `- ${categoryName}：${counts.get(categoryName) || 0} 个行业`),
    "",
    "## 索引表",
    "",
    "下表目录列相对于本调研目录的 `结果/`；分类名称保持不变。",
    "",
    "| 行业名称 | 目录 | 研究范围提示 | 专题类型 | 分类变更备注 |",
    "|---|---|---|---|---|",
    ...orderedEntries.map((entry) => "| " + [tableCell(entry.subject), "`" + tableCell(entry.category) + "/`", tableCell(entry.researchScope), tableCell(entry.topicType || "行业"), tableCell(entry.classificationNote)].join(" | ") + " |"),
    "",
  ];

  return `${lines.join("\n")}`;
}

function orderEntriesByCategory(entries, categoryOrder) {
  const knownCategories = new Set(categoryOrder);
  const ordered = categoryOrder.flatMap((categoryName) => entries.filter((entry) => entry.category === categoryName));
  const unknown = entries.filter((entry) => !knownCategories.has(entry.category));
  return [...ordered, ...unknown];
}

function countByCategory(entries, categoryOrder) {
  const counts = new Map(categoryOrder.map((categoryName) => [categoryName, 0]));
  for (const entry of entries) {
    counts.set(entry.category, (counts.get(entry.category) || 0) + 1);
  }
  return counts;
}

function assertAllowedCategory(domain, category, allowedCategories) {
  if (!allowedCategories.includes(category)) {
    throw new Error(`unsupported ${domain} category: ${category}`);
  }
}

function cleanCategory(value) {
  return String(value || "").replace(/`/g, "").replace(/[\\/]\s*$/, "").trim();
}

function tableCell(value) {
  return String(value || "").replace(/\r?\n/g, " ").replace(/\|/g, "/").trim();
}
