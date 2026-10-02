from pathlib import Path
import json, hashlib, datetime

ROOT=Path('D:/drive/Investment')
OUT=Path(__file__).resolve().parent
e=json.loads((OUT/'排序证据.json').read_text(encoding='utf-8'))
s=json.loads((OUT/'修改前快照.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=[r['path'] for r in s['protected'] if sha(ROOT/r['path'])!=r['sha256']]
prefix='基本面/行业调研/研究方法/会议/'
archive=[r['path'] for r in s['withdrawn'] if sha(OUT/'撤回的会议入口'/r['path'].removeprefix(prefix))!=r['sha256']]
canonical=ROOT/'基本面/行业调研/研究方法/会议调研方案.md'
assert not protected and not archive
assert not (ROOT/prefix).exists()
assert canonical.read_bytes()==(OUT/'会议方案正文.txt').read_bytes()
assert all(sha(OUT/'原文件'/r['path'])==r['sha256'] for r in s['editable'])
plans={r['method_id']:r for r in e['ranking_views']}
assert len(plans)==15
assert all(not (ROOT/r['expected_output_file']).exists() for r in plans.values())
check={'checked_on':'2026-09-08','protected_files_unchanged':len(s['protected']),'archived_files_hash_matched':len(s['withdrawn']),'original_backups_hash_matched':len(s['editable']),'withdrawn_formal_directory_absent':True,'canonical_matches_reviewed_body':True,'current_plans':len(plans),'new_results_exist':False,'performance_mean_checks':34,'price_data_cutoff':'2026-09-04','mismatches':protected+archive}
(OUT/'交付核验.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
ideas={
'01':('比较风险调整赔率：上行、估值、下行和资金承受能力。','A+B主轴，C/D/E补决定性证据'),
'02':('识别市场预期与具体兑现条件；准备度不能解释成成功概率。','A+B，C/D/E核验订单、采用、兑现时间'),
'03':('压力防守；检查现金、融资、订单及估值反证。','A+B，C/E核验坏路径'),
'04':('五维简单基准，权重30/25/20/15/10，用来检验复杂方法的增量。','A+B；必要时C/D/E补证'),
'05':('反证优先，判断风险是否闭环，而非因叙事完整而加分。','A+B，C/E优先寻找反证'),
'06':('同源事实分F价值、G成长、E事件三种取舍；属于一个方法家族。','A+B共同事实底稿，C/D/E补各视图关键事实'),
'07':('独立估算12—24个月收入台阶，弱环节约束成长，并解释3/6个月重估理由。','C+D+B独立建模，A只作参考，E验证客户与交付'),
'08':('判断证据能支持到哪一步、缺失如何改变Top30；不是收益评分。','A+B及C/D/E原始证据与缺失、冲突记录'),
'09':('弹性成长、触发条件和下行；价格确认占22%。','A+B+C/D/E，另需5/10/20交易日可比收益'),
'N01':('基准兑现与估值承载，六维比较，强调基础情景是否撑得住现价。','A+B主轴，C/D/E核基准路径'),
'N02':('反证闭环、尾部生存与永久损失；应提供风险审查，不作收益赞成票。','A+B，C/E现金、债务、融资与合同证据'),
'N03':('识别真实预期差增量与证据升级，不把报告变长当新信息。','A+B+C/D/E；必须有可比T-1与T0原始事实'),
'N04':('收入台阶如何转成现金与每股价值；现金转化权重20%。','A+B+C/D/E，收入桥、回款、资本开支及稀释'),
'N05':('先按固定阈值判市场状态，再按状态调整评价权重。','A+B+C/D/E；公司池20日价格、5日中位数、上涨占比、IV分位及两期盈利增量'),
'N06':('发现早期非线性成长与多倍价值，兼顾24—60个月以上路径和3/6个月参与理由。','A+B+C/D/E，长期采用、供给、资本需求与每股价值')}
def link(label,p):return f'[{label}](<{p}>)'
def pct(v):return f'{float(v)*100:+.2f}%'
lines=['# 会议入口收拢与15份排序方案复核','', '完成核验：2026-09-08。会议修订及本目录在9月7日开始；历史回测仍冻结至9月4日，不把工作日期变化当行情已更新。','',
'## 会议已实施内容','',
'唯一会议研究方案为'+link('会议调研方案.md',canonical.as_posix())+'。正文按“对象与资料边界→新变化→技术与采用核验→商业传导→反证与下游判断→交付”六段统一重写，不附项目或对话迭代史。','',
'对工程工具、硬件架构、机器人、长周期合同按证据类型选择核验重点，保持统一流程；允许原创发现、合理未知和零投资机会。严格区分演示、独立验证、采用、订单、收入与现金，也区分长期价值和3/6个月可验证变化。报告明确哪些信息可以给下游用、哪些推断还缺桥梁。','',
'新增会议子目录的注册表、说明和五份通用/分会议方案，共7个文件已整体撤回到'+link('撤回的会议入口',(OUT/'撤回的会议入口').as_posix())+'，逐文件校验未改变。同步修改研究入口导航和行业AGENTS。会议名称与年份通过明确任务信息或file-run输出文件名传入；不另建会议包装入口。','',
'15份排序方案、注册状态及专项本轮未修改。只完成会议入口调整，以下合并与淘汰属于讨论。','',
'## 回测口径与有效性边界','',
'当前15份均为9月7日修订、未运行版本。表中成绩绑定各自旧版原始结果：7月13日复权收盘至9月4日最近可得复权收盘；另以7月14日复权开盘重算。共39个日收益区间，不能代表完整3个月或3—6个月有效性。MICLF末价为9月3日。等权Top30不含费用、税与交易冲击，也不是实际成交组合。','',
'15份方案对应17个榜单视图，因为06有F/G/E三榜。Rank IC为全公司名次与该窗口收益的排序关系；命中为Top30中有几家进入192家公司事后涨幅前30，随机等规模基线约4.69家，不能直接解释为显著性。','',
'|基准|收盘起点|次日开盘起点|','|---|---:|---:|']
for name,b in {**e['benchmarks'],'192家公司等权池':e['pool']}.items():lines.append(f'|{name}|{pct(b["close"])}|{pct(b["open"])}|')
lines += ['', '17榜在收盘口径均未跑赢SPY。N02在次日开盘口径只高于SPY约0.09个百分点，不能据此宣称稳健超额。大量方法虽然跑输宽基，却跑赢半导体或公司池；因此必须区分绝对表现、行业暴露及真正选股增量。','',
'## 当前15份文件与旧版成绩','', '|方案及当前文件|当前版本|旧结果版本|Top30收盘/次日开盘|Rank IC|命中涨幅前30|','|---|---|---|---:|---:|---:|']
for mid,r in plans.items():
 views=[v for v in e['ranking_views'] if v['method_id']==mid]
 returns='；'.join((v['list_id']+': ' if len(views)>1 else '')+pct(v['top30_return'])+'/'+pct(v['top30_next_open_return']) for v in views)
 ic=' / '.join(f'{float(v["rank_ic"]):+.3f}' for v in views)
 hits=' / '.join(v['top30_actual_winner30'] for v in views)
 lines.append(f'|{link(mid+" "+r["method_name"],(ROOT/r["prompt_file"]).as_posix())}|{r["version_id"].split("_")[0]}|{link(r["old_version"],r["old_result"])}|{returns}|{ic}|{hits}|')
lines += ['', '**N03不能把机械Top30当成30家合格推荐。** 旧报告只确认8家合格：MU、PENG、TSLA、TT、ASX、APLD、BWXT、BDC；其等权回报为'+pct(e['N03_qualified8']['close'])+'/'+pct(e['N03_qualified8']['open'])+'。机械排名其他位置包含不合格者；该榜的Top30指标仅用于统一诊断。','',
'01、02、04和N02在这一窗口相对公司池较好；05最弱。03/05近零IC、06G/E负IC提示排序目标与收益次序存在问题，但单窗口不能证明长期失效。N05全榜IC较好而头部收益不强，说明全榜排序质量不能替代Top30目标。N03/N06职责的长周期属性，也不自动构成短期落后的免责理由。','',
'## 输入文件与研究思路','',
'以下是当前方案允许读取的输入范围与优先重点。新版本尚未运行，没有实际消费文件清单；不能把目录权限冒充已经读取某份报告。实际运行必须保留当时使用的文件、版本与日期。','',
'- A：'+link('公司情景投资决策/结果',(ROOT/'分析报告/公司情景投资决策/结果').as_posix())+'；当前4种情景×3种期限作为事实/假设模型，不作独立投票或已校准概率。',
'- B：'+link('每日金融数据',(ROOT/'金融资料/每日金融数据').as_posix())+'；不晚于截止时点的完整主快照，同日补充仅校准，并核复权行情；必要时取金融资料中的带日期财务原始事实。',
'- C：'+link('公司调研',(ROOT/'基本面/公司调研').as_posix())+'；经营机制、产品、客户与财务传导。',
'- D：'+link('行业调研',(ROOT/'基本面/行业调研').as_posix())+'；相关产业、背景和会议成果，研究方案文本本身不是事实来源。',
'- E：外部一手资料，例如公司、客户、供应商、监管、证券条款和标准；使用最早公开日期控制时点。','',
'15份已统一输入权限，差异在判断职责，不应靠隔绝决定性证据制造多角度。其他排序、回测结果、特征评分、技术面/情绪面结论不作主事实；明确提供的同截止同行结果只可在自身判断冻结后用于比较，不能回灌证明自身结论。','',
'|方案|研究思路|输入重点|','|---|---|---|']
for mid,(idea,inputs) in ideas.items():lines.append(f'|{mid}|{idea}|{inputs}|')
lines += ['', '## 对“重复”的数值核验','', '同名近义不等于相同输出。以下相关系数是旧全公司名次数列间相关，不是收益Rank IC；重合为两个旧Top30的交集。','', '|方案对|Top30重合|名次相关|','|---|---:|---:|']
for p in e['pairs']:lines.append(f'|{p["a"]} / {p["b"]}|{p["top30_overlap"]}/30|{p["rank_correlation"]:+.3f}|')
lines += ['',(OUT/'取舍讨论.txt').read_text(encoding='utf-8'), '## 证据与交付核验','',
'- '+link('原始Top30指标',(ROOT/'备份/流程审计与研究方案改进_2026-09-05/data/sorting_top30_metrics.csv').as_posix()),
'- '+link('公司收益及原始名次',(ROOT/'备份/项目反思_2026-09-04/data/company_returns.csv').as_posix()),
'- '+link('逐日行情',(ROOT/'备份/项目反思_2026-09-04/data/daily_prices.csv').as_posix()),
'- '+link('本次逐榜重算与重合证据',(OUT/'排序证据.json').as_posix())+'；17榜×2口径共34个均值重算一致。',
'- '+link('文件交付核验',(OUT/'交付核验.json').as_posix())+'；受保护文件及撤回历史文件逐一核SHA-256。',
'- '+link('file-run单入口静态构建核验',(OUT/'会议入口构建核验.json').as_posix())+'；只创建内存任务并构建提示，没有入队或运行研究。','']
(OUT/'00_会议收拢与15排序方案清单和取舍.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(check,ensure_ascii=False))
