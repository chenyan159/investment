from pathlib import Path
import json, csv, re, hashlib, statistics

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
analysis = json.loads((OUT / 'analysis.json').read_text(encoding='utf-8'))
companies = analysis['companies']
cs = {c['ticker']: c for c in companies}
selected = json.loads((OUT / '重点20家判断.json').read_text(encoding='utf-8'))
rank = {m['ticker']: i+1 for i, m in enumerate(selected)}
scenarios = ['悲观', '基准', '乐观', '突破']

def pct(n):
    return f'{n:+.1f}%'

def interval(v):
    return f'{pct(v[0])}～{pct(v[1])}'

def clean(s):
    return re.sub(r'<br\s*/?>', '；', s).replace('|', '／').replace('\n', ' ')

def link(c, label=None):
    return f'[{label or c["ticker"]}](/D:/investment/{c["path"]}:{c["table_line"]})'

def artifact(name, label):
    return f'[{label}](/D:/investment/备份/全公司情景投资横评_2026-10-02/{name})'

def table(headers, rows):
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |'] + ['| '+' | '.join(map(str,r))+' |' for r in rows])

category_rows = []
for x in sorted(analysis['stats']['categories'], key=lambda x:x['median_base_annual'], reverse=True):
    category_rows.append([x['category'].replace('_',' / '), x['count'], x['base_positive_low'], x['base_negative_high'], pct(x['median_base_total']), pct(x['median_base_annual']), pct(x['median_pess_low'])])
category_table = table(['索引行业','家数','基准全正','基准全负','基准中点累计中位数','基准中点年化中位数','悲观下沿中位数'], category_rows)

valid = [c for c in companies if c['ticker']!='ATKR']
base_low = lambda c:c['scenarios']['基准']['annual_report'][0]
bear_low = lambda c:c['scenarios']['悲观']['return_calculated'][0]
front = [c for c in valid if not any(base_low(o)>=base_low(c) and bear_low(o)>=bear_low(c) and (base_low(o)>base_low(c) or bear_low(o)>bear_low(c)) for o in valid)]
frontier_table = table(['公司','基准年化下沿','悲观终点下沿'], [[link(c),pct(base_low(c)),pct(bear_low(c))] for c in sorted(front,key=base_low,reverse=True)])
pass_list = '、'.join(link(c) for c in valid if base_low(c)>=8) + '。'

alternatives = {
 'CC':'基准数字很高，但PFAS等现金索赔、债务与近全额本金损失路径，使其属于特殊情形；不按稳健正常经营回报优先。',
 'SMCI':'最接近入选的高弹性替补。两季回款、毛利和营运资本仍是前置条件，基准目标还包含9.31倍向12—15倍的估值恢复；现金未证实前排在20家之外。',
 'FLNC':'储能兑现有机会，约93%的悲观终点损失提示项目、保证与信用责任风险；不能只按订单价值排名。',
 'CRWV':'高杠杆、未来资金缺口和GPU更新寿命决定普通股存续价值，客户订单不能替代融资闭环。',
 'NBIS':'实际算力交付有基础，但工程、融资和客户预算尚未形成与成熟平台同等的现金保护。',
 'ORCL':'数据库现金是优势，新增OCI容量、客户供卡、预付与设备更新承担巨大资本要求；不把全部RPO当可分配收益。',
 'SOMMY':'住友化学有转型赔率，但药品、材料、Rabigh和集团债务共同决定母公司可得现金，复杂资本桥与约69%悲观损失削弱优先级。',
 'SKHY':'公司存储实力值得研究；报告估计美国ADS相对韩国原股约43.6%溢价，证券溢价消失可以独立消化业务增长；优先比较原股实际买价。',
 'AEIS':'半导体和数据中心电源有强增长，当前价格需要持续执行，第二客户复制、产线现金和约61%悲观损失使其暂居成长替补。',
 'BDC':'工业网络与RUCKUS有真实入口；收购债务、整合与约68%悲观终点损失，当前价格尚未提供充分资本容错。',
 'FTV':'最接近入选的成熟现金替补，基准固定倍数回报约49%；医药预算、软件扩单和较低成长上限，在本次成长/赔率目标下略后。保守目标可替换PSIX。',
 'CMI':'可靠的发动机、零部件、发电与服务底盘；当前DCF低于买价，卡车/排放周期与资本投入需验证。成熟工业目标可替换PSIX或SNPS。',
 'DKILY':'全球HVAC与服务修复有价值；北美净价、铜和运输成本、中国住宅业务及回购资本负担需要同步验证，作为非AI分散替补。',
 'ASGLY':'材料与生命科学有真实客户，但成本修复、产能现金与集团组合较复杂；中心价值余量有限，保留为工业复苏候选。',
 'ETR':'受监管资产增长与大客户协议有依据，但持续融资和股权稀释不可省略；本次价格回报口径低估股息，收入型目标应另列。',
 'EQIX':'托管与互联是高质量资产，新增建设资本、重置费用与利率占用回报；以AFFO直接当股东现金不充分。收入型目标应纳入股息比较。',
 'FLEX':'真实制造与电力增长，现价高于报告约96美元当前DCF，收购及净资本回报还需改善。',
 'IESC':'工程交付已兑现，但固定价合同、住宅与DBM整合风险，当前价格更要求执行，订单不直接等于自由现金。',
 'NTNX':'真实基础设施软件替代机会，当前价格仍需新客户扩单、存储兼容的净增与经济SBC改善。',
 'MSI':'公共安全底盘较强，但现价同时要求原有业务增长恢复和收购回报，较低正常年化使其进入质量替补。',
 'TSM':'业务质量很高，但本次报告买价的正常收益相对有限，客户预算和先进节点资本回报不能只用行业地位替代。'
}
alt_rows=[]
for t,reason in alternatives.items():
    c=cs[t]
    alt_rows.append([link(c),interval(c['scenarios']['基准']['return_calculated']),pct(c['base_mid_annual_report']),pct(bear_low(c)),reason])
alternative_table=table(['公司','基准累计回报','基准中点年化','悲观下沿','未优先入选的原因'],alt_rows)

top_rows=[]; dcf_rows=[]; stress_rows=[]; deep=[]
for i,m in enumerate(selected,1):
    c=cs[m['ticker']]; b=c['scenarios']['基准']
    top_rows.append([i,link(c),m['role'],c['target'],f'{c["years"]:.2f}',*[interval(c['scenarios'][s]['return_calculated']) for s in scenarios],interval(b['annual_report'])])
    v=m['dcf']; tv=m['target_dcf']; pv=m['bear_dcf']
    dcf_rows.append([link(c),f'{c["quote"]:,.2f}',f'{v:,.2f}',pct((c['quote']/v-1)*100),f'{tv:,.2f}' if tv else '—',f'{pv:,.2f}' if pv else '—',clean(b['fixed_text'])])
    stress_rows.append([link(c),pct(c['base_mid_annual_report']),pct(c['base_mid_price20cut']),pct(c['base_mid_annual_delay']),f'{c["snapshot_price"]:,.2f}',pct(c['base_mid_annual_snapshot'])])
    deep += [f'### {i}. {c["ticker"]} — {c["name"]}：{m["role"]}', '', m['thesis'], '', '**横向取舍：** '+m['comparison'], '', '**主要损失机制：** '+m['risk'], '', '**未来两次财报看什么：** '+m['check'], '', '**哪些信号改变判断：** '+m['fail'], '', f'原始研究：{link(c, c["ticker"]+"四情景与全文")}。当前基准DCF {v:,.2f}美元，报告参考买价{c["quote"]:,.2f}美元。', '']

top_table=table(['序','公司','研究角色','目标日','年数','悲观','基准','乐观','突破','基准年化'],top_rows)
dcf_table=table(['公司','报告买价USD','当前基准DCF','现价相对DCF偏离','目标日基准DCF','当前受损DCF','基准固定倍数参考价'],dcf_rows)
stress_table=table(['公司','原基准中点年化','目标价折让20%','兑现延迟一年','10/2快照买价','快照复算中点年化'],stress_rows)

output_links='\n\n'.join([
 artifact('全公司逐项明细.md','221家公司逐项明细'),
 artifact('全公司四情景复算.csv','全公司四情景CSV（884行）'),
 artifact('重点20家公司比较.csv','20家公司比较CSV（80行情景）'),
 artifact('20家公司回报对比.png','20家公司基准年化与悲观终点图'),
 artifact('复核记录.json','覆盖、数值与来源一致性复核')])

body=(OUT/'报告正文.md').read_text(encoding='utf-8')
values={'CATEGORY_TABLE':category_table,'PASS_LIST':pass_list,'FRONTIER_TABLE':frontier_table,'ALTERNATIVE_TABLE':alternative_table,'TOP20_TABLE':top_table,'DCF_TABLE':dcf_table,'STRESS_TABLE':stress_table,'DEEP20':'\n'.join(deep),'OUTPUT_LINKS':output_links}
for k,v in values.items():body=body.replace('{{'+k+'}}',v)
(OUT/'综合分析与20家公司对比.md').write_text(body,encoding='utf-8')

details=['# 全221家公司逐项比较', '', '基准日期2026-10-02。全部为条件模型价格回报，不含股息、税费及额外外汇变化；区间不是概率，悲观目标不是最大损失。按行业列全公司，再提供经营、资本和支撑依据。主表沿用报告买价；TOELY快照证券口径不兼容，不复算快照回报。', '', artifact('综合分析与20家公司对比.md','综合结论与20家深入分析'), '']
for cat in [x['category'] for x in analysis['stats']['categories']]:
    group=[c for c in companies if c['category']==cat]
    details += ['## '+cat.replace('_',' / '), '']
    rows=[]
    for c in group:
        rows.append([link(c),f'{c["quote"]:,.2f}',c['target'],*[interval(c['scenarios'][s]['return_calculated']) for s in scenarios],interval(c['scenarios']['基准']['annual_report']),rank.get(c['ticker'],'—'),c['bucket']])
    details += [table(['公司','报告买价（原证券币种）','目标日','悲观','基准','乐观','突破','基准年化','20家序','筛选分类'],rows), '']
    for c in group:
        b=c['scenarios']['基准']; capital=next((v for k,v in b['fields'].items() if any(w in k for w in ['状态','基本面','经营结果','财务','资本']) and k!='经营情景'),b['cells'][1])
        conclusion=c['summary'][0] if c['summary'] else '参见原始报告。'
        details += [f'### {c["ticker"]} — {c["name"]}', '', f'**原报告结论摘要：** {conclusion}', '', '**基准经营与资本：** '+clean(capital), '', '**固定倍数参考：** '+clean(b['fixed_text']), '', '**四情景依据：**']
        for s in scenarios:details += [f'- {s}：'+clean(c['scenarios'][s]['evidence_text'])]
        note=c.get('security_note','')
        details += ['',f'**本次分类：** {c["bucket"]}；入选20家序号：{rank.get(c["ticker"],"未入选")}。'+(' ATKR按现金并购事件处理，独立经营目标不作为正常兑现价格。' if c['ticker']=='ATKR' else ''),f'**证券/价格口径备注：** {note or "主表保留原报告证券、币种及买价；快照属于不同取价时点。"}',f'**来源：** {link(c,"四情景摘要与全文")}；SHA-256 `{c["sha256"]}`。', '']
(OUT/'全公司逐项明细.md').write_text('\n'.join(details),encoding='utf-8')

rows=[]
for m in selected:
 c=cs[m['ticker']]
 for s in scenarios:
  x=c['scenarios'][s]
  rows.append({'rank':rank[c['ticker']],'ticker':c['ticker'],'name':c['name'],'role':m['role'],'target':c['target'],'years':c['years'],'report_price':c['quote'],'snapshot_price':c['snapshot_price'],'scenario':s,'target_price_low':x['price'][0],'target_price_high':x['price'][1],'return_low_pct':x['return_calculated'][0],'return_high_pct':x['return_calculated'][1],'annual_low_pct':x['annual_report'][0],'annual_high_pct':x['annual_report'][1],'evidence':x['evidence'],'fixed_price_text':x['fixed_text'],'current_base_dcf':m['dcf'],'target_base_dcf':m['target_dcf'],'current_bear_dcf':m['bear_dcf'],'source':c['path'],'source_line':x['line'],'source_sha256':c['sha256']})
with (OUT/'重点20家公司比较.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

# Static chart from numeric data; drawn with Pillow, no generated artwork.
from PIL import Image, ImageDraw, ImageFont
fontfile=Path('C:/Windows/Fonts/msyh.ttc')
font=lambda n:ImageFont.truetype(str(fontfile),n)
img=Image.new('RGB',(1450,1510),'#f7f8fb'); draw=ImageDraw.Draw(img)
draw.text((65,35),'20家公司：基准年化与悲观终点',font=font(34),fill='#142231')
draw.text((65,85),'2026-10-02报告买价；价格回报，不含股息；区间为条件预测',font=font(20),fill='#526071')
draw.text((65,140),'综合顺序',font=font(21),fill='#142231')
draw.text((350,140),'基准年化回报（蓝线=区间，圆点=中点价格的年化）',font=font(19),fill='#142231')
draw.text((925,140),'悲观累计价格回报',font=font(21),fill='#142231')
xbase=lambda x:330+x/35*480
xbear=lambda x:925+(x+80)/80*300
for v in [0,10,20,30]:
 x=xbase(v);draw.line((x,190,x,1350),fill='#d8dfe7',width=1);draw.text((x-14,174),f'{v}%',font=font(17),fill='#657386')
for v in [-80,-60,-40,-20,0]:
 x=xbear(v);draw.line((x,190,x,1350),fill='#d8dfe7',width=1);draw.text((x-25,174),f'{v}%',font=font(17),fill='#657386')
for i,m in enumerate(selected):
 y=228+i*56;c=cs[m['ticker']];b=c['scenarios']['基准'];p=c['scenarios']['悲观']
 if i%2==0:draw.rectangle((55,y-15,1395,y+28),fill='#edf1f6')
 draw.text((66,y-11),f'{i+1:02d}  {c["ticker"]}',font=font(22),fill='#172f46')
 draw.text((200,y-8),f'{c["years"]:.2f}年',font=font(18),fill='#627386')
 x0,x1=[xbase(v) for v in b['annual_report']];draw.line((x0,y+6,x1,y+6),fill='#226bb4',width=7)
 x=xbase(c['base_mid_annual_report']);draw.ellipse((x-6,y,x+6,y+12),fill='#133f72')
 draw.text((818,y-7),f'{b["annual_report"][0]:.1f}–{b["annual_report"][1]:.1f}%',font=font(16),fill='#172f46')
 x0,x1=[xbear(v) for v in p['return_calculated']];draw.line((x0,y+6,x1,y+6),fill='#bb6658',width=7)
 draw.text((1260,y-7),f'{p["return_calculated"][0]:.1f}%',font=font(16),fill='#753e36')
draw.text((65,1400),'两图期限与尺度不同；悲观终点不是持有期间最大回撤。排名包含现金、资本和估值判断。',font=font(20),fill='#526071')
draw.text((65,1442),'数据：221家现行研究中的重点20家；完整明细与公式见同目录报告、CSV。',font=font(18),fill='#526071')
img.save(OUT/'20家公司回报对比.png')

print(json.dumps({'main_chars':len(body),'details_chars':len('\n'.join(details)),'companies':len(cs),'top20':len(selected),'top20_scenario_rows':len(rows),'frontier':[c['ticker'] for c in front]},ensure_ascii=False))
