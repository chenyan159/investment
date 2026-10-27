import React, {useMemo, useState} from 'react';
import {ArrowRight, ArrowUpRight, Layers3, GitCompareArrows, BookOpen, Compass} from 'lucide-react';
import {SCENARIOS, SCENARIO_NAMES, num, navigate} from './lib';
import {Panel, Metric, SearchBox, Empty, CompanySelect} from './components';
import {CompanyScatter} from './company-atlas-charts';
import {scatterMeta} from './company-atlas-data';
import {CompanyLeaders,LEADER_DIMENSIONS} from './company-leaders';
import {RevisionScatter} from './overview-charts';
import './overview.css';

export function Overview({data}) {
  const [query,setQuery]=useState(''), [sector,setSector]=useState('all'), [scenario,setScenario]=useState('base'), [source,setSource]=useState('comparison'), [quickTicker,setQuickTicker]=useState('NVDA');
  const sectors=useMemo(()=>[...new Set(data.companies.map(c=>c.sector).filter(Boolean))].sort(),[data]);
  const companies=useMemo(()=>data.companies.filter(c=>(sector==='all'||c.sector===sector)&&`${c.name} ${c.ticker} ${c.sector}`.toLowerCase().includes(query.toLowerCase())),[data,query,sector]);
  const counts=data.meta?.counts||{};
  const quickCompany=companies.find(c=>c.ticker===quickTicker)||companies.find(c=>c.ticker==='NVDA')||companies[0];
  const selectCompany=ticker=>navigate('comparisons',ticker);

  return <div className="overview-dashboard">
    <section className="hero"><div><div className="eyebrow"><span className="status-dot"/> A RESEARCH ATLAS</div><h1>看见情景。<br/><em>理解取舍。</em></h1><p>每一个点，都是一家公司。<br/>从不同情景与研究角度，发现值得深入的对象。</p><div className="hero-actions"><button className="button primary" onClick={()=>navigate('scenarios','NVDA')}>探索公司情景<ArrowRight size={17}/></button><button className="text-button" onClick={()=>navigate('comparisons','NVDA')}>进入公司对比<ArrowUpRight size={17}/></button></div></div><div className="hero-art" aria-hidden="true"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="orbit orbit-three"/><div className="art-label top">经营 · 价值 · 选择</div><div className="art-center">A<span>ANANTA</span></div><div className="orbit-node one"/><div className="orbit-node two"/><div className="orbit-node three"/><div className="art-label bottom">多种未来，一份清晰的研究。</div></div></section>
    <div className="metrics-grid"><Metric label="公司研究覆盖" value={num(data.companies.length,0)} note="从全景进入每家公司" icon={Compass}/><Metric label="公司情景报告" value={num(counts.scenarios,0)} note="四种情景 · 保留原始判断" icon={Layers3}/><Metric label="公司对比报告" value={num(counts.comparisonReports,0)} note={`${counts.peerComparisons?.toLocaleString('zh-CN')||'—'} 条定向公司比较`} icon={GitCompareArrows}/><Metric label="研究背景资料" value={num(data.research.filter(r=>r.kind!=='company').length,0)} note="产业背景与行业调研" icon={BookOpen}/></div>

    <div className="overview-controls"><div className="overview-controls-label"><span className="eyebrow">EXPLORE THE RESEARCH</span><strong>筛选整个研究图谱</strong></div><div className="filter-row"><SearchBox value={query} onChange={setQuery}/><select aria-label="筛选行业" value={sector} onChange={e=>setSector(e.target.value)}><option value="all">全部行业</option>{sectors.map(s=><option key={s}>{s}</option>)}</select><span className="overview-sample-count">{companies.length}<small>家公司</small></span>{(query||sector!=='all')&&<button className="text-button" onClick={()=>{setQuery('');setSector('all');}}>清除筛选</button>}</div></div>

    <div className="section-heading"><div><div className="eyebrow">01 / THE COMPANY UNIVERSE</div><h2>把公司，放在同一张图里</h2><p>每个点都能找到具体公司。悬浮或聚焦看数值，点击阅读完整研究。</p></div><div className="segment"><button className={source==='scenario'?'active':''} onClick={()=>setSource('scenario')}>情景原报告</button><button className={source==='comparison'?'active':''} onClick={()=>setSource('comparison')}>对比复核后</button></div></div>
    <div className="overview-viz-grid">{['risk_return','base_upside','range_return','evidence_return'].map(mode=>{const meta=scatterMeta(mode);return <Panel key={mode} title={meta.title} description={meta.description}><CompanyScatter companies={companies} source={source} mode={mode} onSelect={ticker=>navigate(source==='scenario'?'scenarios':'comparisons',ticker)}/></Panel>})}</div>

    <div className="section-heading"><div><div className="eyebrow">02 / BEFORE & AFTER</div><h2>同一家公司，复核前后</h2><p>保留两份报告的独立判断，看清每家公司的变化。</p></div><label className="overview-scenario-select">复核分析情景<select aria-label="选择复核分析情景" value={scenario} onChange={e=>setScenario(e.target.value)}>{SCENARIOS.map(k=><option key={k} value={k}>{SCENARIO_NAMES[k]}情景</option>)}</select></label></div>
    <Panel title="复核改变了多少回报？" description={`${SCENARIO_NAMES[scenario]}情景年化回报中点：原报告与复核结果一一对应。`} className="overview-revision-panel"><RevisionScatter companies={companies} scenario={scenario} onSelect={selectCompany}/></Panel>

    <div className="section-heading"><div><div className="eyebrow">03 / LEADING COMPANIES BY LENS</div><h2>不同角度，找到靠前的公司</h2><p>每张图列出该维度前 8 家，明确公司名称、回报区间和证据等级。</p></div><span className="overview-scenario-tag">{source==='comparison'?'对比复核后':'情景原报告'}</span></div>
    <div className="overview-viz-grid">{['base','bear','bull','breakthrough',...(source==='comparison'?['steady','offense']:[])].map(dimension=><Panel key={dimension} title={LEADER_DIMENSIONS[dimension].title} description={LEADER_DIMENSIONS[dimension].description}><CompanyLeaders companies={companies} source={source} dimension={dimension} onSelect={ticker=>navigate(source==='scenario'?'scenarios':'comparisons',ticker)}/></Panel>)}</div>
    <p className="overview-ranking-note">这些图按单一维度展示当前筛选样本，不合成综合排名。排序采用各报告年化回报区间两个端点的中点，不含股息；各公司报价日、目标日可能不同。回报空间与研究证据需一同阅读，中点不代表预期收益。</p>
    {quickCompany?<div className="overview-quick-company"><div><span className="eyebrow">FROM THE ATLAS TO A COMPANY</span><h2>选一家公司，深入完整研究</h2><p>原始情景、对比复核、证据与推导都在公司页面。</p></div><div className="overview-quick-actions"><CompanySelect companies={companies} value={quickCompany.ticker} onChange={setQuickTicker}/><div><button className="button secondary" onClick={()=>navigate('scenarios',quickCompany.ticker)}>情景原报告<ArrowUpRight size={15}/></button><button className="button primary" onClick={()=>navigate('comparisons',quickCompany.ticker)}>对比复核<ArrowUpRight size={15}/></button></div></div></div>:<Empty hint="调整公司或行业筛选，继续探索研究图谱"/>}
  </div>;
}
