from pathlib import Path
import json, re, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT = Path(__file__).parent
ROOT = OUT.parent.parent
data = json.loads((OUT/'本地情景与比较数据.json').read_text(encoding='utf-8'))
rows = {r['ticker']:r for r in data['rows']}

def link(path, line=None):
    p = Path(path).as_posix()
    return '/' + p + (':' + str(line) if line else '')

def num(value):
    return '—' if value is None else f'{value:.1f}'

def pct(value):
    return '—' if value is None else f'{value:+.1f}%'

def band(row, case, months=36):
    v = row['scenarios'].get(f'{case}_{months}m', {})
    return pct(v.get('low'))+'～'+pct(v.get('high'))

def table(tickers, main=False):
    header = '|公司|9/9价格$|Forward PE|基准三年|乐观三年|突破三年|'
    sep = '|---|---:|---:|---:|---:|---:|'
    if not main:
        header = '|公司及情景来源|价格$|PE|Forward PE|基准三年|乐观三年|突破三年|悲观三年|'
        sep = '|---|---:|---:|---:|---:|---:|---:|---:|'
    out = [header, sep]
    for t in tickers:
        r = rows[t]
        name = t + ('（原20）' if r['in_prior20'] else '')
        if main:
            vals = [name, num(r['price']), num(r['forward_pe']), band(r,'基准'), band(r,'乐观'), band(r,'突破')]
        else:
            name = f'[{name}]({link(r["report_path"])})'
            vals = [name,num(r['price']),num(r['pe']),num(r['forward_pe']),band(r,'基准'),band(r,'乐观'),band(r,'突破'),band(r,'悲观')]
        out.append('|'+'|'.join(vals)+'|')
    return '\n'.join(out)

focus = ['MU','MSFT','NVDA','ADBE','NTAP','IBM','SMCI','BDC','CRDO','LITE','COHR','FN','CRWV','IREN','NBIS','APLD','NVT','EME','HUBB','HTHIY','ETN','VRT']
report_path = OUT/'三板块深度分析与研究遗漏审计.md'
report = report_path.read_text(encoding='utf-8')
report = report.replace('<!-- MAIN_COMPARISON_TABLE -->',table(focus,main=True))
report = report.replace('/D:/drive/Investment/基本面/公司调研/电力_电气设备_散热/ETN_Eaton_公司调研_2026-09-07.md',link(rows['ETN']['company_report_paths'][0]))
for t in ['SMCI','BDC']:
    report = report.replace(f'./公司研究来源索引.md#{t}',link(rows[t]['company_report_paths'][0]))
addendum = '''**5. ORCL、DLR与EQIX提供的是另外几种组合选择。**

ORCL保留数据库与企业软件基础，同时扩大AI基础设施。其现行情景报告指出，行情源Forward PE约14.7倍没有明确预测年度，而公司FY2027指引对应约20.1倍调整后盈利；这个差异本身就说明统一表格里的低PE不能直接当便宜证据。若客户出资购买设备、Oracle只保留服务费，资本压力可能下降，但收入与收费权必须一起重算。该路径已经在现有报告中讨论，不能只加回CapEx来证明低估。[本地ORCL情景报告](/D:/drive/Investment/分析报告/公司情景投资决策/结果/ORCL_经营情景市场状态投资决策_2026-09-09.md:11)。

DLR、EQIX更适合提供成熟数据中心与互连敞口。应结合FFO/AFFO、维护投入、开发支出、净债务和JV归属权益判断，单看PE容易失真。原模型中，DLR基准三年约−24.2%至−1.8%、乐观+23.1%至+61.1%；EQIX分别约−18.3%至+6.4%、+27.4%至+67.4%。它们未必提供最强爆发力，但有资格与高资本风险NeoCloud比较现金质量，而不应因为增长更慢就退出机会集。[本地DLR情景报告](/D:/drive/Investment/分析报告/公司情景投资决策/结果/DLR_经营情景市场状态投资决策_2026-09-09.md)、[本地EQIX情景报告](/D:/drive/Investment/分析报告/公司情景投资决策/结果/EQIX_经营情景市场状态投资决策_2026-09-09.md)。

'''
marker = '**四、电力设备：较适合兼顾AI增长与防御，但估值并不普遍便宜**'
if '**5. ORCL、DLR与EQIX' not in report:
    report = report.replace(marker,addendum+marker)
report_path.write_text(report,encoding='utf-8')

intro = '''# 65家公司同日价格与原情景模型对照

价格、PE及Forward PE为2026年9月9日收盘项目行情口径；模型源于9月8—9日现行正式情景报告，并重算到同一买价。所有回报为三年累计条件值，不是年化、胜率、置信区间或预期收益。原报告目标日期保留一天差异。PE与Forward PE的会计和预测年度可能不同；REIT应另核对FFO/AFFO。缺失PE不填零。

主表仅呈现原模型，不代表本次重估；决定性的替代经济解释见深度报告正文。65份情景文件均与前次数据保留的SHA256一致。新补六家公司CORZ、HUT、CIFR、WULF、GLXY、RIOT未纳入这些数值行，原因是尚无同口径完全稀释估值，不能把缺失值当负回报。

'''
parts=[intro]
for group, tickers in data['groups'].items():
    parts.append('**'+group+'**\n\n'+table(tickers)+'\n')
parts.append('**前次20家公司**\n\n'+table(data['prior20'])+'\n')
(OUT/'现有模型横向对照.md').write_text('\n'.join(parts),encoding='utf-8')

idx=['# 本地现行公司与情景报告来源\n','所有路径指向当前正式文件；不以历史备份版本作为本次模型输入。\n','|公司|公司研究|情景投资决策|报告日期|与前次数据哈希一致|','|---|---|---|---|---|']
for r in data['rows']:
    c='、'.join(f'[公司报告]({link(p)})' for p in r['company_report_paths'])
    idx.append('|'+ '|'.join([r['ticker'],c,f'[情景报告]({link(r["report_path"])})',r['report_date'],'是' if r['source_hash_matches'] else '否'])+'|')
(OUT/'公司研究来源索引.md').write_text('\n'.join(idx)+'\n',encoding='utf-8')

main_universe=json.loads((ROOT/'备份/20家公司投资价值与多维图谱_2026-09-09/market_scenario_data.json').read_text(encoding='utf-8'))
tickers={r['ticker'] for r in main_universe['companies']}
new_tickers=['CORZ','HUT','CIFR','WULF','GLXY','RIOT']
checks={'rows':len(rows),'old20_count':len(data['prior20']),'old20_unique':len(set(data['prior20'])),'universe_count':len(tickers),
        'new_six_absent_from_universe':{t:t not in tickers for t in new_tickers},'formal_files_unchanged':[],'broken_local_links':[],'local_links_checked':0}
for x in data['manifest']:
    p=Path(x['path']); h=hashlib.sha256(p.read_bytes()).hexdigest()
    checks['formal_files_unchanged'].append({'path':str(p),'unchanged':h.lower()==x['sha256'].lower()})
for fname in ['三板块深度分析与研究遗漏审计.md','研究方案补充条款建议.md','现有模型横向对照.md','公司研究来源索引.md']:
    p=OUT/fname
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if target.startswith(('https://','http://')): continue
        q=target.strip('<>').split('#')[0]
        q=re.sub(r':\d+$','',q)
        if re.match(r'^/[A-Za-z]:/',q): q=q[1:]
        path=Path(q) if re.match(r'^[A-Za-z]:',q) else OUT/q
        checks['local_links_checked']+=1
        if not path.exists():checks['broken_local_links'].append({'file':fname,'target':target})
checks['unreplaced_placeholder']='<!-- MAIN_COMPARISON_TABLE -->' in report
checks['formal_unchanged_count']=sum(x['unchanged'] for x in checks['formal_files_unchanged'])
checks['report_characters']=len(report)
checks['proposals_characters']=len((OUT/'研究方案补充条款建议.md').read_text(encoding='utf-8'))
(OUT/'交付核查.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in checks.items() if k!='formal_files_unchanged'},ensure_ascii=False,indent=2))
assert len(rows)==65 and len(data['prior20'])==20
assert all(checks['new_six_absent_from_universe'].values())
assert checks['formal_unchanged_count']==len(data['manifest'])
assert not checks['broken_local_links'] and not checks['unreplaced_placeholder']
