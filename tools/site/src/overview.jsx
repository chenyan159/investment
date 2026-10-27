import React, {useMemo, useState} from 'react';
import {ArrowRight, ArrowUpRight, Layers3, GitCompareArrows, BookOpen, Compass} from 'lucide-react';
import {SCENARIOS, SCENARIO_NAMES, label, num, navigate} from './lib';
import {Panel, Metric, SearchBox, Empty, CompanySelect} from './components';
import {Scatter} from './charts';
import {RevisionScatter, ReturnDistribution, SectorRevisions, EvidenceEvolution} from './overview-charts';
import './overview.css';

const DECISIONS = ['steady_allocation','offense_allocation','near_term_timing'];
const VIEWS = ['near_term_delivery','long_term_compounding','base_valuation','upside_potential','downside_resilience','relative_attractiveness'];
const DECISION_COLORS = {preferred_participate:'#267b6c',high_priority_offense:'#267b6c',build_now:'#267b6c',conditional_wait:'#d1ae70',small_option_bet:'#8fa7a0',wait_for_trigger:'#d1ae70',avoid:'#b97865'};
const VIEW_COLORS = {positive:'#267b6c',mixed:'#d1b67c',negative:'#b97865',neutral:'#8fa7a0',uncertain:'#a6a4b3',missing:'#dce1d7'};

function categoryCounts(reports, group, key, order=[]) {
  const counts = new Map();
  for (const report of reports) {
    const value = report?.[group]?.[key] || 'missing';
    counts.set(value, (counts.get(value) || 0) + 1);
  }
  return [...counts].sort(([a],[b]) => {
    const ai=order.indexOf(a), bi=order.indexOf(b);
    return (ai<0?99:ai)-(bi<0?99:bi)||a.localeCompare(b);
  });
}

function DistributionTrack({counts, total, colors, name}) {
  return <div className="overview-distribution-track" role="img" aria-label={`${name}：${counts.map(([key,count])=>`${label(key==='missing'?null:key)} ${count} 家`).join('，')}`}>
    {counts.map(([key,count])=><div key={key} style={{width:`${count/total*100}%`,background:colors[key]||'#a5afa3',color:['preferred_participate','high_priority_offense','build_now','positive','negative','avoid'].includes(key)?'#fff':'#354d3e'}} title={`${label(key==='missing'?null:key)}：${count} 家（${num(count/total*100)}%）`} tabIndex={0} aria-label={`${label(key==='missing'?null:key)} ${count} 家，占 ${num(count/total*100)}%`}>
      {count/total>.09&&<span>{count}</span>}
    </div>)}
  </div>;
}

function DecisionDistribution({companies}) {
  const reports=companies.map(c=>c.comparison).filter(r=>r&&r.structuredAvailable!==false);
  if(!reports.length)return <Empty hint="当前筛选下没有结构化公司对比"/>;
  return <div className="overview-decision-distribution">
    {DECISIONS.map((key,i)=>{
      const counts=categoryCounts(reports,'decision',key,['preferred_participate','high_priority_offense','build_now','conditional_wait','small_option_bet','wait_for_trigger','avoid']);
      return <div className="overview-decision-row" key={key}>
        <div className="overview-band-title"><span>0{i+1}</span><h3>{label(key)}</h3><small>{reports.length} 家</small></div>
        <DistributionTrack counts={counts} total={reports.length} colors={DECISION_COLORS} name={label(key)}/>
        <div className="overview-band-legend">{counts.map(([value,count])=><span key={value}><i style={{background:DECISION_COLORS[value]||'#a5afa3'}}/>{label(value==='missing'?null:value)}<b>{count}</b></span>)}</div>
      </div>;
    })}
    <p className="chart-note">每一行都是同一组公司的独立判断。颜色表示报告中的分类，条带宽度表示公司数量占比。</p>
  </div>;
}

function ViewDistribution({companies}) {
  const reports=companies.map(c=>c.comparison).filter(r=>r&&r.structuredAvailable!==false);
  const [active,setActive]=useState(null);
  if(!reports.length)return <Empty hint="当前筛选下没有六维判断数据"/>;
  const keys=['positive','mixed','negative','neutral','uncertain','missing'];
  const present=keys.filter(k=>VIEWS.some(view=>reports.some(r=>(r.views?.[view]||'missing')===k)));
  return <div className="overview-views">
    <div className="overview-view-legend">{present.map(key=><span key={key}><i style={{background:VIEW_COLORS[key]}}/>{label(key==='missing'?null:key)}</span>)}<small>每个维度 {reports.length} 家</small></div>
    {VIEWS.map((key,i)=>{
      const counts=categoryCounts(reports,'views',key,keys);
      return <div className={`overview-view-row ${active===key?'is-active':''}`} key={key} onMouseEnter={()=>setActive(key)} onMouseLeave={()=>setActive(null)}>
        <div><span>0{i+1}</span><strong>{label(key)}</strong></div>
        <DistributionTrack counts={counts} total={reports.length} colors={VIEW_COLORS} name={label(key)}/>
        <span className="overview-view-counts">{counts.map(([value,count])=><span key={value}>{label(value==='missing'?null:value)} <b>{count}</b></span>)}</span>
      </div>;
    })}
    <p className="chart-note">六个视角分别呈现，不合成总分。横条与图下注明每种判断的公司数，完整保留少数类别。</p>
  </div>;
}

export function Overview({data}) {
  const [query,setQuery]=useState(''), [sector,setSector]=useState('all'), [scenario,setScenario]=useState('base'), [source,setSource]=useState('comparison'), [quickTicker,setQuickTicker]=useState('NVDA');
  const sectors=useMemo(()=>[...new Set(data.companies.map(c=>c.sector).filter(Boolean))].sort(),[data]);
  const companies=useMemo(()=>data.companies.filter(c=>(sector==='all'||c.sector===sector)&&`${c.name} ${c.ticker} ${c.sector}`.toLowerCase().includes(query.toLowerCase())),[data,query,sector]);
  const counts=data.meta?.counts||{};
  const quickCompany=companies.find(c=>c.ticker===quickTicker)||companies.find(c=>c.ticker==='NVDA')||companies[0];
  const selectCompany=ticker=>navigate('comparisons',ticker);
  const setSectorFromChart=value=>{setSector(value);setQuery('');};
  return <div className="overview-dashboard">
    <section className="hero"><div><div className="eyebrow"><span className="status-dot"/> A RESEARCH ATLAS</div><h1>看见情景。<br/><em>理解取舍。</em></h1><p>把原报告与对比复核放在一起，<br/>看清回报、证据与公司选择如何变化。</p><div className="hero-actions"><button className="button primary" onClick={()=>navigate('scenarios','NVDA')}>探索公司情景<ArrowRight size={17}/></button><button className="text-button" onClick={()=>navigate('comparisons','NVDA')}>进入公司对比<ArrowUpRight size={17}/></button></div></div><div className="hero-art" aria-hidden="true"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="orbit orbit-three"/><div className="art-label top">经营 · 价值 · 选择</div><div className="art-center">A<span>ANANTA</span></div><div className="orbit-node one"/><div className="orbit-node two"/><div className="orbit-node three"/><div className="art-label bottom">多种未来，一份清晰的研究。</div></div></section>
    <div className="metrics-grid"><Metric label="公司研究覆盖" value={num(data.companies.length,0)} note="从全景进入每家公司" icon={Compass}/><Metric label="公司情景报告" value={num(counts.scenarios,0)} note="四种情景 · 保留原始判断" icon={Layers3}/><Metric label="公司对比报告" value={num(counts.comparisonReports,0)} note={`${counts.peerComparisons?.toLocaleString('zh-CN')||'—'} 条定向公司比较`} icon={GitCompareArrows}/><Metric label="研究背景资料" value={num(data.research.filter(r=>r.kind!=='company').length,0)} note="产业背景与行业调研" icon={BookOpen}/></div>

    <div className="overview-controls"><div className="overview-controls-label"><span className="eyebrow">EXPLORE THE RESEARCH</span><strong>筛选整个研究图谱</strong></div><div className="filter-row"><SearchBox value={query} onChange={setQuery}/><select aria-label="筛选行业" value={sector} onChange={e=>setSector(e.target.value)}><option value="all">全部行业</option>{sectors.map(s=><option key={s}>{s}</option>)}</select><span className="overview-sample-count">{companies.length}<small>家公司</small></span>{(query||sector!=='all')&&<button className="text-button" onClick={()=>{setQuery('');setSector('all');}}>清除筛选</button>}</div></div>

    <div className="section-heading"><div><div className="eyebrow">01 / BEFORE & AFTER</div><h2>原报告，经过复核之后</h2><p>从单家公司到整体分布，同时看见两份研究的判断。</p></div><label className="overview-scenario-select">复核分析情景<select aria-label="选择复核分析情景" value={scenario} onChange={e=>setScenario(e.target.value)}>{SCENARIOS.map(k=><option key={k} value={k}>{SCENARIO_NAMES[k]}情景</option>)}</select></label></div>
    <div className="overview-viz-grid"><Panel title="复核改变了多少回报？" description={`${SCENARIO_NAMES[scenario]}情景年化回报中点：原报告与复核结果一一对应。`}><RevisionScatter companies={companies} scenario={scenario} onSelect={selectCompany}/></Panel><Panel title="回报分布，前后对照" description="同一组公司，两个报告版本。分布是样本数量，不是收益概率。"><ReturnDistribution companies={companies} scenario={scenario}/></Panel></div>

    <div className="section-heading"><div><div className="eyebrow">02 / WHERE THINGS CHANGE</div><h2>变化发生在哪里</h2><p>将公司放回行业，再看经营证据是否也发生了变化。</p></div><span className="overview-scenario-tag">{SCENARIO_NAMES[scenario]}情景</span></div>
    <div className="overview-viz-grid overview-sector-grid"><Panel title="各行业的复核变化" description="同一可比样本中，公司年化回报中点的行业中位数。点击行业可联动筛选。"><SectorRevisions companies={companies} scenario={scenario} onSector={setSectorFromChart}/></Panel><Panel title="证据强度，也要前后对照" description="按同一组双报告公司，分别统计经营证据等级。"><EvidenceEvolution companies={companies} scenario={scenario}/></Panel></div>

    <div className="section-heading"><div><div className="eyebrow">03 / RISK & CHOICE</div><h2>从情景，走向公司选择</h2><p>价格空间、下行情景与配置裁决，分别展开阅读。</p></div></div>
    <div className="overview-viz-grid"><Panel title="回报与下行情景" description="横轴：悲观年化中点。纵轴：基准年化中点。点击公司进入完整研究。" action={<div className="segment"><button className={source==='scenario'?'active':''} onClick={()=>setSource('scenario')}>情景原报告</button><button className={source==='comparison'?'active':''} onClick={()=>setSource('comparison')}>对比复核后</button></div>}><Scatter companies={companies} source={source} onSelect={t=>navigate(source==='scenario'?'scenarios':'comparisons',t)}/><p className="chart-note">各公司使用自己报告的参考价与目标日，不含股息；跨公司目标日可能不同。点的颜色表示基准经营证据，不代表概率。</p></Panel><Panel title="三种配置判断的分布" description="来自公司对比复核报告，稳健、进攻和近期时机各自保留。"><DecisionDistribution companies={companies}/></Panel></div>
    <Panel title="六个视角，分别看" kicker="04 / SIX INDEPENDENT LENSES" description="长期经营有利，未必意味着当前价格有利。沿着六个维度，理解研究结论之间的差别。"><ViewDistribution companies={companies}/></Panel>

    {quickCompany?<div className="overview-quick-company"><div><span className="eyebrow">FROM THE ATLAS TO A COMPANY</span><h2>选一家公司，深入完整研究</h2><p>原始情景、对比复核、证据与推导都在公司页面。</p></div><div className="overview-quick-actions"><CompanySelect companies={companies} value={quickCompany.ticker} onChange={setQuickTicker}/><div><button className="button secondary" onClick={()=>navigate('scenarios',quickCompany.ticker)}>情景原报告<ArrowUpRight size={15}/></button><button className="button primary" onClick={()=>navigate('comparisons',quickCompany.ticker)}>对比复核<ArrowUpRight size={15}/></button></div></div></div>:<Empty hint="调整公司或行业筛选，继续探索研究图谱"/>}
  </div>;
}
