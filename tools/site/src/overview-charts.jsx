import React, { useMemo, useState } from 'react';
import { comparablePairs, classifyRevision } from './overview-data';
import { percent, num, SCENARIO_NAMES } from './lib';
import './overview-charts.css';

const GREEN = '#277b68', DOWN = '#b47a64', SAME = '#9caf9c';
const ticks = (min, max, count = 5) => Array.from({ length: count }, (_, i) => min + (max - min) * i / (count - 1));
function domain(values) { const lo = Math.min(0, ...values), hi = Math.max(0, ...values); const pad = Math.max(3, (hi - lo) * .08); return [lo - pad, hi + pad]; }
function NoData() {return <div className="ov-empty">当前筛选没有符合口径的研究样本。</div>;}
function BasisNote({count,excluded}) {return <p className="ov-note">{count} 家可比公司；排除 {excluded} 家。仅纳入参考价、报价日、币种、目标日完全一致且具备有效区间的双报告。年化回报不含股息。</p>;}
function activate(event, action) {if(event.key==='Enter'||event.key===' '){event.preventDefault();action();}}

export function RevisionScatter({companies=[],scenario='base',onSelect=()=>{}}) {
  const sample = useMemo(()=>comparablePairs(companies,scenario),[companies,scenario]);
  const [active,setActive] = useState(null);
  const {pairs} = sample;
  if(!pairs.length)return <div><NoData/><BasisNote count={0} excluded={sample.excluded}/></div>;
  const [lo,hi]=domain(pairs.flatMap(p=>[p.original,p.revised]));
  const x=v=>58+(v-lo)/(hi-lo)*588, y=v=>328-(v-lo)/(hi-lo)*284;
  const selected=pairs.find(p=>p.ticker===active);
  return <div className="ov-revision"><div className="ov-revision-stats"><span><i style={{background:GREEN}}/>上调 <strong>{sample.up}</strong></span><span><i style={{background:DOWN}}/>下调 <strong>{sample.down}</strong></span><span><i style={{background:SAME}}/>基本不变 <strong>{sample.unchanged}</strong></span></div><div className="ov-plot-scroll" tabIndex={0} role="region" aria-label="图表，可横向滚动"><svg className="ov-svg" viewBox="0 0 700 385" role="group" aria-label={`${SCENARIO_NAMES[scenario]}情景原报告与复核后年化回报对照散点图`}><text x="58" y="18" className="ov-axis-title">复核后年化中点 ↑</text><rect x="58" y="44" width="588" height="284" fill="#fafbf7"/>{ticks(lo,hi).map(t=><g key={t}><line x1="58" x2="646" y1={y(t)} y2={y(t)} className="ov-grid"/><line x1={x(t)} x2={x(t)} y1="44" y2="328" className="ov-grid"/><text x="47" y={y(t)+4} textAnchor="end" className="ov-tick">{num(t,0)}%</text><text x={x(t)} y="349" textAnchor="middle" className="ov-tick">{num(t,0)}%</text></g>)}<line x1={x(lo)} y1={y(lo)} x2={x(hi)} y2={y(hi)} stroke="#b4bfae" strokeWidth="1.5" strokeDasharray="5 5"/><text x="646" y="377" textAnchor="end" className="ov-axis-title">原报告年化中点 →</text>{pairs.map(p=>{const color=classifyRevision(p.delta)==='up'?GREEN:classifyRevision(p.delta)==='down'?DOWN:SAME;return <g key={p.ticker} tabIndex="0" role="button" aria-label={`${p.ticker}，原报告${percent(p.original)}，复核后${percent(p.revised)}，变化${num(p.delta,2)}个百分点`} onMouseEnter={()=>setActive(p.ticker)} onMouseLeave={()=>setActive(null)} onFocus={()=>setActive(p.ticker)} onBlur={()=>setActive(null)} onClick={()=>onSelect(p.ticker)} onKeyDown={e=>activate(e,()=>onSelect(p.ticker))}><circle cx={x(p.original)} cy={y(p.revised)} r={active===p.ticker?6.5:4.2} fill={color} stroke={active===p.ticker?'#224e3b':'white'} strokeWidth={active===p.ticker?1.5:1} opacity={active&&active!==p.ticker?.toString()?0.4:0.87}/><title>{`${p.name} (${p.ticker}) · 原报告 ${percent(p.original)} → 复核 ${percent(p.revised)}`}</title>{active===p.ticker&&<text x={Math.min(x(p.original)+9,599)} y={Math.max(y(p.revised)-10,36)} className="ov-point-label">{p.ticker}</text>}</g>})}</svg></div><p className="ov-scroll-hint">↔ 左右滑动查看完整图表</p><div className="ov-focus-readout" aria-live="polite">{selected?<><strong>{selected.ticker}</strong><span>原报告 {percent(selected.original)}</span><span>→ 复核 {percent(selected.revised)}</span><b className={classifyRevision(selected.delta)==='down'?'ov-down':classifyRevision(selected.delta)==='up'?'ov-up':'ov-unchanged'}>{selected.delta>0?'+':''}{num(selected.delta,2)} 个百分点</b></>:<span>虚线为原报告 = 复核后；悬浮或键盘聚焦查看数值，点击进入公司。</span>}</div><BasisNote count={pairs.length} excluded={sample.excluded}/><p className="ov-note ov-note-tight">“基本不变”定义为年化中点变化不超过 ±0.1 个百分点；区间中点不是预测期望收益。</p></div>;
}
