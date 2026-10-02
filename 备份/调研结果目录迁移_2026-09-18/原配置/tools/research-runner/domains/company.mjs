import { resolveCurrentPlan } from "../research-plan-store.mjs";
import path from "node:path";
import { buildCompanyFormalPrompt } from "../prompts/company.mjs";
import {
  categoryFromOutputFile,
  FUNDAMENTAL_ROOT,
  formatLocalDate,
  formatLocalIso,
  normalizeProjectPath,
  parseLegacyCompanyQueue,
  parseMarkdownTableRows,
  PROJECT_ROOT,
  readUtf8,
  safeIdPart,
} from "../queue-store.mjs";
import {
  backupExistingOutputs,
  rollbackPreparedOutputs,
} from "./output-backup.mjs";
import { primarySubject, safeOutputNamePart } from "./output-path.mjs";

export const COMPANY_CATEGORIES = [
  "AI计算芯片_EDA_IP_custom_ASIC",
  "AI服务器_存储_EMS",
  "AI网络_光互联_连接器",
  "电子材料_化学品_基板_PCB",
  "晶圆制造_前道设备",
  "封测_检测_计量_光罩",
  "功率半导体_电源管理_传感器",
  "配电_电源系统_电气设备",
  "电力_发电_能源_储能",
  "热管理_流体_水处理",
  "工程建设_机电安装",
  "机器人_工业自动化_智能硬件",
  "航空航天_卫星_高可靠系统",
  "云算力_IDC_边缘云",
  "企业软件_数据平台",
  "网络安全_身份权限_治理",
];

export const companyDomain = {
  domain: "company",
  label: "公司调研",
  subjectHelp: "ticker",
  requiresIndexedSubject: true,
  get promptPath() { return resolveCurrentPlan(path.join(FUNDAMENTAL_ROOT, "公司调研", "研究方案")); },
  indexPath: path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
  placeholder: "【公司股票代号】",
  outputPrefix: "基本面/公司调研/",
  outputFilePattern: /_公司调研_\d{4}-\d{2}-\d{2}\.md$/u,
  allowedCategories: new Set(COMPANY_CATEGORIES),
  requiredPaths: [
    path.join(FUNDAMENTAL_ROOT, "公司调研", "研究方案"),
    path.join(FUNDAMENTAL_ROOT, "公司调研", "公司索引.md"),
  ],
  expectedOutputFile(item, runDate) {
    const entry = companyDomain.resolveIndexEntry(item?.subject || "");
    const category = cleanCategory(item?.category || entry?.category || "");
    if (!category) throw new Error(`company output category is missing: ${item?.subject || ""}`);
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    const companyName = safeOutputNamePart(item?.displayName || entry?.displayName, "公司");
    return `基本面/公司调研/${category}/${ticker}_${companyName}_公司调研_${runDate}.md`;
  },
  buildFormalPrompt(item, outputContract) {
    return buildCompanyFormalPrompt(item, companyDomain, outputContract);
  },
  prepareFormalRun(item, outputContract) {
    return backupExistingCompanyOutputs(item, outputContract);
  },
  rollbackFormalRun(item, prepareResult, outputContract) {
    return rollbackCompanyFormalRun(item, prepareResult, outputContract);
  },
  parseIndexEntries() {
    return parseCompanyIndexEntries(companyDomain.indexPath);
  },
  resolveIndexEntry(subject) {
    return resolveCompanyIndexEntry(companyDomain.indexPath, subject);
  },
  createQueueItem(options) {
    return createCompanyQueueItem(options);
  },
  validateOutputFileForItem({ item, fileName }) {
    const ticker = safeOutputNamePart(primarySubject(item?.subject), "ticker");
    if (!fileName.toUpperCase().startsWith(`${ticker.toUpperCase()}_`)) {
      throw new Error(`company outputFile filename must start with ${ticker}_: ${fileName}`);
    }
  },
};

export function parseCompanyIndexEntries(indexPath = companyDomain.indexPath) {
  return parseMarkdownTableRows(readUtf8(indexPath), "股票代号")
    .filter((cells) => cells.length >= 3)
    .map((cells) => ({
      subject: cells[0].trim(),
      displayName: cells[1].trim(),
      category: cleanCategory(cells[2]),
      ...(cells.length > 3 ? {
        businessTags: (cells[3] || "").trim(),
        industrySubjects: (cells[4] || "").trim(),
        listingNote: (cells[5] || "").trim(),
      } : {}),
    }))
    .filter((entry) => entry.subject && entry.category);
}

export function resolveCompanyIndexEntry(indexPath, subject) {
  const wanted = subjectKeys(subject);
  for (const entry of parseCompanyIndexEntries(indexPath)) {
    const keys = subjectKeys(entry.subject);
    if (wanted.some((key) => keys.includes(key))) return entry;
  }
  return null;
}

export function createCompanyQueueItem({
  subject,
  displayName = "",
  category = "",
  sourceDate = formatLocalDate(new Date()),
  status = "pending",
  id = "",
  outputFile = "",
  startedAt = "",
  finishedAt = "",
  attempts = 0,
  note = "",
  extra = {},
} = {}) {
  if (!subject) throw new Error("company queue item requires --subject or --ticker");
  const entry = companyDomain.resolveIndexEntry(subject);
  const nowIso = formatLocalIso(new Date());
  return {
    id: id || `company-${safeIdPart(subject)}-${safeIdPart(nowIso)}`,
    domain: "company",
    sourceDate,
    subject,
    displayName: displayName || entry?.displayName || "",
    category: category || entry?.category || categoryFromOutputFile(outputFile),
    status,
    attempts,
    outputFile: normalizeCompanyOutputFile(outputFile),
    startedAt,
    finishedAt,
    note,
    createdAt: nowIso,
    updatedAt: nowIso,
    ...extra,
  };
}

export function migrateLegacyCompanyMarkdownQueue({ oldQueuePath, force = false }) {
  const rows = parseLegacyCompanyQueue(readUtf8(oldQueuePath));
  const active = [];
  const done = [];
  const nowIso = formatLocalIso(new Date());

  for (const row of rows) {
    const item = createCompanyQueueItem({
      subject: row.subject,
      displayName: row.displayName,
      sourceDate: row.sourceDate,
      status: row.status || "pending",
      attempts: row.attempts,
      outputFile: row.outputFile,
      startedAt: row.startedAt,
      finishedAt: row.finishedAt,
      note: row.note,
      id: `company-${safeIdPart(row.subject)}-${safeIdPart(row.row)}`,
      extra: { legacyQueueRow: row.row },
    });

    if (item.status === "done") done.push({ ...item, archivedAt: nowIso });
    else active.push(item);
  }

  return { active, done, force };
}

export function backupExistingCompanyOutputs(item, outputContract = {}) {
  const outputDir = companyOutputDir(item);
  const primary = primarySubject(item?.subject);
  if (!outputDir || !primary) return { backupDir: "", files: [] };

  return backupExistingOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    backupKey: primary,
    expectedFileName: outputContract.expectedOutputFile?.split("/").pop() || "",
    matchFileName: (fileName) => fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyDomain.outputFilePattern.test(fileName),
  });
}

export function rollbackCompanyFormalRun(item, prepareResult = {}, outputContract = {}) {
  const outputDir = companyOutputDir(item);
  const primary = primarySubject(item?.subject);
  if (!outputDir || !primary) return { removed: [], files: [] };

  return rollbackPreparedOutputs({
    rootDir: PROJECT_ROOT,
    outputDir,
    expectedFileName: outputContract.expectedOutputFile?.split("/").pop() || "",
    prepareResult,
    newFileNameMatcher: (fileName) => fileName.toUpperCase().startsWith(`${primary.toUpperCase()}_`)
      && companyDomain.outputFilePattern.test(fileName),
  });
}

function companyOutputDir(item) {
  const entry = companyDomain.resolveIndexEntry(item?.subject || "");
  const category = cleanCategory(item?.category || entry?.category || "");
  if (!category) return "";
  return path.join(FUNDAMENTAL_ROOT, "公司调研", category);
}

function subjectKeys(subject) {
  const raw = String(subject || "").trim();
  return [raw, ...raw.split("/")]
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => part.toUpperCase().replace(/\s+/g, ""));
}

function cleanCategory(value) {
  return String(value || "").replace(/`/g, "").replace(/[\\/]\s*$/, "").trim();
}

function normalizeCompanyOutputFile(value) {
  const normalized = normalizeProjectPath(value);
  return normalized.startsWith("公司调研/") ? `基本面/${normalized}` : normalized;
}
