from pathlib import Path
import csv,json
ROOT=Path(r'D:\drive\Investment')
OUT=ROOT/'备份/流程审计与研究方案改进_2026-09-05'
inventory=list(csv.DictReader((OUT/'data/company_industry_inventory.csv').open(encoding='utf-8-sig')))
lookup={(r['domain'],r['subject']):r for r in inventory}
company={
'PENG':(5,13,'利润现金分离；前九月CFO11.2m/净利润90.8m，非现金造假证据'),
'SMCI':(11,17,'GPU内容占比不等于利润捕获；基准收入46–53B包含51.71B一致预期'),
'MU':(302,314,'每光口是经济分摊而非物理BOM；更新版仍需自行解释模板适用性'),
'P':(529,531,'明确第二客户资格/小批量不计大额收入，不能批评完全忽略信息时钟'),
'SOMMY':(11,16,'制药和农业、处置收益与持续利润均已研究，反驳所有非AI业务被忽略'),
'AEHR':(12,18,'7/18已吸收130–150m FY27指引；名义产能超288m不等于需求'),
'MOD':(11,17,'7/31已识别可取消容量协议、毛利执行问题与未来两个季度重点'),
'WOLF':(15,26,'供给过剩、负毛利、现金流、资本稀释明确存在'),
'ADBE':(294,299,'每MW等NA，自选seat/credit/workflow单位经济；233行明确不能略过成熟核心'),
'ORCL':(9,13,'传统软件融资云扩张与资本结构、租赁承诺已有识别')}
industry=[
('数据中心电力接入与高压变电',17,19,'point_annual_run_rate','point_annual_run_rate','point_annual_run_rate'),
('数据中心直液冷系统',157,161,'next_3m_revenue','next_12m_revenue','months_13_24_revenue'),
('HBM与高带宽内存',41,47,'next_3m_revenue','next_12m_revenue','next_24m_cumulative'),
('AI-native存储与KV Cache基础设施',60,66,'next_3m_revenue','point_annual_run_rate','point_annual_run_rate'),
('CXL内存扩展与内存池化',60,60,'next_3m_revenue','next_12m_revenue','months_13_24_revenue'),
('AI集群调度与推理运行时',9,9,'point_forward_12m_pool','point_forward_12m_pool','point_forward_12m_pool'),
('800G/1.6T可插拔光模块',38,44,'next_3m_revenue','next_12m_revenue','next_24m_cumulative'),
('HBM与存储测试设备',64,69,'next_3m_revenue','next_12m_revenue','point_forward_12m_pool'),
('机器人硬件',34,41,'next_3m_revenue','next_12m_revenue','months_13_24_revenue'),
('商业火箭与商业航天',3,5,'point_annual_run_rate','point_annual_run_rate','point_annual_run_rate')]
rows=[]
for subject,(a,b,note) in company.items():
    r=lookup['company',subject]
    rows.append(dict(domain='company',subject=subject,path=r['path'],date=r['report_date'],line_start=a,line_end=b,t3='',t12='',t24='',note=note))
for subject,a,b,t3,t12,t24 in industry:
    r=lookup['industry',subject]
    rows.append(dict(domain='industry',subject=subject,path=r['path'],date=r['report_date'],line_start=a,line_end=b,t3=t3,t12=t12,t24=t24,note='人工核对正文口径；不同定义不等于篇内错误；仅本10份定向诊断样本，不外推77份比例'))
with (OUT/'data/company_industry_manual_sample.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({'company_n':len(company),'industry_n':len(industry),'industry_categories':len(set(lookup['industry',x[0]]['category'] for x in industry)),'scope':'Purposive mechanism diagnostic sample; current front sections and cited windows manually read, not full external factual validation; no statistical prevalence estimate.'},ensure_ascii=False))
