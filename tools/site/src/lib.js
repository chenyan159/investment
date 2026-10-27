import { useEffect, useState } from 'react';

export const SCENARIOS = ['bear', 'base', 'bull', 'breakthrough'];
export const SCENARIO_NAMES = {bear:'悲观',base:'基准',bull:'乐观',breakthrough:'突破'};
export const COLORS = {bear:'#b86c55',base:'#27766a',bull:'#4a84ab',breakthrough:'#9a79b0'};
export const LABELS = {
  strong:'强',medium:'中',weak:'弱',unknown:'未明确',
  positive:'有利',mixed:'利弊并存',negative:'不利',neutral:'中性',uncertain:'不确定',
  adopt:'采用',revise:'修正',reestimate:'重新估计',reject:'不采用',insufficient:'证据不足',
  conditional_wait:'有条件等待',small_option_bet:'小额期权式参与',wait_for_trigger:'等待触发条件',both_avoid:'双方回避',value_chain:'价值链关联',
  target_preferred:'本公司占优',peer_preferred:'对手占优',comparable:'大致相当',split_by_mandate:'分视角取舍',insufficient_evidence:'证据不足',
  direct_competitor:'直接竞争',alternative:'替代路线',upstream:'上游',downstream:'下游',adjacent:'相邻环节',opportunity_cost:'机会成本',
  preferred_participate:'优先参与',participate:'可以参与',selective_participate:'选择性参与',watch:'观察',avoid:'回避',wait:'等待',
  high_priority_offense:'优先进攻',selective_offense:'选择性进攻',limited_offense:'有限进攻',not_suitable:'不适合',
  build_now:'当前分批建立',wait_for_pullback:'等待回调',wait_for_evidence:'等待验证',hold:'持有观察',reduce:'降低配置',
  steady_allocation:'稳健配置',offense_allocation:'进攻配置',near_term_timing:'近期时机',
  near_term_delivery:'近期兑现',long_term_compounding:'长期复利',base_valuation:'基准价格赔率',upside_potential:'上行情景潜力',downside_resilience:'下行韧性',relative_attractiveness:'相对吸引力',
};
export const label = value => LABELS[value] || value || '未提供';
export const num = (v,d=1) => typeof v==='number' && Number.isFinite(v) ? v.toLocaleString('zh-CN',{maximumFractionDigits:d}) : '—';
export const percent = v => typeof v==='number' && Number.isFinite(v) ? `${v>0?'+':''}${num(v,1)}%` : '—';
export const price = v => num(v,2);
export const bounds = v => Array.isArray(v) ? v.filter(x=>typeof x==='number'&&Number.isFinite(x)) : typeof v==='number' ? [v,v] : [];
export function returnRange(report,key='base',field='target_price') {
  const ref=report?.reference_price?.value;
  if (!(ref>0)) return [];
  return bounds(report?.scenarios?.[key]?.[field]).map(x=>(x/ref-1)*100);
}
export function midpoint(range) {return range?.length ? (range[0]+range[range.length-1])/2 : null;}
export function annualRange(report,key='base') {
  const ref=report?.reference_price?.value;
  const years=(Date.parse(report?.target_date)-Date.parse(report?.reference_price?.date))/(365.25*86400000);
  if (!(ref>0&&years>0)) return [];
  return bounds(report?.scenarios?.[key]?.target_price).map(x=>(Math.pow(x/ref,1/years)-1)*100);
}
export const rangeText = (xs,formatter=price) => xs?.length ? xs[0]===xs[xs.length-1] ? formatter(xs[0]) : `${formatter(xs[0])} – ${formatter(xs[xs.length-1])}` : '未提供';
export const cleanText = (s='') => String(s).replace(/\[([^\]]+)\]\([^)]+\)/g,'$1').replace(/[#*`_>]/g,'').replace(/<[^>]+>/g,'').trim();
export function useData(url) {
  const [state,setState]=useState({data:null,error:null,loading:true});
  useEffect(()=>{if(!url){setState({data:null,error:null,loading:false});return;} const ctrl=new AbortController();setState({data:null,error:null,loading:true});fetch(url,{signal:ctrl.signal,cache:'no-cache'}).then(r=>{if(!r.ok)throw new Error(`数据读取失败 (${r.status})`);return r.json();}).then(data=>setState({data,error:null,loading:false})).catch(e=>{if(e.name!=='AbortError')setState({data:null,error:e.message,loading:false});});return()=>ctrl.abort();},[url]);
  return state;
}
export function navigate(page,ticker='') {window.location.hash=`${page}${ticker?'/'+encodeURIComponent(ticker):''}`;}
export function useRoute() {
  const read=()=>{const [page='overview',ticker='']=window.location.hash.replace(/^#/,'').split('/');return {page,ticker:decodeURIComponent(ticker)}};
  const [route,setRoute]=useState(read);
  useEffect(()=>{const fn=()=>{setRoute(read());window.scrollTo({top:0,behavior:'instant'});};window.addEventListener('hashchange',fn);return()=>window.removeEventListener('hashchange',fn);},[]);
  return route;
}
export function tone(value) {if(['positive','target_preferred','strong','adopt'].includes(value))return 'good';if(['negative','peer_preferred','reject','weak'].includes(value))return 'bad';return 'neutral';}
