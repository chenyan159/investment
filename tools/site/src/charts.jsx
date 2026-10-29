import React, { useMemo, useState } from 'react';
import { SCENARIOS, SCENARIO_NAMES, COLORS, bounds, num, price, percent, returnRange, annualRange, midpoint, label } from './lib';

export function RangeChart({report,comparison=null,mode='price',targetLabel='情景报告目标交易价'}) {
  const [hover,setHover]=useState(null);
  const rows=SCENARIOS.map(key=>({key,values:mode==='return'?returnRange(report,key):bounds(report?.scenarios?.[key]?.target_price),dcf:mode==='price'?bounds(report?.scenarios?.[key]?.dcf_price):[],business:mode==='price'?bounds(report?.scenarios?.[key]?.business_price):[],revised:comparison?(mode==='return'?returnRange(comparison,key):bounds(comparison?.scenarios?.[key]?.target_price)):[]}));
  const all=rows.flatMap(x=>[...x.values,...x.dcf,...x.business,...x.revised]);
  if(!all.length)return <div className="empty-chart">当前报告无可用价格。请阅读证券状态与适用边界。</div>;
  const ref=mode==='return'?0:report?.reference_price?.value;
  const min=Math.min(mode==='return'?-10:0,...all),max=Math.max(...all,ref||0)*1.08;
  const x=v=>95+(v-min)/(max-min||1)*660;
  const ticks=Array.from({length:5},(_,i)=>min+(max-min)*i/4);
  return <div className="chart"><svg viewBox="0 0 830 295" role="img" aria-label="四种经营情景目标价格区间图"><rect width="830" height="295" fill="transparent"/>{ticks.map(t=><g key={t}><line x1={x(t)} x2={x(t)} y1="20" y2="245" stroke="#e7ebe8" strokeDasharray="3 5"/><text x={x(t)} y="275" textAnchor="middle" className="chart-label">{mode==='return'?percent(t):price(t)}</text></g>)}{typeof ref==='number'&&<g><line x1={x(ref)} x2={x(ref)} y1="18" y2="246" stroke="#354c48" strokeDasharray="5 4"/><text x={x(ref)+5} y="12" className="chart-label">{mode==='return'?'参考买价':'参考价 '+price(ref)}</text></g>}{rows.map((row,i)=>{const y=48+i*57;return <g key={row.key} onMouseEnter={()=>setHover(row.key)} onMouseLeave={()=>setHover(null)}><rect x="0" y={y-24} width="830" height="53" fill={hover===row.key?'#f4f6f3':'transparent'}/><text x="12" y={y+4} className="chart-row-label">{SCENARIO_NAMES[row.key]}</text>{row.values.length?<><line x1={x(row.values[0])} x2={x(row.values[row.values.length-1])} y1={y} y2={y} stroke={COLORS[row.key]} strokeWidth="12" strokeLinecap="round"/><circle cx={x(row.values[0])} cy={y} r="3" fill="white"/><circle cx={x(row.values[row.values.length-1])} cy={y} r="3" fill="white"/><title>{`${SCENARIO_NAMES[row.key]}目标区间：${row.values.map(v=>mode==='return'?percent(v):price(v)).join(' 至 ')}`}</title></>:<text x="100" y={y+4} className="chart-label">未提供</text>}{row.dcf.length>0&&<g><circle cx={x(midpoint(row.dcf))} cy={y} r="5" fill="#fff" stroke="#253d39" strokeWidth="2"/><title>DCF：{row.dcf.map(price).join(' – ')}</title></g>}{row.business.length>0&&<g><path d={`M${x(midpoint(row.business))} ${y-6}l6 6-6 6-6-6z`} fill="#daa554" stroke="white"/><title>纯业务参考价：{row.business.map(price).join(' – ')}</title></g>}{row.revised.length>0&&<g><line x1={x(row.revised[0])} x2={x(row.revised[row.revised.length-1])} y1={y+16} y2={y+16} stroke="#152f2c" strokeWidth="4" strokeLinecap="round"/><title>对比复核后：{row.revised.map(v=>mode==='return'?percent(v):price(v)).join(' – ')}</title></g>}</g>})}</svg><div className="chart-legend"><span><i className="legend-line"/>{targetLabel}</span>{mode==='price'&&rows.some(r=>r.dcf.length)&&<span><i className="legend-dot"/>DCF 参考价</span>}{mode==='price'&&rows.some(r=>r.business.length)&&<span><i className="legend-diamond"/>纯业务参考价</span>}{comparison&&<span><i className="legend-line dark"/>对比报告复核价</span>}</div></div>;
}

export function Scatter({companies,selected,onSelect,source='comparison'}) {
  const [hover,setHover]=useState(null);
  const points=useMemo(()=>companies.map(c=>{const report=c[source];return {c,x:midpoint(annualRange(report,'bear')),y:midpoint(annualRange(report,'base')),evidence:report?.scenarios?.base?.evidence};}).filter(p=>p.x!==null&&p.y!==null),[companies,source]);
  if(!points.length)return <div className="empty-chart">当前筛选下没有可比较的完整情景价格。</div>;
  const xmin=Math.min(-5,...points.map(p=>p.x))-5,xmax=Math.max(5,...points.map(p=>p.x))+5,ymin=Math.min(0,...points.map(p=>p.y))-3,ymax=Math.max(5,...points.map(p=>p.y))+5;
  const x=v=>65+(v-xmin)/(xmax-xmin)*650,y=v=>310-(v-ymin)/(ymax-ymin)*270;
  const xt=Array.from({length:5},(_,i)=>xmin+(xmax-xmin)*i/4),yt=Array.from({length:5},(_,i)=>ymin+(ymax-ymin)*i/4);
  const palette={strong:'#267b6c',medium:'#7e9d8c',weak:'#c99a64',insufficient:'#a8aaa4'};
  const shown=points.find(p=>p.c.ticker===hover);
  return <div className="chart scatter"><svg viewBox="0 0 780 380" role="img" aria-label="公司悲观和基准情景年化价格回报分布"><rect x="65" y="40" width="650" height="270" fill="#fbfcf9"/>{yt.map(t=><g key={t}><line x1="65" x2="715" y1={y(t)} y2={y(t)} stroke="#e7ebe8"/><text x="52" y={y(t)+4} textAnchor="end" className="chart-label">{num(t,0)}%</text></g>)}{xt.map(t=><g key={t}><line x1={x(t)} x2={x(t)} y1="40" y2="310" stroke="#e7ebe8"/><text x={x(t)} y="332" textAnchor="middle" className="chart-label">{num(t,0)}%</text></g>)}<line x1={x(0)} x2={x(0)} y1="40" y2="310" stroke="#b9c6bf" strokeDasharray="4 4"/><line x1="65" x2="715" y1={y(0)} y2={y(0)} stroke="#b9c6bf" strokeDasharray="4 4"/><text x="65" y="21" className="chart-axis">基准情景年化价格回报 ↑</text><text x="715" y="365" textAnchor="end" className="chart-axis">悲观情景年化价格回报 →</text>{points.map(p=><g key={p.c.ticker} tabIndex="0" role="button" aria-label={`${p.c.ticker}，悲观年化${percent(p.x)}，基准年化${percent(p.y)}`} onClick={()=>onSelect(p.c.ticker)} onKeyDown={e=>{if(e.key==='Enter')onSelect(p.c.ticker);}} onMouseEnter={()=>setHover(p.c.ticker)} onMouseLeave={()=>setHover(null)} onFocus={()=>setHover(p.c.ticker)}><circle cx={x(p.x)} cy={y(p.y)} r={selected===p.c.ticker||hover===p.c.ticker?7:4.5} fill={palette[p.evidence]||'#a8aaa4'} stroke={hover===p.c.ticker||selected===p.c.ticker?'#163f36':'white'} strokeWidth={hover===p.c.ticker?2:1} opacity={hover&&hover!==p.c.ticker?.toString()?.trim()?0.45:0.9}/>{(hover===p.c.ticker||selected===p.c.ticker)&&<text x={Math.min(x(p.x)+10,678)} y={y(p.y)-10} className="chart-point-label">{p.c.ticker}</text>}<title>{`${p.c.name} (${p.c.ticker})\n悲观年化 ${percent(p.x)}\n基准年化 ${percent(p.y)}`}</title></g>)}</svg><div className="scatter-footer"><div className="chart-legend"><span><i style={{background:palette.strong}}/>证据强</span><span><i style={{background:palette.medium}}/>证据中</span><span><i style={{background:palette.weak}}/>证据弱</span></div><span className="micro">{shown?`${shown.c.ticker} · 基准 ${percent(shown.y)}`:`${points.length} 家 · 点击查看公司`}</span></div></div>;
}

export function OutcomeBar({comparisons=[]}) {
  const keys=['target_preferred','peer_preferred','split_by_mandate','comparable','both_avoid','insufficient'];
  const palette=['#267b6c','#bc775c','#d8b56e','#91a3ad','#735f63','#c7ccc6'];
  const counts=keys.map(key=>comparisons.filter(c=>c.verdict===key).length);
  const other=comparisons.length-counts.reduce((a,b)=>a+b,0);
  if(other){keys.push('其他裁决');counts.push(other);palette.push('#999');}
  return <div className="outcome"><div className="outcome-track" role="img" aria-label={keys.map((k,i)=>`${label(k)} ${counts[i]}家`).join('，')}>{keys.map((key,i)=>counts[i]>0&&<div key={key} style={{width:`${counts[i]/comparisons.length*100}%`,background:palette[i]}} title={`${label(key)}：${counts[i]}`}>{counts[i]}</div>)}</div><div className="outcome-legend">{keys.map((k,i)=>counts[i]>0&&<span key={k}><i style={{background:palette[i]}}/>{label(k)}<strong>{counts[i]}</strong></span>)}</div></div>;
}

export function EvidenceGrid({companies,source='scenario',onSelect}) {
  const palette={strong:'#267b6c',medium:'#99b8a6',weak:'#d7b78a',insufficient:'#dadeda'};
  return <div className="evidence-grid" role="list" aria-label="公司基准情景证据分布">{companies.filter(c=>c[source]).map(c=><button key={c.ticker} role="listitem" title={`${c.ticker} ${c.name} · 基准证据${label(c[source].scenarios?.base?.evidence)}`} style={{background:palette[c[source].scenarios?.base?.evidence]||'#dadeda'}} onClick={()=>onSelect(c.ticker)}><span>{c.ticker}</span></button>)}</div>;
}

export function ScenarioComparisonBars({companies,scenario='base',source='comparison'}) {
  const rows=companies.map(c=>({c,values:annualRange(c[source],scenario)})).filter(r=>r.values.length);
  if(!rows.length)return <div className="empty-chart">所选公司没有同口径的可用年化区间。</div>;
  const min=Math.min(0,...rows.flatMap(r=>r.values)),max=Math.max(0,...rows.flatMap(r=>r.values));
  const x=v=>120+(v-min)/(max-min||1)*560;
  const height=rows.length*48+60;
  return <div className="chart"><svg viewBox={`0 0 780 ${height}`} role="img" aria-label="所选公司年化回报区间比较"><line x1={x(0)} x2={x(0)} y1="10" y2={height-35} stroke="#a8b9b0" strokeDasharray="4 4"/>{rows.map(({c,values},i)=><g key={c.ticker}><text x="10" y={i*48+31} className="chart-row-label">{c.ticker}</text><line x1={x(values[0])} x2={x(values[values.length-1])} y1={i*48+26} y2={i*48+26} stroke={COLORS[scenario]} strokeWidth="12" strokeLinecap="round"/><text x={x(values[values.length-1])+12} y={i*48+31} className="chart-label">{percent(midpoint(values))}</text><title>{c.ticker}：{values.map(percent).join(' 至 ')}</title></g>)}<text x="120" y={height-10} className="chart-label">{percent(min)}</text><text x="680" y={height-10} textAnchor="end" className="chart-label">{percent(max)}</text></svg></div>;
}
