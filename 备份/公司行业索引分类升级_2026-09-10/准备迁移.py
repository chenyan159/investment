from pathlib import Path
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, shutil, os, stat

ROOT=Path(r'D:\drive\Investment')
OUT=Path(__file__).parent
PREVIOUS=ROOT/'备份/美股新增候选与行业分类复核_2026-09-10'
COMPANY_ROOT=ROOT/'基本面/公司调研'
INDUSTRY_ROOT=ROOT/'基本面/行业调研'
DATE='2026-09-10'
data=json.loads((PREVIOUS/'候选公司与分类建议.json').read_text(encoding='utf-8'))
proposal=json.loads((PREVIOUS/'行业调整建议.json').read_text(encoding='utf-8'))
CATS=data['proposed_categories']

def parse_table(file,mincols):
    rows=[]
    for line in file.read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('| ') and chr(96) in line:
            cells=[s.strip().strip(chr(96)).rstrip('/') for s in line.strip('|').split('|')]
            if len(cells)>=mincols: rows.append(cells)
    return rows

old_companies=[dict(zip(['symbol','name','category'],r[:3])) for r in parse_table(COMPANY_ROOT/'公司索引.md',3)]
old_industries=[{'name':r[0],'category':r[1],'scope':r[2] if len(r)>2 else ''} for r in parse_table(INDUSTRY_ROOT/'行业索引.md',2)]
assert len(old_companies)==193 and len(old_industries)==82
old_by_symbol={x['symbol']:x for x in old_companies}
old_company_cats=list(dict.fromkeys(x['category'] for x in old_companies))
old_industry_cats=list(dict.fromkeys(x['category'] for x in old_industries))
mapping={}
reasons={}
def assign(symbols,cat,reason):
    for s in symbols.split():
        assert s in old_by_symbol,s
        mapping[s]=cat;reasons[s]=reason

assign('ADI TXN ON STM',CATS['G07'],'统一模拟、电源与传感器研究归属；保留各自其他业务标签')
assign('AOSL DIOD LFUS MPWR POWI ST VSH WOLF IFNNY NVTS MRAAY TTDKY',CATS['G07'],'由混合电力大类拆出器件、电源管理、保护、传感及相关被动元件')
assign('ABBNY ATKR HUBB MIELY POWL VICR ETN NVT',CATS['G08'],'由混合电力大类拆出配电及电源系统设备')
assign('CARR DCI PH PNR TT VRT DOV JCI MOD AAON',CATS['G10'],'机电大类拆分：热管理、流体及水处理')
assign('FIX IESC EME MYRG PWR',CATS['G11'],'工程建设和机电安装归为同类，区别于设备销售')
assign('ALLE FTV MSI TSLA',CATS['G12'],'机电大类拆分：自动化、智能硬件与控制；集团其他业务保留标签')
assign('RKLB SPCX',CATS['G13'],'航天公司从机电冷却大类独立')
assign('CAT',CATS['G09'],'项目主要跟踪发电动力业务，工程机械保留为集团存量业务标签')
assign('ECL DKILY',CATS['G10'],'水处理/温控/制冷归属热管理；集团其他业务保留标签')
assign('NDSN',CATS['G06'],'精密点胶、装配和检测设备归属设备与检测，区别于材料供应')
assign('AMZN APLD CRWV DLR GOOGL IREN MSFT ORCL BABA EQIX NBIS',CATS['G14'],'云与数据中心经营归属独立；多业务集团保留软件/广告/零售等标签')
assign('ADBE IBM META NTNX',CATS['G15'],'软件、数据与数字应用平台从云资产经营中拆出')
assign('CRWD',CATS['G16'],'网络安全和身份治理形成独立公司类别')

tags={
 'ADI':'模拟信号链、数据转换、电源管理、汽车与工业','TXN':'模拟芯片、电源管理、嵌入式处理、汽车与工业',
 'ON':'功率半导体、SiC、图像传感、汽车与工业','STM':'功率半导体、MCU、传感器、汽车与工业',
 'LFUS':'电路保护、熔断器、功率器件、工业与汽车','MRAAY':'MLCC、被动元件、通信模块、电源与传感',
 'TTDKY':'被动元件、磁性材料、传感器、电池','VICR':'模块化电源、功率转换、封装工艺',
 'CAT':'发电机组、发动机、工程机械、矿业机械、金融服务','ECL':'水处理、清洁与卫生服务、流体化学、热管理',
 'DKILY':'暖通空调、冷水机组、制冷剂、氟化学','NDSN':'精密点胶、装配设备、检测、医疗耗材',
 'PWR':'输配电工程、并网、机电施工、项目交付','ALLE':'门禁、物理安防、建筑智能硬件',
 'FTV':'测量仪表、工业诊断、检测软件','MSI':'关键通信、视频安防、指挥调度软件',
 'PH':'流体控制、运动控制、航空航天部件','VRT':'热管理、电源系统、数据中心集成交付',
 'TSLA':'汽车、能源储能、智能驾驶、机器人期权','RKLB':'运载火箭、航天器、空间系统',
 'SPCX':'运载火箭、卫星通信、地面终端','AMZN':'云计算、零售、广告、物流自动化、卫星通信',
 'GOOGL':'云计算、搜索广告、数字分发、AI应用','MSFT':'云计算、企业软件、AI应用、开发工具',
 'BABA':'云计算、电商、数字平台','ORCL':'云基础设施、数据库、企业应用软件',
 'IBM':'企业软件、主机、混合云、咨询实施','META':'广告推荐、数字分发、AI应用、智能硬件',
 'NTNX':'虚拟化、混合云管理、存储软件、AI基础设施软件','ADBE':'创作软件、文档软件、企业营销软件',
 'CRWD':'终端安全、云安全、身份安全、安全运营','DHR':'生命科学、生物工艺、诊断、精密分析；沿用项目研究分类',
 'HOCPY':'光罩、精密光学、医疗与视力保健','TMO':'科学仪器、分析检测、生命科学服务',
}
links={
 'ADI':['功率半导体与高压保护器件','工业机器视觉与精密感知'],
 'TXN':['功率半导体与高压保护器件','服务器BMC、MCU与嵌入式控制'],
 'ON':['功率半导体与高压保护器件','工业机器视觉与精密感知'],
 'STM':['功率半导体与高压保护器件','服务器BMC、MCU与嵌入式控制'],
 'MRAAY':['MLCC与高端陶瓷电容','机柜级供电与服务器电源架构'],
 'TTDKY':['MLCC与高端陶瓷电容','工业机器视觉与精密感知'],
 'VICR':['机柜级供电与服务器电源架构'],
 'CAT':['数据中心自备发电与微电网'],
 'PWR':['数据中心电力接入与高压变电','数据中心土建、MEP与预制化交付'],
 'ECL':['冷却液、水处理、过滤与制冷剂','数据中心直液冷系统'],
 'DKILY':['数据中心风冷、冷水机组与HVAC','冷却液、水处理、过滤与制冷剂'],
 'NDSN':['先进封装设备与混合键合','半导体检测量测设备'],
 'RKLB':['运载火箭、航天器与空间基础设施'],
 'SPCX':['运载火箭、航天器与空间基础设施','低轨卫星通信、直连手机与地面终端'],
 'TSLA':['人形机器人与关键执行部件','AI边缘推理芯片'],
 'FTV':['工业机器视觉与精密感知','工业自动化控制、工业机器人与协作机器人'],
 'ALLE':['机柜、围护结构与物理安防'],'MSI':['机柜、围护结构与物理安防'],
 'PH':['液冷小组件与流体控制','运载火箭、航天器与空间基础设施'],
 'VRT':['数据中心直液冷系统','数据中心风冷、冷水机组与HVAC','机柜级供电与服务器电源架构'],
 'AMZN':['AI云算力外包和NeoCloud与AI数据中心运营商','广告推荐、搜索与数字分发','仓储物流机器人与自动化系统','低轨卫星通信、直连手机与地面终端'],
 'GOOGL':['AI云算力外包和NeoCloud与AI数据中心运营商','广告推荐、搜索与数字分发','企业AI与Agent工作流软件'],
 'MSFT':['AI云算力外包和NeoCloud与AI数据中心运营商','企业AI与Agent工作流软件','网络安全、身份权限与AI治理'],
 'BABA':['AI云算力外包和NeoCloud与AI数据中心运营商','企业AI与Agent工作流软件'],
 'ORCL':['AI云算力外包和NeoCloud与AI数据中心运营商','数据平台、数据库与AI数据软件'],
 'IBM':['企业AI与Agent工作流软件','数据平台、数据库与AI数据软件'],
 'META':['广告推荐、搜索与数字分发'],
 'NTNX':['AI集群调度与推理运行时','数据平台、数据库与AI数据软件'],
 'ADBE':['AI创作与文档生产软件','企业AI与Agent工作流软件'],
 'CRWD':['网络安全、身份权限与AI治理'],
}
industry_rename=proposal['industry_parent_category_renames']
split_map={a['name']:a['targets'] for a in proposal['actions'] if a['action']=='拆分：1变3'}
industries=[]
for e in old_industries:
    if e['name'] in split_map: continue
    n={**e,'category':industry_rename.get(e['category'],e['category']),'type':'行业','mapping':''}
    n['scope']=n['scope'].removeprefix('新增待调研。')
    if e['name'].startswith('OCI '):
        n['type']='横向专题'
        n['scope']='光线路接口、靠近ASIC连接/维修边界和高密度可插拔形态的横向比较；经济归属关联CPO/NPO、封装内光I/O、连接器和光模块，不单独作为可加总终端市场。'
        n['mapping']='原题名及报告保留；经济口径转为横向专题'
    industries.append(n)
for a in proposal['actions']:
    if a['action']=='新增':
        industries.append({'name':a['name'],'category':a['proposed_parent_category'],'scope':a['scope'],'type':'行业','mapping':'2026-09-10新增登记'})
    elif a['action']=='拆分：1变3':
        scopes={
         '工业自动化控制、工业机器人与协作机器人':'工业控制、运动/过程控制、工业与协作机器人；设备、软件、集成和服务分清收入层级。',
         '仓储物流机器人与自动化系统':'仓储物流机器人、调度软件、系统集成和维护；区分设备交付与系统验收。',
         '人形机器人与关键执行部件':'人形及具身平台、执行器和关键部件；区分研发/展示用途与持续生产用途，整机与部件收入不重复相加。',
         '运载火箭、航天器与空间基础设施':'运载任务、航天器、空间系统与部件；区分对外商业采购和自有星座内部使用。',
         '低轨卫星通信、直连手机与地面终端':'通信星座、直连手机、地面终端及连接服务；区分覆盖人口、有效容量与付费用户。',
         '地球观测、遥感数据与空间信息服务':'遥感星座、影像、地理数据及主权系统；硬件交付、数据订阅和服务分别归属。',
        }
        for target in a['targets']:
            industries.append({'name':target,'category':a['proposed_parent_category'],'scope':scopes[target],'type':'行业','mapping':f'由“{a["name"]}”拆分；原综合报告归档'})
assert len(industries)==91 and sum(x['type']=='行业' for x in industries)==90
names={x['name'] for x in industries}
new_quote={x['symbol']:x.get('quote',{}) for x in json.loads((PREVIOUS/'美股交易身份与行情核查.json').read_text(encoding='utf-8'))}
companies=[]
for e in old_companies:
    cat=mapping.get(e['symbol'],CATS['G04'] if e['category']=='半导体材料_化学品_基板' else e['category'])
    assert cat in CATS.values(),(e['symbol'],cat)
    companies.append({**e,'old_category':e['category'],'category':cat,'tags':tags.get(e['symbol'],''),'industries':links.get(e['symbol'],[]),'listing_note':'','is_new':False,'change_reason':reasons.get(e['symbol'],'分类目录名称扩容' if cat!=e['category'] else '')})
for e in data['candidates']:
    assert e['ticker'] not in old_by_symbol
    related=[]
    for n in e['existing_industries']+e['proposed_industries']:
        if n in split_map: continue
        if n not in related: related.append(n)
    ex=new_quote[e['ticker']]['exchange']
    listing={'NGM':'Nasdaq','NMS':'Nasdaq','NYQ':'NYSE','PNK':'美国OTC ADR；需券商支持'}[ex]
    companies.append({'symbol':e['ticker'],'name':e['name'],'old_category':None,'category':CATS[e['category_id']],'tags':e['technology'],'industries':related,'listing_note':listing+'；2026-09-10新增登记','is_new':True,'change_reason':'用户批准新增'})
assert len(companies)==218 and len({x['symbol'] for x in companies})==218
for e in companies: assert all(n in names for n in e['industries']),(e['symbol'],e['industries'])
companies.sort(key=lambda e:(list(CATS.values()).index(e['category']),e['symbol']))
industry_cats=[industry_rename.get(c,c) for c in old_industry_cats]
industries.sort(key=lambda e:industry_cats.index(e['category']))

assert not (OUT/'迁移计划.json').exists(),'已有迁移计划，禁止覆盖迁移前基线'
OUT.mkdir(parents=True,exist_ok=True)
def safe(p):
    p=p.resolve()
    assert p.is_relative_to(ROOT.resolve()),str(p)
    return p
def file_record(p):
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
snapshot=[]
for base,cats in [(COMPANY_ROOT,old_company_cats),(INDUSTRY_ROOT,old_industry_cats)]:
    for cat in cats:
        for current,dirs,files in os.walk(base/cat,followlinks=False):
            for n in dirs+files:
                p=Path(current)/n
                assert not (p.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT),str(p)
            snapshot.extend(file_record(Path(current)/n) for n in files)
protected=[]
for base in [COMPANY_ROOT,INDUSTRY_ROOT]:
    for current,dirs,files in os.walk(base,followlinks=False):
        dirs[:]=[d for d in dirs if not ((Path(current)/d).lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)]
        p=Path(current)
        if any('研究方案' in s or '研究方法' in s for s in p.relative_to(base).parts):
            protected.extend(file_record(p/n) for n in files)
protected += [file_record(p) for p in (ROOT/'tools/research-runner/prompts').glob('*.mjs')]
protected += [file_record(p) for p in [ROOT/'tools/queue.jsonl',ROOT/'tools/queue.done.jsonl'] if p.exists()]
source_code=[ROOT/'tools/research-runner/domains/company.mjs',ROOT/'tools/research-runner/domains/industry.mjs',ROOT/'tools/research-runner/index-updater.mjs',ROOT/'tools/site/etl/build-data.mjs']
backup_files=[COMPANY_ROOT/'公司索引.md',INDUSTRY_ROOT/'行业索引.md']+source_code
for p in backup_files:
    target=OUT/'原文件'/p.relative_to(ROOT)
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,target)

renames=[
 {'source':str(COMPANY_ROOT/'半导体材料_化学品_基板'),'destination':str(COMPANY_ROOT/CATS['G04'])},
 {'source':str(INDUSTRY_ROOT/'晶圆制造_设备_材料_测试'),'destination':str(INDUSTRY_ROOT/'半导体与电子制造_设备_材料_测试')},
]
archive_dirs=[]
for cat in ['机电_冷却_工程_水处理_边缘工业AI','配电_电源_功率器件','云算力_IDC_AI软件平台']:
    archive_dirs.append({'source':str(COMPANY_ROOT/cat),'destination':str(OUT/'原分类历史/公司调研'/cat)})
for cat in ['机器人_硬件_零部件','商业航天_火箭_卫星']:
    archive_dirs.append({'source':str(INDUSTRY_ROOT/cat),'destination':str(OUT/'原综合行业'/cat)})
file_moves=[]
direct_before=[]
path_overrides={}
for e in companies:
    if e['is_new']: continue
    files=list((COMPANY_ROOT/e['old_category']).glob(e['symbol']+'_*.md'))
    assert len(files)==1,(e['symbol'],files)
    f=files[0];destination=COMPANY_ROOT/e['category']/f.name
    direct_before.append({'symbol':e['symbol'],'source':str(f),'destination':str(destination),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    path_overrides[str(f)]=str(destination)
    actual_source=f
    if e['old_category']=='半导体材料_化学品_基板': actual_source=COMPANY_ROOT/CATS['G04']/f.name
    if actual_source!=destination: file_moves.append({'source':str(actual_source),'destination':str(destination)})
final_files=[]
for record in snapshot:
    p=Path(record['path']);dest=path_overrides.get(str(p))
    if dest is None:
        for op in renames+archive_dirs:
            src=Path(op['source'])
            if p.is_relative_to(src): dest=str(Path(op['destination'])/p.relative_to(src));break
    final_files.append({**record,'destination':dest or str(p)})
for op in renames+archive_dirs+file_moves:
    safe(Path(op['source']));safe(Path(op['destination']))
    assert op['source']!=op['destination']
dirs=[str(COMPANY_ROOT/c) for c in CATS.values()]+[str(INDUSTRY_ROOT/c) for c in industry_cats]
def cell(value):return str(value).replace('|','/').replace('\n',' ').strip()
company_counts=Counter(e['category'] for e in companies)
lines=['# 218家公司股票代号、公司名称和分类目录','',f'更新日期：{DATE}','',
 '本索引是公司名称、股票代号、主分类和正式报告目录的权威入口。现有193家公司保留，新增25家；共16个正式主分类。新增公司只登记，不生成占位研究报告。','',
 '主类别用于项目研究归属，不代表集团全部收入。业务标签和关联行业是分类元数据，不是研究结论或研究方案；未填关联行业的公司沿用主类别关联。未知业务份额不按100%推定。美国OTC ADR交易须券商支持。','',
 '2026-09-10迁移时点：193家公司已有正式报告，25家新增待研究；后续研究完成情况以分类目录内实际最新报告为准。历史备份不计入当前报告数量。','', '## 目录统计','']
lines += [f'- {c}：{company_counts[c]} 家' for c in CATS.values()]
lines += ['', '## 索引表','', '| 股票代号 | 公司名称 | 目录 | 业务标签 | 关联行业 | 交易身份与登记备注 |','|---|---|---|---|---|---|']
for e in companies:
    lines.append(f"| {cell(e['symbol'])} | {cell(e['name'])} | \x60{e['category']}/\x60 | {cell(e['tags'])} | {cell('；'.join(e['industries']))} | {cell(e['listing_note'])} |")
new_company_text='\n'.join(lines)+'\n'
industry_counts=Counter(e['category'] for e in industries)
lines=['# 91个行业与横向专题名称和分类目录','',f'更新日期：{DATE}','',
 '共90个经济研究主题和1个横向标准专题，分属7个行业父类别。公司分类与行业专题为多对多关系，不要求目录名称一一对应。','',
 '本索引是标准行业名称、分类和正式报告路径的权威入口。原“机器人硬件”和“商业火箭与商业航天”拆分为6个新主题，原综合报告及历史版本完整归档；另新增5个主题。OCI原名称与报告保留，类型改为横向专题。','',
 '2026-09-10迁移时点：80个活动条目已有报告（79个经济主题及1个横向专题），11个新主题待研究。此前新增的5个AI软件行业均已有2026-09-06报告。完成状态以后续实际最新报告为准；本次不生成研究报告或修改研究方案。','', '## 目录统计','']
lines += [f'- {c}：{industry_counts[c]} 个条目'+('（17个经济主题＋1个横向专题）' if c=='AI网络_光互联_铜互联' else '') for c in industry_cats]
lines+=['','## 索引表','','| 行业名称 | 目录 | 研究范围提示 | 专题类型 | 分类变更备注 |','|---|---|---|---|---|']
for e in industries:
    lines.append(f"| {cell(e['name'])} | \x60{e['category']}/\x60 | {cell(e['scope'])} | {e['type']} | {cell(e['mapping'])} |")
lines+=['','研究范围提示用于划清相邻专题的对象和交叉关系，不替代研究方案，也不预设研究结论。原综合报告归档路径和完整迁移清单见项目备份目录“公司行业索引分类升级_2026-09-10”。']
new_industry_text='\n'.join(lines)+'\n'
(OUT/'新公司索引.md').write_text(new_company_text,encoding='utf-8')
(OUT/'新行业索引.md').write_text(new_industry_text,encoding='utf-8')
plan={'prepared_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'root':str(ROOT),'output':str(OUT),'old_companies':old_companies,'companies':companies,'old_industries':old_industries,'industries':industries,'company_categories':list(CATS.values()),'industry_categories':industry_cats,'renames':renames,'file_moves':file_moves,'archive_dirs':archive_dirs,'ensure_dirs':dirs,'all_source_files':final_files,'direct_company_reports':direct_before,'protected_files':protected,'source_code':[str(p) for p in source_code],'index_updates':[{'source':str(OUT/'新公司索引.md'),'destination':str(COMPANY_ROOT/'公司索引.md')},{'source':str(OUT/'新行业索引.md'),'destination':str(INDUSTRY_ROOT/'行业索引.md')}],'original_index_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in backup_files[:2]}}
(OUT/'迁移计划.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'companies':len(companies),'categories':dict(company_counts),'industries':len(industries),'industry_categories':dict(industry_counts),'current_company_reports':len(direct_before),'changed_existing_company_categories':sum(e['old_category']!=e['category'] for e in companies if not e['is_new']),'individual_report_moves':len(file_moves),'all_preserved_files':len(snapshot),'protected_files':len(protected),'directory_renames':len(renames),'archive_directories':len(archive_dirs)},ensure_ascii=False))
