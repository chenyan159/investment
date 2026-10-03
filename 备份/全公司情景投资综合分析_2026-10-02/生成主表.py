from pathlib import Path
import json,re

OUT=Path(__file__).parent
ROOT=Path(r'D:\investment')
a=json.loads((OUT/'复算数据.json').read_text(encoding='utf-8'))
rs={r['ticker']:r for r in a['companies']}
chosen=['ADBE','NVDA','MU','TEL','PNR','DOV','AVGO','MSFT','APH','ST','SPXC','SBGSY','VISN','BABA','QCOM','ET','CMI','CRM','FTV','PSIX']
roles={'ADBE':'折价现金流','NVDA':'核心成长','MU':'周期进攻','TEL':'工业成长底盘','PNR':'水业务修复','DOV':'现金工业底盘','AVGO':'客户项目成长','MSFT':'质量平台','APH':'连接成长','ST':'利润及资本修复','SPXC':'工业冷却成长','SBGSY':'电气系统成长','VISN':'特殊经营修复','BABA':'中国平台与资本验证','QCOM':'利润池替代','DT':'平台成长验证','CMI':'工业动力底盘','CRM':'现金与降债','FTV':'流程及工具现金','PSIX':'小盘动力卫星'}
roles['ET']='收益基础设施；含分配年化12.6%至16.6%'
def pct(xs):return '～'.join(f'{v:+.1f}%' for v in xs)
def link(r):return f'[{r["ticker"]}](/'+(ROOT/r['path']).as_posix()+f':{r["table_line"]})'
sector=['| 主分类 | 公司数及可比数 | 基准中点年化中位数 | 悲观下沿中位数 | 基准下沿至少8% | 基准区间全负 |\n|---|---:|---:|---:|---:|---:|\n']
for c in a['stats']['categories']:
    label=c['category'].replace('_',' ')
    sector.append(f'| {label} | {c["count"]} / {c["comparable"]} | {c["base_mid_annual"]:+.1f}% | {c["pess_low"]:+.1f}% | {c["base_low_gt8"]} | {c["base_full_negative"]} |\n')
top=['| 公司及原报告 | 当前快照价 | 目标日 | 基准价格年化 | 悲观价格损失 | 投资角色 |\n|---|---:|---|---:|---:|---|\n']
four=['| 公司 | 悲观价格回报 | 基准价格回报 | 乐观价格回报 | 突破价格回报 |\n|---|---:|---:|---:|---:|\n']
stress=['| 公司 | 基准中点年化 | 延后一年 | 终点价减20% | 两者叠加 |\n|---|---:|---:|---:|---:|\n']
for t in chosen:
    r=rs[t];s=r['scenarios']
    top.append(f'| {link(r)} | {r["snapshot_price"]:.2f} | {r["target"]} | {pct(s["基准"]["annual_snapshot"])} | {pct(s["悲观"]["return_snapshot"])} | {roles[t]} |\n')
    four.append(f'| {t} | '+ ' | '.join(pct(s[k]['return_snapshot']) for k in ['悲观','基准','乐观','突破'])+' |\n')
    stress.append(f'| {t} | {r["base_mid_annual_snapshot"]:+.1f}% | {r["delay_annual_snapshot"]:+.1f}% | {r["cut20_annual_snapshot"]:+.1f}% | {r["joint_annual_snapshot"]:+.1f}% |\n')
path=OUT/'综合结论与20家公司深度比较.md'
text=path.read_text(encoding='utf-8')
for tag,parts in [('__SECTOR_TABLE__',sector),('__TOP20_TABLE__',top),('__FOUR_TABLE__',four),('__STRESS_TABLE__',stress)]:
    table=''.join(parts)
    if tag in text:
        text=text.replace(tag,table)
    else:
        header=parts[0].splitlines()[0]
        start=text.index(header)
        end=text.index('\n\n',start)
        text=text[:start]+table.rstrip('\n')+text[end:]
path.write_text(text,encoding='utf-8')
(OUT/'20家选择.json').write_text(json.dumps({'date':'2026-10-02','companies':[{'ticker':t,'role':roles[t]} for t in chosen]},ensure_ascii=False,indent=2),encoding='utf-8')
viz=Path(r'C:\Users\cheny\.codex\visualizations\2026\10\03\01a10020-5d34-7232-8a18-8e06df369a99\scenario-risk-return.html')
data=[{'t':r['ticker'],'x':round(r['scenarios']['悲观']['return_snapshot'][0],2),'y':round(r['base_mid_annual_snapshot'],2),'target':r['target'],'top':r['ticker'] in chosen} for r in a['companies'] if r['eligible']]
v=viz.read_text(encoding='utf-8')
v=re.sub(r'(<script type="application/json" id="scenario-data">).*?(</script>)',lambda m:m[1]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+m[2],v,count=1,flags=re.S)
viz.write_text(v,encoding='utf-8')
print('Assembled 20 company tables and 16 categories')
