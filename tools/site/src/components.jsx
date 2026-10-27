import React, { useMemo, useState, useEffect } from 'react';
import { ArrowUpRight, Search, ChevronDown, X, FileText, Download, ArrowLeft, ExternalLink, AlertCircle, ChevronRight } from 'lucide-react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { label, tone, cleanText, num, useData } from './lib';

export function Badge({children,variant=''}) {return <span className={`badge ${variant}`}>{children}</span>}
export function Status({loading,error}) {return <div className="state-panel">{loading?<><div className="spinner"/><p>正在读取研究资料…</p></>:<><AlertCircle size={30}/><h3>暂时无法读取数据</h3><p>{error}</p><button className="button" onClick={()=>window.location.reload()}>重新加载</button></>}</div>}
export function Empty({children='没有匹配的资料',hint}) {return <div className="empty"><Search size={26}/><h3>{children}</h3>{hint&&<p>{hint}</p>}</div>}
export function Panel({title,kicker,description,action,children,className=''}) {return <section className={`panel ${className}`}><div className="panel-head"><div>{kicker&&<div className="eyebrow">{kicker}</div>}<h2>{title}</h2>{description&&<p>{description}</p>}</div>{action}</div>{children}</section>}
export function SearchBox({value,onChange,placeholder='搜索公司名称或代码'}) {return <div className="search-box"><Search size={17}/><input aria-label={placeholder} value={value} onChange={e=>onChange(e.target.value)} placeholder={placeholder}/>{value&&<button className="icon-button" aria-label="清除搜索" onClick={()=>onChange('')}><X size={16}/></button>}</div>}
export function CompanySelect({companies,value,onChange}) {
  const [open,setOpen]=useState(false),[query,setQuery]=useState('');
  const company=companies.find(c=>c.ticker===value);
  const items=companies.filter(c=>`${c.ticker} ${c.name} ${c.sector}`.toLowerCase().includes(query.toLowerCase()));
  return <div className="company-select"><button className="company-select-trigger" aria-expanded={open} onClick={()=>setOpen(!open)}><span className="ticker-box">{value?.slice(0,4)||'?'}</span><span><strong>{company?.name||value||'选择公司'}</strong><small>{value} · {company?.sector||'研究对象'}</small></span><ChevronDown size={17}/></button>{open&&<><button className="select-overlay" aria-label="关闭公司选择" onClick={()=>setOpen(false)}/><div className="company-options"><SearchBox value={query} onChange={setQuery}/><div>{items.map(c=><button key={c.ticker} className={c.ticker===value?'selected':''} onClick={()=>{onChange(c.ticker);setOpen(false);setQuery('');}}><strong>{c.ticker}</strong><span>{c.name}</span><small>{c.sector}</small></button>)}{!items.length&&<Empty/>}</div></div></>}</div>;
}
export function ReportButton({onClick,label:buttonLabel='阅读完整报告'}) {return <button className="button secondary" onClick={onClick}><FileText size={16}/>{buttonLabel}<ArrowUpRight size={15}/></button>}
export function InlineValue({value}) {return <Badge variant={tone(value)}>{label(value)}</Badge>}

export function Markdown({text}) {
  const html=useMemo(()=>DOMPurify.sanitize(marked.parse(text||'',{gfm:true,breaks:false}),{ADD_ATTR:['target'],FORBID_TAGS:['img','iframe','style','script']}),[text]);
  return <div className="markdown" dangerouslySetInnerHTML={{__html:html}} onClick={e=>{const a=e.target.closest('a');if(a&&a.getAttribute('href')&&!/^(https?:|#)/i.test(a.getAttribute('href'))){e.preventDefault();a.title='本地来源路径，请参阅报告中的来源说明';}}}/>;
}
export function ReportReader({report,onClose}) {
  const [mode,setMode]=useState('report'),[section,setSection]=useState(report?._initialSection||'all');
  useEffect(()=>{const old=document.body.style.overflow;document.body.style.overflow='hidden';const handler=e=>{if(e.key==='Escape')onClose()};window.addEventListener('keydown',handler);return()=>{document.body.style.overflow=old;window.removeEventListener('keydown',handler)};},[onClose]);
  useEffect(()=>{setMode('report');setSection(report?._initialSection||'all');},[report]);
  if(!report)return null;
  const sections=report.sections||[];
  const current=sections.find(s=>s.id===section);
  const sectionIndex=sections.findIndex(s=>s.id===section);
  const nextParent=current?sections.findIndex((s,i)=>i>sectionIndex&&s.level<=current.level):-1;
  const chapterMarkdown=current?sections.slice(sectionIndex,nextParent<0?undefined:nextParent).map(s=>s.markdown).join('\n\n'):null;
  const download=()=>{const blob=new Blob([report.markdown||''],{type:'text/markdown;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`${report.ticker||report.id||'research'}-${report.research_date||report.date||''}.md`;a.click();URL.revokeObjectURL(url);};
  return <div className="reader-backdrop" role="dialog" aria-modal="true" aria-label="研究报告阅读器"><div className="reader"><header className="reader-header"><button className="icon-button" aria-label="关闭报告" onClick={onClose}><ArrowLeft size={21}/></button><div><div className="eyebrow">RESEARCH DOCUMENT</div><h2>{report.title||report.ticker}</h2></div><button className="icon-button" aria-label="下载完整Markdown" title="下载完整Markdown" onClick={download}><Download size={20}/></button><button className="icon-button" aria-label="关闭阅读器" onClick={onClose}><X size={22}/></button></header><div className="reader-body"><aside className="reader-toc"><div className="segment"><button className={mode==='report'?'active':''} onClick={()=>setMode('report')}>报告原文</button><button className={mode==='data'?'active':''} onClick={()=>setMode('data')}>结构化数据</button></div><p className="micro">{report.research_date||report.date||'日期未标注'}</p>{mode==='report'&&<><button className={section==='all'?'active':''} onClick={()=>setSection('all')}>完整报告</button>{sections.map((s,i)=><button key={`${s.id}-${i}`} className={`${section===s.id?'active':''} level-${s.level}`} onClick={()=>setSection(s.id)}>{cleanText(s.title)}</button>)}</>}<div className="source-note">来源：{report.source||'正式研究结果'}<br/>展示数据不改写研究原文。</div></aside><article className="reader-content" key={`${mode}-${section}`}>{mode==='data'?<><h2>配套结构化结果</h2><p className="muted">保留正式研究 JSON 字段。报告中的假设、限定和来源请结合原文阅读。</p><pre className="json-view">{JSON.stringify(report.raw||{message:'此报告没有配套结构化 JSON。'},null,2)}</pre></>:<Markdown text={chapterMarkdown ? chapterMarkdown+'\n\n'+(report.markdown||'').split('\n').filter(line=>/^\s*\[[^\]]+\]:/.test(line)).join('\n') : report.markdown||'此报告暂无可展示正文。'}/>}</article></div></div></div>;
}
export function LazyResearchReader({item,onClose}) {const {data,error,loading}=useData(item?.detailUrl);return loading||error?<div className="reader-backdrop" role="dialog" aria-modal="true"><div className="reader"><button className="button" onClick={onClose}><X size={18}/>关闭</button><Status loading={loading} error={error}/></div></div>:<ReportReader report={data} onClose={onClose}/>}
export function Metric({label:caption,value,note,icon:Icon,accent=false}) {return <div className={`metric ${accent?'accent':''}`}><div className="metric-label">{caption}{Icon&&<Icon size={17}/>}</div><strong>{value}</strong><small>{note}</small></div>}
