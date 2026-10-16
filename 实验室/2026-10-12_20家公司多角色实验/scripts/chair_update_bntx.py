import json,pathlib
b=pathlib.Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
p=b/'05_chair/chair_card_inputs.json';r=json.loads(p.read_text(encoding='utf-8'))
c=next(x for x in r if x['ticker']=='BNTX')
c['strongest_bear']='地区销售、销售版税、利润分成和试验终止均会改变归属价值；真实阶梯费率部分保密，研发烧损与终端销售仍主导估值，现金不是股价底'
c['forecast_caveat']='现金从2026-06-30滚到2028-04-12约21.4个月。末审改六桶：pumitamig50%利润；gotistobart全球独家但扣销售版税；T-Pam除大陆港澳权益；DB1311美国五月已行使利润分成；BNT113全有；autogene仅存续胰腺50%。15%版税、85%区域销售、美国60%销售及DB1311美国50%分利均研究假设，非合同披露率。成功概率只乘一次'
c['minority_view']='修正并非统一砍价：gotistobart销售版税拖累与T-Pam较宽地区权益部分抵消，DB1311和mRNA分桶再校准；旧四桶133.83改131.68，核心资金/临床论点保留。CRC和尿路上皮已终止，不可用成功总管线掩盖；未公开费率不等最差值必发生'
p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
p=b/'scripts/chair_publish.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace("for rank,r in enumerate(rows,1):", """extras['BNTX']=[
('https://www.sec.gov/Archives/edgar/data/1776985/000177698523000016/ex991230320proncoc4.htm','2023-03-20','gotistobart全球独家商业权与双位数阶梯销售版税，不能混成80%股权'),
('https://www.sec.gov/Archives/edgar/data/1776985/000177698524000027/exhibit450dualityher2agree.htm','2023-03-16','T-Pam授权排除大陆香港澳门但包含台湾，销售版税数字删节'),
('https://en.dualitybiologics.com/news/615.html','2026-08-28','合作方确认DB1311美国利润/成本分成期权五月已行使，旧未行使状态作废'),
('https://www.biontech.com/au/en/home/mediaroom/news/statements/2026/08/BioNTech-Provides-Update-on-Phase-2-Clinical-Trial-of-Autogene-Cevumeran-in-Resected-Colorectal-Cancer.html','2026-08-28','autogene CRC试验终止，胰腺项目保留，不重新计入停止项目销售')]
for rank,r in enumerate(rows,1):""")
s=s.replace("r['sources']=ss", """r['sources']=ss
 if t=='BNTX':
  r['evidence_files']+=['04_verification/V1_BNTX权益追加核验.md','04_verification/V2_BNTX_rights_correction.md']
  r['round_chain']+=['V1/V2权益追加与主席再裁决']
  r['verified_facts']+=['gotistobart是全球独家授权加双位数销售版税；T-Pam排除大陆港澳而包含台湾；DB1311美国成本/利润期权2026年5月已行使；autogene CRC及尿路上皮试验终止。']""")
s=s.replace("def basebridge(c):\n s=c['scenarios'][1];x=s['inputs'];typ=c['model_type']", """def basebridge(c):
 s=c['scenarios'][1];x=s['inputs'];typ=c['model_type']
 if c['ticker']=='BNTX':
  buckets='；'.join(z['name']+' PV '+format(z['rNPV_B'],'.3f')+'B' for z in x['branches'])
  return '现金16.6342B欧元×1.10−3.6B观察日前烧损=14.69762B美元；六桶'+buckets+'；相加后扣观察日后开发/里程碑PV2.5B，除258M ADS。goti成功利润=3×(45%−15%销售版税)×80%；T-Pam=3.5×85%地区×(40%−15%)×80%；DB1311=1.5×[60%美国×40%利润率×50%分利+25%其他地区×(40%−15%)]×80%，美国不再扣同项版税。版税10–20%和美国分利40–60%的其他条件不变敏感价为124.72–138.65美元，不是概率区间。'
""")
s=s.replace('BMS自方财报验证经济权利；合作临床稿不能算独立重复试验。修订后管线地区权益仍需按资产审计。','BMS及Duality自方财报、原协议验证不同经济权利；合作临床稿不算独立重复试验。精确版税/美国分利被删节，地区销售权重与净价仍需假设。')
p.write_text(s,encoding='utf-8')
print('updated BNTX inputs and generator, awaiting final go')
