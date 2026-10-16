import json,csv,re,pathlib
R=pathlib.Path(r'D:\investment\实验室\2026-10-12_3至6个月超高收益20家公司实验')
U=json.loads((R/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))
deep='SMCI PSIX FLNC LEU RDW APLD IREN POET AMPX WOLF TE KYTX BNTX IONS ALNY ENPH NVTS AOSL ACMR PLAB AMBA AVAV ASTS OKLO SMR LWLG VISN CC PENG'.split()
rows=[]
for x in U:
 text='\n'.join((R/p).read_text(encoding='utf-8-sig') for p in x['sources'].get('company',[]) if (R/p).exists())
 catalysts=re.findall(r'[^\n]{0,80}(?:2026Q4|2027Q1|Q4 2026|Q1 2027|2027年初|2026年年底|未来两次财报|2027年第一季度)[^\n]{0,160}',text)
 financing=re.findall(r'[^\n]{0,40}(?:融资缺口|净债务|不受限现金|债务本金|完全稀释|现金消耗)[^\n]{0,100}',text)
 size=x['finance'].get('市值','')
 if x['ticker'] in deep: decision='深读并比较事件/融资'
 elif 'T' in size or ('B' in size and float(re.sub(r'[^0-9.]','',size) or 0)>80):decision='非优先:大市值翻倍需新增巨额权益价值;未见足够近期非线性事件'
 else:decision='未提名:本轮事件线索未胜出;非断言无机会'
 rows.append(dict(ticker=x['ticker'],category=x['category'],price=x['finance'].get('最新价格'),market_cap=size,currency=x['finance'].get('currency'),screen_method='全部公司原文关键词/财务结构扫描;非逐篇精读',catalyst_excerpt=' / '.join(catalysts[:2]),funding_excerpt=' / '.join(financing[:2]),disposition=decision,source_paths=';'.join(x['sources'].get('company',[]))))
with (R/'07_logs/X1_full245_screen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
notes=['# X1 独立原文阅读笔记','仅阅读本实验冻结原文，未读取其他X结论/上一实验排名。245为结构化全文检索扫描，不冒称245篇精读。29家公司深读的是开篇决定性判断、财务/融资/近两季催化相关段落；不声称通读全部正文。下列带行号原文摘录为复核导航，本地事实仍需外部复核。']
for t in deep:
 x=next(z for z in U if z['ticker']==t); notes += ['\n## '+t]
 for typ in ['company','scenario','comparison']:
  for p in x['sources'].get(typ,[]):
   ls=(R/p).read_text(encoding='utf-8-sig').splitlines()
   wanted=list(range(min(26,len(ls)))) if typ=='company' else []
   hits=[i for i,l in enumerate(ls) if re.search('未来两次财报|最近两次财报|2027Q1|2026Q4|2027年初|2027年第一季度|近期.*催化|融资缺口|完全稀释|净债务',l)]
   for i in hits[:5]: wanted.extend(range(max(0,i-1),min(len(ls),i+2)))
   notes += ['\n### '+typ+' '+p, '\n'.join(f'L{i+1}: {ls[i]}' for i in sorted(set(wanted)))]
(R/'07_logs/X1_reading_notes.md').write_text('\n'.join(notes),encoding='utf-8')
print('screen',len(rows),'deep',len(deep),'notes bytes',(R/'07_logs/X1_reading_notes.md').stat().st_size)
