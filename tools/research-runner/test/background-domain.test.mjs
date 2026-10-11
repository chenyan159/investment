import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  backgroundDomain,
  backupBackgroundOutputs,
  createBackgroundQueueItem,
  isSameSubjectOutput,
  listBackgroundTopics,
  parseConferenceSubject,
  rollbackBackgroundRun,
} from "../domains/background.mjs";
import { BACKGROUND_PLAN_DIRECTORY, bindResearchPlan } from "../research-plan-store.mjs";
import { createOutputContract, validateOutputFilePath } from "../validators/output-validator.mjs";

const startedAt = "2026-10-12 09:00:00";
const queued = (subject) => bindResearchPlan({ ...backgroundDomain.createQueueItem({ subject }), startedAt });

test("registered topics keep their plan ids and write one flat result file", () => {
  const expected = {
    "AI产业链全局图谱与口径字典": "background-1",
    "AI产业链瓶颈与反证指标总表": "background-2",
    "全球AI需求与Token经济框架": "background-3",
    "数据中心建设规模": "background-4",
    "头部AI芯片": "background-5",
  };
  // 已登记专题沿用原ID；之后新增的专题无需登记，按 background:<专题> 绑定。
  const topics = [...listBackgroundTopics()];
  for (const topic of Object.keys(expected)) assert.ok(topics.includes(topic), topic);
  for (const topic of topics) {
    const item = queued(topic);
    assert.equal(item.planId, expected[topic] || `background:${topic}`);
    const contract = createOutputContract(item, backgroundDomain);
    assert.equal(contract.expectedOutputFile, `基本面/产业背景/结果/${topic}_2026-10-12.md`);
    const prompt = backgroundDomain.buildFormalPrompt(item, contract);
    assert.ok(prompt.includes(contract.expectedOutputFile));
    assert.ok(!prompt.includes("基本面\\行业调研\\产业背景"));
  }
});

test("conference subjects use the shared plan, fill placeholders and name files by series and year", () => {
  assert.deepEqual(parseConferenceSubject("OCP Global Summit 2026"), { series: "OCP Global Summit", year: "2026" });
  assert.equal(parseConferenceSubject("OCP Global Summit"), null);
  const item = queued("OCP  Global Summit 2026");
  assert.equal(item.planId, "conference");
  assert.equal(item.subject, "OCP Global Summit 2026");
  const contract = createOutputContract(item, backgroundDomain);
  assert.equal(contract.expectedOutputFile, "基本面/产业背景/结果/会议调研_OCP_Global_Summit_2026_2026-10-12.md");
  const prompt = backgroundDomain.buildFormalPrompt(item, contract);
  assert.ok(prompt.includes("OCP Global Summit"));
  assert.ok(!prompt.includes("【会议名称】") && !prompt.includes("【会议年份】"));
});

test("outputs must stay in 结果 and belong to the queued subject", () => {
  const item = queued("NVIDIA GTC 2027");
  assert.throws(() => validateOutputFilePath({ item, domain: backgroundDomain, outputFile: "基本面/产业背景/备份/会议调研_NVIDIA_GTC_2027_2026-10-12.md" }));
  assert.throws(() => validateOutputFilePath({ item, domain: backgroundDomain, outputFile: "基本面/产业背景/结果/会议调研_OFC_2027_2026-10-12.md" }), /does not belong/);
  validateOutputFilePath({ item, domain: backgroundDomain, outputFile: "基本面/产业背景/结果/会议调研_NVIDIA_GTC_2027_2026-10-12.md" });
});

test("unknown subjects and older conference editions are refused", () => {
  assert.equal(backgroundDomain.resolveIndexEntry("不存在的专题"), null);
  assert.throws(() => backgroundDomain.createQueueItem({ subject: "不存在的专题" }), /background subject/);
  const resultDir = fs.mkdtempSync(path.join(os.tmpdir(), "background-newer-"));
  try {
    fs.writeFileSync(path.join(resultDir, "会议调研_NVIDIA_GTC_2026_2026-05-08.md"), "x");
    assert.throws(() => backgroundDomain.createQueueItem({ subject: "NVIDIA GTC 2025", resultDir }), /更新的一届/);
    assert.equal(backgroundDomain.createQueueItem({ subject: "NVIDIA GTC 2027", resultDir }).conferenceYear, "2027");
  } finally {
    fs.rmSync(resultDir, { recursive: true, force: true });
  }
});

test("rerun moves only the same topic or conference series into 备份, outside 结果, and rollback restores it", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "background-backup-"));
  const resultDir = path.join(root, "基本面", "产业背景", "结果");
  const backupDir = path.join(root, "基本面", "产业背景", "备份");
  const files = {
    gtc: "会议调研_NVIDIA_GTC_2026_2026-05-08.md",
    taipei: "会议调研_NVIDIA_GTC_Taipei_2026_2026-06-11.md",
    topic: "数据中心建设规模_2026-09-18.md",
    lookalike: "数据中心建设规模扩展_2026-09-18.md",
  };
  try {
    fs.mkdirSync(resultDir, { recursive: true });
    for (const name of Object.values(files)) fs.writeFileSync(path.join(resultDir, name), name);
    const options = { rootDir: root, resultDir, backupDir };

    const conference = createBackgroundQueueItem({ subject: "NVIDIA GTC 2027", resultDir });
    const conferenceContract = { expectedOutputFile: "基本面/产业背景/结果/会议调研_NVIDIA_GTC_2027_2026-10-12.md" };
    const prepared = backupBackgroundOutputs(conference, conferenceContract, options);
    assert.deepEqual(prepared.files.map((file) => path.posix.basename(file.from)), [files.gtc]);
    assert.match(prepared.backupDir, /^基本面\/产业背景\/备份\//u);
    assert.ok(fs.existsSync(path.join(resultDir, files.taipei)));
    assert.equal(fs.existsSync(path.join(resultDir, "备份")), false);

    fs.writeFileSync(path.join(resultDir, "会议调研_NVIDIA_GTC_2027_2026-10-12.md"), "new");
    rollbackBackgroundRun(conference, prepared, conferenceContract, options);
    assert.ok(fs.existsSync(path.join(resultDir, files.gtc)));
    assert.equal(fs.existsSync(path.join(resultDir, "会议调研_NVIDIA_GTC_2027_2026-10-12.md")), false);

    const topic = createBackgroundQueueItem({ subject: "数据中心建设规模", resultDir });
    const topicPrepared = backupBackgroundOutputs(topic, { expectedOutputFile: "基本面/产业背景/结果/数据中心建设规模_2026-10-12.md" }, options);
    assert.deepEqual(topicPrepared.files.map((file) => path.posix.basename(file.from)), [files.topic]);
    assert.ok(fs.existsSync(path.join(resultDir, files.lookalike)));
    assert.ok(isSameSubjectOutput({ kind: "conference", series: "nvidia-gtc" }, files.gtc));
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("a new topic directory needs no registration to bind its plan", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "background-topic-"));
  try {
    const dir = path.join(root, BACKGROUND_PLAN_DIRECTORY, "新专题");
    fs.mkdirSync(path.join(dir, "20261010_090000"), { recursive: true });
    fs.writeFileSync(path.join(dir, "研究方案_20261010_090000.md"), "# 新专题\n");
    fs.copyFileSync(path.join(dir, "研究方案_20261010_090000.md"), path.join(dir, "20261010_090000", "研究方案_20261010_090000.md"));
    const item = bindResearchPlan({ domain: "background", subject: "新专题", backgroundKind: "topic", backgroundTopic: "新专题" }, root);
    assert.equal(item.planId, "background:新专题");
    assert.equal(item.planVersion, "20261010_090000");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
