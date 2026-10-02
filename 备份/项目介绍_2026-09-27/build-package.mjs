import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { parseCompanyIndexEntries } from '../../tools/research-runner/domains/company.mjs';
import { parseIndustryIndexEntries } from '../../tools/research-runner/domains/industry.mjs';

const root = 'D:/investment';
const out = path.join(root, '备份/项目介绍_2026-09-27');
const registry = JSON.parse(fs.readFileSync(path.join(root, 'tools/research-runner/research-plans.json'), 'utf8'));
const ids = ['background-1','background-2','background-3','background-4','background-5','conference','industry','company','company-investment-decision'];
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const entries = ids.map((id, i) => {
  const p = registry.find(p => p.id === id);
  const files = fs.readdirSync(path.join(root,p.directory)).filter(n => /^研究方案_\d{8}_\d{6}\.md$/.test(n));
  if (files.length !== 1) throw Error(`Expected one current plan: ${id}`);
  return {id,label:p.label,source:`${p.directory}/${files[0]}`,filename:`${String(i+1).padStart(2,'0')}_${p.label}_${files[0]}`};
});
entries.push({id:'company-index',label:'公司列表',source:'基本面/公司调研/公司索引.md',filename:'10_公司索引.md'}, {id:'industry-index',label:'行业列表',source:'基本面/行业调研/行业索引.md',filename:'11_行业索引.md'});
fs.mkdirSync(path.join(out,'附件'),{recursive:true});
for (const e of entries) {
  const bytes = fs.readFileSync(path.join(root,e.source));
  e.sha256 = hash(bytes); e.bytes = bytes.length;
  fs.writeFileSync(path.join(out,'附件',e.filename),bytes);
  if (hash(fs.readFileSync(path.join(out,'附件',e.filename))) !== e.sha256) throw Error('Copy mismatch');
}
const c=parseCompanyIndexEntries(), i=parseIndustryIndexEntries();
if(c.length!==221 || i.length!==91) throw Error('Index counts changed; review introduction');
const esc = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const tableRows=entries.map(e=>`<tr><td>${esc(e.filename)}</td><td>${esc(e.id)}</td><td><code>D:\\investment\\${esc(e.source.replaceAll('/','\\'))}</code></td></tr>`).join('\n');
const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Investment 研究项目介绍</title></head><body style="font-family:Arial,'Microsoft YaHei',sans-serif;line-height:1.7;color:#20252b;max-width:1100px;margin:24px auto;padding:0 16px">
<h1>Investment 研究项目介绍</h1>
<p>核对日期：2026-09-27（America/Los_Angeles）。项目唯一当前根目录：<code>D:\\investment</code>。本介绍依据现行研究方案、索引及 Research Runner 实现整理；调度描述属于静态代码核对，不代表本次重新运行过整条研究流水线。</p>
<h2>1. 项目要做什么</h2>
<p>这是一套从外部原始证据出发，逐层形成产业背景、行业研究、公司研究和公司情景投资决策的研究系统。研究方案规定每层需要回答的问题、允许使用的资料和交付要求；公司与行业索引定义研究对象和输出归属；Research Runner 负责把这些研究任务批量、独立、可追溯地执行。</p>
<p>当前索引实际解析得到 <strong>221 家公司、16 个公司主分类，91 个行业研究主题、7 个行业父类别</strong>。公司与行业是多对多关系：一家公司可以涉及多个行业，一个行业也可以覆盖多家公司。这些数量是登记覆盖范围，不等于已完成报告数量。索引中的历史完成情况也不能当作今天的运行状态。</p>
<h2>2. 九份研究方案与各层职责</h2>
<table border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;width:100%"><tr><th>研究层</th><th>方案 / planId</th><th>执行 domain</th><th>职责与正式成果位置（相对项目根）</th></tr>
<tr><td rowspan="6">产业背景与会议</td><td>AI产业链全局图谱与口径字典 / background-1</td><td>file-run</td><td>产业分层、计量口径、跨层对账；成果进入 基本面/行业调研/产业背景/。</td></tr>
<tr><td>AI产业链瓶颈与反证指标总表 / background-2</td><td>file-run</td><td>约束、缓解、价值转移与反证；成果进入同一产业背景目录。</td></tr>
<tr><td>全球AI需求与Token经济框架 / background-3</td><td>file-run</td><td>实际使用、支付、Token经济及基础设施预算；成果进入同一产业背景目录。</td></tr>
<tr><td>数据中心建设规模 / background-4</td><td>file-run</td><td>资金、建设、上电、验收与订单传导；成果进入同一产业背景目录。</td></tr>
<tr><td>头部AI芯片 / background-5</td><td>file-run</td><td>技术路线、供给释放、平台竞争与配套需求；成果进入同一产业背景目录。</td></tr>
<tr><td>会议调研 / conference</td><td>file-run</td><td>按会议名称和年份研究公开成果；默认成果进入 基本面/行业调研/产业背景/顶级会议信息/。</td></tr>
<tr><td>行业</td><td>行业调研 / industry</td><td>industry</td><td>需求、有效供给、技术、竞争、价格与价值分配；成果进入 基本面/行业调研/结果/&lt;索引分类&gt;/。</td></tr>
<tr><td>公司</td><td>公司调研 / company</td><td>company</td><td>业务、技术、客户、竞争、经营与资本条件；成果进入 基本面/公司调研/结果/&lt;索引分类&gt;/。</td></tr>
<tr><td>投资决策</td><td>公司情景投资决策 / company-investment-decision</td><td>company-investment-decision</td><td>业务前景、经营情景、权益传导、情景股价与当前投资判断；成果进入 分析报告/公司情景投资决策/结果/。</td></tr></table>
<p><strong>planId 与 domain 是两回事：</strong>planId 标识具体研究方案及版本；domain 标识执行适配器。前六份方案共享 file-run 执行器，并非六个独立 domain。会议方案可以复用于多场会议，故九份方案不等于九项运行任务。</p>
<h2>3. 研究资料的 dependency：谁可以读取谁</h2>
<pre style="background:#f3f5f7;padding:16px;white-space:pre-wrap">外部公开原始资料
  ├─ 五个产业背景专题（彼此独立） ─┐
  └─ 指定会议研究（各会议独立） ──┴─ 产业背景资料库
                                      ├─ 行业调研 → 行业报告 ─┬─ 公司调研 → 公司报告 ─┐
                                      └─────────────────────┘                      │
                                                    行业报告 ──────────────────────┤
                                                    每日金融数据 ──────────────────┤
                                                                                   ↓
                                                                          公司情景投资决策</pre>
<ul><li>五个背景专题和会议研究：均从外部公开资料独立研究，不读取或继承项目内旧报告、其他专题结论或中间材料。它们在研究依赖上可以并行，没有固定先后顺序。</li>
<li>行业调研：本地研究资料仅来自 <code>基本面/行业调研/产业背景/</code>及子目录，同时独立联网核验与拓展。</li>
<li>公司调研：本地研究资料来自 <code>基本面/行业调研/结果/</code>和<code>基本面/行业调研/产业背景/</code>及子目录，同时独立联网取证。产业背景可以直接传入公司研究。</li>
<li>公司情景投资决策：读取目标公司的正式公司报告、相关正式行业报告，以及<code>金融资料/每日金融数据/</code>中有日期的经营、财务、证券、价格和市场事实，并独立取证。当前方案没有授权直接读取产业背景目录。</li>
<li>上游报告提供事实线索、机制和待核验判断；下游须检验其适用条件，自行形成预测、概率、估值及投资选择。不能把同源转述重复计为独立证据。</li></ul>
<p>公司索引和行业索引属于<strong>任务管理输入</strong>：用于确认股票代号、主题、分类及正式输出路径；行业索引的研究范围提示会进入提示词以划清对象边界。索引、队列、分类元数据本身不是经营事实、投资结论或研究证据。正式提示的研究输入限制与 runner 为管理任务而读取索引是不同层次。</p>
<h2>4. Research Runner 的简单工作原理</h2>
<p>可以把 runner 理解为“读任务清单、选择方案、启动独立研究、验收文件并记录结果”的执行器。它使用 Codex SDK，每项研究建立独立线程，不通过第二个模型重新评价研究质量。</p>
<ol><li><strong>入队：</strong>按公司股票代号、行业主题或会议/专题生成任务，写入 <code>tools/queue.jsonl</code>。任务包含 domain、subject、状态、尝试次数、推理强度和方案版本等。</li>
<li><strong>绑定方案：</strong>方案目录根部唯一的时间戳文件是现行入口。入队绑定 planId、planVersion、planSnapshotFile、planSha256 等；执行读取绑定副本，并记录实际提示文件与哈希。因此更新现行方案不会静默把已绑定任务换成新版。README 和修改记录不拼入研究正文。</li>
<li><strong>路由与组装：</strong>domain 适配器决定对象校验、正式输出路径和备份规则；提示组装替换研究对象，附加输出要求。背景/会议任务由注册的 file-run 方案提供输出边界。</li>
<li><strong>独立运行：</strong>按并发上限领取任务，执行研究方案。模型负责取证和研究；runner 负责执行生命周期、配额、超时及队列状态。</li>
<li><strong>验收与归档：</strong>标准 domain 运行前锁定输出路径并备份同主题旧文件；成功须通过本地输出契约，例如本轮生成或修改的非空正式文件。成功标为 done 并归档到 <code>tools/queue.done.jsonl</code>；失败按规则重试或标为 failed。日志在 <code>tools/research-runner/logs/</code>。</li></ol>
<p>并发通过 <code>tools/queue.control.json</code>控制。代码默认并发为 10，但实际值可由控制文件或启动参数覆盖；这里不报告实时并发。额度不足时停止领取新任务并在在途任务收尾后退出，恢复额度后需要再次启动。文件验收通过只证明符合执行输出契约，不证明内容质量或投资结论正确。</p>
<h2>5. 当前代码实际执行的 domain 顺序</h2>
<pre style="background:#f3f5f7;padding:16px;white-space:pre-wrap">第 1 组：industry
第 2 组：company
第 3 组：feature-quantization、company-sentiment
第 4 组：company-investment-decision
第 5 组：company-comparison、file-run</pre>
<p>这是 <code>runner.mjs</code> 中的 PRIORITY_GROUPS。调度器选择仍有 pending、running 或 retry_pending 的最高优先级组；只有这一组可以领取新任务。同组按活动队列顺序领取，可在并发上限内同时执行。高组只有 running、没有可领取任务时，也不会越级领取低组。</p>
<p><strong>这是一套按 domain 分组的优先级屏障，不是逐任务的 dependency DAG。</strong>当前领取逻辑没有根据“公司 A 依赖行业 X、行业 X 依赖背景 Y”自动建图，也不会自动补齐上游任务或确认上游报告都是本批最新版本。failed 和 done 不在阻塞状态集合内；因此上游最终失败后，低组仍可能运行，不能把“低组已开始”解释为“上游全部成功”。</p>
<p>量化、情绪、公司对比是 runner 支持的其他 domain，不在本邮件九份方案范围内。尤其量化/情绪虽然调度早于投资决策，<strong>不代表它们是投资决策的研究资料依赖</strong>：当前投资决策方案明确不继承量化评分、技术面和情绪结论、比较排序及既有投资决策。</p>
<h2>6. 自动化运行这套研究的组织思路</h2>
<p>下列是基于现有 runner 的<strong>分阶段组织方式</strong>，不是宣称现有代码已实现自动 DAG，也不是本次新建了定时任务。外层自动化负责何时启动、选择本次对象、分阶段入队及检查阶段结果；runner 负责执行各阶段内任务。</p>
<ol><li><strong>准备：</strong>确定研究截止时间、对象范围和方案版本，读取公司/行业索引，检查正式路径；按需要准备有日期的每日金融数据。金融数据是投资决策的独立上游支线，不在这九份方案内。</li>
<li><strong>阶段 A——产业背景与会议：</strong>先只安排所需的五个背景专题及指定会议 file-run 任务。相互独立的研究可以并发。检查所需输出是否成功、是否满足本批截止与覆盖要求。</li>
<li><strong>阶段 B——行业：</strong>阶段 A 满足本批要求后，按行业索引生成 industry 任务；全量覆盖时为 91 个主题，也可按范围只更新相关行业。不同主题可以并发。</li>
<li><strong>阶段 C——公司：</strong>相关上游资料就绪后，按公司索引生成 company 任务；全量覆盖时为 221 家公司。根据公司的业务关联选择相关行业材料，不按分类目录做机械一一映射。</li>
<li><strong>阶段 D——公司情景投资决策：</strong>检查目标公司报告、相关行业报告和金融数据的可用性、日期与缺口后，再生成 company-investment-decision 任务。全量覆盖时为 221 家公司；也可以只研究选定公司。</li>
<li><strong>阶段收尾：</strong>汇总 done、failed、重试与输出路径，记录方案版本、信息截止和缺口；失败或资料不足的处理遵循本次任务与方案要求，不能仅凭进程退出码或队列清空宣布整条研究成功。</li></ol>
<p><strong>为什么要分阶段入队：</strong>背景和会议在知识上是上游，但执行 domain 是最低优先级组的 file-run。如果把它们与 industry、company、投资决策一起入队，代码会先跑行业和公司，最后才跑背景，无法保证本批上游先更新。应在阶段 A 完成检查后再释放后续阶段；仅改变队列行顺序不能覆盖跨组优先级。若活动队列已有其他高组任务，需先安排好本批与现有任务的边界。</p>
<p>每层也可独立更新，并非每次公司研究都要重做全部产业背景和 91 个行业。需要的是可解释的资料日期、覆盖与取证边界，而不是把所有上游历史任务重跑一遍。时间触发可以来自定时器，事件触发可以来自新财报、会议结束或方案更新；触发器不应替代研究方案本身。</p>
<p>常用执行入口（下列为说明，本次未执行入队或启动研究）：<code>npm run queue:validate</code>、<code>npm run queue:status</code>、<code>npm start</code>。行业可使用 <code>queue:seed-industry-from-index</code>；公司和投资决策可按索引逐项调用对应 add 命令；背景/会议使用 <code>queue:add-file-run</code> 并指定注册方案目录及会议名称/年份。</p>
<h2>7. 附件与原始路径</h2>
<p>邮件附上 <strong>9 份现行研究方案 + 公司索引 + 行业索引，共 11 个 Markdown 文件</strong>。为避免同名附件混淆，附件文件名增加序号和专题名；文件内容按原始字节复制，编码、换行及正文均未改写，逐份 SHA-256 已与源文件核对一致。以下路径均为发送时来源位置。</p>
<table border="1" cellpadding="7" cellspacing="0" style="border-collapse:collapse;width:100%;word-break:break-all"><tr><th>附件文件名</th><th>方案/索引标识</th><th>原始完整路径</th></tr>${tableRows}</table>
<h2>8. 本介绍核对依据</h2>
<p>研究内容与资料边界：随附九份方案及两份索引；横向专题的成果位置与独立性：<code>基本面/行业调研/横向专题/README.md</code>；执行机制：<code>tools/research-runner/README.md</code>、<code>research-plans.json</code>、<code>runner.mjs</code>、<code>queue-store.mjs</code>、<code>domains/</code>、<code>prompts/</code>、<code>docs/DOMAINS.md</code>及<code>docs/OPERATIONS.md</code>。这些路径相对 D:\\investment。</p>
</body></html>`;
fs.writeFileSync(path.join(out,'项目介绍.html'),html,'utf8');
fs.writeFileSync(path.join(out,'附件校验清单.json'),JSON.stringify(entries,null,2),'utf8');
console.log(JSON.stringify({out,attachmentCount:entries.length,totalBytes:entries.reduce((s,e)=>s+e.bytes,0),companies:c.length,industries:i.length,verified:true}));
