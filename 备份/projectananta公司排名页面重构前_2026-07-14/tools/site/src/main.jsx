import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import DOMPurify from "dompurify";
import { marked } from "marked";
import {
  AlertTriangle,
  ArrowDownUp,
  BarChart3,
  Building2,
  Download,
  FileText,
  Gauge,
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

const featureGroupLabels = {
  alpha: "收益型特征",
  gates: "门槛层",
  validatedAlpha: "前向有效",
};

const featureGroupDescriptions = {
  alpha: "用于形成未来收益排序判断；是否有效由独立的前向验证决定。",
  gates: "用于证据、可投资性和风险约束，不作为独立收益信号。",
  validatedAlpha: "仅包含已经满足多期前向证据标准的收益型特征。",
};

const featureStatusLabels = {
  qualified: "前向有效",
  awaiting_forward_cohorts: "等待成熟前向样本",
  insufficient_forward_evidence: "前向证据不足",
  not_alpha: "非收益信号",
};

function featureStatusLabel(feature) {
  if (!feature) return "";
  return featureStatusLabels[feature.registryStatus] || (feature.layer === "gate" ? "非收益信号" : "等待前向验证");
}

const navItems = [
  { id: "overview", label: "首页", icon: Home },
  { id: "companies", label: "公司", icon: Building2 },
  { id: "industries", label: "行业", icon: Layers },
  { id: "rankings", label: "排名", icon: BarChart3 },
  { id: "companyComparisons", label: "公司对比", icon: ArrowDownUp },
  { id: "features", label: "特征量化", icon: Gauge },
  { id: "dailyNews", label: "AI 新闻", icon: Newspaper },
  { id: "quality", label: "质量告警", icon: ShieldCheck },
];

function formatValue(value, fallback = "-") {
  if (value === null || value === undefined || value === "") return fallback;
  return String(value);
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
        const [meta, companies, industries, rankings, companyComparisons, features, quality, dailyNews] = await Promise.all(
          ["meta", "companies", "industries", "rankings", "company-comparisons", "features", "quality", "daily-news"].map((name) =>
            fetch(`${DATA_BASE}/${name}.json`, name === "company-comparisons" ? { cache: "no-store" } : undefined).then((r) => {
              if (!r.ok) throw new Error(`${name}.json ${r.status}`);
              return r.json();
            }),
          ),
        );
        setState({ loading: false, error: null, meta, companies, industries, rankings, companyComparisons, features, quality, dailyNews });
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
            <strong>Investment</strong>
            <span>Research Dashboard</span>
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
        {view === "features" && <Features data={data} rankingByTicker={rankingByTicker} />}
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
  const defaultKey = defaultRankingKey(data);
  const defaultRun = data.rankings.runs[defaultKey];
  const topRows = (defaultRun?.rows || []).slice(0, 8);
  const dailyNewsCount = data.meta.dailyNewsCount || data.dailyNews.items.length;
  const rankingCount = rankingEntries(data).length;

  return (
    <>
      <PageHeader eyebrow="只读研究看板" title="AI 产业链公司、行业与排名" />
      <section className="stat-grid">
        <Stat
          icon={Building2}
          label="公司数"
          value={data.meta.companyCount}
          note={`报告 ${data.meta.companyReportCount} / 评估 ${data.meta.companyEvaluationCount || 0}`}
        />
        <Stat icon={Layers} label="行业数" value={data.meta.industryCount} note={`有报告 ${data.meta.industryReportCount}`} />
        <Stat
          icon={BarChart3}
          label="当前榜单"
          value={rankingCount}
          note={`${data.meta.rankingMethodCount || 0}个方案 · 默认 ${defaultRun?.label || "-"}`}
        />
        <Stat
          icon={ArrowDownUp}
          label="公司对比"
          value={data.meta.companyComparisonCount || 0}
          note={`最新 ${data.meta.latestCompanyComparisonDate || "-"}`}
        />
        <Stat icon={Table2} label="最新金融数据" value={data.meta.latestFinancialDate || "-"} note="每日金融数据" />
        <Stat icon={Newspaper} label="最新 AI 新闻" value={data.meta.latestDailyNewsDate || "-"} note={`最近 ${dailyNewsCount} 天`} />
      </section>

      <InvestmentConclusionPanel data={data} setView={setView} />

      <section className="dashboard-grid">
        <div className="panel span-2">
          <PanelTitle icon={ArrowDownUp} title="公司对比最终胜出 Top 8" action={<TextButton onClick={() => setView("companyComparisons")}>查看公司对比</TextButton>} />
          <DenseTable
            rows={(data.companyComparisons?.top20 || []).slice(0, 8)}
            columns={[
              { key: "rank", label: "Rank", className: "num" },
              { key: "ticker", label: "Ticker" },
              { key: "name", label: "公司" },
              { key: "category", label: "分类" },
              { key: "wins", label: "胜出", className: "num" },
              { key: "losses", label: "落败", className: "num" },
              { key: "net", label: "净胜", className: "num" },
            ]}
            onRowClick={(row) => {
              setView("companyComparisons");
              window.location.hash = `companyComparison/${encodeURIComponent(row.ticker)}`;
            }}
          />
        </div>
        <div className="panel span-2">
          <PanelTitle icon={BarChart3} title={`${defaultRun?.label || "公司排序"} Top 8`} action={<TextButton onClick={() => setView("rankings")}>查看排名</TextButton>} />
          <DenseTable
            rows={topRows}
            columns={[
              { key: "rank", label: "Rank", className: "num" },
              { key: "ticker", label: "Ticker" },
              { key: "name", label: "公司" },
              { key: "tier", label: "Tier" },
              { key: "expectedReturn", label: "预期收益", className: "num" },
              { key: "score", label: "Score", className: "num" },
            ]}
            onRowClick={(row) => {
              window.location.hash = `company/${encodeURIComponent(row.ticker)}`;
            }}
          />
        </div>
      </section>

      <section className="panel">
        <PanelTitle icon={Gauge} title="特征量化架构" action={<TextButton onClick={() => setView("features")}>查看特征</TextButton>} />
        <div className="feature-strip-groups">
          {["alpha", "gates"].map((groupKey) => (
            <div key={groupKey}>
              <strong>{featureGroupLabels[groupKey]}</strong>
              <div className="feature-strip">
                {(data.features.featureGroups?.[groupKey] || []).map((id) => {
                  const feature = data.features.features.find((item) => item.id === id);
                  return (
                    <span key={`${groupKey}-${id}`} className="feature-chip" title={feature?.name || id}>
                      {id}
                    </span>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <PanelTitle icon={Newspaper} title="最近 AI 新闻" action={<TextButton onClick={() => setView("dailyNews")}>查看新闻</TextButton>} />
        <div className="news-strip">
          {data.dailyNews.items.slice(0, 5).map((item) => (
            <button
              key={item.date}
              className="news-strip-item"
              onClick={() => {
                setView("dailyNews");
                window.location.hash = "dailyNews";
              }}
            >
              <span>{item.date}</span>
              <strong>{item.title}</strong>
            </button>
          ))}
        </div>
      </section>
    </>
  );
}

function InvestmentConclusionPanel({ data, setView }) {
  const openCompany = (ticker) => {
    setView("companies");
    window.location.hash = `company/${encodeURIComponent(ticker)}`;
  };
  const evaluation = data.rankings?.currentEvaluation;
  if (!evaluation) {
    return (
      <section className="panel conclusion-panel">
        <PanelTitle icon={LineChart} title="排序综合结论" />
        <p className="muted">当前正式评估尚未载入。</p>
      </section>
    );
  }
  const methodGroups = [
    { label: "3个月历史回看前列", items: evaluation.topMethods3m || [], field: "rankIc3m", neutral: "categoryNeutralRankIc3m", spread: "top20Bottom20Spread3m" },
    { label: "6个月历史回看前列", items: evaluation.topMethods6m || [], field: "rankIc6m", neutral: "categoryNeutralRankIc6m", spread: "top20Bottom20Spread6m" },
  ];

  return (
    <section className="panel conclusion-panel">
      <PanelTitle
        icon={LineChart}
        title="最新排序评估"
        action={<span className="panel-date">股价截至 {evaluation.priceAsOf}</span>}
      />
      <div className="conclusion-lead">
        <strong>
          {evaluation.coverage.methodCount}个方案、{evaluation.coverage.listCount}张榜、每榜{evaluation.coverage.rankedCompanyCount}家公司
        </strong>
        <p>
          {evaluation.evidenceType}。其中{evaluation.coverage.pricedCompanyCount}家公司有完整价格历史；本页展示的是排序与已经发生价格的对应关系，不是未来收益证明。
        </p>
      </div>
      <div className="conclusion-groups">
        {methodGroups.map((group) => (
          <div key={group.label} className="conclusion-group">
            <h2>{group.label}</h2>
            <div className="conclusion-list">
              {group.items.slice(0, 6).map((item) => (
                <article key={`${group.label}-${item.methodId}`} className="conclusion-item">
                  <div>
                    <strong>{item.methodId} · {item.label}</strong>
                    <p>
                      Rank IC {formatSigned(item[group.field], 3)} · 行业中性 {formatSigned(item[group.neutral], 3)} · Top20-Bottom20 {formatRatioPercent(item[group.spread])}
                    </p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        ))}
      </div>
      <div className="conclusion-group">
        <h2>跨方案共识候选</h2>
        <div className="ticker-stack">
          {(evaluation.consensus || []).slice(0, 12).map((item) => (
            <button
              key={item.ticker}
              className="ticker-chip"
              title={`26方案平均名次 ${formatValue(item.meanRank)}；Top20出现 ${formatValue(item.top20Count)} 次`}
              onClick={() => openCompany(item.ticker)}
            >
              {item.ticker}
            </button>
          ))}
        </div>
        <p className="muted">共识只用于确定进一步研究顺序；历史已大涨的公司尤其需要重新检查估值和追高风险。</p>
      </div>
      <div className="conclusion-group">
        <h2>公司与行业调研输入扩展</h2>
        <div className="conclusion-list">
          {(evaluation.inputComparisons || []).map((item) => (
            <article key={`${item.base}-${item.extended}`} className="conclusion-item">
              <div>
                <strong>{item.base} → {item.extended}</strong>
                <p>
                  排名相似度 {formatSigned(item.rankSimilarity, 3)} · Top20重合 {item.top20Overlap}/20 · 平均绝对变化 {toNumber(item.meanAbsoluteRankChange)?.toFixed(1) || "-"} 名
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
      <div className="conclusion-cautions">
        {(evaluation.caveats || []).map((item) => (
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

  return (
    <>
      <PageHeader eyebrow="日度资料" title="AI 新闻稿与语音" />
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
                      </div>
                      <audio
                        controls
                        preload="metadata"
                        src={item.audio.url}
                        aria-label={`${item.date} ${item.title} 语音`}
                        onPlay={() => setSelectedDate(item.date)}
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
                  </div>
                  <audio controls preload="metadata" src={selected.audio.url} />
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
        hasEvaluationText: company.hasEvaluation ? "有" : "缺",
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
    { key: "hasEvaluationText", label: "评估" },
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
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingEvaluation, setLoadingEvaluation] = useState(false);
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

  useEffect(() => {
    let active = true;
    setEvaluation(null);
    if (!company.evaluation?.dataFile) return;
    setLoadingEvaluation(true);
    fetch(`${DATA_BASE}/${company.evaluation.dataFile}`)
      .then((r) => (r.ok ? r.json() : null))
      .then((json) => {
        if (active) setEvaluation(json);
      })
      .finally(() => {
        if (active) setLoadingEvaluation(false);
      });
    return () => {
      active = false;
    };
  }, [company.ticker, company.evaluation?.dataFile]);

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
        <Mini label="评估日期" value={company.evaluation?.reportDate} />
      </div>
      <SectionBlock title="源文件">
        <div className="source-stack">
          {company.report ? (
            <LabeledPath label="公司报告" value={company.report.sourcePath} />
          ) : (
            <p className="muted">未匹配到正式公司报告。</p>
          )}
          {company.evaluation ? (
            <LabeledPath label="公司评估" value={company.evaluation.sourcePath} />
          ) : (
            <p className="muted">未匹配到公司评估。</p>
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
      <SectionBlock title="公司评估">
        {loadingEvaluation ? <p className="muted">正在加载评估...</p> : null}
        {evaluation ? (
          <MarkdownView markdown={evaluation.markdown} />
        ) : !loadingEvaluation ? (
          <p className="muted">没有可渲染评估。</p>
        ) : null}
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
              <em>{featureStatusLabel(row.feature)}</em>
            </div>
            <div className="feature-bars">
              <MetricBar label="分数" value={row.score} max={10} display={formatValue(row.score)} />
              <MetricBar label="排名" value={rankStrength} max={100} display={row.rank ? `#${row.rank}${row.rowCount ? `/${row.rowCount}` : ""}` : "-"} />
            </div>
            <div className="feature-score-meta">
              {row.feature.layer === "alpha" ? <span>成熟样本 {row.feature.forwardValidation?.nCohorts || 0}</span> : <span>不进入收益型名单</span>}
              {row.feature.layer === "alpha" ? <span>前向 IC {formatSigned(row.feature.forwardValidation?.meanSpearmanIc, 3)}</span> : null}
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
  const baseRows = run?.rows || [];
  const viewRows = range === "bottom" ? [...baseRows].slice(-50).reverse() : baseRows.slice(0, 80);
  const rows = sortRows(viewRows, sortKey, sortDirection);
  const columns = rankingColumns(run);

  return (
    <>
      <PageHeader
        eyebrow={`${run?.status || run?.strategy || "公司排序"} · 当前运行 ${run?.runId || "-"}`}
        title={run?.label || "公司排序"}
        actions={
          <IconButton label="导出当前排名" icon={Download} onClick={() => downloadCsv(`${kind}-ranking.csv`, rows, columns)} />
        }
      />
      <section className="ranking-profile-grid">
        <div className="panel ranking-profile">
          <h2>适用方法</h2>
          <p>{run?.useCase || "查看该排序的适用场景和约束。"}</p>
          <p className="muted">{run?.caution || ""}</p>
        </div>
        <div className="panel ranking-profile">
          <h2>生成前历史回看</h2>
          <div className="metric-grid">
            <Metric label="3M Rank IC" value={formatSigned(run?.metrics?.rankIc3m, 3)} />
            <Metric label="3M 行业中性IC" value={formatSigned(run?.metrics?.categoryNeutralRankIc3m, 3)} />
            <Metric label="3M Top20-Bottom20" value={formatRatioPercent(run?.metrics?.top20Bottom20Spread3m)} />
            <Metric label="6M Rank IC" value={formatSigned(run?.metrics?.rankIc6m, 3)} />
            <Metric label="6M 行业中性IC" value={formatSigned(run?.metrics?.categoryNeutralRankIc6m, 3)} />
            <Metric label="6M Top20-Bottom20" value={formatRatioPercent(run?.metrics?.top20Bottom20Spread6m)} />
          </div>
          <p className="muted">{data.rankings.currentEvaluation?.evidenceType || "-"}，不能解释为当前版本的样本外有效性。</p>
        </div>
        <div className="panel ranking-profile">
          <h2>管理与来源</h2>
          <p>方法/榜单：<code>{run?.methodId || "-"} / {run?.listId || "-"}</code></p>
          <p>迭代目录：{run?.iterationCount ?? 0} 个；当前样本：{run?.rowCount ?? 0}</p>
          <p>排序目录：<code>{run?.folderPath || "-"}</code></p>
          <p>正式评估：<code>{run?.evaluationPath || "-"}</code></p>
        </div>
      </section>
      <FilterBar>
        <SelectBox
          label="榜单"
          value={kind}
          onChange={(value) => {
            setRankingKey(value);
            setSortKey("rank");
            setSortDirection("asc");
          }}
          options={entries.map(({ key, run }) => ({ value: key, label: run.label }))}
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
        <div className="data-note">来源：{run?.sourcePath || "-"}</div>
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
        eyebrow={`公司横评 · ${comparisons.reportDate || "-"} · 价格截止 ${comparisons.priceDate || "-"} · 持有 ${comparisons.holdingPeriod || "8—16个月"}`}
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
        eyebrow={`公司对比 · ${comparisons.reportDate || "-"} · ${comparisons.qualityNote || ""}`}
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
  const registryStatus = data.features.effectiveRegistry?.status;
  const validationNote = data.features.effectiveRegistry?.asOf
    ? `截至 ${data.features.effectiveRegistry.asOf}`
    : registryStatus === "awaiting_sufficient_forward_evidence"
      ? "等待足够的成熟前向样本"
      : "尚无前向评估日期";

  return (
    <>
      <PageHeader eyebrow="特征量化" title="收益型特征与门槛层" />
      <section className="stat-grid">
        <Stat icon={LineChart} label="收益型特征" value={data.features.alphaFeatureIds?.length || 0} note="N01-N16" />
        <Stat icon={ShieldCheck} label="门槛层" value={data.features.gateIds?.length || 0} note="G01-G03" />
        <Stat icon={Gauge} label="前向有效" value={data.features.effectiveFeatureIds?.length || 0} note={validationNote} />
        <Stat icon={SlidersHorizontal} label="评分文件" value={data.features.scoreFileCount || 0} note="仅正式 N/G 结果" />
      </section>

      <FilterBar>
        <SegmentedControl
          value={scope}
          onChange={setScope}
          options={[
            { value: "alpha", label: "收益型 N01-N16" },
            { value: "gates", label: "门槛层 G01-G03" },
            { value: "validatedAlpha", label: "前向有效" },
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
        <FeatureEffectivenessPanel feature={feature} />
      ) : (
        <section className="panel feature-metric-panel">
          <PanelTitle icon={Gauge} title="尚无通过前向标准的收益型特征" />
          <p className="muted">当前有效名单为空是正常状态。收益型特征仍可在 N01-N16 中查看；只有完成多期成熟前向验证并达到注册标准后，才会进入这里。</p>
        </section>
      )}

      <section className="panel">
        <PanelTitle icon={Gauge} title={`${featureGroupLabels[scope]}概览`} />
        <div className="effective-feature-grid">
          {featureOptions.map((item) => (
            <EffectiveFeatureCard
              key={`${scope}-${item.id}`}
              feature={item}
              active={item.id === feature?.id}
              onSelect={() => setFeatureId(item.id)}
            />
          ))}
        </div>
        {!featureOptions.length ? <p className="muted">当前没有满足前向有效标准的收益型特征。</p> : null}
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

function FeatureEffectivenessPanel({ feature }) {
  if (!feature) return null;
  const validation = feature.forwardValidation;
  return (
    <section className="panel feature-metric-panel">
      <PanelTitle icon={Gauge} title={`${feature.id} ${feature.name}`} />
      <div className="feature-metric-layout">
        <div>
          <p className="feature-concept">{feature.concept || featureGroupDescriptions[feature.layer === "alpha" ? "alpha" : "gates"]}</p>
          <div className="feature-score-meta">
            <span>{feature.layerLabel}</span>
            <span>{featureStatusLabel(feature)}</span>
            <span>{feature.sourcePath || "尚无评分文件"}</span>
          </div>
        </div>
        {feature.layer === "alpha" ? (
          <div className="metric-stack">
            <MetricBar label="成熟样本" value={validation?.nCohorts} max={3} display={formatValue(validation?.nCohorts, "0")} />
            <MetricBar label="平均 IC" value={Math.max(0, toNumber(validation?.meanSpearmanIc) || 0)} max={0.5} display={formatSigned(validation?.meanSpearmanIc, 3)} />
            <MetricBar label="中性 IC" value={Math.max(0, toNumber(validation?.meanNeutralSpearmanIc) || 0)} max={0.5} display={formatSigned(validation?.meanNeutralSpearmanIc, 3)} />
          </div>
        ) : (
          <p className="muted">门槛层用于过滤、约束或调整可靠性，不参与收益型有效名单评选。</p>
        )}
      </div>
    </section>
  );
}

function EffectiveFeatureCard({ feature, active, onSelect }) {
  const validation = feature.forwardValidation;
  return (
    <button className={active ? "effective-feature-card active" : "effective-feature-card"} onClick={onSelect}>
      <span>{feature.id}</span>
      <strong>{feature.name}</strong>
      <em>{featureStatusLabel(feature)}</em>
      <div className="feature-card-metrics">
        {feature.layer === "alpha" ? <small>成熟样本 {validation?.nCohorts || 0}</small> : <small>不作为收益信号</small>}
        {feature.layer === "alpha" ? <small>IC {formatSigned(validation?.meanSpearmanIc, 3)}</small> : null}
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
          note={`报告 ${data.quality.summary.companyReportUnique} / 评估 ${data.quality.summary.companyEvaluationUnique || 0}`}
        />
        <Stat icon={Layers} label="索引行业" value={data.quality.summary.industryIndexCount} note={`报告唯一 ${data.quality.summary.industryReportUnique}`} />
        <Stat
          icon={Gauge}
          label="特征评分文件"
          value={data.quality.summary.featureFileCount}
          note={`架构 ${data.quality.summary.alphaFeatureCount || 0}+${data.quality.summary.gateCount || 0} / 前向有效 ${data.quality.summary.effectiveFeatureCount || 0}`}
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
