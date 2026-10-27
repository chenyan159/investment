import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { LayoutGrid, Layers3, GitCompareArrows, BookOpen, Compass, Menu, X, ChevronRight } from 'lucide-react';
import { useData, useRoute, navigate } from './lib';
import { Status } from './components';
import { Overview, CompanyPage, ResearchLibrary } from './pages';
import './styles.css';
import './boundaries.css';

const NAV=[{page:'overview',label:'研究总览',english:'Overview',icon:LayoutGrid},{page:'scenarios',label:'公司情景',english:'Scenarios',icon:Layers3},{page:'comparisons',label:'公司对比',english:'Comparisons',icon:GitCompareArrows},{page:'research',label:'研究资料',english:'Research library',icon:BookOpen},{page:'background',label:'产业背景',english:'Industry context',icon:Compass}];
class ErrorBoundary extends React.Component {
  constructor(props){super(props);this.state={error:null}}
  static getDerivedStateFromError(error){return {error}}
  render(){return this.state.error?<div className="app-error"><h1>这个视图暂时无法显示</h1><p>数据格式可能已更新，请重新加载。</p><button className="button primary" onClick={()=>window.location.reload()}>重新加载</button></div>:this.props.children}
}
function App(){
  const {data,error,loading}=useData('data/index.json');
  const route=useRoute();
  const [mobileOpen,setMobileOpen]=useState(false);
  const page=NAV.some(n=>n.page===route.page)?route.page:'overview';
  const go=(p,t='')=>{navigate(p,t);setMobileOpen(false)};
  const updated=data?.generatedAt?new Date(data.generatedAt).toLocaleDateString('zh-CN',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'America/Los_Angeles'}):'—';
  return <div className="app-shell"><a className="skip-link" href="#main-content" onClick={e=>{e.preventDefault();const main=document.getElementById('main-content');main?.focus();main?.scrollIntoView();}}>跳至主要内容</a>{mobileOpen&&<button className="sidebar-shade" aria-label="关闭导航" onClick={()=>setMobileOpen(false)}/>}<aside className={`sidebar ${mobileOpen?'open':''}`}><button className="brand" onClick={()=>go('overview')} aria-label="Project Ananta 首页"><span className="brand-symbol">a<span/></span><span>ANANTA<small>RESEARCH ATLAS</small></span></button><div className="sidebar-label">研究工作台</div><nav>{NAV.slice(0,3).map(({page:p,label,english,icon:Icon})=><button key={p} className={page===p?'active':''} onClick={()=>go(p,p==='overview'?'':route.ticker||'NVDA')}><Icon size={19}/><span>{label}<small>{english}</small></span>{page===p&&<ChevronRight size={15}/>}</button>)}</nav><div className="sidebar-label context-label">背景与依据</div><nav>{NAV.slice(3).map(({page:p,label,english,icon:Icon})=><button key={p} className={page===p?'active':''} onClick={()=>go(p)}><Icon size={18}/><span>{label}<small>{english}</small></span></button>)}</nav><div className="sidebar-bottom"><div className="sidebar-mark">∞</div><p>看清经营的可能。<br/>做有依据的选择。</p><div className="sidebar-divider"/><span><i/>正式研究 · 只读展示</span><small>PROJECT ANANTA / 2026</small></div></aside><main className="workspace" id="main-content" tabIndex={-1}><header className="topbar"><div><button className="mobile-menu icon-button" aria-label="打开导航" onClick={()=>setMobileOpen(!mobileOpen)}>{mobileOpen?<X size={21}/>:<Menu size={21}/>}</button><span className="breadcrumb">PROJECT ANANTA <ChevronRight size={13}/> {NAV.find(n=>n.page===page)?.label}</span></div><span className="freshness"><span className="status-dot"/>资料构建于 {updated}</span></header><div className="main-content">{loading||error?<Status loading={loading} error={error}/>:page==='overview'?<Overview data={data}/>:page==='scenarios'||page==='comparisons'?<CompanyPage key={`${page}-${route.ticker}`} data={data} ticker={route.ticker} mode={page}/>:<ResearchLibrary key={page} data={data} initialKind={page==='background'?'background':'all'}/>}<footer className="site-footer"><div><strong>ANANTA</strong><span>独立研究 · 条件推演 · 多维比较</span></div><p>价格为报告参考时点数据，不是实时行情。情景、证据等级和比较裁决保留原研究口径；请结合完整报告中的假设与限制阅读。</p><small>© 2026 Project Ananta</small></footer></div></main></div>
}
createRoot(document.getElementById('root')).render(<React.StrictMode><ErrorBoundary><App/></ErrorBoundary></React.StrictMode>);
