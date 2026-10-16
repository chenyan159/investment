import json, re
from pathlib import Path
ROOT = Path(r"D:\investment\实验室\2026-10-12_3至6个月超高收益20家公司实验").resolve()
data = json.loads((ROOT/"04_verification/V1_evidence.json").read_text(encoding="utf-8"))
universe = {x["ticker"]:x for x in json.loads((ROOT/"01_inputs/universe.json").read_text(encoding="utf-8-sig"))}
for c in data["companies"]:
    u=universe[c["ticker"]]
    c["company_name"]=u["name"]
    c["frozen_company_paths"]=u["sources"].get("company",[])
    c["frozen_scenario_paths"]=u["sources"].get("scenario",[])
    c["frozen_comparison_paths"]=u["sources"].get("comparison",[])
    c["local_read_scope"]="公司报告身份、时间、催化与相关财务段；不是全文。情景/对比的结论主要继承前轮，未重新逐行读取。"
    c["source_dates_in_local_filenames"]=[p[-13:-3] for p in c["frozen_company_paths"] if re.search(r"\d{4}-\d{2}-\d{2}\.md$",p)]
    f=u.get("finance",{})
    c["snapshot_identity"]={k:f.get(k) for k in ["最新价格","价格日期","currency","financial_currency","listing_type","adr_ratio","shares_outstanding"]}
    c["security_verification_limit"]="snapshot_identity为冻结输入，不保证最终完整经济股数；security_notes记录V1原文识别的边界，最终数值以V2权益桥为准。"
    assert c["source_urls"]
    assert all((ROOT/p).exists() for p in c["frozen_company_paths"])
assert len(data["companies"])==38 and len({c["ticker"] for c in data["companies"]})==38
(ROOT/"04_verification/V1_evidence.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["# V1 独立事实、事件与证券边界核验",
"",
"截止：2026-10-12 20:50 America/Los_Angeles。三/六个月终点：2027-01-12、2027-04-12。",
"",
"覆盖34家核心及APLD、NBIS、TTMI、AEIS，共38家。每家公司至少重新打开一个决定性原始公告/SEC文件相关段。此稿认证披露与事件边界，不认证前轮目标价或翻倍概率。多数未来财报月份是估计，不是官方日程。所有金额按卡片原币种，B=十亿、M=百万。",
"",
"## 裁决必须带入的修正",
"",
"- AMPX：CAMINUS 10/5协议计划2027Q1逐步量产，不能只用2028年赠款工厂否定近端路径；仍未闭合订单、认证和毛利。",
"- KYTX：Q4 BLA/PMS数据是计划；gMG mid2027是入组而非读出。BNTX肿瘤读出是事件累积驱动，不能视为日期确定或结果必阳。",
"- LEU：新规模产能2029；合同、租约、承购和融资可先重估。ENPH：11月演示、2027试点，不能认作半年批量收入。",
"- VISN：160M退税在2027H2，超出本实验六个月窗口。MOD：10/1拆分完成，THRM份额归原股东，10/12新买MOD不能再领取。",
"- ACMR：2.5B USD等值订单含待验收出货，尚非收入；上海73.2%所有权、A+B、NCI口径必须处理。",
"- AMBA：客户终止带来9M研发费冲回，Q2经营亏损正常化后约17.1M而非8.1M。AOSL仍亏，MRAM调整盈利剔除重要成本。",
"- MU：客户保证金进入融资现金流，不能伪装FCF。NVDA：FY27 nonGAAP已含SBC，不能重复扣；证券收益仍须与经营分开。",
"- SMCI：强制可转优先股2029强转而不是今天自动转；债和转股不可双扣。CRWV：RPO多年确认，不能和backlog重复相加。",
"- PLAB、APLD、NBIS及RDW：分别处理JV现金/NCI、可赎回NCI与优先股、A+B及技术C股、已清零优先股和库存股；数字最终交V2。",
"",
"## 逐公司证据卡",
""]
for n,c in enumerate(data["companies"],1):
    lines += [f"### {n}. {c['ticker']} — {c['company_name']}",
              "",
              f"**独立原文及首次公开口径：** {c['published']}。本日期指所用公告/文件，不声称穷尽更早所有披露。",
              f"**3个月：** {c['event_3m']}",
              f"**6个月：** {c['event_6m']}",
              f"**核到的决定性事实：** {c['independent_finding']}",
              f"**价值传导：** {c['value_mechanism']}",
              f"**反证/未闭合：** {c['counterevidence_unclosed']}",
              f"**对本地或旧论证的修正：** {c['local_correction']}",
              f"**证券和币种：** {c['security_notes']}",
              "**来源：** "+ "；".join(f"[独立打开原文{i+1}]({u})" for i,u in enumerate(c["source_urls"])),
              "**本地冻结公司报告：** "+"；".join(f"[{Path(p).name}]({(ROOT/p).as_posix()})" for p in c["frozen_company_paths"]),
              ""]
lines += ["## 阅读与残余限制",
"",
"公司公告证明公司说过、披露过或计划做某事，不证明未来会发生。所有估计财报月份、未知验收日和未披露订单额度均不作硬催化。股价继承控制器已独立核验的10/12正常收盘，本角色未重复采集报价。",
"",
"外部券商观点和多空论据主要继承S1/S2及控制器；V1未重读券商原研全文，不重复计数。VISN电话会为第三方逐字稿承载公司原话，不是第三方独立支持。细分监管、现金受限和全部潜在稀释由V2继续量化，卡片明确保留的缺口不因封卷自动关闭。",
"",
"本地公司报告读取身份、事件和相关财务段，不宣称38份全文或全部情景/对比全文重读。原始IR读取失败后使用SEC同公告，失败链接不作事实支持。结构化证据见V1_evidence.json；打开日志与访问边界见07_logs/V1_sources.json、V1_reading_notes.md。"]
(ROOT/"04_verification/V1_evidence.md").write_text("\n\n".join(lines)+"\n",encoding="utf-8")
notes=["# V1 阅读记录",
"",
"任务：独立事实、近端事件及证券边界核验。所有写入仅在本实验ROOT；未spawn、未git、未安装依赖。",
"",
"已读根AGENTS.md、实验章程、核验阶段交接规则。读取universe冻结公司路径及S1/S2来源索引，读取S1报告与控制器AMPX/AAOI、生物医药、ICHR/PENG/AEHR、AOSL/MRAM、ENPH/VISN/POET核验。",
"",
"逐公司原文阅读不是全文逐行：先打开公告或10-Q/10-K，随后对事件、客户验收、股本、NCI、可转债、现金流和一次性项目作定点find/open。日志保留工具引用ID用于审计；正式引用使用真实URL。",
"",
"独立来源覆盖38/38；同一URL重复打开不算多项独立证据。为每家公司附本地冻结报告定位，抽读标题日期、身份和决定性财务/事件段。情景和对比报告结论主要继承前轮。",
"",
"访问边界：IONS IR页面/PDF有403，已以SEC附件重开；AVAV IR node失败，已以SEC公告重开。付费券商研究未读全文，不将摘要/继承列为V1独立外部意见。对无明确未来日期的事项使用计划/估计，不补造日期。",
"",
"精确度限制：UCTT/PSIX末次复开分别确认8/3和8/6披露；本次publication字段是所用文件首次公开日期，不宣称行业事件历史上的绝对最早披露。10/12仅日期无时间的资料不构成本卡唯一决定性来源。",
"",
"重点复开结果：SNDK9/29日历确认10/29 13:30PT；AAOI10/5 ATM净额和新股均入考虑；VISN电话会原话两次为2027H2退税；ACMR10-Q确认73.2%上海持股；RDW6/30优先股清零但现金含受限；SMCI股本/可转证券条款按最终10-K；MRAM合同签日4/24、公开4/29、按里程碑30个月。",
"",
"结论：已完成本角色的独立关键事实核验，未把目标价或未来盈利认证为事实。所有残余边界留在证据卡，裁决不能删去这些条件。",
"",
"## 本地阅读定位",
""]
for c in data["companies"]:
    notes += [f"- {c['ticker']}: "+ "; ".join(c["frozen_company_paths"])+"；原文: "+ "; ".join(c["source_urls"])]
(ROOT/"07_logs/V1_reading_notes.md").write_text("\n".join(notes)+"\n",encoding="utf-8")
print(json.dumps({"companies":len(data["companies"]),"all_in_universe":True,"local_paths_exist":True,"outputs":["04_verification/V1_evidence.json","04_verification/V1_evidence.md","07_logs/V1_sources.json","07_logs/V1_reading_notes.md"]},ensure_ascii=False))


