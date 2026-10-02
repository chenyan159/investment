import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { companyDomain, COMPANY_CATEGORIES } from "../domains/company.mjs";
import { industryDomain, INDUSTRY_CATEGORIES } from "../domains/industry.mjs";
import { updateIndexForQueueAdd } from "../index-updater.mjs";

function withTemporaryIndex(domain, body, run) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "index-classification-"));
  const file = path.join(dir, "index.md");
  const original = domain.indexPath;
  try {
    fs.writeFileSync(file, body, "utf8");
    domain.indexPath = file;
    run(file);
  } finally {
    domain.indexPath = original;
    assert.equal(path.dirname(path.resolve(dir)), path.resolve(os.tmpdir()));
    assert.ok(path.basename(dir).startsWith("index-classification-"));
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test("adding an indexed company preserves its existing multi-industry classification", () => {
  const tick = String.fromCharCode(96);
  const category = "航空航天_卫星_高可靠系统";
  const body = [
    "| 股票代号 | 公司名称 | 目录 | 业务标签 | 关联行业 | 交易身份与登记备注 |",
    "|---|---|---|---|---|---|",
    "| KEPT | Existing Company | " + tick + category + "/" + tick + " | 卫星、通信 | 运载火箭、航天器与空间基础设施；低轨卫星通信、直连手机与地面终端 | 原交易备注 |",
  ].join("\n");
  withTemporaryIndex(companyDomain, body, (file) => {
    updateIndexForQueueAdd("company", {
      subject: "ADDED",
      displayName: "Added Company",
      category: "企业软件_数据平台",
    });
    const rows = companyDomain.parseIndexEntries();
    assert.equal(rows.length, 2);
    const kept = rows.find((row) => row.subject === "KEPT");
    assert.equal(kept.category, category);
    assert.equal(kept.businessTags, "卫星、通信");
    assert.equal(kept.industrySubjects, "运载火箭、航天器与空间基础设施；低轨卫星通信、直连手机与地面终端");
    assert.equal(kept.listingNote, "原交易备注");
    assert.ok(fs.readFileSync(file, "utf8").includes("下 " + COMPANY_CATEGORIES.length + " 个正式分类目录"));
  });
});

test("adding an industry preserves scope, horizontal type and classification history", () => {
  const tick = String.fromCharCode(96);
  const body = [
    "| 行业名称 | 目录 | 研究范围提示 | 专题类型 | 分类变更备注 |",
    "|---|---|---|---|---|",
    "| Existing standard | " + tick + "AI网络_光互联_铜互联/" + tick + " | 不重复加总市场。 | 横向专题 | 原题名和历史保留 |",
  ].join("\n");
  withTemporaryIndex(industryDomain, body, (file) => {
    updateIndexForQueueAdd("industry", {
      subject: "Added industry",
      category: "工业自动化_机器人_感知",
    });
    const rows = industryDomain.parseIndexEntries();
    assert.equal(rows.length, 2);
    const kept = rows.find((row) => row.subject === "Existing standard");
    assert.equal(kept.researchScope, "不重复加总市场。");
    assert.equal(kept.topicType, "横向专题");
    assert.equal(kept.classificationNote, "原题名和历史保留");
    assert.ok(fs.readFileSync(file, "utf8").includes("下 " + INDUSTRY_CATEGORIES.length + " 个正式分类目录"));
  });
});
