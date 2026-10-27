import React, { useId, useMemo, useState } from 'react';
import { atlasPoints, scatterMeta } from './company-atlas-data';
import { num, label } from './lib';
import './company-atlas-charts.css';

const PALETTE={strong:'#247965',medium:'#83a68e',weak:'#c3a06a',insufficient:'#a5aaa1',missing:'#a5aaa1'};
const EVIDENCE=['弱','中','强','不足 / 未提供'];
const percent=value=>`${value>0?'+':''}${num(value,2)}%`;
const unitValue=(value,unit)=>unit==='category'?EVIDENCE[Math.round(value)]||'未提供':unit==='pp'||unit==='percentage_points'?`${num(value,2)} 个百分点`:percent(value);
const finite=value=>typeof value==='number'&&Number.isFinite(value);
function paddedDomain(values,floor=-100){const min=Math.min(0,...values),max=Math.max(0,...values);const pad=Math.max(2,(max-min)*.09);return [Math.max(floor,min-pad),max+pad];}
function axisTicks(min,max,count=5){return Array.from({length:count},(_,i)=>min+(max-min)*i/(count-1));}
function jitter(ticker){let value=2166136261;for(const ch of ticker)value=Math.imul(value^ch.charCodeAt(0),16777619);return ((value>>>0)%1000/999-.5)*.24;}
function shortUnit(value,unit){return unit==='pp'||unit==='percentage_points'?`${num(value,1)} pp`:`${num(value,1)}%`;}
function overlaps(a,b){return a.x < b.x+b.w+5 && a.x+a.w+5>b.x && a.y < b.y+b.h+4 && a.y+a.h+4>b.y;}

function placeLabels(points,xScale,yScale,left,right,top,bottom){
  const boxes=[];
  for(const point of points){
    const px=xScale(point),py=yScale(point.y),width=Math.max(38,point.ticker.length*7.1+14),height=21;
    const direction=px>(left+right)*.5?-1:1;
    const candidates=[];
    for(const offset of [-16,20,-36,40,-56,60,-76,80,-96,100])for(const dir of [direction,-direction]){
      const x=Math.max(left+2,Math.min(right-width-2,px+(dir>0?10:-width-10)));
      const y=Math.max(top+1,Math.min(bottom-height,py+offset-height/2));
      candidates.push({x,y,w:width,h:height,px,py,point});
    }
    const chosen=candidates.find(candidate=>!boxes.some(box=>overlaps(candidate,box)))||candidates[0];
    boxes.push(chosen);
  }
  return boxes;
}

export function CompanyScatter({companies=[],source='comparison',mode='risk_return',onSelect=()=>{}}){
  const meta=scatterMeta(mode);
  const points=useMemo(()=>atlasPoints(companies,source,mode).filter(point=>finite(point.x)&&finite(point.y)),[companies,source,mode]);
  const [active,setActive]=useState(null);
  const id=useId();
  const selected=points.find(point=>point.ticker===active);
  const leaders=useMemo(()=>[...points].sort((a,b)=>b.y-a.y||a.ticker.localeCompare(b.ticker)).slice(0,6),[points]);
  const leaderSet=new Set(leaders.map(point=>point.ticker));
  const categorical=meta.categorical||mode==='evidence_return';
  const [xmin,xmax]=paddedDomain(points.map(point=>point.x),mode==='range_return'?0:-100);
  const [ymin,ymax]=paddedDomain(points.map(point=>point.y));
  const left=68,right=668,top=45,bottom=344;
  const scaleXValue=value=>left+(value-xmin)/(xmax-xmin)*(right-left);
  const scaleX=point=>categorical?left+(point.x+.5+jitter(point.ticker))/4*(right-left):scaleXValue(point.x);
  const scaleY=value=>bottom-(value-ymin)/(ymax-ymin)*(bottom-top);
  const annotated=selected&&!leaderSet.has(selected.ticker)?[selected,...leaders]:leaders;
  const labels=placeLabels(annotated,scaleX,scaleY,left,right,top,bottom);
  const ordered=[...points.filter(point=>!leaderSet.has(point.ticker)),...leaders];
  const empty=!points.length;
  return <div className="ca-chart">
    <div className="ca-chart-header"><div><strong>{points.length}</strong><span>家公司形成有效坐标</span></div><span className="ca-sample-scope">筛选范围 {companies.length} 家 · 未绘制 {companies.length-points.length} 家</span></div>
    {empty?<div className="ca-empty">当前筛选没有满足两项指标的完整数据。请调整公司或来源筛选。</div>:<>
      <div className="ca-plot-scroll" role="region" tabIndex={0} aria-label={`${meta.title||'公司散点图'}，可横向滚动`}>
        <svg className="ca-svg" viewBox="0 0 720 405" role="group" aria-label={`${meta.xLabel}与${meta.yLabel}公司分布`}>
          <text x={left} y="21" className="ca-axis-title">{meta.yLabel} ↑</text>
          <rect x={left} y={top} width={right-left} height={bottom-top} fill="#fafcf7"/>
          {categorical&&EVIDENCE.map((name,index)=><g key={name}><rect x={left+index*(right-left)/4} y={top} width={(right-left)/4} height={bottom-top} fill={index%2===0?'#f2f6eb':'#fafcf7'}/><text x={left+(index+.5)*(right-left)/4} y="369" textAnchor="middle" className="ca-tick ca-category-tick">{name}</text></g>)}
          {axisTicks(ymin,ymax).map(value=><g key={value}><line x1={left} x2={right} y1={scaleY(value)} y2={scaleY(value)} className="ca-grid"/><text x={left-11} y={scaleY(value)+4} textAnchor="end" className="ca-tick">{num(value,1)}%</text></g>)}
          {!categorical&&axisTicks(xmin,xmax).map(value=><g key={value}><line x1={scaleXValue(value)} x2={scaleXValue(value)} y1={top} y2={bottom} className="ca-grid"/><text x={scaleXValue(value)} y="369" textAnchor="middle" className="ca-tick">{shortUnit(value,meta.xUnit)}</text></g>)}
          {!categorical&&xmin<0&&xmax>0&&<line x1={scaleXValue(0)} x2={scaleXValue(0)} y1={top} y2={bottom} className="ca-zero"/>}
          {ymin<0&&ymax>0&&<line x1={left} x2={right} y1={scaleY(0)} y2={scaleY(0)} className="ca-zero"/>}
          <text x={right} y="396" textAnchor="end" className="ca-axis-title">{meta.xLabel} →</text>
          {ordered.map(point=>{const emphasized=leaderSet.has(point.ticker)||selected?.ticker===point.ticker;return <g key={point.ticker} tabIndex={0} role="button" aria-label={`${point.ticker} ${point.name}，${meta.xLabel}${unitValue(point.x,meta.xUnit)}，${meta.yLabel}${unitValue(point.y,meta.yUnit)}，点击打开研究`} aria-describedby={selected?.ticker===point.ticker?id:undefined} onMouseEnter={()=>setActive(point.ticker)} onFocus={()=>setActive(point.ticker)} onClick={()=>onSelect(point.ticker)} onKeyDown={event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();onSelect(point.ticker);}}}>
            <circle cx={scaleX(point)} cy={scaleY(point.y)} r={selected?.ticker===point.ticker?7:emphasized?6:4.4} fill={PALETTE[point.evidence]||PALETTE.missing} stroke={emphasized?'#28523f':'#fff'} strokeWidth={emphasized?1.5:1} opacity={selected&&selected.ticker!==point.ticker&&!leaderSet.has(point.ticker)?0.4:.9}/>
            <title>{`${point.ticker} ${point.name}\n${meta.xLabel}：${unitValue(point.x,meta.xUnit)}\n${meta.yLabel}：${unitValue(point.y,meta.yUnit)}\n研究 ${point.report?.research_date||'未注明'}；报价 ${point.report?.reference_price?.date||'未注明'}；目标 ${point.report?.target_date||'未注明'}`}</title>
          </g>})}
          {labels.map(box=><g key={box.point.ticker} className={`ca-point-annotation ${selected?.ticker===box.point.ticker?'ca-point-annotation-active':''}`} aria-hidden="true" pointerEvents="none"><line x1={box.px} y1={box.py} x2={box.x+box.w/2} y2={box.y+box.h/2} stroke="#829b73" strokeWidth=".8"/><rect x={box.x} y={box.y} width={box.w} height={box.h} rx="4"/><text x={box.x+7} y={box.y+14.5}>{box.point.ticker}</text></g>)}
        </svg>
      </div>
      <p className="ca-scroll-hint">↔ 左右滑动查看完整公司图谱</p>
      <div className="ca-legend"><span><i style={{background:PALETTE.strong}}/>基准证据强</span><span><i style={{background:PALETTE.medium}}/>中</span><span><i style={{background:PALETTE.weak}}/>弱</span><span><i style={{background:PALETTE.missing}}/>不足 / 未提供</span></div>
      <div className="ca-leaders"><span>纵轴数值最高的 {leaders.length} 家</span><div>{leaders.map(point=><button key={point.ticker} className={active===point.ticker?'active':''} onMouseEnter={()=>setActive(point.ticker)} onFocus={()=>setActive(point.ticker)} onClick={()=>onSelect(point.ticker)}><strong>{point.ticker}</strong><span>{percent(point.y)}</span></button>)}</div></div>
      <div className={`ca-detail ${selected?'is-selected':''}`} id={id} aria-live="polite">{selected?<><div className="ca-detail-company"><strong>{selected.ticker}</strong><span>{selected.name}</span><button onClick={()=>onSelect(selected.ticker)}>进入报告 ↗</button></div><div className="ca-detail-values"><div><small>{meta.xLabel}</small><b>{unitValue(selected.x,meta.xUnit)}</b></div><div><small>{meta.yLabel}</small><b>{unitValue(selected.y,meta.yUnit)}</b></div><div><small>基准经营证据</small><b>{label(selected.evidence)}</b></div><div><small>研究日 / 报价日</small><b>{selected.report?.research_date||'未注明'} / {selected.report?.reference_price?.date||'未注明'}</b></div><div><small>目标日</small><b>{selected.report?.target_date||'未注明'}</b></div><div><small>参考价</small><b>{num(selected.report?.reference_price?.value,2)} {selected.report?.reference_price?.currency||''}</b></div></div></>:<div className="ca-detail-placeholder">每个点对应一家公司。悬浮或键盘聚焦查看完整身份、数值与报告日期，点击点或公司代码进入研究。</div>}</div>
    </>}
    <p className="ca-note">绘制 {points.length} 家 / 筛选 {companies.length} 家。价格回报按各自报告的参考价与实际目标年限年化，不含股息；报告日期、币种和目标日可能不同。标注公司按纵轴数值选取，不构成推荐排序。</p>
    {categorical&&<p className="ca-note ca-note-tight">横轴是证据分类，不是分数；同类点的轻微横向错位仅用于减少重叠。证据等级不代表情景发生概率。</p>}
    {mode==='range_return'&&<p className="ca-note ca-note-tight">区间宽度 = 基准年化区间上限 − 下限，单位为百分点；它描述报告区间跨度，不是统计波动率。</p>}
  </div>;
}
