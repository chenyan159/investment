import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import DOMPurify from "dompurify";
import { marked } from "marked";
import {
  Activity,
  AlertTriangle,
  ArrowDownUp,
  BarChart3,
  Building2,
  Download,
  FileText,
  Gauge,
  Grid3X3,
  Home,
  Layers,
  LineChart,
  Newspaper,
  Search,
  ShieldCheck,
  SlidersHorizontal,
  Table2,
  Volume2,
  X,
} from "lucide-react";
import "./styles.css";

const DATA_BASE = "./data";
const DAILY_NEWS_LISTENED_STORAGE_KEY = "project-ananta:daily-news-listened:v1";

const featureGroupLabels = {
  alpha: "收益型特征",
  gates: "门槛层",
};

const featureGroupDescriptions = {
  alpha: "用于形成未来收益排序判断；有效性在需要时另行直接评估。",
  gates: "用于证据、可投资性和风险约束，不作为独立收益信号。",
};

const navItems = [
  { id: "overview", label: "首页", icon: Home },
  { id: "companies", label: "公司", icon: Building2 },
  { id: "industries", label: "行业", icon: Layers },
  { id: "rankings", label: "排名", icon: BarChart3 },
  { id: "companyComparisons", label: "公司对比", icon: ArrowDownUp },
  { id: "scenarioDecisions", label: "情景决策", icon: Grid3X3 },
  { id: "features", label: "特征量化", icon: Gauge },
  { id: "technicalResearch", label: "技术面", icon: Activity },
  { id: "dailyNews", label: "AI 新闻", icon: Newspaper },
  { id: "quality", label: "质量告警", icon: ShieldCheck },
];

const homepageFocusCompanies = [
  { rank: 1, ticker: "ADBE", why: "低预期 × 高现金流，AI 颠覆担忧可能定价过度", watch: "AI 使用能否变成付费 ARR" },
  { rank: 2, ticker: "META", why: "广告 AI 已经兑现，现金引擎仍在加速", watch: "AI 再投资能否抬升 FCF 与 ROIC" },
  { rank: 3, ticker: "QCOM", why: "授权现金流托底，汽车与定制芯片提供右尾", watch: "数据中心赢单到收入的转化" },
  { rank: 4, ticker: "ORCL", why: "RPO 与 OCI 加速，增长错位最明显之一", watch: "高 CapEx 后的每股自由现金流" },
  { rank: 5, ticker: "ET", why: "合同现金流、分派与低隐含门槛形成防守赔率", watch: "成长投入后的可分配现金" },
  { rank: 6, ticker: "MSFT", why: "企业分发与云软件复利闭环最完整", watch: "AI CapEx 利用率与增量回报" },
  { rank: 7, ticker: "NVDA", why: "平台、产品代际与现金流同时成立", watch: "整柜交付、电力就绪与客户验收" },
  { rank: 8, ticker: "TEL", why: "连接器认证壁垒叠加 AI、电网与汽车分散度", watch: "订单向收入与毛利的转化" },
  { rank: 9, ticker: "CEG", why: "AI 负荷与清洁电力的实物映射最直接", watch: "合同能否变成送电负荷与现金" },
  { rank: 10, ticker: "TSM", why: "先进节点与先进封装的双重收费站", watch: "7 月 16 日业绩后需优先更新" },
  { rank: 11, ticker: "HPE", why: "AI 服务器、网络整合与估值缓冲并存", watch: "GPU 转售收入能否留下利润和现金" },
  { rank: 12, ticker: "NTNX", why: "订阅现金流带来较好的上下行结构", watch: "TCV/RPO 向续约与收入的转化" },
  { rank: 13, ticker: "BABA", why: "净现金、云 AI 与制度折价构成重估空间", watch: "高投入后云业务能否形成 FCF" },
  { rank: 14, ticker: "VST", why: "稀缺发电资产与数据中心合同，但价格偏满", watch: "并购、起供、杠杆与 FCF 同步兑现" },
  { rank: 15, ticker: "NTAP", why: "成熟 FCF 底盘叠加低资本密度 AI 可选性", watch: "AI wins 能否变成有金额的订单" },
  { rank: 16, ticker: "AVGO", why: "XPU、AI 网络与软件形成多层利润池", watch: "业务强度与当前买入赔率的裂口" },
  { rank: 17, ticker: "MU", why: "HBM 已进利润表，经营弹性最陡之一", watch: "周期高点、CapEx 与追高风险" },
  { rank: 18, ticker: "HTHIY", why: "能源积压、工业服务与净现金构成多引擎", watch: "积压经过验收后能否转成核心 FCF" },
  { rank: 19, ticker: "ETN", why: "配电是 AI 扩张的第二层硬瓶颈", watch: "订单穿过交付、验收与营运资本" },
  { rank: 20, ticker: "IBM", why: "软件与主机现金底盘仍稳，成交时点错位", watch: "延迟交易能否在下半年确认" },
];

const homepageFocusGroups = [
  { title: "质量最强，价格更敏感", note: "业务确定性高；当前回报更依赖估值、利用率或执行。", from: 6, to: 10 },
  { title: "经营与估值形成不对称", note: "证据正在累积，市场尚未给出完全一致的定价。", from: 11, to: 15 },
  { title: "周期与高信息量观察", note: "产业位置突出，但价格、周期或现金传导仍需验证。", from: 16, to: 20 },
];

function formatValue(value, fallback = "-") {
  if (value === null || value === undefined || value === "") return fallback;
  return String(value);
}

function loadListenedDailyNewsDates() {
  try {
    const stored = JSON.parse(window.localStorage.getItem(DAILY_NEWS_LISTENED_STORAGE_KEY) || "[]");
    return new Set(Array.isArray(stored) ? stored.filter((date) => typeof date === "string") : []);
  } catch {
    return new Set();
  }
}

function saveListenedDailyNewsDates(dates) {
  try {
    window.localStorage.setItem(DAILY_NEWS_LISTENED_STORAGE_KEY, JSON.stringify([...dates]));
  } catch {
    // Listening history is optional when browser storage is unavailable.
  }
}

function toNumber(value) {
  if (value === null || value === undefined) return null;
  const cleaned = String(value).replace(/[+$,%]/g, "").replace(/,/g, "").trim();
  if (!cleaned || cleaned === "-" || cleaned.toLowerCase() === "nan") return null;
  const n = Number(cleaned);
  return Number.isFinite(n) ? n : null;
}

function sortRows(rows, sortKey, direction) {
  if (!sortKey) return rows;
  return [...rows].sort((a, b) => {
    const av = a[sortKey];
    const bv = b[sortKey];
    const an = toNumber(av);
    const bn = toNumber(bv);
    let cmp;
    if (an !== null && bn !== null) {
      cmp = an - bn;
    } else if (an === null && bn !== null) {
      return 1;
    } else if (an !== null && bn === null) {
      return -1;
    } else {
      cmp = formatValue(av, "").localeCompare(formatValue(bv, ""), "zh-Hans-CN");
    }
    return direction === "asc" ? cmp : -cmp;
  });
}

function rankingEntries(data) {
  const runs = data.rankings?.runs || {};
  const order = data.rankings?.order || Object.keys(runs);
  return order.map((key) => ({ key, run: runs[key] })).filter((item) => item.run);
}

function rankingEffectiveness(data, methodId) {
  return (data.rankings?.effectiveness?.methods || []).find((row) => row.methodId === methodId) || null;
}

function defaultRankingKey(data) {
  const entries = rankingEntries(data);
  return data.rankings?.defaultRunKey && data.rankings.runs[data.rankings.defaultRunKey]
    ? data.rankings.defaultRunKey
    : entries[0]?.key || "";
}

function preferredCompanyRankingKey(data) {
  return defaultRankingKey(data);
}

function rankingRowForTicker(run, ticker) {
  return (run?.rows || []).find((row) => row.ticker === ticker) || null;
}

function rankBucket(rank, rowCount) {
  const r = toNumber(rank);
  const c = toNumber(rowCount);
  if (r === null || c === null || c <= 0) return "-";
  return `Top ${Math.max(1, Math.ceil((r / c) * 100))}%`;
}

function rankingValidationText(run) {
  const ic3 = run?.metrics?.rankIc3m;
  const neutral3 = run?.metrics?.categoryNeutralRankIc3m;
  const ic6 = run?.metrics?.rankIc6m;
  return [
    ic3 !== null && ic3 !== undefined ? `3M ρ ${formatSigned(ic3, 3)}` : "",
    neutral3 !== null && neutral3 !== undefined ? `3M中性ρ ${formatSigned(neutral3, 3)}` : "",
    ic6 !== null && ic6 !== undefined ? `6M ρ ${formatSigned(ic6, 3)}` : "",
  ]
    .filter(Boolean)
    .join(" / ") || "-";
}

function companyRankingRows(data, ticker, activeRankingKey) {
  return rankingEntries(data).map(({ key, run }) => {
    const row = rankingRowForTicker(run, ticker);
    const rowCount = run.rowCount || run.rows?.length || "";
    return {
      key,
      label: run.label,
      strategy: run.strategy || "公司排序",
      rank: row?.rank || "",
      rankText: row?.rank ? `#${row.rank}/${rowCount}` : "未覆盖",
      bucket: row?.rank ? rankBucket(row.rank, rowCount) : "-",
      tier: row?.tier || "-",
      score: row?.score || "-",
      expectedReturn: row?.expectedReturn || "-",
      useCase: run.useCase || "查看该排序的适用场景和约束。",
      caution: run.caution || "",
      validation: rankingValidationText(run),
      isActive: key === activeRankingKey,
    };
  });
}

function csvEscape(value) {
  const s = formatValue(value, "");
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function downloadCsv(filename, rows, columns) {
  const content = [
    columns.map((c) => csvEscape(c.label)).join(","),
    ...rows.map((row) => columns.map((c) => csvEscape(row[c.key])).join(",")),
  ].join("\n");
  const blob = new Blob(["\ufeff", content], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function useData() {
  const [state, setState] = useState({ loading: true, error: null });

  useEffect(() => {
    async function load() {
      try {
        const [meta, companies, industries, rankings, companyComparisons, scenarioDecisions, technicalResearch, features, quality, dailyNews] = await Promise.all(
          ["meta", "companies", "industries", "rankings", "company-comparisons", "scenario-decisions", "technical-research", "features", "quality", "daily-news"].map((name) =>
            fetch(`${DATA_BASE}/${name}.json`, ["company-comparisons", "scenario-decisions"].includes(name) ? { cache: "no-store" } : undefined).then((r) => {
              if (!r.ok) throw new Error(`${name}.json ${r.status}`);
              return r.json();
            }),
          ),
        );
        setState({ loading: false, error: null, meta, companies, industries, rankings, companyComparisons, scenarioDecisions, technicalResearch, features, quality, dailyNews });
      } catch (error) {
        setState({ loading: false, error: error.message });
      }
    }
    load();
  }, []);

  return state;
}

function App() {
  const data = useData();
  const [view, setView] = useState("overview");
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedIndustry, setSelectedIndustry] = useState(null);
  const [selectedRankingKey, setSelectedRankingKey] = useState(null);
  const [selectedComparisonTicker, setSelectedComparisonTicker] = useState(null);
  const [selectedScenarioTicker, setSelectedScenarioTicker] = useState(null);
  const [selectedTechnicalFactor, setSelectedTechnicalFactor] = useState(null);

  useEffect(() => {
    const applyHash = () => {
      const hash = window.location.hash.replace(/^#\/?/, "");
      if (!hash) return;
      const [kind, id] = hash.split("/");
      if (kind === "company" && id) {
        setSelectedCompany(decodeURIComponent(id));
        setView("companies");
      } else if (kind === "industry" && id) {
        setSelectedIndustry(decodeURIComponent(id));
        setView("industries");
      } else if (kind === "companyComparison" && id) {
        setSelectedComparisonTicker(decodeURIComponent(id));
        setView("companyComparisons");
      } else if (kind === "scenarioDecision" && id) {
        setSelectedScenarioTicker(decodeURIComponent(id));
        setView("scenarioDecisions");
      } else if (kind === "technicalResearch" && id) {
        setSelectedTechnicalFactor(decodeURIComponent(id));
        setView("technicalResearch");
      } else if (navItems.some((item) => item.id === kind)) {
        setView(kind);
      }
    };
    applyHash();
    window.addEventListener("hashchange", applyHash);
    return () => window.removeEventListener("hashchange", applyHash);
  }, []);

  if (data.loading) return <LoadingScreen />;
  if (data.error) return <ErrorScreen error={data.error} />;

  const activeRankingKey =
    selectedRankingKey && data.rankings.runs[selectedRankingKey] ? selectedRankingKey : preferredCompanyRankingKey(data);
  const activeRankingRun = data.rankings.runs[activeRankingKey] || {};
  const ranking = activeRankingRun.rows || [];
  const rankingByTicker = Object.fromEntries(ranking.map((row) => [row.ticker, row]));

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <LineChart size={22} />
          <div>
            <strong>Project Ananta</strong>
            <span>Research → Attention</span>
          </div>
        </div>
        <nav className="nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={view === item.id ? "nav-item active" : "nav-item"}
                onClick={() => {
                  setView(item.id);
                  window.location.hash = item.id;
                }}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
        <div className="sidebar-meta">
          <span>数据生成</span>
          <strong>{data.meta.generatedAtDisplay}</strong>
        </div>
      </aside>

      <main className="main">
        {view === "overview" && <Overview data={data} setView={setView} />}
        {view === "companies" && (
          <Companies
            data={data}
            rankingKey={activeRankingKey}
            rankingRun={activeRankingRun}
            setRankingKey={setSelectedRankingKey}
            rankingByTicker={rankingByTicker}
            selectedTicker={selectedCompany}
            setSelectedTicker={setSelectedCompany}
          />
        )}
        {view === "industries" && (
          <Industries
            data={data}
            rankingByTicker={rankingByTicker}
            rankingRun={activeRankingRun}
            selectedSlug={selectedIndustry}
            setSelectedSlug={setSelectedIndustry}
          />
        )}
        {view === "rankings" && (
          <Rankings data={data} rankingKey={activeRankingKey} setRankingKey={setSelectedRankingKey} />
        )}
        {view === "companyComparisons" && (
          <CompanyComparisons data={data} selectedTicker={selectedComparisonTicker} setSelectedTicker={setSelectedComparisonTicker} />
        )}
        {view === "scenarioDecisions" && (
          <ScenarioDecisions data={data} selectedTicker={selectedScenarioTicker} setSelectedTicker={setSelectedScenarioTicker} />
        )}
        {view === "features" && <Features data={data} rankingByTicker={rankingByTicker} />}
        {view === "technicalResearch" && (
          <TechnicalResearch
            data={data}
            selectedFactorId={selectedTechnicalFactor}
            setSelectedFactorId={setSelectedTechnicalFactor}
          />
        )}
        {view === "dailyNews" && <DailyNews data={data} />}
        {view === "quality" && <Quality data={data} />}
      </main>
    </div>
  );
}

function LoadingScreen() {
  return (
    <div className="center-screen">
      <LineChart size={30} />
      <p>正在加载研究数据</p>
    </div>
  );
}

function ErrorScreen({ error }) {
  return (
    <div className="center-screen error">
      <AlertTriangle size={30} />
      <p>数据加载失败：{error}</p>
      <span>请先运行 npm run build:data</span>
    </div>
  );
}

function PageHeader({ eyebrow, title, actions }) {
  return (
    <header className="page-header">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
      </div>
      {actions ? <div className="header-actions">{actions}</div> : null}
    </header>
  );
}

function Overview({ data, setView }) {
  const scenarioByTicker = new Map((data.scenarioDecisions?.companies || []).map((item) => [item.ticker, item]));
  const comparisonByTicker = new Map((data.companyComparisons?.finalRanking || []).map((item) => [item.ticker, item]));
  const companyByTicker = new Map((data.companies || []).map((item) => [item.ticker, item]));
  const focusRows = homepageFocusCompanies.map((item) => ({
    ...item,
    company: companyByTicker.get(item.ticker),
    scenario: scenarioByTicker.get(item.ticker),
    comparison: comparisonByTicker.get(item.ticker),
  }));
  const currentMetrics = data.scenarioDecisions?.metrics?.current || {};
  const openCompany = (ticker) => {
    setView("companies");
    window.location.hash = `company/${encodeURIComponent(ticker)}`;
  };

  return (
    <div className="focus-home">
      <section className="focus-hero">
        <div className="focus-hero-copy">
          <span className="focus-kicker">PROJECT ANANTA · 投资注意力清单</span>
          <h1>现在，先看这 20 家公司</h1>
          <p>
            从 {data.meta.companyCount} 家公司、{formatValue(data.meta.companyComparisonRowCount)} 次定向比较和 {formatValue(data.meta.scenarioDecisionCellCount)} 个情景格子中交叉筛选。
            先看赔率与现金兑现，再看故事。
          </p>
          <div className="focus-actions">
            <button className="focus-action-primary" onClick={() => { setView("scenarioDecisions"); window.location.hash = "scenarioDecisions"; }}>
              看全部情景决策
            </button>
            <button className="focus-action-secondary" onClick={() => { setView("companyComparisons"); window.location.hash = "companyComparisons"; }}>
              看公司对比证据
            </button>
          </div>
        </div>
        <div className="focus-scoreboard" aria-label="研究覆盖摘要">
          <article className="focus-score-primary">
            <span>本期重点</span>
            <strong>20</strong>
            <small>不是买入指令，是研究优先级</small>
          </article>
          <article>
            <strong>{currentMetrics.positive || 0}</strong>
            <span>当前正面</span>
          </article>
          <article>
            <strong>{currentMetrics.adviceCounts?.strongYes || 0}</strong>
            <span>强烈建议</span>
          </article>
        </div>
      </section>

      <div className="focus-method-note">
        <ShieldCheck size={18} />
        <p><strong>这不是热度榜。</strong> 公司对比判断相对质量，情景矩阵判断当前赔率，排序只作为第三层结构证据。</p>
        <span>数据截至：对比 {data.meta.latestCompanyComparisonDate} · 情景 {data.meta.latestScenarioDecisionDate}</span>
      </div>

      <section className="focus-section">
        <div className="focus-section-heading">
          <div>
            <span>01 / CURRENT SETUPS</span>
            <h2>当前机会与跨模型证据最清楚</h2>
          </div>
          <p>优先验证现金传导；不是因为故事最热，而是当前价格仍有可讨论的余量。</p>
        </div>
        <div className="focus-lead-grid">
          {focusRows.slice(0, 5).map((item) => (
            <button key={item.ticker} className="focus-lead-card" onClick={() => openCompany(item.ticker)}>
              <div className="focus-card-topline">
                <span>#{String(item.rank).padStart(2, "0")}</span>
                <AdviceBadge adviceKey={item.scenario?.current?.adviceKey} />
              </div>
              <div className="focus-company-name">
                <strong>{item.ticker}</strong>
                <span>{item.company?.name || item.scenario?.name || item.ticker}</span>
              </div>
              <p>{item.why}</p>
              <div className="focus-watch">
                <span>关键观察</span>
                <strong>{item.watch}</strong>
              </div>
              <footer>
                <span>{item.comparison?.rank ? `公司对比 #${item.comparison.rank}` : "跨模型精选"}</span>
                <strong>{item.scenario?.current?.returnRangeText || "查看情景"}</strong>
              </footer>
            </button>
          ))}
        </div>
      </section>

      <section className="focus-section focus-secondary-section">
        <div className="focus-section-heading">
          <div>
            <span>02 / NEXT FIFTEEN</span>
            <h2>另外 15 家，按投资问题分组</h2>
          </div>
          <p>“值得关注”不等于“当前便宜”；中性公司保留在清单里，是因为下一条证据的信息价值很高。</p>
        </div>
        <div className="focus-group-grid">
          {homepageFocusGroups.map((group) => {
            const rows = focusRows.filter((item) => item.rank >= group.from && item.rank <= group.to);
            return (
              <article key={group.title} className="focus-group-card">
                <header>
                  <h3>{group.title}</h3>
                  <p>{group.note}</p>
                </header>
                <div className="focus-company-list">
                  {rows.map((item) => (
                    <button key={item.ticker} className="focus-company-row" onClick={() => openCompany(item.ticker)}>
                      <span className="focus-row-rank">{item.rank}</span>
                      <span className="focus-row-body">
                        <span className="focus-row-title"><strong>{item.ticker}</strong><small>{item.company?.name || item.scenario?.name || item.ticker}</small></span>
                        <span className="focus-row-why">{item.why}</span>
                      </span>
                      <span className={`focus-row-advice tone-text-${item.scenario?.current?.adviceKey || "unavailable"}`}>
                        {shortAdvice(item.scenario?.current?.adviceKey)}
                      </span>
                    </button>
                  ))}
                </div>
              </article>
            );
          })}
        </div>
      </section>

      <section className="focus-footer-note">
        <div>
          <strong>怎么使用这张首页</strong>
          <p>先点开公司查看完整研究，再用情景矩阵检查“好公司”是否仍是“好价格”。排序当前尚无本版本生成后样本，不做等权投票。</p>
        </div>
        <div>
          <strong>本期更新提醒</strong>
          <p>TSM 的 7 月 16 日 Q2 已跨过报告窗口；涉及 TSM、ASML、ABB 及其上下游的结论应优先刷新。</p>
        </div>
      </section>
    </div>
  );
}

function InvestmentConclusionPanel({ data, setView }) {
  const openCompany = (ticker) => {
    setView("companies");
    window.location.hash = `company/${encodeURIComponent(ticker)}`;
  };
  const evaluation = data.rankings?.currentEvaluation;
  const publication = data.rankings?.publicationPolicy;
  const methods = data.rankings?.effectiveness?.methods || [];
  if (!evaluation) {
    return (
      <section className="panel conclusion-panel">
        <PanelTitle icon={LineChart} title="排序综合结论" />
        <p className="muted">当前正式评估尚未载入。</p>
      </section>
    );
  }
  const postGeneration = methods
    .filter((method) => method.postGeneration.checkCount > 0)
    .sort((a, b) => (b.postGeneration.medianRankIc || -99) - (a.postGeneration.medianRankIc || -99));
  const historicalCandidates = methods
    .filter((method) => method.group === "历史候选")
    .sort(
      (a, b) =>
        (b.historicalLookback.metrics.rankIc3m + b.historicalLookback.metrics.rankIc6m) / 2 -
        (a.historicalLookback.metrics.rankIc3m + a.historicalLookback.metrics.rankIc6m) / 2,
    );

  return (
    <section className="panel conclusion-panel">
      <PanelTitle
        icon={LineChart}
        title="公司排序证据摘要"
        action={<TextButton onClick={() => setView("rankings")}>查看完整证据</TextButton>}
      />
      <div className="conclusion-lead">
        <strong>
          公开{publication?.publishedMethodCount || evaluation.coverage.methodCount}个方法、{publication?.publishedListCount || evaluation.coverage.listCount}张榜
        </strong>
        <p>
          {publication?.excludedMethodCount || 0}个退出、明显反向或证据不足的方法不公开公司名次。当前运行尚无严格生成后样本；已有真实生成后检查均为同方法家族前身版本的14至32个交易日短窗。
        </p>
      </div>
      <div className="conclusion-groups">
        <div className="conclusion-group">
          <h2>前身版本真实生成后短窗</h2>
          <div className="conclusion-list">
            {postGeneration.slice(0, 5).map((method) => (
              <article key={`post-${method.methodId}`} className="conclusion-item">
                <div>
                  <strong>{method.methodId} · {method.label}</strong>
                  <p>
                    中位Rank IC {formatSigned(method.postGeneration.medianRankIc, 3)} · Top10相对全体 {formatSignedPercent(method.postGeneration.medianTopUniverseExcessPct)} · {method.postGeneration.checkCount}次
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
        <div className="conclusion-group">
          <h2>当前运行仅历史回看候选</h2>
          <div className="conclusion-list">
            {historicalCandidates.map((method) => (
              <article key={`history-${method.methodId}`} className="conclusion-item">
                <div>
                  <strong>{method.methodId} · {method.label}</strong>
                  <p>
                    3M IC {formatSigned(method.historicalLookback.metrics.rankIc3m, 3)} · 6M IC {formatSigned(method.historicalLookback.metrics.rankIc6m, 3)} · 尚无生成后样本
                  </p>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
      <div className="conclusion-group">
        <h2>{evaluation.coverage.consensusMethodCount}个独立在用方法的共识候选</h2>
        <div className="ticker-stack">
          {(evaluation.consensus || []).slice(0, 12).map((item) => (
            <button
              key={item.ticker}
              className="ticker-chip"
              title={`平均名次 ${formatValue(item.meanRank)}；Top20出现 ${formatValue(item.top20Count)} 次`}
              onClick={() => openCompany(item.ticker)}
            >
              {item.ticker}
            </button>
          ))}
        </div>
        <p className="muted">共识只用于确定进一步研究顺序；历史已大涨的公司尤其需要重新检查估值和追高风险。</p>
      </div>
      <div className="conclusion-cautions">
        {(evaluation.caveats || []).slice(0, 3).map((item) => (
          <p key={item}>{item}</p>
        ))}
      </div>
    </section>
  );
}

function DailyNews({ data }) {
  const items = data.dailyNews.items || [];
  const [query, setQuery] = useState("");
  const [selectedDate, setSelectedDate] = useState(items[0]?.date || "");
  const [listenedDates, setListenedDates] = useState(loadListenedDailyNewsDates);

  useEffect(() => {
    if (!selectedDate && items[0]) setSelectedDate(items[0].date);
  }, [items, selectedDate]);

  const filteredItems = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return items;
    return items.filter((item) =>
      [item.date, item.title, item.summary, item.sourcePath].some((value) => formatValue(value, "").toLowerCase().includes(q)),
    );
  }, [items, query]);

  const selected = items.find((item) => item.date === selectedDate) || filteredItems[0] || items[0] || null;

  const markListened = (date) => {
    setSelectedDate(date);
    setListenedDates((current) => {
      if (current.has(date)) return current;
      const next = new Set(current);
      next.add(date);
      saveListenedDailyNewsDates(next);
      return next;
    });
  };

  return (
    <>
      <PageHeader eyebrow="金融资料" title="AI 新闻稿与语音" />
      <FilterBar>
        <SearchBox value={query} onChange={setQuery} placeholder="搜索日期、标题、摘要" />
        <div className="data-note">
          {data.dailyNews.oldestDate || "-"} 至 {data.dailyNews.latestDate || "-"}
        </div>
      </FilterBar>

      <div className="news-layout">
        <div className="panel news-list-panel">
          <PanelTitle icon={Newspaper} title={`最近 ${items.length} 天`} />
          <div className="news-list">
            {filteredItems.length ? (
              filteredItems.map((item) => (
                <article key={item.date} className={selected?.date === item.date ? "news-list-item active" : "news-list-item"}>
                  <button type="button" className="news-list-summary" onClick={() => setSelectedDate(item.date)}>
                    <span className="news-date">{item.date}</span>
                    <strong>{item.title}</strong>
                    <p>{item.summary}</p>
                  </button>
                  {item.audio ? (
                    <div className="news-list-audio">
                      <div>
                        <Volume2 size={14} />
                        <span>语音</span>
                        <span className={`news-audio-status ${listenedDates.has(item.date) ? "ok" : "unheard"}`}>
                          {listenedDates.has(item.date) ? "已听" : "未听"}
                        </span>
                      </div>
                      <audio
                        controls
                        preload="metadata"
                        src={item.audio.url}
                        aria-label={`${item.date} ${item.title} 语音`}
                        onPlay={() => markListened(item.date)}
                      />
                    </div>
                  ) : (
                    <span className="news-audio-status missing">无音频</span>
                  )}
                </article>
              ))
            ) : (
              <p className="muted">没有匹配的新闻稿。</p>
            )}
          </div>
        </div>

        <article className="panel news-detail">
          {selected ? (
            <>
              <div className="news-detail-heading">
                <span>{selected.date}</span>
                <h2>{selected.title}</h2>
              </div>
              {selected.audio ? (
                <div className="audio-panel">
                  <div>
                    <Volume2 size={18} />
                    <strong>{selected.audio.originalFileName}</strong>
                    <span className={`news-audio-status ${listenedDates.has(selected.date) ? "ok" : "unheard"}`}>
                      {listenedDates.has(selected.date) ? "已听" : "未听"}
                    </span>
                  </div>
                  <audio controls preload="metadata" src={selected.audio.url} onPlay={() => markListened(selected.date)} />
                </div>
              ) : (
                <p className="muted">这一天没有匹配到可发布的语音文件。</p>
              )}
              <SectionBlock title="源文件">
                <code className="path-code">{selected.sourcePath}</code>
              </SectionBlock>
              <MarkdownView markdown={selected.markdown} />
            </>
          ) : (
            <p className="muted">没有可发布的新闻稿。</p>
          )}
        </article>
      </div>
    </>
  );
}

function Stat({ icon: Icon, label, value, note }) {
  return (
    <div className="stat">
      <div className="stat-icon">
        <Icon size={20} />
      </div>
      <span>{label}</span>
      <strong>{value}</strong>
      <em>{note}</em>
    </div>
  );
}

function PanelTitle({ icon: Icon, title, action }) {
  return (
    <div className="panel-title">
      <div>
        <Icon size={18} />
        <h2>{title}</h2>
      </div>
      {action}
    </div>
  );
}

function TextButton({ children, onClick }) {
  return (
    <button className="text-button" onClick={onClick}>
      {children}
    </button>
  );
}

function FilterBar({ children }) {
  return <div className="filter-bar">{children}</div>;
}

function SearchBox({ value, onChange, placeholder }) {
  return (
    <label className="search-box">
      <Search size={16} />
      <input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    </label>
  );
}

function SelectBox({ value, onChange, options, label }) {
  return (
    <label className="select-box">
      <span>{label}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function SegmentedControl({ value, onChange, options }) {
  return (
    <div className="segmented-control" role="tablist">
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          className={value === option.value ? "segment-button active" : "segment-button"}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

function Companies({ data, rankingKey, rankingRun, setRankingKey, rankingByTicker, selectedTicker, setSelectedTicker }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [tier, setTier] = useState("all");
  const [sortKey, setSortKey] = useState("rank");
  const [sortDirection, setSortDirection] = useState("asc");
  const entries = rankingEntries(data);

  const rows = useMemo(() => {
    const merged = data.companies.map((company) => {
      const rank = rankingByTicker[company.ticker] || {};
      return {
        ...company,
        rank: rank.rank ?? null,
        tier: rank.tier || "未评分",
        expectedReturn: rank.expectedReturn || "",
        score: rank.score || "",
        certainty: rank.certainty || "",
        protection: rank.protection || "",
        pe: rank.pe || "",
        fpe: rank.fpe || "",
        ps: rank.ps || "",
        iv: rank.iv || "",
        marketCap: rank.marketCap || "",
        hasReportText: company.hasReport ? "有" : "缺",
      };
    });
    return sortRows(
      merged.filter((row) => {
        const q = query.trim().toLowerCase();
        const matchesQuery =
          !q ||
          [row.ticker, row.name, row.category].some((value) => formatValue(value, "").toLowerCase().includes(q));
        const matchesCategory = category === "all" || row.category === category;
        const matchesTier = tier === "all" || row.tier === tier;
        return matchesQuery && matchesCategory && matchesTier;
      }),
      sortKey,
      sortDirection,
    );
  }, [data.companies, rankingByTicker, query, category, tier, sortKey, sortDirection]);

  const selected = selectedTicker ? data.companies.find((c) => c.ticker === selectedTicker) : null;
  const categories = [...new Set(data.companies.map((c) => c.category))].sort();
  const tiers = [...new Set(Object.values(rankingByTicker).map((r) => r.tier).filter(Boolean))].sort();
  const columns = companyColumns();

  return (
    <>
      <PageHeader
        eyebrow={`公司列表 · 当前口径 ${rankingRun?.label || "-"}`}
        title="公司调研与排序画像"
        actions={
          <IconButton
            label="导出当前列表"
            icon={Download}
            onClick={() => downloadCsv("companies.csv", rows, columns)}
          />
        }
      />
      <FilterBar>
        <SearchBox value={query} onChange={setQuery} placeholder="搜索 ticker、公司、分类" />
        <SelectBox
          label="排序口径"
          value={rankingKey}
          onChange={(value) => {
            setRankingKey(value);
            setSortKey("rank");
            setSortDirection("asc");
          }}
          options={entries.map(({ key, run }) => ({ value: key, label: run.label }))}
        />
        <SelectBox
          label="分类"
          value={category}
          onChange={setCategory}
          options={[{ value: "all", label: "全部分类" }, ...categories.map((c) => ({ value: c, label: c }))]}
        />
        <SelectBox
          label="Tier"
          value={tier}
          onChange={setTier}
          options={[{ value: "all", label: "全部 Tier" }, ...tiers.map((t) => ({ value: t, label: t }))]}
        />
        <div className="data-note">用途：{rankingRun?.strategy || "公司排序"}；{rankingRun?.useCase || ""}</div>
      </FilterBar>
      <div className={selected ? "split-view" : ""}>
        <div className="panel table-panel">
          <SortableTable
            rows={rows}
            columns={columns}
            sortKey={sortKey}
            sortDirection={sortDirection}
            onSort={(key) => {
              setSortDirection(sortKey === key && sortDirection === "asc" ? "desc" : "asc");
              setSortKey(key);
            }}
            onRowClick={(row) => {
              setSelectedTicker(row.ticker);
              window.location.hash = `company/${encodeURIComponent(row.ticker)}`;
            }}
          />
        </div>
        {selected ? (
          <CompanyDetail
            company={selected}
            data={data}
            rankingKey={rankingKey}
            rankingRun={rankingRun}
            rankingByTicker={rankingByTicker}
            comparisonSummary={data.companyComparisons?.companies?.find((item) => item.ticker === selected.ticker)}
            onClose={() => {
              setSelectedTicker(null);
              window.location.hash = "companies";
            }}
          />
        ) : null}
      </div>
    </>
  );
}

function companyColumns() {
  return [
    { key: "rank", label: "Rank", className: "num" },
    { key: "tier", label: "Tier" },
    { key: "ticker", label: "Ticker" },
    { key: "name", label: "公司" },
    { key: "category", label: "分类" },
    { key: "hasReportText", label: "报告" },
    { key: "expectedReturn", label: "预期收益", className: "num" },
    { key: "score", label: "Score", className: "num" },
    { key: "certainty", label: "确定性", className: "num" },
    { key: "protection", label: "保护力", className: "num" },
    { key: "pe", label: "PE", className: "num" },
    { key: "fpe", label: "FPE", className: "num" },
    { key: "ps", label: "PS", className: "num" },
    { key: "iv", label: "IV", className: "num" },
    { key: "marketCap", label: "市值", className: "num" },
  ];
}

function CompanyDetail({ company, data, rankingKey, rankingRun, rankingByTicker, comparisonSummary, onClose }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const rank = rankingByTicker[company.ticker] || {};
  const rankingRows = companyRankingRows(data, company.ticker, rankingKey);
  const featureScoreIndex = data.features.scoreIndex[company.ticker] || {};
  const relatedIndustries = data.industries.filter((industry) => company.relatedIndustrySlugs.includes(industry.slug));

  useEffect(() => {
    let active = true;
    setReport(null);
    if (!company.report?.dataFile) return;
    setLoading(true);
    fetch(`${DATA_BASE}/${company.report.dataFile}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((json) => {
        if (active) setReport(json);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [company.ticker, company.report?.dataFile]);

  return (
    <aside className="detail-panel">
      <button className="close-button" onClick={onClose} aria-label="关闭公司详情">
        <X size={18} />
      </button>
      <div className="detail-heading">
        <span>{company.ticker}</span>
        <h2>{company.name}</h2>
        <p>{company.category}</p>
      </div>
      <div className="mini-grid">
        <Mini label="当前口径" value={rankingRun?.label} />
        <Mini label="当前Rank" value={rank.rank ? `#${rank.rank}` : ""} />
        <Mini label="当前Tier" value={rank.tier} />
        <Mini label="当前收益" value={rank.expectedReturn} />
        <Mini label="当前Score" value={rank.score} />
        <Mini label="PE/FPE" value={`${formatValue(rank.pe)}/${formatValue(rank.fpe)}`} />
        <Mini label="PS / IV" value={`${formatValue(rank.ps)} / ${formatValue(rank.iv)}`} />
        <Mini label="市值" value={rank.marketCap} />
        <Mini label="报告日期" value={company.report?.reportDate} />
      </div>
      <SectionBlock title="源文件">
        <div className="source-stack">
          {company.report ? (
            <LabeledPath label="公司报告" value={company.report.sourcePath} />
          ) : (
            <p className="muted">未匹配到正式公司报告。</p>
          )}
        </div>
      </SectionBlock>
      <SectionBlock title="当前排序口径">
        <div className="current-ranking-note">
          <strong>{rankingRun?.label || "未选择排序"}</strong>
          <span>{rankingRun?.strategy || "公司排序"}</span>
          <p>{rankingRun?.useCase || "当前表格和详情顶部指标使用这个排序口径。"}</p>
          {rankingRun?.caution ? <p className="muted">{rankingRun.caution}</p> : null}
        </div>
      </SectionBlock>
      <SectionBlock title="公司对比">
        {comparisonSummary ? (
          <div className="comparison-mini">
            <div className="company-ranking-stats">
              <span>
                总榜 <strong>#{comparisonSummary.finalRank}</strong>
              </span>
              <span>
                净胜 <strong>{comparisonSummary.finalNet}</strong>
              </span>
              <span>
                自身胜负 <strong>{comparisonSummary.selfWins}/{comparisonSummary.selfLosses}</strong>
              </span>
              <span>
                覆盖 <strong>{comparisonSummary.comparedCount}</strong>
              </span>
            </div>
            <p>{comparisonSummary.onePage?.[0] || "公司对比摘要已生成。"}</p>
            <TextButton
              onClick={() => {
                window.location.hash = `companyComparison/${encodeURIComponent(company.ticker)}`;
              }}
            >
              打开完整对比
            </TextButton>
          </div>
        ) : (
          <p className="muted">未匹配到公司对比结果。</p>
        )}
      </SectionBlock>
      <SectionBlock title="排序画像">
        <CompanyRankingProfile rows={rankingRows} />
      </SectionBlock>
      <SectionBlock title="相关行业">
        <div className="tag-list">
          {relatedIndustries.length ? (
            relatedIndustries.map((industry) => <span key={industry.slug}>{industry.name}</span>)
          ) : (
            <span>暂无映射</span>
          )}
        </div>
      </SectionBlock>
      <SectionBlock title="收益型特征评分">
        <CompanyFeatureGroup data={data} featureScoreIndex={featureScoreIndex} groupKey="alpha" />
      </SectionBlock>
      <SectionBlock title="门槛层结果">
        <CompanyFeatureGroup data={data} featureScoreIndex={featureScoreIndex} groupKey="gates" />
      </SectionBlock>
      <SectionBlock title="公司报告">
        {loading ? <p className="muted">正在加载报告...</p> : null}
        {report ? <MarkdownView markdown={report.markdown} /> : !loading ? <p className="muted">没有可渲染报告。</p> : null}
      </SectionBlock>
    </aside>
  );
}

function CompanyRankingProfile({ rows }) {
  if (!rows.length) return <p className="muted">没有可展示的排序画像。</p>;

  return (
    <div className="company-ranking-list">
      {rows.map((row) => (
        <div className={row.isActive ? "company-ranking-row active" : "company-ranking-row"} key={row.key}>
          <div className="company-ranking-head">
            <div>
              <strong>{row.label}</strong>
              <span>{row.strategy}</span>
            </div>
            {row.isActive ? <em>当前口径</em> : null}
          </div>
          <div className="company-ranking-stats">
            <span>
              Rank <strong>{row.rankText}</strong>
            </span>
            <span>
              分位 <strong>{row.bucket}</strong>
            </span>
            <span>
              Tier <strong>{row.tier}</strong>
            </span>
            <span>
              Score <strong>{row.score}</strong>
            </span>
          </div>
          <p>{row.useCase}</p>
          <p className="muted">验证：{row.validation}</p>
          {row.caution ? <p className="muted">注意：{row.caution}</p> : null}
        </div>
      ))}
    </div>
  );
}

function LabeledPath({ label, value }) {
  return (
    <div className="labeled-path">
      <span>{label}</span>
      <code className="path-code">{value}</code>
    </div>
  );
}

function Mini({ label, value }) {
  return (
    <div className="mini">
      <span>{label}</span>
      <strong>{formatValue(value)}</strong>
    </div>
  );
}

function SectionBlock({ title, children }) {
  return (
    <section className="section-block">
      <h3>{title}</h3>
      {children}
    </section>
  );
}

function CompanyFeatureGroup({ data, featureScoreIndex, groupKey }) {
  const ids = data.features.featureGroups?.[groupKey] || [];
  const rows = ids
    .map((id) => {
      const feature = data.features.features.find((item) => item.id === id);
      const scoreRow = featureScoreIndex[id];
      const rank = toNumber(scoreRow?.rank);
      const rowCount = toNumber(feature?.rowCount);
      const score = toNumber(scoreRow?.score);
      return { id, feature, scoreRow, rank, rowCount, score };
    })
    .filter((row) => row.feature && row.scoreRow)
    .sort((a, b) => (a.rank || 9999) - (b.rank || 9999));

  if (!rows.length) return <p className="muted">当前尚无该公司在{featureGroupLabels[groupKey]}中的正式评分。</p>;

  return (
    <div className="feature-score-list">
      {rows.map((row) => {
        const rankStrength = row.rank && row.rowCount ? 100 - ((row.rank - 1) / Math.max(row.rowCount - 1, 1)) * 100 : null;
        return (
          <div className="feature-score-item" key={`${groupKey}-${row.id}`}>
            <div className="feature-score-head">
              <div>
                <strong>
                  {row.id} {row.feature.name}
                </strong>
                <span>{row.feature.concept || featureGroupDescriptions[groupKey]}</span>
              </div>
              <em>{row.feature.hasScores ? `评分 ${row.feature.date}` : "待生成"}</em>
            </div>
            <div className="feature-bars">
              <MetricBar label="分数" value={row.score} max={10} display={formatValue(row.score)} />
              <MetricBar label="排名" value={rankStrength} max={100} display={row.rank ? `#${row.rank}${row.rowCount ? `/${row.rowCount}` : ""}` : "-"} />
            </div>
            <div className="feature-score-meta">
              <span>{row.feature.layerLabel}</span>
              <span>{row.scoreRow.confidence || "置信度 -"}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function MetricBar({ label, value, max, display }) {
  const numeric = toNumber(value);
  const width = numeric === null ? 0 : Math.max(0, Math.min(100, (numeric / max) * 100));
  return (
    <div className="metric-bar-row">
      <span>{label}</span>
      <div className="bar-track">
        <i style={{ width: `${width}%` }} />
      </div>
      <strong>{display}</strong>
    </div>
  );
}

function formatSigned(value, digits = 2) {
  const n = toNumber(value);
  if (n === null) return "-";
  return `${n >= 0 ? "+" : ""}${n.toFixed(digits)}`;
}

function formatSignedPercent(value) {
  const n = toNumber(value);
  if (n === null) return "-";
  return `${n >= 0 ? "+" : ""}${n.toFixed(2)}%`;
}

function formatRatioPercent(value, digits = 1) {
  const n = toNumber(value);
  if (n === null) return "-";
  const percent = n * 100;
  return `${percent >= 0 ? "+" : ""}${percent.toFixed(digits)}%`;
}

function Industries({ data, rankingByTicker, rankingRun, selectedSlug, setSelectedSlug }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const selected = selectedSlug ? data.industries.find((i) => i.slug === selectedSlug) : null;
  const categories = [...new Set(data.industries.map((i) => i.category))].sort();
  const rows = data.industries.filter((row) => {
    const q = query.trim().toLowerCase();
    return (
      (!q || [row.name, row.category].some((value) => formatValue(value, "").toLowerCase().includes(q))) &&
      (category === "all" || row.category === category)
    );
  });

  return (
    <>
      <PageHeader eyebrow={`行业列表 · 相关公司按 ${rankingRun?.label || "当前公司排序"} 排序`} title="行业调研与相关公司" />
      <FilterBar>
        <SearchBox value={query} onChange={setQuery} placeholder="搜索行业、分类" />
        <SelectBox
          label="分类"
          value={category}
          onChange={setCategory}
          options={[{ value: "all", label: "全部分类" }, ...categories.map((c) => ({ value: c, label: c }))]}
        />
      </FilterBar>
      <div className={selected ? "split-view" : ""}>
        <div className="panel table-panel">
          <DenseTable
            rows={rows}
            columns={[
              { key: "name", label: "行业名称" },
              { key: "category", label: "分类" },
              { key: "companyCount", label: "相关公司", className: "num" },
              { key: "reportDate", label: "报告日期" },
              { key: "hasReportText", label: "报告" },
            ]}
            onRowClick={(row) => {
              setSelectedSlug(row.slug);
              window.location.hash = `industry/${encodeURIComponent(row.slug)}`;
            }}
          />
        </div>
        {selected ? (
          <IndustryDetail
            industry={selected}
            data={data}
            rankingByTicker={rankingByTicker}
            rankingRun={rankingRun}
            onClose={() => {
              setSelectedSlug(null);
              window.location.hash = "industries";
            }}
          />
        ) : null}
      </div>
    </>
  );
}

function IndustryDetail({ industry, data, rankingByTicker, rankingRun, onClose }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const companies = data.companies
    .filter((company) => company.relatedIndustrySlugs.includes(industry.slug))
    .map((company) => ({ ...company, ...(rankingByTicker[company.ticker] || {}) }))
    .sort((a, b) => (toNumber(a.rank) ?? 9999) - (toNumber(b.rank) ?? 9999));

  useEffect(() => {
    let active = true;
    setReport(null);
    if (!industry.report?.dataFile) return;
    setLoading(true);
    fetch(`${DATA_BASE}/${industry.report.dataFile}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((json) => {
        if (active) setReport(json);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [industry.slug, industry.report?.dataFile]);

  return (
    <aside className="detail-panel">
      <button className="close-button" onClick={onClose} aria-label="关闭行业详情">
        <X size={18} />
      </button>
      <div className="detail-heading">
        <span>行业</span>
        <h2>{industry.name}</h2>
        <p>{industry.category}</p>
      </div>
      <div className="mini-grid">
        <div className="mini">
          <span>所属大类</span>
          <strong>{industry.category}</strong>
        </div>
        <div className="mini">
          <span>相关公司</span>
          <strong>{companies.length}</strong>
        </div>
      </div>
      <SectionBlock title={`行业内公司排名：${rankingRun?.label || "当前口径"}`}>
        <DenseTable
          rows={companies.slice(0, 30)}
          columns={[
            { key: "rank", label: "Rank", className: "num" },
            { key: "ticker", label: "Ticker" },
            { key: "name", label: "公司" },
            { key: "expectedReturn", label: "预期收益", className: "num" },
            { key: "score", label: "Score", className: "num" },
          ]}
          onRowClick={(row) => {
            window.location.hash = `company/${encodeURIComponent(row.ticker)}`;
          }}
        />
      </SectionBlock>
      <SectionBlock title="源文件">
        {industry.report ? <code className="path-code">{industry.report.sourcePath}</code> : <p className="muted">未匹配到正式行业报告。</p>}
      </SectionBlock>
      <SectionBlock title="行业报告">
        {loading ? <p className="muted">正在加载报告...</p> : null}
        {report ? <MarkdownView markdown={report.markdown} /> : !loading ? <p className="muted">没有可渲染报告。</p> : null}
      </SectionBlock>
    </aside>
  );
}

function Rankings({ data, rankingKey, setRankingKey }) {
  const entries = rankingEntries(data);
  const [range, setRange] = useState("top");
  const [sortKey, setSortKey] = useState("rank");
  const [sortDirection, setSortDirection] = useState("asc");
  const kind = data.rankings.runs[rankingKey] ? rankingKey : entries[0]?.key;
  const run = data.rankings.runs[kind] || entries[0]?.run;
  const method = rankingEffectiveness(data, run?.methodId);
  const publication = data.rankings.publicationPolicy || {};
  const evaluation = data.rankings.currentEvaluation || {};
  const effectiveness = data.rankings.effectiveness || { methods: [], definitions: {} };
  const baseRows = run?.rows || [];
  const viewRows = range === "bottom" ? [...baseRows].slice(-50).reverse() : baseRows.slice(0, 80);
  const rows = sortRows(viewRows, sortKey, sortDirection);
  const columns = rankingColumns(run);
  const postRows = (method?.postGeneration?.rows || []).map((row) => ({
    runId: row.runId,
    generationDate: row.rankingGeneratedDate,
    window: `${row.evaluationStart} → ${row.evaluationEnd}`,
    holdingDays: row.holdingDays,
    topUniverseExcess: formatSignedPercent(row.topUniverseExcessPct),
    topBottomSpread: formatSignedPercent(row.topBottomSpreadPct),
    rankIc: formatSigned(row.rankIc, 3),
    drawdown: formatSignedPercent(row.maxDrawdownPct),
  }));

  return (
    <>
      <PageHeader
        eyebrow={`证据优先发布 · 股价截至 ${evaluation.priceAsOf || "-"}`}
        title="公司排名与有效性"
        actions={
          <IconButton label="导出当前排名" icon={Download} onClick={() => downloadCsv(`${kind}-ranking.csv`, rows, columns)} />
        }
      />

      <section className="ranking-evidence-strip" aria-label="发布与证据范围">
        <div className="panel ranking-evidence-stat">
          <span>公开范围</span>
          <strong>{publication.publishedMethodCount || 0}个方法 · {publication.publishedListCount || 0}张榜</strong>
          <p>{publication.excludedMethodCount || 0}个退出、反向或证据不足的方法不公开公司名次</p>
        </div>
        <div className="panel ranking-evidence-stat">
          <span>真实生成后短窗</span>
          <strong>{publication.strictPostEvidenceMethodCount || 0}个方法家族</strong>
          <p>14至32个交易日；多数来自前身版本，不能直接等同当前运行</p>
        </div>
        <div className="panel ranking-evidence-stat warning">
          <span>当前运行事后样本</span>
          <strong>{publication.exactCurrentRunPostEvidenceMethodCount || 0}个方法</strong>
          <p>2026-07-13当前榜尚未积累严格生成后窗口</p>
        </div>
      </section>

      <section className="ranking-chart-grid">
        <div className="panel ranking-chart-panel">
          <PanelTitle icon={BarChart3} title="前身版本：真实生成后短窗" />
          <p className="chart-intro">同时看Top10相对全体收益和Rank IC；正值表示榜首方向在该短窗更有效。</p>
          <PostGenerationEvidenceChart methods={effectiveness.methods} />
          <p className="chart-footnote">{effectiveness.definitions.postGeneration}</p>
        </div>
        <div className="panel ranking-chart-panel">
          <PanelTitle icon={LineChart} title="当前版本：3个月与6个月历史同向性" />
          <p className="chart-intro">右上象限表示两个生成前窗口均同向；它不是当前版本的事后验证。</p>
          <HistoricalLookbackScatter methods={effectiveness.methods} />
          <p className="chart-footnote">{effectiveness.definitions.historicalLookback}</p>
        </div>
      </section>

      <section className="panel ranking-contract" aria-label="公司排序数据依赖">
        <div className="ranking-contract-step">
          <span>1</span>
          <strong>注册表 + 发布策略 + 当前评估</strong>
          <small>研究目录维护事实和公开范围</small>
        </div>
        <b aria-hidden="true">→</b>
        <div className="ranking-contract-step active">
          <span>2</span>
          <strong>站点数据 / current.json</strong>
          <small>唯一稳定数据契约</small>
        </div>
        <b aria-hidden="true">→</b>
        <div className="ranking-contract-step">
          <span>3</span>
          <strong>Project Ananta</strong>
          <small>只校验和展示，不猜目录</small>
        </div>
      </section>

      <FilterBar>
        <SelectBox
          label="公开榜单"
          value={kind}
          onChange={(value) => {
            setRankingKey(value);
            setSortKey("rank");
            setSortDirection("asc");
          }}
          options={entries.map(({ key, run: item }) => ({ value: key, label: `[${item.siteGroup}] ${item.label}` }))}
        />
        <SelectBox
          label="范围"
          value={range}
          onChange={setRange}
          options={[
            { value: "top", label: "Top 80" },
            { value: "bottom", label: "Bottom 50" },
          ]}
        />
        <div className="data-note">当前：{run?.methodId || "-"}/{run?.listId || "-"} · {run?.evidenceLabel || "-"}</div>
      </FilterBar>

      <section className="ranking-method-grid">
        <div className="panel ranking-method-profile">
          <div className="ranking-method-title">
            <span className={`evidence-pill ${evidenceClass(method?.group)}`}>{method?.group || "-"}</span>
            <span className="evidence-label">{method?.evidenceLabel || "-"}</span>
          </div>
          <h2>{run?.label || "公司排序"}</h2>
          <p>{run?.useCase || "查看该排序的适用场景和约束。"}</p>
          <p className="muted">{method?.publishReason || run?.caution || ""}</p>
        </div>
        <div className="panel ranking-method-evidence">
          <h2>真实生成后证据</h2>
          {method?.postGeneration?.checkCount ? (
            <div className="metric-grid compact">
              <Metric label="检查次数" value={method.postGeneration.checkCount} />
              <Metric label="中位 Rank IC" value={formatSigned(method.postGeneration.medianRankIc, 3)} />
              <Metric label="Top10-全体" value={formatSignedPercent(method.postGeneration.medianTopUniverseExcessPct)} />
              <Metric label="Top10-Bottom10" value={formatSignedPercent(method.postGeneration.medianTopBottomSpreadPct)} />
            </div>
          ) : (
            <p className="evidence-empty">尚无严格生成后样本</p>
          )}
          <p className="muted">{method?.postGeneration?.relationToCurrentRun || "-"}</p>
        </div>
        <div className="panel ranking-method-evidence">
          <h2>当前版本生成前历史回看</h2>
          <div className="metric-grid compact">
            <Metric label="3M Rank IC" value={formatSigned(method?.historicalLookback?.metrics?.rankIc3m, 3)} />
            <Metric label="3M 行业中性" value={formatSigned(method?.historicalLookback?.metrics?.categoryNeutralRankIc3m, 3)} />
            <Metric label="6M Rank IC" value={formatSigned(method?.historicalLookback?.metrics?.rankIc6m, 3)} />
            <Metric label="6M 行业中性" value={formatSigned(method?.historicalLookback?.metrics?.categoryNeutralRankIc6m, 3)} />
          </div>
          <p className="muted">{evaluation.evidenceType || "-"}，只表示与已发生价格的同向性。</p>
        </div>
      </section>

      {postRows.length ? (
        <section className="panel ranking-post-history">
          <PanelTitle icon={ShieldCheck} title="严格生成后检查明细" />
          <DenseTable
            rows={postRows}
            columns={[
              { key: "runId", label: "前身运行" },
              { key: "generationDate", label: "生成日" },
              { key: "window", label: "未见窗口" },
              { key: "holdingDays", label: "交易日", className: "num" },
              { key: "topUniverseExcess", label: "Top10-全体", className: "num" },
              { key: "topBottomSpread", label: "Top10-Bottom10", className: "num" },
              { key: "rankIc", label: "Rank IC", className: "num" },
              { key: "drawdown", label: "Top10回撤", className: "num" },
            ]}
          />
        </section>
      ) : null}

      <FilterBar>
        <div className="data-note">榜单生成：{run?.date || "-"} · 每榜{run?.rowCount || 0}家公司 · 结果来源已由研究侧数据契约校验</div>
      </FilterBar>
      <div className="panel table-panel">
        <SortableTable
          rows={rows}
          columns={columns}
          sortKey={sortKey}
          sortDirection={sortDirection}
          onSort={(key) => {
            setSortDirection(sortKey === key && sortDirection === "asc" ? "desc" : "asc");
            setSortKey(key);
          }}
          onRowClick={(row) => {
            window.location.hash = `company/${encodeURIComponent(row.ticker)}`;
          }}
        />
      </div>
    </>
  );
}

function evidenceClass(group) {
  if (group === "实证优先") return "verified";
  if (group === "在用观察") return "watch";
  if (group === "历史候选") return "candidate";
  return "neutral";
}

function PostGenerationEvidenceChart({ methods }) {
  const rows = (methods || []).filter((method) => method.postGeneration.checkCount > 0);
  if (!rows.length) return <p className="evidence-empty">暂无生成后证据。</p>;
  const width = 900;
  const rowHeight = 42;
  const height = 76 + rows.length * rowHeight;
  const excessCenter = 300;
  const excessHalf = 135;
  const excessMax = Math.max(15, ...rows.map((method) => Math.abs(method.postGeneration.medianTopUniverseExcessPct || 0)));
  const icCenter = 700;
  const icHalf = 125;
  const icMax = 0.6;
  const excessX = (value) => excessCenter + ((value || 0) / excessMax) * excessHalf;
  const icX = (value) => icCenter + ((value || 0) / icMax) * icHalf;
  const signColor = (value) => (value >= 0 ? "#2f6f73" : "#b45f50");

  return (
    <svg className="ranking-evidence-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-labelledby="post-chart-title post-chart-desc">
      <title id="post-chart-title">公开方法前身版本生成后短窗有效性</title>
      <desc id="post-chart-desc">每行显示一个方法的Top10相对全体收益中位数和Rank IC中位数，正值位于零线右侧。</desc>
      <text x="165" y="22" className="chart-heading">Top10 相对全体收益，中位数（百分点）</text>
      <text x="575" y="22" className="chart-heading">Rank IC，中位数</text>
      <line x1={excessCenter} y1="34" x2={excessCenter} y2={height - 12} className="chart-zero-line" />
      <line x1={icCenter} y1="34" x2={icCenter} y2={height - 12} className="chart-zero-line" />
      {rows.map((method, index) => {
        const y = 56 + index * rowHeight;
        const excess = method.postGeneration.medianTopUniverseExcessPct || 0;
        const excessEnd = excessX(excess);
        const ic = method.postGeneration.medianRankIc || 0;
        const icEnd = icX(ic);
        return (
          <g key={method.methodId}>
            <line x1="145" y1={y + 14} x2="835" y2={y + 14} className="chart-row-line" />
            <text x="12" y={y + 4} className="chart-method-id">{method.methodId}</text>
            <text x="42" y={y + 4} className="chart-method-name">{method.label}</text>
            <text x="42" y={y + 19} className="chart-method-note">n={method.postGeneration.checkCount}</text>
            <rect
              x={Math.min(excessCenter, excessEnd)}
              y={y - 7}
              width={Math.max(2, Math.abs(excessEnd - excessCenter))}
              height="12"
              rx="3"
              fill={signColor(excess)}
            >
              <title>{method.methodId} Top10相对全体 {formatSignedPercent(excess)}</title>
            </rect>
            <text x={excess >= 0 ? excessEnd + 7 : excessEnd - 7} y={y + 3} textAnchor={excess >= 0 ? "start" : "end"} className="chart-value">
              {formatSignedPercent(excess)}
            </text>
            <circle cx={icEnd} cy={y - 1} r="6" fill={signColor(ic)}>
              <title>{method.methodId} Rank IC {formatSigned(ic, 3)}</title>
            </circle>
            <text x={ic >= 0 ? icEnd + 10 : icEnd - 10} y={y + 3} textAnchor={ic >= 0 ? "start" : "end"} className="chart-value">
              {formatSigned(ic, 3)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function HistoricalLookbackScatter({ methods }) {
  const rows = methods || [];
  if (!rows.length) return <p className="evidence-empty">暂无历史回看数据。</p>;
  const width = 540;
  const height = 370;
  const left = 58;
  const right = 512;
  const top = 34;
  const bottom = 306;
  const min = -0.4;
  const max = 0.35;
  const scaleX = (value) => left + ((value - min) / (max - min)) * (right - left);
  const scaleY = (value) => bottom - ((value - min) / (max - min)) * (bottom - top);
  const zeroX = scaleX(0);
  const zeroY = scaleY(0);
  const ticks = [-0.4, -0.2, 0, 0.2];
  const groupColor = {
    实证优先: "#2f6f73",
    在用观察: "#c28a2c",
    历史候选: "#765d9c",
  };

  return (
    <svg className="ranking-scatter-chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-labelledby="scatter-title scatter-desc">
      <title id="scatter-title">当前公开方法3个月和6个月生成前历史Rank IC</title>
      <desc id="scatter-desc">横轴为3个月Rank IC，纵轴为6个月Rank IC；右上象限代表两个历史窗口均为正。</desc>
      <rect x={zeroX} y={top} width={right - zeroX} height={zeroY - top} className="chart-positive-quadrant" />
      {ticks.map((tick) => (
        <g key={`x-${tick}`}>
          <line x1={scaleX(tick)} y1={top} x2={scaleX(tick)} y2={bottom} className={tick === 0 ? "chart-zero-line" : "chart-grid-line"} />
          <text x={scaleX(tick)} y={bottom + 19} textAnchor="middle" className="chart-tick">{tick.toFixed(1)}</text>
        </g>
      ))}
      {ticks.map((tick) => (
        <g key={`y-${tick}`}>
          <line x1={left} y1={scaleY(tick)} x2={right} y2={scaleY(tick)} className={tick === 0 ? "chart-zero-line" : "chart-grid-line"} />
          <text x={left - 10} y={scaleY(tick) + 4} textAnchor="end" className="chart-tick">{tick.toFixed(1)}</text>
        </g>
      ))}
      <text x={(left + right) / 2} y={height - 12} textAnchor="middle" className="chart-axis-label">3个月 Rank IC</text>
      <text x="14" y={(top + bottom) / 2} transform={`rotate(-90 14 ${(top + bottom) / 2})`} textAnchor="middle" className="chart-axis-label">6个月 Rank IC</text>
      <text x={right - 4} y={top + 16} textAnchor="end" className="chart-quadrant-label">两个窗口均同向</text>
      {rows.map((method) => {
        const x = scaleX(method.historicalLookback.metrics.rankIc3m);
        const y = scaleY(method.historicalLookback.metrics.rankIc6m);
        const color = groupColor[method.group] || "#607080";
        return (
          <g key={method.methodId}>
            {method.group === "在用观察" ? (
              <rect x={x - 6} y={y - 6} width="12" height="12" rx="2" fill={color} />
            ) : method.group === "历史候选" ? (
              <polygon points={`${x},${y - 7} ${x + 7},${y} ${x},${y + 7} ${x - 7},${y}`} fill={color} />
            ) : (
              <circle cx={x} cy={y} r="6" fill={color} />
            )}
            <title>{method.methodId} {method.label}：3M {formatSigned(method.historicalLookback.metrics.rankIc3m, 3)}，6M {formatSigned(method.historicalLookback.metrics.rankIc6m, 3)}</title>
            <text x={x + 9} y={y - 8} className="chart-point-label">{method.methodId}</text>
          </g>
        );
      })}
      <g transform="translate(74 344)" className="chart-legend">
        <circle cx="0" cy="0" r="5" fill={groupColor.实证优先} />
        <text x="10" y="4">实证优先</text>
        <rect x="100" y="-5" width="10" height="10" rx="2" fill={groupColor.在用观察} />
        <text x="119" y="4">在用观察</text>
        <polygon points="220,-6 226,0 220,6 214,0" fill={groupColor.历史候选} />
        <text x="232" y="4">历史候选</text>
      </g>
    </svg>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric-item">
      <span>{label}</span>
      <strong>{formatValue(value)}</strong>
    </div>
  );
}

function rankingColumns(run) {
  const common = [
    { key: "rank", label: "Rank", className: "num" },
    { key: "tier", label: "Tier" },
    { key: "ticker", label: "Ticker" },
    { key: "name", label: "公司" },
    { key: "category", label: "分类" },
    { key: "expectedReturn", label: "预期收益", className: "num" },
    { key: "score", label: "Score", className: "num" },
    { key: "certainty", label: "确定性", className: "num" },
    { key: "protection", label: "保护力", className: "num" },
    { key: "pe", label: "PE", className: "num" },
    { key: "fpe", label: "FPE", className: "num" },
    { key: "ps", label: "PS", className: "num" },
    { key: "iv", label: "IV", className: "num" },
    { key: "marketCap", label: "市值", className: "num" },
    { key: "reason", label: "排序理由" },
  ];
  const always = new Set(["rank", "ticker", "name", "category"]);
  return common.filter(
    (column) => always.has(column.key) || (run?.rows || []).some((row) => formatValue(row[column.key], "") !== ""),
  );
}

function ScenarioDecisions({ data, selectedTicker, setSelectedTicker }) {
  const scenarioData = data.scenarioDecisions || { companies: [], metrics: {}, scenarioGrid: [], categories: [], insights: {} };
  const selected = selectedTicker ? scenarioData.companies.find((row) => row.ticker === selectedTicker) : null;
  const [query, setQuery] = useState("");
  const [adviceGroup, setAdviceGroup] = useState("all");
  const [operatingScenario, setOperatingScenario] = useState("all");
  const [marketState, setMarketState] = useState("all");
  const [matrixScope, setMatrixScope] = useState("all");
  const [category, setCategory] = useState("all");
  const [sortKey, setSortKey] = useState("currentAdviceRank");
  const [sortDirection, setSortDirection] = useState("desc");
  const [focusedCell, setFocusedCell] = useState({ operatingScenario: "base", marketState: "broad" });

  if (selected) {
    return (
      <ScenarioDecisionDetail
        summary={selected}
        scenarioData={scenarioData}
        onClose={() => {
          setSelectedTicker(null);
          window.location.hash = "scenarioDecisions";
        }}
      />
    );
  }

  const categories = [...new Set(scenarioData.companies.map((row) => row.category).filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));
  const rows = scenarioData.companies
    .map((row) => ({
      ...row,
      currentAdvice: row.current.adviceLabel,
      currentAdviceRank: row.current.adviceRank,
      currentPosition: `${row.current.operatingLabel} × ${row.current.marketLabel}`,
      currentReturn: row.current.returnRangeText,
      positiveCells: row.matrix.positiveCellCount,
      basePositive: row.matrix.basePositiveCount,
      stressPositive: row.matrix.stressPositiveCount,
    }))
    .filter((row) => {
      const q = query.trim().toLowerCase();
      const matchesQuery = !q || [row.ticker, row.name, row.category, row.current.weakLink].some((value) => formatValue(value, "").toLowerCase().includes(q));
      const matchesAdvice = adviceGroup === "all" || row.current.adviceGroup === adviceGroup;
      const matchesOperating = operatingScenario === "all" || row.current.operatingScenario === operatingScenario;
      const matchesMarket = marketState === "all" || row.current.marketState === marketState;
      const matchesCategory = category === "all" || row.category === category;
      const matchesScope =
        matrixScope === "all" ||
        (matrixScope === "robust" && row.matrix.basePositiveCount >= 3) ||
        (matrixScope === "baseAny" && row.matrix.basePositiveCount > 0) ||
        (matrixScope === "stress" && row.matrix.stressPositiveCount > 0) ||
        (matrixScope === "breakthrough" && row.matrix.breakthroughDependent) ||
        (matrixScope === "none" && row.matrix.positiveCellCount === 0);
      return matchesQuery && matchesAdvice && matchesOperating && matchesMarket && matchesCategory && matchesScope;
    });
  const sortedRows = sortRows(rows, sortKey, sortDirection);
  const metrics = scenarioData.metrics || { current: {}, matrix: {} };
  const focused = scenarioData.scenarioGrid.find(
    (cell) => cell.operatingScenario === focusedCell.operatingScenario && cell.marketState === focusedCell.marketState,
  );

  const handleSort = (key) => {
    if (sortKey === key) setSortDirection((value) => (value === "asc" ? "desc" : "asc"));
    else {
      setSortKey(key);
      setSortDirection(["ticker", "name", "category", "currentPosition"].includes(key) ? "asc" : "desc");
    }
  };
  const openCompany = (ticker) => {
    setSelectedTicker(ticker);
    window.location.hash = `scenarioDecision/${encodeURIComponent(ticker)}`;
  };

  return (
    <>
      <PageHeader
        eyebrow={`个股绝对决策 · ${scenarioData.reportDate || "-"} · 概率层不参与汇总`}
        title="经营情景 × 市场状态"
        actions={
          <TextButton
            onClick={() =>
              downloadCsv(
                `scenario-decisions-${scenarioData.reportDate || "current"}.csv`,
                sortedRows,
                [
                  { key: "ticker", label: "Ticker" },
                  { key: "name", label: "公司" },
                  { key: "category", label: "分类" },
                  { key: "currentAdvice", label: "当前条件建议" },
                  { key: "currentPosition", label: "当前位置" },
                  { key: "currentReturn", label: "当前回报区间" },
                  { key: "positiveCells", label: "全矩阵正面格" },
                  { key: "basePositive", label: "基准行正面格" },
                ],
              )
            }
          >
            导出筛选结果
          </TextButton>
        }
      />

      <section className="scenario-intro panel">
        <div>
          <span>条件地图，而不是单一目标价</span>
          <strong>先看公司经营兑现，再看市场如何放大或压缩价值。</strong>
        </div>
        <p>当前条件建议包含必要的复合定位与明确板块修正；4×5主矩阵始终保持纯经营情景。点击任一公司可查看二十格理由、改变条件和完整研究原文。</p>
      </section>

      <section className="stat-grid scenario-stat-grid">
        <Stat icon={Grid3X3} label="覆盖公司" value={scenarioData.companyCount || 0} note={`${scenarioData.estimableCellCount || 0}/${scenarioData.cellCount || 0} 格可估值`} />
        <Stat icon={LineChart} label="当前正面" value={metrics.current?.positive || 0} note={`${formatScenarioPercent(metrics.current?.positiveShare)} · 谨慎建议及以上`} />
        <Stat icon={Gauge} label="当前中性" value={metrics.current?.neutral || 0} note={`${metrics.current?.compositeCount || 0}家使用复合定位`} />
        <Stat icon={AlertTriangle} label="当前负面" value={metrics.current?.negative || 0} note={`${metrics.current?.rotationAdjustedCount || 0}家明确采用板块修正`} />
        <Stat icon={BarChart3} label="矩阵正面格" value={metrics.matrix?.positive || 0} note={`${formatScenarioPercent(metrics.matrix?.positiveShare)} · 不含概率加权`} />
      </section>

      <section className="scenario-visual-grid">
        <div className="panel scenario-heatmap-panel">
          <div className="comparison-section-heading">
            <div><span>全体公司条件地图</span><h2>二十格正面建议率</h2></div>
            <p>“正面”指谨慎建议投资及以上。点击格子查看该组合的公司数与中位回报区间。</p>
          </div>
          <ScenarioGlobalHeatmap data={scenarioData} focused={focusedCell} onFocus={setFocusedCell} />
          {focused ? (
            <div className="scenario-focus-note">
              <strong>{focused.operatingLabel} × {focused.marketLabel}</strong>
              <span>{focused.positiveCount}/{focused.estimableCount} 家正面 · 中位回报 {formatSignedPercent(focused.medianLowReturn)} 至 {formatSignedPercent(focused.medianHighReturn)}</span>
            </div>
          ) : null}
        </div>
        <div className="scenario-side-stack">
          <div className="panel">
            <div className="comparison-section-heading compact"><div><span>当前位置</span><h2>建议强度分布</h2></div></div>
            <ScenarioAdviceDistribution scenarioData={scenarioData} />
          </div>
          <div className="panel">
            <div className="comparison-section-heading compact"><div><span>敏感度</span><h2>经营行与市场列</h2></div></div>
            <ScenarioAxisBars rows={metrics.matrix?.scenarioStats || []} />
            <div className="scenario-axis-divider" />
            <ScenarioAxisBars rows={metrics.matrix?.marketStats || []} compact />
          </div>
        </div>
      </section>

      <section className="panel scenario-category-panel">
        <div className="comparison-section-heading compact">
          <div><span>行业结构</span><h2>当前建议与基准可投资宽度</h2></div>
          <p>颜色表示当前建议方向；右侧数字表示基准经营行至少有一个正面市场状态的公司数。</p>
        </div>
        <ScenarioCategoryBars rows={scenarioData.categories || []} onSelect={(value) => setCategory(value)} />
      </section>

      <section className="scenario-insight-grid">
        <ScenarioInsightCard title="基准更稳健" note="基准行至少3个正面格" rows={scenarioData.insights?.robustBase || []} metric={(row) => `${row.matrix.basePositiveCount}/5`} onSelect={openCompany} />
        <ScenarioInsightCard title="当前条件正面" note="含复合与板块修正" rows={scenarioData.insights?.currentPositive || []} metric={(row) => shortAdvice(row.current.adviceKey)} onSelect={openCompany} />
        <ScenarioInsightCard title="突破依赖" note="基准与乐观均无正面格" rows={scenarioData.insights?.breakthroughDependent || []} metric={(row) => `${row.matrix.positiveCellCount}/20`} onSelect={openCompany} />
        <ScenarioInsightCard title="全矩阵无正面" note="即使突破也未覆盖价格" rows={scenarioData.insights?.noPositive || []} metric={() => "0/20"} onSelect={openCompany} />
      </section>

      <section className="panel scenario-explorer">
        <div className="comparison-section-heading compact">
          <div><span>192家公司</span><h2>条件决策浏览器</h2></div>
          <p>显示 {sortedRows.length}/{scenarioData.companies.length || 0} 家；当前建议与纯矩阵不同时，以当前定位为准。</p>
        </div>
        <FilterBar>
          <SearchBox value={query} onChange={setQuery} placeholder="搜索Ticker、公司、分类或最弱环节" />
          <SelectBox label="建议" value={adviceGroup} onChange={setAdviceGroup} options={[{ value: "all", label: "全部方向" }, { value: "positive", label: "正面" }, { value: "neutral", label: "中性" }, { value: "negative", label: "负面" }]} />
          <SelectBox label="经营" value={operatingScenario} onChange={setOperatingScenario} options={[{ value: "all", label: "全部经营行" }, ...(scenarioData.operatingScenarios || []).map((row) => ({ value: row.key, label: row.shortLabel }))]} />
          <SelectBox label="市场" value={marketState} onChange={setMarketState} options={[{ value: "all", label: "全部市场列" }, ...(scenarioData.marketStates || []).map((row) => ({ value: row.key, label: row.shortLabel }))]} />
          <SelectBox label="矩阵" value={matrixScope} onChange={setMatrixScope} options={[{ value: "all", label: "全部矩阵形状" }, { value: "robust", label: "基准≥3格正面" }, { value: "baseAny", label: "基准至少1格" }, { value: "stress", label: "压力列仍正面" }, { value: "breakthrough", label: "仅突破转正" }, { value: "none", label: "无正面格" }]} />
          <SelectBox label="分类" value={category} onChange={setCategory} options={[{ value: "all", label: "全部分类" }, ...categories.map((value) => ({ value, label: value }))]} />
        </FilterBar>
        <div className="table-scroll scenario-table-wrap">
          <table className="data-table scenario-table">
            <thead><tr>
              <ScenarioSortHeader label="Ticker / 公司" sortKey="ticker" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="当前条件建议" sortKey="currentAdviceRank" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="当前位置" sortKey="currentPosition" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="当前回报" sortKey="currentReturn" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="正面格" sortKey="positiveCells" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="基准正面" sortKey="basePositive" active={sortKey} direction={sortDirection} onSort={handleSort} />
              <ScenarioSortHeader label="压力正面" sortKey="stressPositive" active={sortKey} direction={sortDirection} onSort={handleSort} />
            </tr></thead>
            <tbody>{sortedRows.map((row) => (
              <tr key={row.ticker} onClick={() => openCompany(row.ticker)}>
                <td><button className="ticker-link" onClick={(event) => { event.stopPropagation(); openCompany(row.ticker); }}>{row.ticker}</button><span className="scenario-company-name">{row.name}</span><em className="scenario-company-category">{row.category}</em></td>
                <td><AdviceBadge adviceKey={row.current.adviceKey} />{row.current.adjustmentType !== "pure" ? <small className="scenario-adjustment-note">{row.current.adjustmentType === "composite" ? "复合定位" : "板块修正"}</small> : null}</td>
                <td>{row.current.operatingLabel}<small>{row.current.marketLabel}</small></td>
                <td className="num">{row.current.returnRangeText || "-"}</td>
                <td className="num"><strong>{row.matrix.positiveCellCount}</strong>/{row.matrix.estimableCellCount}</td>
                <td className="num">{row.matrix.basePositiveCount}/5</td>
                <td className="num">{row.matrix.stressPositiveCount}/4</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
        <div className="scenario-quality-note"><ShieldCheck size={15} /><span>{scenarioData.qualityNote} 当前市场状态来自各主要定价市场的报告快照，跨公司比较时应优先使用完整条件矩阵。</span></div>
      </section>
    </>
  );
}

function ScenarioGlobalHeatmap({ data, focused, onFocus }) {
  const byKey = new Map((data.scenarioGrid || []).map((row) => [`${row.operatingScenario}:${row.marketState}`, row]));
  return (
    <div className="scenario-global-heatmap" role="grid" aria-label="全体公司经营情景与市场状态正面建议率">
      <div className="scenario-heatmap-corner">经营 \ 市场</div>
      {(data.marketStates || []).map((market) => <div key={market.key} className="scenario-heatmap-header">{market.shortLabel}</div>)}
      {(data.operatingScenarios || []).flatMap((scenario) => [
        <div key={`${scenario.key}-label`} className="scenario-heatmap-row-label">{scenario.label}</div>,
        ...(data.marketStates || []).map((market) => {
          const cell = byKey.get(`${scenario.key}:${market.key}`);
          const active = focused.operatingScenario === scenario.key && focused.marketState === market.key;
          return (
            <button
              key={`${scenario.key}-${market.key}`}
              className={`scenario-global-cell ${scenarioHeatClass(cell?.positiveShare || 0)} ${active ? "active" : ""}`}
              onClick={() => onFocus({ operatingScenario: scenario.key, marketState: market.key })}
              aria-label={`${scenario.label}、${market.label}，正面率${formatScenarioPercent(cell?.positiveShare)}`}
            >
              <strong>{formatScenarioPercent(cell?.positiveShare)}</strong>
              <span>{cell?.positiveCount || 0}/{cell?.estimableCount || 0}</span>
            </button>
          );
        }),
      ])}
    </div>
  );
}

function ScenarioAdviceDistribution({ scenarioData }) {
  const counts = scenarioData.metrics?.current?.adviceCounts || {};
  const total = scenarioData.companyCount || 1;
  const levels = [...(scenarioData.adviceLevels || [])].reverse();
  return (
    <>
      <div className="scenario-advice-stack" aria-label="当前建议强度分布">
        {levels.map((level) => <span key={level.key} className={`tone-${level.key}`} style={{ width: `${((counts[level.key] || 0) / total) * 100}%` }} title={`${level.label}：${counts[level.key] || 0}`} />)}
      </div>
      <div className="scenario-advice-legend">
        {levels.map((level) => <div key={level.key}><i className={`tone-${level.key}`} /><span>{level.label}</span><strong>{counts[level.key] || 0}</strong></div>)}
      </div>
    </>
  );
}

function ScenarioAxisBars({ rows, compact = false }) {
  return <div className={compact ? "scenario-axis-bars compact" : "scenario-axis-bars"}>{rows.map((row) => (
    <div key={row.key}>
      <span>{row.shortLabel || row.label}</span>
      <i><b style={{ width: `${Math.max(0, Math.min(100, (row.positiveShare || 0) * 100))}%` }} /></i>
      <strong>{formatScenarioPercent(row.positiveShare)}</strong>
    </div>
  ))}</div>;
}

function ScenarioCategoryBars({ rows, onSelect }) {
  const sorted = [...rows].sort((a, b) => b.positive / b.companyCount - a.positive / a.companyCount || b.baseAnyPositive - a.baseAnyPositive);
  return <div className="scenario-category-bars">{sorted.map((row) => (
    <button key={row.category} onClick={() => onSelect(row.category)}>
      <span title={row.category}>{row.category}</span>
      <i>
        <b className="positive" style={{ width: `${(row.positive / row.companyCount) * 100}%` }} />
        <b className="neutral" style={{ width: `${(row.neutral / row.companyCount) * 100}%` }} />
        <b className="negative" style={{ width: `${(row.negative / row.companyCount) * 100}%` }} />
      </i>
      <em>{row.positive}/{row.neutral}/{row.negative}</em>
      <strong>基准 {row.baseAnyPositive}/{row.companyCount}</strong>
    </button>
  ))}</div>;
}

function ScenarioInsightCard({ title, note, rows, metric, onSelect }) {
  return (
    <div className="panel scenario-insight-card">
      <div><strong>{title}</strong><span>{note}</span></div>
      <ol>{rows.slice(0, 8).map((row) => <li key={row.ticker}><button onClick={() => onSelect(row.ticker)}><span>{row.ticker}<small>{row.name}</small></span><em>{metric(row)}</em></button></li>)}</ol>
      {!rows.length ? <p className="muted">当前没有符合条件的公司。</p> : null}
    </div>
  );
}

function ScenarioSortHeader({ label, sortKey, active, direction, onSort }) {
  return <th><button onClick={() => onSort(sortKey)}>{label}{active === sortKey ? <span>{direction === "asc" ? "↑" : "↓"}</span> : null}</button></th>;
}

function ScenarioDecisionDetail({ summary, scenarioData, onClose }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedCell, setSelectedCell] = useState({
    operatingScenario: summary.current.operatingScenario,
    marketState: summary.current.marketState,
  });

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`${DATA_BASE}/${summary.dataFile}`, { cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error(`${summary.dataFile} ${response.status}`);
        return response.json();
      })
      .then((value) => { if (!cancelled) setReport(value); })
      .catch(() => { if (!cancelled) setReport(null); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [summary.dataFile]);

  const activeCell = report?.cells?.find((cell) => cell.operatingScenario === selectedCell.operatingScenario && cell.marketState === selectedCell.marketState) || null;
  const adjustmentText = summary.current.adjustmentType === "composite"
    ? `复合定位：纯格子为${summary.current.pureAdviceLabel}，当前应用为${summary.current.adviceLabel}`
    : summary.current.adjustmentType === "sectorRotation"
      ? `板块轮动修正：纯格子为${summary.current.pureAdviceLabel}，当前应用为${summary.current.adviceLabel}`
      : "当前直接采用纯经营格子";

  return (
    <>
      <PageHeader
        eyebrow={`公司情景决策 · ${summary.reportDate}`}
        title={`${summary.ticker} · ${summary.name}`}
        actions={<><TextButton onClick={() => { window.location.hash = `company/${encodeURIComponent(summary.ticker)}`; }}>打开公司主页</TextButton><TextButton onClick={onClose}>返回全部公司</TextButton></>}
      />
      <section className="scenario-company-hero panel">
        <div>
          <span>{summary.category}</span>
          <AdviceBadge adviceKey={summary.current.adviceKey} large />
          <p>{summary.current.operatingLabel} × {summary.current.marketLabel}</p>
        </div>
        <div>
          <strong>{adjustmentText}</strong>
          <p>{summary.current.weakLink ? `最弱传导环节：${summary.current.weakLink}` : "最弱传导环节见完整报告。"}</p>
        </div>
      </section>

      <section className="stat-grid scenario-detail-stats">
        <Stat icon={Grid3X3} label="正面区域" value={`${summary.matrix.positiveCellCount}/${summary.matrix.estimableCellCount}`} note="全矩阵正面格" />
        <Stat icon={TargetIcon} label="基准稳健性" value={`${summary.matrix.basePositiveCount}/5`} note="基准行正面市场状态" />
        <Stat icon={ShieldCheck} label="压力韧性" value={`${summary.matrix.stressPositiveCount}/4`} note="流动性压力列正面经营行" />
        <Stat icon={LineChart} label="当前回报区间" value={summary.current.returnRangeText || "-"} note={summary.current.perShareValue || "当前条件区间"} />
        <Stat icon={Gauge} label="正面价格边界" value={summary.current.priceBoundary || "-"} note="经营与市场假设不变" />
      </section>

      <section className="panel scenario-company-matrix-panel">
        <div className="comparison-section-heading compact">
          <div><span>公司条件地图</span><h2>二十格投资建议</h2></div>
          <p>点击格子查看估值方法、每股价值、决定性理由和结论改变条件。NA表示当前证据不足以可靠估值。</p>
        </div>
        {loading ? <p className="muted">正在加载二十格明细...</p> : null}
        {report ? <ScenarioCompanyMatrix data={scenarioData} cells={report.cells} selected={selectedCell} onSelect={setSelectedCell} /> : null}
      </section>

      {activeCell ? (
        <section className="scenario-cell-detail-grid">
          <div className="panel scenario-cell-verdict">
            <span>{activeCell.operatingLabel} × {activeCell.marketLabel}</span>
            <AdviceBadge adviceKey={activeCell.adviceKey} large />
            <strong>{activeCell.returnRangeText || "无法可靠估值"}</strong>
            <p>{activeCell.perShareValue || "每股价值区间 NA"} · 估值置信度 {activeCell.confidence || "NA"}</p>
          </div>
          <div className="panel scenario-cell-evidence"><span>主估值理念</span><p>{activeCell.valuationMethod || "详见完整报告"}</p><span>决定性理由</span><p>{activeCell.decisiveReason || "详见完整报告"}</p></div>
          <div className="panel scenario-cell-evidence"><span>结论改变条件</span><p>{activeCell.changeCondition || "详见完整报告"}</p><span>稀释后股权市值</span><p>{activeCell.equityValue || "NA"}</p></div>
        </section>
      ) : null}

      <section className="scenario-current-grid">
        <div className="panel">
          <div className="comparison-section-heading compact"><div><span>当前定位</span><h2>条件摘要</h2></div></div>
          <p className="scenario-current-summary">{summary.current.summary}</p>
        </div>
        <div className="panel scenario-matrix-profile">
          <div className="comparison-section-heading compact"><div><span>矩阵形状</span><h2>正面区域分布</h2></div></div>
          {(scenarioData.operatingScenarios || []).map((scenario) => <div key={scenario.key}><span>{scenario.label}</span><i><b style={{ width: `${(summary.matrix.rowPositive?.[scenario.key] || 0) * 20}%` }} /></i><strong>{summary.matrix.rowPositive?.[scenario.key] || 0}/5</strong></div>)}
        </div>
      </section>

      <section className="panel comparison-source-report">
        <PanelTitle icon={FileText} title="完整研究报告" />
        <p className="comparison-panel-note">结构化页面用于快速定位；需要核对财务桥、行业证据、事件树和全部来源时可展开原始Markdown。</p>
        {report ? <details className="markdown-details"><summary>展开完整报告</summary><MarkdownView markdown={report.markdown} /></details> : null}
      </section>
    </>
  );
}

function ScenarioCompanyMatrix({ data, cells, selected, onSelect }) {
  const byKey = new Map((cells || []).map((row) => [`${row.operatingScenario}:${row.marketState}`, row]));
  return (
    <div className="scenario-company-matrix" role="grid" aria-label="公司经营情景与市场状态投资建议矩阵">
      <div className="scenario-company-matrix-corner">经营 \ 市场</div>
      {(data.marketStates || []).map((market) => <div key={market.key} className="scenario-company-matrix-header">{market.shortLabel}</div>)}
      {(data.operatingScenarios || []).flatMap((scenario) => [
        <div key={`${scenario.key}-label`} className="scenario-company-matrix-label">{scenario.label}</div>,
        ...(data.marketStates || []).map((market) => {
          const cell = byKey.get(`${scenario.key}:${market.key}`);
          const active = selected.operatingScenario === scenario.key && selected.marketState === market.key;
          return <button key={`${scenario.key}-${market.key}`} className={`scenario-company-cell tone-${cell?.adviceKey || "unavailable"} ${active ? "active" : ""}`} onClick={() => onSelect({ operatingScenario: scenario.key, marketState: market.key })}><strong>{shortAdvice(cell?.adviceKey)}</strong><span>{cell?.returnRangeText || "NA"}</span></button>;
        }),
      ])}
    </div>
  );
}

function AdviceBadge({ adviceKey, large = false }) {
  return <span className={`scenario-advice-badge tone-${adviceKey || "unavailable"} ${large ? "large" : ""}`}>{shortAdvice(adviceKey)}</span>;
}

function shortAdvice(key) {
  return {
    strongNo: "强烈不建议",
    no: "不建议",
    neutral: "中性 / 等待",
    cautious: "谨慎建议",
    yes: "建议投资",
    strongYes: "强烈建议",
  }[key] || "NA";
}

function scenarioHeatClass(value) {
  if (value >= 0.75) return "heat-5";
  if (value >= 0.5) return "heat-4";
  if (value >= 0.3) return "heat-3";
  if (value >= 0.15) return "heat-2";
  if (value > 0) return "heat-1";
  return "heat-0";
}

function formatScenarioPercent(value) {
  const numeric = toNumber(value);
  return numeric === null ? "-" : `${(numeric * 100).toFixed(1)}%`;
}

const TargetIcon = Gauge;

function CompanyComparisons({ data, selectedTicker, setSelectedTicker }) {
  const [query, setQuery] = useState("");
  const [scope, setScope] = useState("top50");
  const [category, setCategory] = useState("all");
  const [archetype, setArchetype] = useState("all");
  const [metric, setMetric] = useState("overall");
  const [sortKey, setSortKey] = useState("activeRank");
  const [sortDirection, setSortDirection] = useState("asc");
  const comparisons = data.companyComparisons || { companies: [], rankings: {}, insights: {}, metrics: {} };
  const selected = selectedTicker ? comparisons.companies.find((item) => item.ticker === selectedTicker) : null;
  const metricOptions = comparisonMetricOptions(comparisons);
  const metricInfo = metricOptions.find((option) => option.value === metric) || metricOptions[0];
  const categories = [...new Set(comparisons.companies.map((row) => row.category).filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));
  const archetypes = [...new Set(comparisons.companies.map((row) => row.archetype).filter(Boolean))].sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));

  if (selected) {
    return (
      <CompanyComparisonDetail
        summary={selected}
        comparisons={comparisons}
        onClose={() => {
          setSelectedTicker(null);
          window.location.hash = "companyComparisons";
        }}
        onSelectTicker={(ticker) => {
          setSelectedTicker(ticker);
          window.location.hash = `companyComparison/${encodeURIComponent(ticker)}`;
        }}
      />
    );
  }

  const ranking = comparisonRankingForMetric(comparisons, metric);
  const rankingByTicker = new Map(ranking.map((row) => [row.ticker, row]));
  const summaryByTicker = new Map(comparisons.companies.map((row) => [row.ticker, row]));
  const leaderboard = ranking.slice(0, 24).map((row) => ({ ...summaryByTicker.get(row.ticker), metricRank: row.rank, metricNet: row.net }));
  const rows = comparisons.companies
    .map((row) => {
      const metricRow = rankingByTicker.get(row.ticker) || {};
      return {
        ...row,
        activeRank: metricRow.rank || 9999,
        metricNet: metricRow.net ?? row.net,
        record: metric === "overall" ? `${row.wins}/${row.losses}/${row.close}` : `${metricRow.wins || 0}/${metricRow.losses || 0}/${metricRow.close || 0}`,
        rankChangeText: formatRankChange(row.rankChange),
        consistentText: `#${row.consistentRank}`,
        highConfidenceText: `#${row.highConfidenceRank}`,
        breadthText: `${row.breadthTop20}/6`,
      };
    })
    .filter((row) => {
      const q = query.trim().toLowerCase();
      const matchesQuery = !q || [row.ticker, row.name, row.category, row.archetype].some((value) => formatValue(value, "").toLowerCase().includes(q));
      const matchesCategory = category === "all" || row.category === category;
      const matchesArchetype = archetype === "all" || row.archetype === archetype;
      const matchesScope =
        scope === "all" ||
        (scope === "top20" && row.activeRank <= 20) ||
        (scope === "top50" && row.activeRank <= 50) ||
        (scope === "rising" && toNumber(row.rankChange) >= 10) ||
        (scope === "conflict" && toNumber(row.reciprocalConflictRate) >= 20);
      return matchesQuery && matchesCategory && matchesArchetype && matchesScope;
    });
  const sortedRows = sortRows(rows, sortKey, sortDirection);
  const columns = [
    { key: "activeRank", label: metricInfo.shortLabel, className: "num" },
    { key: "ticker", label: "Ticker" },
    { key: "name", label: "公司" },
    { key: "category", label: "分类" },
    { key: "archetype", label: "类型" },
    { key: "rankChangeText", label: "较上版", className: "num" },
    { key: "record", label: "胜/负/接近", className: "num" },
    { key: "metricNet", label: "净胜", className: "num" },
    { key: "consistentText", label: "双向一致", className: "num" },
    { key: "highConfidenceText", label: "强胜", className: "num" },
    { key: "breadthText", label: "Top20广度", className: "num" },
  ];
  const reciprocal = comparisons.metrics?.reciprocal || { percentages: {} };
  const version = comparisons.metrics?.version || {};

  return (
    <>
      <PageHeader
        eyebrow={`公司横评 · ${comparisons.reportDateLabel || comparisons.reportDate || "-"} · 价格截止 ${comparisons.priceDate || "-"} · 持有 ${comparisons.holdingPeriod || "8—16个月"}`}
        title="公司横评排名"
        actions={<IconButton label="导出当前视图" icon={Download} onClick={() => downloadCsv("company-comparisons.csv", sortedRows, columns)} />}
      />

      <section className="stat-grid comparison-stat-grid">
        <Stat icon={Building2} label="完整覆盖" value={`${comparisons.companyCount || 0}/192`} note={`${formatNumberForUi(comparisons.rowCount)} 项定向判断`} />
        <Stat icon={BarChart3} label="总体第一" value={comparisons.top20?.[0]?.ticker || "-"} note={`净胜 ${comparisons.top20?.[0]?.net ?? "-"}`} />
        <Stat icon={ShieldCheck} label="双向同胜方" value={formatPercentValue(reciprocal.percentages?.sameWinner)} note={`${formatNumberForUi(reciprocal.sameWinner)} 组公司对`} />
        <Stat icon={ArrowDownUp} label="双方互选对手" value={formatPercentValue(reciprocal.percentages?.eachOther)} note="当前最重要的方法噪声" />
        <Stat icon={LineChart} label="与上一版相关" value={version.rankCorrelation !== null && version.rankCorrelation !== undefined ? Number(version.rankCorrelation).toFixed(3) : "-"} note={`Top20重合 ${version.top20Overlap ?? "-"}/20`} />
      </section>

      <section className="panel comparison-metric-panel">
        <div className="comparison-section-heading">
          <div>
            <span>切换观察口径</span>
            <h2>{metricInfo.label}</h2>
          </div>
          <p>{metricInfo.description}</p>
        </div>
        <div className="comparison-metric-tabs" role="tablist" aria-label="公司横评口径">
          {metricOptions.map((option) => (
            <button
              key={option.value}
              className={metric === option.value ? "active" : ""}
              onClick={() => {
                setMetric(option.value);
                setSortKey("activeRank");
                setSortDirection("asc");
              }}
            >
              {option.label}
            </button>
          ))}
        </div>
      </section>

      <section className="comparison-visual-grid">
        <div className="panel comparison-leaderboard-panel">
          <PanelTitle icon={BarChart3} title={`${metricInfo.label} Top 12`} />
          <ComparisonLeaderboard rows={leaderboard.slice(0, 12)} total={comparisons.companyCount || 192} onSelect={setComparisonTicker(setSelectedTicker)} />
        </div>
        <div className="panel">
          <PanelTitle icon={ArrowDownUp} title="总排名与双向一致排名" />
          <p className="comparison-panel-note">越靠左上越强；远离对角线的公司更依赖单向报告或接近判断。</p>
          <RankAgreementPlot rows={comparisons.companies} total={comparisons.companyCount || 192} onSelect={setComparisonTicker(setSelectedTicker)} />
        </div>
      </section>

      <section className="panel comparison-heatmap-panel">
        <div className="comparison-section-heading compact">
          <div>
            <span>六种独立投资哲学</span>
            <h2>领先公司的六维排名热力图</h2>
          </div>
          <p>数字为维度名次，颜色越深代表越靠前；这里展示当前所选口径的前24名。</p>
        </div>
        <ComparisonHeatmap rows={leaderboard} dimensions={comparisons.dimensions || []} total={comparisons.companyCount || 192} onSelect={setComparisonTicker(setSelectedTicker)} />
      </section>

      <section className="comparison-insight-grid">
        <ComparisonInsightCard title="综合核心" note="总榜、双向一致和强胜均靠前" rows={comparisons.insights?.robustCore || []} onSelect={setComparisonTicker(setSelectedTicker)} />
        <ComparisonInsightCard title="价格与低预期" note="价格赔率或定价错位突出" rows={comparisons.insights?.valueSpecialists || []} onSelect={setComparisonTicker(setSelectedTicker)} />
        <ComparisonInsightCard title="进攻与爆发" note="近端兑现或爆发突破领先" rows={comparisons.insights?.offenseCandidates || []} onSelect={setComparisonTicker(setSelectedTicker)} />
        <ComparisonInsightCard title="本版最大上升" note="与紧邻上一版相比" rows={comparisons.insights?.biggestRisers || []} onSelect={setComparisonTicker(setSelectedTicker)} showChange />
      </section>

      <FilterBar>
        <SearchBox value={query} onChange={setQuery} placeholder="搜索 ticker、公司、分类或类型" />
        <SelectBox
          label="范围"
          value={scope}
          onChange={setScope}
          options={[
            { value: "top20", label: "当前口径 Top 20" },
            { value: "top50", label: "当前口径 Top 50" },
            { value: "rising", label: "较上版上升10名+" },
            { value: "conflict", label: "双向冲突20%+" },
            { value: "all", label: "全部192家公司" },
          ]}
        />
        <SelectBox label="分类" value={category} onChange={setCategory} options={[{ value: "all", label: "全部分类" }, ...categories.map((value) => ({ value, label: value }))]} />
        <SelectBox label="类型" value={archetype} onChange={setArchetype} options={[{ value: "all", label: "全部类型" }, ...archetypes.map((value) => ({ value, label: value }))]} />
        <div className="data-note">显示 {sortedRows.length} 家</div>
      </FilterBar>

      <div className="panel table-panel comparison-ranking-table">
        <SortableTable
          rows={sortedRows}
          columns={columns}
          sortKey={sortKey}
          sortDirection={sortDirection}
          onSort={(key) => {
            setSortDirection(sortKey === key && sortDirection === "asc" ? "desc" : "asc");
            setSortKey(key);
          }}
          onRowClick={(row) => {
            setSelectedTicker(row.ticker);
            window.location.hash = `companyComparison/${encodeURIComponent(row.ticker)}`;
          }}
        />
      </div>

      <div className="comparison-quality-note">
        <ShieldCheck size={16} />
        <span>
          构建校验：192份报告、每份191个对手、36,672项定向判断、18,336组公司对。
          {comparisons.quality?.parseWarningCount ? ` 另有 ${comparisons.quality.parseWarningCount} 个非关键字段代码告警。` : " 未发现解析告警。"}
        </span>
      </div>
    </>
  );
}

function CompanyComparisonDetail({ summary, comparisons, onClose, onSelectTicker }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pairQuery, setPairQuery] = useState("");
  const [pairScope, setPairScope] = useState("all");

  useEffect(() => {
    let active = true;
    setReport(null);
    if (!summary?.dataFile) return undefined;
    setLoading(true);
    fetch(`${DATA_BASE}/${summary.dataFile}`, { cache: "no-store" })
      .then((response) => (response.ok ? response.json() : null))
      .then((json) => {
        if (active) setReport(json);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [summary?.ticker, summary?.dataFile]);

  const dimensions = (comparisons.dimensions || []).map((dimension) => summary.dimensionStats?.[dimension.key]).filter(Boolean);
  const pairs = report?.pairs || [];
  const filteredPairs = pairs.filter((pair) => {
    const q = pairQuery.trim().toLowerCase();
    const matchesQuery = !q || [pair.opponentTicker, pair.opponentName, pair.opponentCategory, pair.reason].some((value) => formatValue(value, "").toLowerCase().includes(q));
    const status = pair.reciprocal?.status;
    const matchesScope =
      pairScope === "all" ||
      (pairScope === "conflict" && ["eachOther", "eachSelf"].includes(status)) ||
      (pairScope === "consistent" && status === "sameWinner") ||
      (pairScope === "win" && pair.overall?.winner === summary.ticker) ||
      (pairScope === "loss" && pair.overall?.status === "winner" && pair.overall?.winner !== summary.ticker) ||
      (pairScope === "close" && pair.overall?.status === "close");
    return matchesQuery && matchesScope;
  });
  const robustWins = pairs.filter((pair) => pair.reciprocal?.status === "sameWinner" && pair.overall?.winner === summary.ticker).slice(0, 10);
  const robustLosses = pairs.filter((pair) => pair.reciprocal?.status === "sameWinner" && pair.overall?.winner === pair.opponentTicker).slice(0, 10);
  const conflicts = pairs.filter((pair) => ["eachOther", "eachSelf"].includes(pair.reciprocal?.status)).slice(0, 10);

  return (
    <>
      <PageHeader
        eyebrow={`公司横评详情 · ${summary.reportDate || comparisons.reportDate || "-"}`}
        title={`${summary.ticker} · ${summary.name}`}
        actions={(
          <>
            <TextButton onClick={onClose}>返回全部公司</TextButton>
            <TextButton onClick={() => { window.location.hash = `company/${encodeURIComponent(summary.ticker)}`; }}>打开公司主页</TextButton>
          </>
        )}
      />
      <section className="comparison-company-hero panel">
        <div>
          <span className="comparison-company-type">{summary.archetype}</span>
          <h2>总体风险调整 #{summary.finalRank}</h2>
          <p>{summary.category}</p>
        </div>
        <div className="comparison-company-summary">
          {(summary.onePage || []).map((item, index) => <p key={`${summary.ticker}-summary-${index}`}>{item}</p>)}
        </div>
      </section>
      <section className="stat-grid comparison-detail-stats">
        <Stat icon={BarChart3} label="总体排名" value={`#${summary.finalRank}`} note={summary.previousRank ? `上一版 #${summary.previousRank} · ${formatRankChange(summary.rankChange)}` : "无上一版"} />
        <Stat icon={ShieldCheck} label="双向一致" value={`#${summary.consistentRank}`} note={`${summary.consistentWins}/${summary.consistentLosses} 一致胜负`} />
        <Stat icon={Gauge} label="六维强胜" value={`#${summary.highConfidenceRank}`} note={`净分 ${summary.highConfidenceNet}`} />
        <Stat icon={ArrowDownUp} label="总记录" value={`${summary.wins}/${summary.losses}/${summary.close}`} note="胜 / 负 / 接近" />
        <Stat icon={Table2} label="双向冲突" value={`${summary.reciprocal?.eachOther || 0}`} note={`冲突率 ${summary.reciprocalConflictRate}%`} />
      </section>

      <section className="comparison-detail-grid">
        <div className="panel">
          <PanelTitle icon={Gauge} title="六维投资画像" />
          <div className="dimension-profile-list">
            {dimensions.map((row) => (
              <div className="dimension-profile-row" key={row.key}>
                <div><strong>{row.label}</strong><span>#{row.rank}/192</span></div>
                <div className="dimension-profile-track"><span style={{ width: `${Math.max(3, 100 - ((row.rank - 1) / 191) * 100)}%` }} /></div>
                <div className="dimension-profile-values"><span>净胜 {row.net}</span><span>{row.wins}/{row.losses}/{row.close}</span></div>
              </div>
            ))}
          </div>
        </div>
        <div className="panel">
          <PanelTitle icon={ArrowDownUp} title="双向判断结构" />
          <ReciprocalBreakdown reciprocal={summary.reciprocal || {}} total={191} />
          <p className="comparison-panel-note">“双方互选对手”表示两份方向报告都选择了报告中的另一家公司，是当前最需要谨慎解释的结果。</p>
        </div>
      </section>

      <section className="comparison-pair-highlights">
        <PairHighlight title="双向一致胜出" rows={robustWins} empty="没有双向一致胜出记录" onSelect={onSelectTicker} />
        <PairHighlight title="双向一致落败" rows={robustLosses} empty="没有双向一致落败记录" onSelect={onSelectTicker} />
        <PairHighlight title="值得复核的冲突" rows={conflicts} empty="没有互相矛盾的方向报告" onSelect={onSelectTicker} />
      </section>

      <section className="panel comparison-pair-browser">
        <div className="comparison-section-heading compact">
          <div><span>191个对手逐项浏览</span><h2>公司对比较明细</h2></div>
          <p>同时显示本报告结论和反向报告结论，便于判断共识、接近与冲突。</p>
        </div>
        <FilterBar>
          <SearchBox value={pairQuery} onChange={setPairQuery} placeholder="搜索对手、分类或理由" />
          <SelectBox
            label="状态"
            value={pairScope}
            onChange={setPairScope}
            options={[
              { value: "all", label: "全部" },
              { value: "consistent", label: "双向一致" },
              { value: "conflict", label: "双向冲突" },
              { value: "win", label: "自身报告胜出" },
              { value: "loss", label: "自身报告落败" },
              { value: "close", label: "自身报告接近" },
            ]}
          />
          <div className="data-note">显示 {filteredPairs.length}/{pairs.length || 191}</div>
        </FilterBar>
        {loading ? <p className="muted">正在加载公司横评明细...</p> : null}
        {report ? <ComparisonPairTable rows={filteredPairs} onSelect={onSelectTicker} /> : !loading ? <p className="muted">没有可用的公司横评明细。</p> : null}
      </section>

      <section className="panel comparison-source-report">
        <PanelTitle icon={FileText} title="完整研究报告" />
        <p className="comparison-panel-note">结构化页面用于浏览；需要逐条核对证据时可展开原始Markdown。</p>
        {report ? (
          <details className="markdown-details">
            <summary>展开完整报告</summary>
            <MarkdownView markdown={report.markdown} />
          </details>
        ) : null}
      </section>
    </>
  );
}

function comparisonMetricOptions(comparisons) {
  const base = [
    { value: "overall", label: "总体风险调整", shortLabel: "总榜", description: "同一笔资本持有8—16个月的最终选择，不由六列多数票生成。" },
    { value: "consistent", label: "双向一致", shortLabel: "一致榜", description: "只统计两份方向报告选择同一胜方的公司对，降低叙事位置偏差。" },
    { value: "highConfidence", label: "六维明显强胜", shortLabel: "强胜榜", description: "汇总六个维度中“明显更优且高置信”的净胜，观察证据强度与广度。" },
  ];
  return [
    ...base,
    ...(comparisons.dimensions || []).map((dimension) => ({
      value: dimension.key,
      label: dimension.label,
      shortLabel: dimension.label,
      description: comparisonDimensionDescription(dimension.key),
    })),
  ];
}

function comparisonDimensionDescription(key) {
  return {
    near: "比较未来几个季度收入、利润与现金流的可验证兑现链。",
    long: "比较3—5年每股价值复合、护城河与再投资空间。",
    odds: "只从当前价格出发比较前瞻收益分布和安全边际。",
    defense: "比较失败情景中的永久损失、融资生存与恢复能力。",
    explosion: "寻找紧急瓶颈、技术落地和利润非线性，同时要求股东价值捕获。",
    mispricing: "比较新增基本面证据、市场隐含预期与价格反应之间的偏差。",
  }[key] || "独立完成一次完整投资选择。";
}

function comparisonRankingForMetric(comparisons, metric) {
  if (metric === "overall") return comparisons.rankings?.overall || comparisons.finalRanking || [];
  if (metric === "consistent") return comparisons.rankings?.consistent || [];
  if (metric === "highConfidence") return comparisons.rankings?.highConfidence || [];
  return comparisons.rankings?.dimensions?.[metric] || [];
}

function setComparisonTicker(setSelectedTicker) {
  return (ticker) => {
    setSelectedTicker(ticker);
    window.location.hash = `companyComparison/${encodeURIComponent(ticker)}`;
  };
}

function ComparisonLeaderboard({ rows, total, onSelect }) {
  return (
    <div className="comparison-leaderboard">
      {rows.map((row) => (
        <button key={row.ticker} onClick={() => onSelect(row.ticker)}>
          <span className="comparison-rank-number">{row.metricRank}</span>
          <span className="comparison-leader-name"><strong>{row.ticker}</strong><em>{row.name}</em></span>
          <span className="comparison-leader-bar"><i style={{ width: `${Math.max(5, 100 - ((row.metricRank - 1) / Math.max(1, total - 1)) * 100)}%` }} /></span>
          <span className="comparison-leader-score">{row.metricNet > 0 ? "+" : ""}{row.metricNet}</span>
        </button>
      ))}
    </div>
  );
}

function RankAgreementPlot({ rows, total, onSelect }) {
  const points = rows;
  return (
    <div className="rank-agreement-wrap">
      <div className="rank-agreement-y">双向一致排名 →</div>
      <div className="rank-agreement-plot">
        <span className="rank-diagonal" />
        {points.map((row) => (
          <button
            key={row.ticker}
            className={`rank-dot archetype-${comparisonClassName(row.archetype)}`}
            style={{ left: `${((row.finalRank - 1) / Math.max(1, total - 1)) * 100}%`, top: `${((row.consistentRank - 1) / Math.max(1, total - 1)) * 100}%` }}
            title={`${row.ticker} 总榜#${row.finalRank} / 双向一致#${row.consistentRank}`}
            aria-label={`${row.ticker} 总榜第${row.finalRank}，双向一致第${row.consistentRank}`}
            onClick={() => onSelect(row.ticker)}
          >
            {row.finalRank <= 12 ? row.ticker : ""}
          </button>
        ))}
      </div>
      <div className="rank-agreement-x">总体风险调整排名 →</div>
    </div>
  );
}

function ComparisonHeatmap({ rows, dimensions, total, onSelect }) {
  return (
    <div className="comparison-heatmap-scroll">
      <div className="comparison-heatmap" style={{ "--dimension-count": dimensions.length }}>
        <div className="comparison-heatmap-header"><span>公司</span>{dimensions.map((dimension) => <strong key={dimension.key}>{dimension.label}</strong>)}</div>
        {rows.map((row) => (
          <button className="comparison-heatmap-row" key={row.ticker} onClick={() => onSelect(row.ticker)}>
            <span><strong>{row.ticker}</strong><em>总#{row.finalRank}</em></span>
            {dimensions.map((dimension) => {
              const rank = row.dimensionStats?.[dimension.key]?.rank || total;
              return <i key={dimension.key} style={{ background: comparisonHeatColor(rank, total) }} title={`${dimension.label} #${rank}`}>#{rank}</i>;
            })}
          </button>
        ))}
      </div>
    </div>
  );
}

function ComparisonInsightCard({ title, note, rows, onSelect, showChange }) {
  return (
    <div className="panel comparison-insight-card">
      <div><strong>{title}</strong><span>{note}</span></div>
      <ol>
        {rows.slice(0, 8).map((row) => (
          <li key={`${title}-${row.ticker}`}><button onClick={() => onSelect(row.ticker)}><span>{row.ticker}</span><em>{showChange ? formatRankChange(row.rankChange) : `#${row.rank}`}</em></button></li>
        ))}
      </ol>
    </div>
  );
}

function ReciprocalBreakdown({ reciprocal, total }) {
  const items = [
    ["sameWinner", "双向同胜方"],
    ["eachOther", "双方互选对手"],
    ["eachSelf", "双方各选自己"],
    ["oneDecisiveOneClose", "一方明确、一方接近"],
    ["bothClose", "双方均接近"],
    ["unavailable", "资料不足"],
  ];
  return <div className="reciprocal-breakdown">{items.map(([key, label]) => { const value = reciprocal[key] || 0; return <div key={key}><span>{label}<strong>{value}</strong></span><i><b style={{ width: `${(value / Math.max(1, total)) * 100}%` }} /></i></div>; })}</div>;
}

function PairHighlight({ title, rows, empty, onSelect }) {
  return (
    <div className="panel pair-highlight">
      <strong>{title}</strong>
      {rows.length ? <div>{rows.map((row) => <button key={row.opponentTicker} onClick={() => onSelect(row.opponentTicker)}><span>{row.opponentTicker}</span><em>{reciprocalStatusLabel(row.reciprocal?.status)}</em></button>)}</div> : <p className="muted">{empty}</p>}
    </div>
  );
}

function ComparisonPairTable({ rows, onSelect }) {
  return (
    <div className="table-scroll">
      <table className="data-table comparison-pair-table">
        <thead><tr><th>对手</th><th>关系</th><th>本报告结论</th><th>反向报告结论</th><th>双向状态</th><th>决定性理由</th></tr></thead>
        <tbody>{rows.map((row) => <tr key={row.opponentTicker}><td><button className="ticker-link" onClick={() => onSelect(row.opponentTicker)}>{row.opponentTicker}</button><span>{row.opponentName}</span></td><td>{row.relation}</td><td>{row.overall?.text || "-"}</td><td>{row.reciprocal?.reverseOverall?.text || "-"}</td><td><span className={`reciprocal-badge status-${row.reciprocal?.status || "unavailable"}`}>{reciprocalStatusLabel(row.reciprocal?.status)}</span></td><td>{row.reason}</td></tr>)}</tbody>
      </table>
    </div>
  );
}

function reciprocalStatusLabel(status) {
  return {
    sameWinner: "同一胜方",
    eachOther: "互选对手",
    eachSelf: "各选自己",
    oneDecisiveOneClose: "明确/接近",
    bothClose: "均接近",
    unavailable: "资料不足",
  }[status] || "资料不足";
}

function formatRankChange(value) {
  const number = toNumber(value);
  if (number === null) return "-";
  if (number > 0) return `↑${number}`;
  if (number < 0) return `↓${Math.abs(number)}`;
  return "—";
}

function formatPercentValue(value) {
  const number = toNumber(value);
  return number === null ? "-" : `${number.toFixed(1)}%`;
}

function formatNumberForUi(value) {
  const number = toNumber(value);
  return number === null ? "-" : number.toLocaleString("en-US");
}

function comparisonHeatColor(rank, total) {
  const strength = 1 - (Math.max(1, rank) - 1) / Math.max(1, total - 1);
  return `rgba(47, 111, 115, ${0.08 + strength * 0.78})`;
}

function comparisonClassName(value) {
  return formatValue(value, "other").replace(/[^\w\u4e00-\u9fa5-]/g, "-");
}

function LegacyCompanyComparisons({ data, selectedTicker, setSelectedTicker }) {
  const [query, setQuery] = useState("");
  const [scope, setScope] = useState("top20");
  const [sortKey, setSortKey] = useState("finalRank");
  const [sortDirection, setSortDirection] = useState("asc");
  const comparisons = data.companyComparisons || { companies: [], top20: [], reports: {} };
  const selected = selectedTicker ? comparisons.companies.find((item) => item.ticker === selectedTicker) : null;

  const rows = useMemo(() => {
    const filtered = comparisons.companies.filter((row) => {
      const q = query.trim().toLowerCase();
      const matchesQuery =
        !q || [row.ticker, row.name, row.category].some((value) => formatValue(value, "").toLowerCase().includes(q));
      const matchesScope =
        scope === "all" ||
        (scope === "top20" && toNumber(row.finalRank) <= 20) ||
        (scope === "top80" && toNumber(row.finalRank) <= 80) ||
        (scope === "positive" && toNumber(row.finalNet) > 0) ||
        (scope === "negative" && toNumber(row.finalNet) < 0);
      return matchesQuery && matchesScope;
    });
    return sortRows(
      filtered.map((row) => ({
        ...row,
        strongestText: row.strongestStyles?.map((item) => item.thought).join(", "),
        weakestText: row.weakestStyles?.map((item) => item.thought).join(", "),
      })),
      sortKey,
      sortDirection,
    );
  }, [comparisons.companies, query, scope, sortKey, sortDirection]);

  const columns = [
    { key: "finalRank", label: "Rank", className: "num" },
    { key: "ticker", label: "Ticker" },
    { key: "name", label: "公司" },
    { key: "category", label: "分类" },
    { key: "finalWins", label: "胜出", className: "num" },
    { key: "finalLosses", label: "落败", className: "num" },
    { key: "finalNet", label: "净胜", className: "num" },
    { key: "selfWins", label: "自身胜", className: "num" },
    { key: "selfLosses", label: "自身负", className: "num" },
    { key: "strongestText", label: "强项" },
    { key: "weakestText", label: "弱项" },
  ];

  return (
    <>
      <PageHeader
        eyebrow={`公司对比 · ${comparisons.reportDateLabel || comparisons.reportDate || "-"} · ${comparisons.qualityNote || ""}`}
        title="公司对比信号"
        actions={<IconButton label="导出当前对比" icon={Download} onClick={() => downloadCsv("company-comparisons.csv", rows, columns)} />}
      />
      <section className="stat-grid">
        <Stat icon={Building2} label="覆盖公司" value={comparisons.companyCount || 0} note={`缺失 ${comparisons.missing?.length || 0}`} />
        <Stat icon={Table2} label="对比行" value={comparisons.rowCount || 0} note="A-centric directed rows" />
        <Stat icon={BarChart3} label="Top 1" value={comparisons.top20?.[0]?.ticker || "-"} note={`净胜 ${comparisons.top20?.[0]?.net ?? "-"}`} />
        <Stat icon={FileText} label="综合报告" value={comparisons.reports?.summary?.reportDate || "-"} note="本地 Markdown 已发布" />
      </section>

      <section className="comparison-option-grid">
        <div className="panel comparison-option">
          <strong>方案一：聚合榜单</strong>
          <p>把 189 份结果汇总为最终胜出排名、Top 20 和多目标候选池。当前页面主表已经采用这个方案，适合快速看全局。</p>
        </div>
        <div className="panel comparison-option">
          <strong>方案二：公司详情摘要</strong>
          <p>在公司详情中加入该公司的对比排名、自身胜负、强弱投资思路和完整对比入口。当前公司详情页已经接入。</p>
        </div>
        <div className="panel comparison-option">
          <strong>方案三：完整 pairwise 浏览器</strong>
          <p>把 35,532 行逐对比较做成可筛选矩阵。数据已按公司报告发布，当前先按需加载；若需要矩阵页，可在此基础上扩展。</p>
        </div>
      </section>

      <FilterBar>
        <SearchBox value={query} onChange={setQuery} placeholder="搜索 ticker、公司、分类" />
        <SelectBox
          label="范围"
          value={scope}
          onChange={(value) => {
            setScope(value);
            setSortKey("finalRank");
            setSortDirection("asc");
          }}
          options={[
            { value: "top20", label: "Top 20" },
            { value: "top80", label: "Top 80" },
            { value: "positive", label: "净胜为正" },
            { value: "negative", label: "净胜为负" },
            { value: "all", label: "全部公司" },
          ]}
        />
        <div className="data-note">来源：{comparisons.resultRoot || "-"}</div>
      </FilterBar>

      <div className={selected ? "split-view" : ""}>
        <div className="panel table-panel">
          <SortableTable
            rows={rows}
            columns={columns}
            sortKey={sortKey}
            sortDirection={sortDirection}
            onSort={(key) => {
              setSortDirection(sortKey === key && sortDirection === "asc" ? "desc" : "asc");
              setSortKey(key);
            }}
            onRowClick={(row) => {
              setSelectedTicker(row.ticker);
              window.location.hash = `companyComparison/${encodeURIComponent(row.ticker)}`;
            }}
          />
        </div>
        {selected ? (
          <LegacyCompanyComparisonDetail
            summary={selected}
            onClose={() => {
              setSelectedTicker(null);
              window.location.hash = "companyComparisons";
            }}
          />
        ) : null}
      </div>
    </>
  );
}

function LegacyCompanyComparisonDetail({ summary, onClose }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;
    setReport(null);
    if (!summary?.dataFile) return;
    setLoading(true);
    fetch(`${DATA_BASE}/${summary.dataFile}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((json) => {
        if (active) setReport(json);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [summary?.ticker, summary?.dataFile]);

  return (
    <aside className="detail-panel">
      <button className="close-button" onClick={onClose} aria-label="关闭公司对比详情">
        <X size={18} />
      </button>
      <div className="detail-heading">
        <span>{summary.ticker}</span>
        <h2>{summary.name}</h2>
        <p>{summary.category}</p>
      </div>
      <div className="mini-grid">
        <Mini label="总榜Rank" value={summary.finalRank ? `#${summary.finalRank}` : ""} />
        <Mini label="总榜净胜" value={summary.finalNet} />
        <Mini label="总榜胜负" value={`${summary.finalWins}/${summary.finalLosses}`} />
        <Mini label="自身胜负" value={`${summary.selfWins}/${summary.selfLosses}`} />
        <Mini label="覆盖对手" value={summary.comparedCount} />
        <Mini label="报告日期" value={summary.reportDate} />
      </div>
      <SectionBlock title="一页结论">
        <ul className="compact-list">
          {(summary.onePage || []).slice(0, 6).map((item, index) => (
            <li key={`${summary.ticker}-one-${index}`}>{item}</li>
          ))}
        </ul>
      </SectionBlock>
      <SectionBlock title="投资思路强弱">
        <DenseTable
          rows={summary.styleStats || []}
          columns={[
            { key: "thought", label: "思路" },
            { key: "score", label: "净分", className: "num" },
            { key: "a", label: "A", className: "num" },
            { key: "b", label: "B", className: "num" },
            { key: "neutral", label: "中性", className: "num" },
          ]}
        />
      </SectionBlock>
      <SectionBlock title="可比关系胜负">
        <DenseTable
          rows={summary.relationStats || []}
          columns={[
            { key: "relation", label: "关系" },
            { key: "wins", label: "胜", className: "num" },
            { key: "losses", label: "负", className: "num" },
            { key: "total", label: "总数", className: "num" },
          ]}
        />
      </SectionBlock>
      <SectionBlock title="直接同业">
        <DenseTable
          rows={summary.directPeers || []}
          columns={[
            { key: "ticker", label: "Ticker" },
            { key: "final", label: "最终" },
            { key: "majority", label: "多数方向" },
            { key: "reason", label: "理由" },
          ]}
        />
      </SectionBlock>
      <SectionBlock title="主要落败对象">
        {(summary.losses || []).length ? (
          <DenseTable
            rows={summary.losses || []}
            columns={[
              { key: "ticker", label: "Ticker" },
              { key: "relation", label: "关系" },
              { key: "majority", label: "多数方向" },
              { key: "reason", label: "理由" },
            ]}
          />
        ) : (
          <p className="muted">自身报告中没有解析到落败对象。</p>
        )}
      </SectionBlock>
      <SectionBlock title="源文件">
        <LabeledPath label="公司对比" value={summary.sourcePath} />
      </SectionBlock>
      <SectionBlock title="完整对比报告">
        {loading ? <p className="muted">正在加载公司对比报告...</p> : null}
        {report ? (
          <details className="markdown-details">
            <summary>展开完整 Markdown</summary>
            <MarkdownView markdown={report.markdown} />
          </details>
        ) : !loading ? (
          <p className="muted">没有可渲染公司对比报告。</p>
        ) : null}
      </SectionBlock>
    </aside>
  );
}

const technicalReadinessLabels = {
  core: "核心证据",
  exploratory: "探索性",
  blocked: "数据受阻",
};

function technicalRangeStyle(low, high) {
  const min = -20;
  const max = 20;
  const clampedLow = Math.max(min, Math.min(max, low));
  const clampedHigh = Math.max(min, Math.min(max, high));
  return {
    left: `${((clampedLow - min) / (max - min)) * 100}%`,
    width: `${((clampedHigh - clampedLow) / (max - min)) * 100}%`,
  };
}

function TechnicalResearch({ data, selectedFactorId, setSelectedFactorId }) {
  const payload = data.technicalResearch;
  const [query, setQuery] = useState("");
  const [familyId, setFamilyId] = useState("all");
  const [readiness, setReadiness] = useState("all");
  const familyById = useMemo(() => Object.fromEntries(payload.families.map((family) => [family.id, family])), [payload.families]);
  const filteredFactors = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return payload.factors.filter((factor) => {
      const matchesQuery =
        !normalized ||
        [factor.id, factor.name, factor.signal, factor.headline, factor.currentState]
          .join(" ")
          .toLowerCase()
          .includes(normalized);
      return matchesQuery && (familyId === "all" || factor.familyId === familyId) && (readiness === "all" || factor.readiness === readiness);
    });
  }, [payload.factors, query, familyId, readiness]);
  const selectedFactor = payload.factors.find((factor) => factor.id === selectedFactorId) || null;

  const openFactor = (factorId) => {
    setSelectedFactorId(factorId);
    window.location.hash = `technicalResearch/${encodeURIComponent(factorId)}`;
  };
  const closeFactor = () => {
    setSelectedFactorId(null);
    window.location.hash = "technicalResearch";
  };

  return (
    <>
      <PageHeader
        eyebrow={`技术面研究 · 截止 ${payload.asOf}`}
        title="大盘状态、风险与独立因子证据"
        actions={<div className="data-note">{payload.factorCount} 因子 · {payload.marketCount} 市场 · {payload.horizonCount} 窗口</div>}
      />

      <section className="technical-hero">
        <div className="technical-hero-copy">
          <span className="technical-kicker">研究审计总览 · 非组合模型</span>
          <h2>{payload.summary.headline}</h2>
          <p>{payload.summary.lede}</p>
          <small>{payload.summary.boundary}</small>
        </div>
        <div className="technical-verdict-grid">
          {payload.summary.verdicts.map((verdict) => (
            <div key={verdict.label} className={`technical-verdict tone-${verdict.tone}`}>
              <span>{verdict.label}</span>
              <strong>{verdict.value}</strong>
              <p>{verdict.note}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel technical-outlook-panel">
        <PanelTitle icon={Table2} title="五市场 × 五窗口：独立因子结果的去重对照" />
        <p className="technical-section-note">颜色表示证据方向与可用性，不代表仓位建议；半年和一年窗口明确保留为“证据不足”。</p>
        <div className="technical-outlook-scroll">
          <table className="technical-outlook-table">
            <thead>
              <tr>
                <th>市场</th>
                {payload.scope.horizons.map((horizon) => <th key={horizon}>{horizon} 日</th>)}
                <th>关键解释</th>
              </tr>
            </thead>
            <tbody>
              {payload.marketOutlook.map((row) => (
                <tr key={row.market}>
                  <th>{row.market}</th>
                  {row.cells.map((cell) => (
                    <td key={`${row.market}-${cell.horizon}`}>
                      <span className={`technical-outlook-cell tone-${cell.tone}`}>{cell.label}</span>
                    </td>
                  ))}
                  <td className="technical-outlook-note">{row.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="technical-dashboard-grid">
        <div className="panel technical-risk-panel">
          <PanelTitle icon={Activity} title="10 日风险区间" />
          <p className="technical-section-note">MF002 的 80% 条件区间；波动率均为年化。区间可靠性高于方向判断。</p>
          <div className="technical-risk-axis"><span>-20%</span><span>0</span><span>+20%</span></div>
          <div className="technical-risk-list">
            {payload.riskForecasts.map((item) => (
              <div key={item.market} className="technical-risk-row">
                <div className="technical-risk-label">
                  <strong>{item.market}</strong>
                  <span>RV {item.realizedVol21.toFixed(1)}% · 预测 {item.forecastVol10.toFixed(1)}%</span>
                </div>
                <div className="technical-risk-track" aria-label={`${item.market} 80%区间 ${item.low}% 到 ${item.high}%`}>
                  <i className="technical-risk-zero" />
                  <b style={technicalRangeStyle(item.low, item.high)} />
                </div>
                <span className="technical-risk-value">{item.low.toFixed(1)}% ～ +{item.high.toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel technical-signal-panel">
          <PanelTitle icon={Gauge} title="当前状态仪表" />
          <p className="technical-section-note">每张卡片标明当前读数、含义和对应研究；点击可直接进入完整报告。</p>
          <div className="technical-signal-grid">
            {payload.currentSignals.map((signal) => (
              <button key={signal.label} className={`technical-signal-card tone-${signal.tone}`} onClick={() => openFactor(signal.factorIds[0])}>
                <span>{signal.label}</span>
                <strong>{signal.value}</strong>
                <p>{signal.stance}</p>
                <small>{signal.factorIds.join(" · ")}</small>
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="panel">
        <PanelTitle icon={Layers} title="六个信息家族：避免把相关因子当成独立投票" />
        <div className="technical-family-grid">
          {payload.families.map((family) => (
            <div key={family.id} className="technical-family-card">
              <div>
                <span>{family.factorIds.length} 个因子</span>
                <h3>{family.name}</h3>
              </div>
              <p>{family.description}</p>
              <div className="technical-family-factors">
                {family.factorIds.map((factorId) => (
                  <button key={factorId} onClick={() => openFactor(factorId)}>{factorId}</button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="technical-explorer">
        <div className="technical-explorer-heading">
          <div>
            <span className="eyebrow">逐因子深读</span>
            <h2>18 份完整研究结果</h2>
          </div>
          <p>先看当前状态、适用角色与局限；打开详情后可阅读全文和原始表格。</p>
        </div>
        <FilterBar>
          <SearchBox value={query} onChange={setQuery} placeholder="搜索编号、因子、结论或当前状态" />
          <SelectBox
            label="信息家族"
            value={familyId}
            onChange={setFamilyId}
            options={[{ value: "all", label: "全部家族" }, ...payload.families.map((family) => ({ value: family.id, label: family.name }))]}
          />
          <SelectBox
            label="研究成熟度"
            value={readiness}
            onChange={setReadiness}
            options={[
              { value: "all", label: "全部" },
              { value: "core", label: technicalReadinessLabels.core },
              { value: "exploratory", label: technicalReadinessLabels.exploratory },
              { value: "blocked", label: technicalReadinessLabels.blocked },
            ]}
          />
          <div className="data-note">显示 {filteredFactors.length} / {payload.factorCount}</div>
        </FilterBar>

        <div className="technical-factor-grid">
          {filteredFactors.map((factor) => (
            <button key={factor.id} className="technical-factor-card" onClick={() => openFactor(factor.id)}>
              <div className="technical-factor-meta">
                <span className="technical-factor-id">{factor.id}</span>
                <span className={`technical-readiness readiness-${factor.readiness}`}>{technicalReadinessLabels[factor.readiness]}</span>
              </div>
              <h3>{factor.name}</h3>
              <strong>{factor.signal}</strong>
              <p>{factor.headline}</p>
              <div className="technical-mini-outlook">
                {payload.scope.horizons.map((horizon) => {
                  const outlook = factor.outlook[String(horizon)];
                  return <span key={horizon} className={`tone-${outlook.tone}`} title={`${horizon}日：${outlook.text}`}>{horizon}D</span>;
                })}
              </div>
              <span className="technical-open-report"><FileText size={15} /> 查看完整研究</span>
            </button>
          ))}
        </div>
        {!filteredFactors.length ? <div className="empty-state">没有符合当前筛选条件的因子。</div> : null}
      </section>

      {selectedFactor ? (
        <TechnicalFactorDetail
          factor={selectedFactor}
          family={familyById[selectedFactor.familyId]}
          horizons={payload.scope.horizons}
          onClose={closeFactor}
        />
      ) : null}
    </>
  );
}

function TechnicalFactorDetail({ factor, family, horizons, onClose }) {
  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    const handleKeyDown = (event) => {
      if (event.key === "Escape") onClose();
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [onClose]);

  return (
    <div className="technical-modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="technical-modal" role="dialog" aria-modal="true" aria-labelledby={`technical-title-${factor.id}`}>
        <div className="technical-modal-topbar">
          <div>
            <span className="technical-factor-id">{factor.id}</span>
            <span className={`technical-readiness readiness-${factor.readiness}`}>{technicalReadinessLabels[factor.readiness]}</span>
          </div>
          <button className="close-button" onClick={onClose} aria-label="关闭因子详情"><X size={18} /></button>
        </div>
        <div className="technical-modal-heading">
          <span>{family?.name || factor.familyId} · 报告日期 {factor.reportDate}</span>
          <h2 id={`technical-title-${factor.id}`}>{factor.name}</h2>
          <p>{factor.headline}</p>
        </div>

        <div className="technical-detail-grid">
          <div><span>当前状态</span><p>{factor.currentState}</p></div>
          <div><span>最适用途</span><p>{factor.useCase}</p></div>
          <div><span>核心局限</span><p>{factor.limitation}</p></div>
        </div>

        <div className="technical-window-grid">
          {horizons.map((horizon) => {
            const outlook = factor.outlook[String(horizon)];
            return (
              <div key={horizon} className={`technical-window-card tone-${outlook.tone}`}>
                <span>{horizon} 日</span>
                <strong>{outlook.text}</strong>
              </div>
            );
          })}
        </div>

        <div className="technical-report-heading">
          <div>
            <span className="eyebrow">完整原始结果</span>
            <h3>{factor.reportTitle}</h3>
          </div>
          <code>{factor.sourceFile}</code>
        </div>
        <div className="technical-report-body">
          <MarkdownView markdown={factor.markdown} />
        </div>
      </section>
    </div>
  );
}

function Features({ data, rankingByTicker }) {
  const initialFeatureId = data.features.featureGroups?.alpha?.[0] || data.features.features[0]?.id || "";
  const [scope, setScope] = useState("alpha");
  const [featureId, setFeatureId] = useState(initialFeatureId);
  const [query, setQuery] = useState("");
  const featureById = Object.fromEntries(data.features.features.map((feature) => [feature.id, feature]));
  const scopedIds = data.features.featureGroups?.[scope] || [];
  const featureOptions = scopedIds.map((id) => featureById[id]).filter(Boolean);
  const feature = featureById[featureId] || featureOptions[0];

  useEffect(() => {
    if (!featureOptions.some((item) => item.id === featureId)) {
      setFeatureId(featureOptions[0]?.id || "");
    }
  }, [scope, featureId, featureOptions]);

  const rows = (data.features.byFeature[feature?.id] || [])
    .filter((row) => {
      const q = query.trim().toLowerCase();
      return !q || [row.ticker, row.companyName, row.category].some((value) => formatValue(value, "").toLowerCase().includes(q));
    })
    .map((row) => ({ ...row, rankOverall: rankingByTicker[row.ticker]?.rank || "" }))
    .sort((a, b) => Number(a.rank) - Number(b.rank));

  const top = rows.filter((r) => r.score !== null).sort((a, b) => Number(b.score) - Number(a.score)).slice(0, 15);
  const bottom = rows.filter((r) => r.score !== null).sort((a, b) => Number(a.score) - Number(b.score)).slice(0, 15);
  const heatmapRows = rows.slice(0, 80);
  return (
    <>
      <PageHeader eyebrow="特征量化" title="收益型特征与门槛层" />
      <section className="stat-grid">
        <Stat icon={LineChart} label="收益型特征" value={data.features.alphaFeatureIds?.length || 0} note="N01-N16" />
        <Stat icon={ShieldCheck} label="门槛层" value={data.features.gateIds?.length || 0} note="G01-G03" />
        <Stat icon={Gauge} label="独立方案" value={data.features.features?.length || 0} note="单方案独立运行" />
        <Stat icon={SlidersHorizontal} label="评分文件" value={data.features.scoreFileCount || 0} note="仅正式 N/G 结果" />
      </section>

      <FilterBar>
        <SegmentedControl
          value={scope}
          onChange={setScope}
          options={[
            { value: "alpha", label: "收益型 N01-N16" },
            { value: "gates", label: "门槛层 G01-G03" },
          ]}
        />
        {featureOptions.length ? (
          <SelectBox
            label="特征"
            value={feature?.id || ""}
            onChange={setFeatureId}
            options={featureOptions.map((f) => ({ value: f.id, label: `${f.id} ${f.name}` }))}
          />
        ) : null}
        <SearchBox value={query} onChange={setQuery} placeholder="搜索公司" />
        <div className="data-note">评分日期：{feature?.date || "-"}</div>
      </FilterBar>

      {feature ? (
        <FeatureSummaryPanel feature={feature} />
      ) : null}

      <section className="panel">
        <PanelTitle icon={Gauge} title={`${featureGroupLabels[scope]}概览`} />
        <div className="effective-feature-grid">
          {featureOptions.map((item) => (
            <FeatureCard
              key={`${scope}-${item.id}`}
              feature={item}
              active={item.id === feature?.id}
              onSelect={() => setFeatureId(item.id)}
            />
          ))}
        </div>
        {!featureOptions.length ? <p className="muted">当前分组没有可展示的研究方案。</p> : null}
      </section>

      {feature && rows.length ? (
        <>
          <section className="dashboard-grid">
            <div className="panel">
              <PanelTitle icon={ArrowDownUp} title="Top 15" />
              <DenseTable rows={top} columns={featureColumns()} />
            </div>
            <div className="panel">
              <PanelTitle icon={ArrowDownUp} title="Bottom 15" />
              <DenseTable rows={bottom} columns={featureColumns()} />
            </div>
          </section>

          <section className="panel table-panel">
            <PanelTitle icon={SlidersHorizontal} title={`${featureGroupLabels[scope]}热力图`} />
            <div className="heatmap-wrap">
              <table className="heatmap">
                <thead>
                  <tr>
                    <th>公司</th>
                    {featureOptions.map((f) => (
                      <th key={f.id} title={f.name}>
                        {f.id}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {heatmapRows.map((row) => {
                    const byId = data.features.scoreIndex[row.ticker] || {};
                    return (
                      <tr key={row.ticker}>
                        <td>
                          <button onClick={() => (window.location.hash = `company/${encodeURIComponent(row.ticker)}`)}>
                            {row.ticker}
                          </button>
                        </td>
                        {featureOptions.map((f) => {
                          const score = byId[f.id]?.score;
                          return (
                            <td key={f.id}>
                              <span className="heat-cell" style={{ background: heatColor(score) }} title={`${f.id} ${formatValue(score)}`}>
                                {formatValue(score, "")}
                              </span>
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </section>
        </>
      ) : feature ? (
        <section className="panel">
          <PanelTitle icon={SlidersHorizontal} title="公司评分尚未生成" />
          <p className="muted">{feature.id} 已纳入当前架构，但正式量化评分目录中还没有可展示的结果文件。</p>
        </section>
      ) : null}
    </>
  );
}

function FeatureSummaryPanel({ feature }) {
  if (!feature) return null;
  return (
    <section className="panel feature-metric-panel">
      <PanelTitle icon={Gauge} title={`${feature.id} ${feature.name}`} />
      <div className="feature-metric-layout">
        <div>
          <p className="feature-concept">{feature.concept || featureGroupDescriptions[feature.layer === "alpha" ? "alpha" : "gates"]}</p>
          <div className="feature-score-meta">
            <span>{feature.layerLabel}</span>
            <span>{feature.hasScores ? `评分日期 ${feature.date}` : "评分待生成"}</span>
            <span>{feature.planPath || "研究方案路径缺失"}</span>
          </div>
        </div>
        <p className="muted">
          {feature.layer === "alpha"
            ? "有效性在需要时直接独立评估，不由常驻自动评估框架登记。"
            : "门槛层用于过滤、约束或调整可靠性，不作为收益加分项。"}
        </p>
      </div>
    </section>
  );
}

function FeatureCard({ feature, active, onSelect }) {
  return (
    <button className={active ? "effective-feature-card active" : "effective-feature-card"} onClick={onSelect}>
      <span>{feature.id}</span>
      <strong>{feature.name}</strong>
      <em>{feature.layerLabel}</em>
      <div className="feature-card-metrics">
        <small>{feature.layer === "alpha" ? "收益研究" : "风险约束"}</small>
        <small>评分 {feature.hasScores ? feature.date : "待生成"}</small>
      </div>
    </button>
  );
}

function featureColumns() {
  return [
    { key: "rank", label: "因子排名", className: "num" },
    { key: "rankOverall", label: "总榜", className: "num" },
    { key: "ticker", label: "Ticker" },
    { key: "companyName", label: "公司" },
    { key: "score", label: "分数", className: "num" },
    { key: "evidenceGrade", label: "证据" },
    { key: "confidence", label: "置信度" },
  ];
}

function heatColor(score) {
  const n = toNumber(score);
  if (n === null) return "#eef1f5";
  if (n >= 8) return "#0f9f6e";
  if (n >= 6.5) return "#76b041";
  if (n >= 5) return "#d5a11e";
  if (n >= 3.5) return "#e27730";
  return "#cf3f4f";
}

function Quality({ data }) {
  return (
    <>
      <PageHeader eyebrow="数据质量" title="覆盖、重复和过期检查" />
      <section className="stat-grid">
        <Stat
          icon={Building2}
          label="索引公司"
          value={data.quality.summary.companyIndexCount}
          note={`正式报告 ${data.quality.summary.companyReportUnique}`}
        />
        <Stat icon={Layers} label="索引行业" value={data.quality.summary.industryIndexCount} note={`报告唯一 ${data.quality.summary.industryReportUnique}`} />
        <Stat
          icon={Gauge}
          label="特征评分文件"
          value={data.quality.summary.featureFileCount}
          note={`架构 ${data.quality.summary.alphaFeatureCount || 0}+${data.quality.summary.gateCount || 0}`}
        />
        <Stat
          icon={ArrowDownUp}
          label="公司对比"
          value={data.quality.summary.companyComparisonCount || 0}
          note={`行数 ${data.quality.summary.companyComparisonRowCount || 0}`}
        />
        <Stat icon={AlertTriangle} label="告警数" value={data.quality.alerts.length} note="含提示项" />
      </section>
      <section className="panel">
        <PanelTitle icon={AlertTriangle} title="告警清单" />
        <div className="quality-list">
          {data.quality.alerts.map((alert, index) => (
            <AlertItem key={`${alert.type}-${index}`} alert={alert} wide />
          ))}
        </div>
      </section>
    </>
  );
}

function AlertItem({ alert, wide }) {
  return (
    <div className={wide ? "alert-item wide" : "alert-item"}>
      <span className={`severity ${alert.severity}`}>{alert.severity}</span>
      <div>
        <strong>{alert.title}</strong>
        <p>{alert.message}</p>
      </div>
    </div>
  );
}

function IconButton({ label, icon: Icon, onClick }) {
  return (
    <button className="icon-button" onClick={onClick} title={label} aria-label={label}>
      <Icon size={17} />
      <span>{label}</span>
    </button>
  );
}

function DenseTable({ rows, columns, onRowClick }) {
  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} className={column.className || ""}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.ticker || row.slug || row.name || index}-${index}`} onClick={onRowClick ? () => onRowClick(row) : undefined}>
              {columns.map((column) => (
                <td key={column.key} className={column.className || ""}>
                  {formatValue(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SortableTable({ rows, columns, sortKey, sortDirection, onSort, onRowClick }) {
  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} className={column.className || ""}>
                <button onClick={() => onSort(column.key)}>
                  {column.label}
                  {sortKey === column.key ? <span>{sortDirection === "asc" ? "↑" : "↓"}</span> : null}
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.ticker || row.name}-${index}`} onClick={onRowClick ? () => onRowClick(row) : undefined}>
              {columns.map((column) => (
                <td key={column.key} className={column.className || ""}>
                  {formatValue(row[column.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MarkdownView({ markdown }) {
  const html = useMemo(() => DOMPurify.sanitize(marked.parse(markdown || "")), [markdown]);
  return <article className="markdown" dangerouslySetInnerHTML={{ __html: html }} />;
}

createRoot(document.getElementById("root")).render(<App />);
