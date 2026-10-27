import React, {useMemo, useState} from 'react';
import {leaderRows} from './company-atlas-data';
import {label, num, percent} from './lib';
import './company-leaders.css';

export const LEADER_DIMENSIONS = {
  base:{title:'基准情景空间',description:'按基准情景年化回报中点排列。',color:'#277b68'},
  bear:{title:'悲观情景韧性',description:'按悲观情景年化回报中点排列，数值越高代表该情景下回撤较小或回报较高。',color:'#8a9f79'},
  bull:{title:'乐观情景空间',description:'按乐观情景年化回报中点排列。',color:'#4e85a7'},
  breakthrough:{title:'突破情景弹性',description:'按突破情景年化回报中点排列，需结合突破条件与证据阅读。',color:'#9c83ab'},
  steady:{title:'复核报告的稳健优选',description:'仅纳入复核裁决为“优先参与”的公司，再按基准年化回报中点排列。',color:'#277b68'},
  offense:{title:'复核报告的优先进攻',description:'仅纳入复核裁决为“优先进攻”的公司，再按突破年化回报中点排列。',color:'#ac865b'},
};
const evidenceText=value=>({strong:'强',medium:'中',weak:'弱',insufficient:'不足'}[value]||'未提供');

export function CompanyLeaders({companies,source='comparison',dimension='base',onSelect}) {
  const [active,setActive]=useState(null);
  const {rows,eligible}=useMemo(()=>leaderRows(companies,{source,dimension,limit:8}),[companies,source,dimension]);
  const definition=LEADER_DIMENSIONS[dimension];
  if(!rows.length)return <div className="cl-empty">当前筛选下没有符合这一维度的公司。</div>;
  const lo=Math.min(0,...rows.flatMap(r=>r.values)), hi=Math.max(0,...rows.flatMap(r=>r.values));
  const span=hi-lo||1, x=v=>205+(v-lo)/span*295, height=rows.length*58+62;
  const selected=rows.find(r=>r.ticker===active);
  return <div className="cl-chart">
    <div className="cl-caption"><span>{source==='comparison'?'对比复核后':'情景原报告'}</span><span>展示前 {rows.length} / {eligible} 家</span></div>
    <div className="cl-scroll" role="region" tabIndex={0} aria-label={`${definition.title}公司区间图，可横向滚动`}>
      <svg viewBox={`0 0 700 ${height}`} role="group" aria-label={`${definition.title}前${rows.length}家公司及年化区间`}>
        <line x1={x(0)} x2={x(0)} y1="12" y2={height-40} stroke="#b7c7b4" strokeDasharray="4 4"/>
        {rows.map((row,i)=>{const y=30+i*58;return <g key={row.ticker} role="button" tabIndex={0} aria-label={`${row.ticker} ${row.name}，年化中点${percent(row.score)}，区间${row.values.map(percent).join('至')}，证据${evidenceText(row.evidence)}`} onMouseEnter={()=>setActive(row.ticker)} onMouseLeave={()=>setActive(null)} onFocus={()=>setActive(row.ticker)} onBlur={()=>setActive(null)} onClick={()=>onSelect(row.ticker)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect(row.ticker)}}}>
          <rect x="0" y={y-24} width="700" height="53" rx="5" fill={active===row.ticker?'#edf3e7':i%2?'#fafbf7':'transparent'}/>
          <text x="8" y={y+2} className="cl-rank">{String(i+1).padStart(2,'0')}</text>
          <text x="39" y={y-3} className="cl-ticker">{row.ticker}</text>
          <text x="39" y={y+15} className="cl-company">{row.name.length>19?row.name.slice(0,18)+'…':row.name}</text>
          <line x1={x(row.values[0])} x2={x(row.values[1])} y1={y} y2={y} stroke={definition.color} strokeWidth="9" strokeLinecap="round"/>
          <circle cx={x(row.score)} cy={y} r="4" fill="white" stroke={definition.color} strokeWidth="2"/>
          <text x="525" y={y-3} className="cl-score">{percent(row.score)}</text>
          <text x="525" y={y+15} className="cl-range">{row.values.map(percent).join(' ~ ')}</text>
          <text x="686" y={y} textAnchor="end" className={`cl-evidence cl-evidence-${row.evidence}`}>{evidenceText(row.evidence)}</text>
          <title>{`${row.name} (${row.ticker}) · ${row.report.reference_price.date} → ${row.report.target_date} · 证据${evidenceText(row.evidence)}`}</title>
        </g>})}
        <text x="205" y={height-15} className="cl-axis">{percent(lo)}</text><text x="500" y={height-15} textAnchor="end" className="cl-axis">{percent(hi)}</text><text x="525" y={height-15} className="cl-axis">中点 / 区间</text><text x="686" y={height-15} textAnchor="end" className="cl-axis">证据</text>
      </svg>
    </div>
    <p className="cl-mobile-hint">↔ 左右滑动查看公司与完整区间</p>
    <div className="cl-readout" aria-live="polite">{selected?<><strong>{selected.name} · {selected.ticker}</strong><span>参考价 {num(selected.report.reference_price.value,2)} {selected.report.reference_price.currency}</span><span>{selected.report.reference_price.date} → {selected.report.target_date}</span><span>证据{label(selected.evidence)}</span></>:<span>横线是年化区间，圆点是区间中点。点击公司进入完整研究。</span>}</div>
  </div>;
}
