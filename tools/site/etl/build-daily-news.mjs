import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SITE_ROOT = path.resolve(__dirname, "..");
const PROJECT_ROOT = path.resolve(SITE_ROOT, "..", "..");
const PUBLIC_DATA = path.join(SITE_ROOT, "public", "data");
const FINANCIAL_MATERIALS_ROOT = path.join(PROJECT_ROOT, "金融资料");
const DAILY_NEWS_ROOT = path.join(FINANCIAL_MATERIALS_ROOT, "最新AI新闻");
const DAILY_NEWS_SCRIPT_ROOT = path.join(DAILY_NEWS_ROOT, "新闻稿");
const DAILY_NEWS_AUDIO_ROOT = path.join(DAILY_NEWS_ROOT, "语音输出");
const DEFAULT_OUTPUT_ROOT = path.join(PUBLIC_DATA, "daily-news");
const OUTPUT_ROOT = process.env.PROJECT_ANANTA_OUTPUT_ROOT?.trim()
  ? path.resolve(process.env.PROJECT_ANANTA_OUTPUT_ROOT)
  : DEFAULT_OUTPUT_ROOT;
const CURRENT_FILE = path.join(OUTPUT_ROOT, "current.json");
const AUDIO_OUTPUT_ROOT = path.join(OUTPUT_ROOT, "audio");
const DAILY_NEWS_LIMIT = 10;

export async function buildDailyNews() {
  const scriptFiles = groupByDate(
    await datedFiles(DAILY_NEWS_SCRIPT_ROOT, /^每日新闻稿_(\d{4}-\d{2}-\d{2})(?:[\s\S]*)\.(md|txt)$/iu),
  );
  const audioFiles = groupByDate(
    await datedFiles(DAILY_NEWS_AUDIO_ROOT, /^每日AI产业链新闻_(\d{4}-\d{2}-\d{2})(?:[\s\S]*)\.(mp3|wav|m4a|ogg)$/iu),
  );
  const dates = [...scriptFiles.keys()].sort().reverse().slice(0, DAILY_NEWS_LIMIT);
  if (!dates.length) throw new Error("没有匹配到可发布的每日 AI 新闻稿");

  await prepareOutput();
  const items = [];

  for (const date of dates) {
    const script = chooseDailyNewsScript(scriptFiles.get(date) || []);
    if (!script) continue;
    const rawMarkdown = redactLocalPaths(await readText(script.file));
    const audio = chooseDailyNewsAudio(audioFiles.get(date) || []);
    let audioPayload = null;

    if (audio) {
      const extension = path.extname(audio.name).toLowerCase();
      const publicFileName = `daily-ai-news-${date}${extension}`;
      await fs.copyFile(audio.file, path.join(AUDIO_OUTPUT_ROOT, publicFileName));
      audioPayload = {
        url: `data/daily-news/audio/${publicFileName}`,
        format: extension.replace(/^\./u, ""),
        sourcePath: relativeProjectPath(audio.file),
        originalFileName: audio.name,
        sizeBytes: audio.size,
      };
    }

    items.push({
      date,
      title: firstMatch(rawMarkdown, /^#\s+(.+)$/mu) || `每日新闻稿 ${date}`,
      summary: markdownSummary(rawMarkdown),
      sourcePath: relativeProjectPath(script.file),
      fileName: script.name,
      sizeBytes: script.size,
      markdown: rawMarkdown,
      audio: audioPayload,
    });
  }

  if (!items.length) throw new Error("每日 AI 新闻稿解析后为空");
  const payload = {
    schemaVersion: 1,
    source: "dailyNewsSiteData",
    generatedAt: new Date().toISOString(),
    limit: DAILY_NEWS_LIMIT,
    latestDate: items[0].date,
    oldestDate: items.at(-1).date,
    sourceDirs: {
      scripts: relativeProjectPath(DAILY_NEWS_SCRIPT_ROOT),
      audio: relativeProjectPath(DAILY_NEWS_AUDIO_ROOT),
    },
    items,
  };

  await writeJson(CURRENT_FILE, payload);
  console.log(`Daily news site data: ${items.length} days, latest ${payload.latestDate}.`);
  console.log(`Wrote ${OUTPUT_ROOT}`);
  return payload;
}

async function prepareOutput() {
  const resolved = path.resolve(OUTPUT_ROOT);
  const expected = path.resolve(DEFAULT_OUTPUT_ROOT);
  const isStaging = path.basename(resolved).startsWith(".daily-news-");
  if (path.dirname(resolved) !== path.resolve(PUBLIC_DATA) || (resolved !== expected && !isStaging)) {
    throw new Error(`拒绝清理非预期目录：${resolved}`);
  }
  await fs.rm(resolved, { recursive: true, force: true });
  await fs.mkdir(AUDIO_OUTPUT_ROOT, { recursive: true });
}

async function datedFiles(dir, pattern) {
  const names = await safeReadDir(dir);
  const files = [];
  for (const name of names) {
    const match = name.match(pattern);
    if (!match) continue;
    const file = path.join(dir, name);
    const stat = await fs.stat(file).catch(() => null);
    if (!stat?.isFile()) continue;
    files.push({
      date: match[1],
      ext: path.extname(name).toLowerCase(),
      file,
      name,
      size: stat.size,
      mtimeMs: stat.mtimeMs,
    });
  }
  return files;
}

function groupByDate(files) {
  const byDate = new Map();
  for (const file of files) {
    if (!byDate.has(file.date)) byDate.set(file.date, []);
    byDate.get(file.date).push(file);
  }
  return byDate;
}

function chooseDailyNewsScript(files) {
  return [...files].sort((a, b) => {
    const priority = dailyNewsScriptPriority(b) - dailyNewsScriptPriority(a);
    return priority || b.name.localeCompare(a.name, "zh-Hans-CN");
  })[0] || null;
}

function dailyNewsScriptPriority(file) {
  return (file.ext === ".md" ? 100 : 0) + (!file.name.includes("口播稿") ? 10 : 0);
}

function chooseDailyNewsAudio(files) {
  return [...files].sort((a, b) => {
    const priority = dailyNewsAudioPriority(b) - dailyNewsAudioPriority(a);
    return priority || b.mtimeMs - a.mtimeMs;
  })[0] || null;
}

function dailyNewsAudioPriority(file) {
  return (
    (file.ext === ".mp3" ? 100 : 0) +
    (file.name.includes("新闻口播稿") ? 10 : 0) +
    (file.name.includes("中文语音") ? 5 : 0)
  );
}

function markdownSummary(markdown) {
  const paragraph = markdown
    .split(/\r?\n/u)
    .map((line) => line.trim())
    .find((line) => line && !line.startsWith("#") && !line.startsWith("|") && !/^-{3,}$/u.test(line));
  if (!paragraph) return "";
  const compact = paragraph.replace(/\s+/gu, " ");
  return compact.length > 220 ? `${compact.slice(0, 217)}...` : compact;
}

function firstMatch(text, pattern) {
  return String(text || "").match(pattern)?.[1]?.trim() || "";
}

function relativeProjectPath(file) {
  return path.relative(PROJECT_ROOT, file).replace(/\\/gu, "/");
}

function redactLocalPaths(text) {
  return String(text)
    .replace(/D:\\(?:drive\\)?Investment\\/giu, "Investment\\")
    .replace(/D:\/(?:drive\/)?Investment\//giu, "Investment/");
}

async function safeReadDir(dir) {
  try {
    return await fs.readdir(dir);
  } catch {
    return [];
  }
}

async function readText(file) {
  return (await fs.readFile(file, "utf8")).replace(/^\ufeff/u, "");
}

async function writeJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

if (path.resolve(process.argv[1] || "") === __filename) {
  buildDailyNews().catch((error) => {
    console.error(error.stack || error.message || error);
    process.exitCode = 1;
  });
}
