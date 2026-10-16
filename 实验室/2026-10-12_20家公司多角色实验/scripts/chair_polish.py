import pathlib,json
b=pathlib.Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
p=b/'05_chair/chair_card_inputs.json';s=p.read_text(encoding='utf-8').replace('旧四桶133.83改131.68','权益修订前133.83改131.68').replace('债務','债务');p.write_text(s,encoding='utf-8')
p=b/'scripts/chair_publish.py';s=p.read_text(encoding='utf-8')
s=s.replace("r['evidence_files']=['02_round1',", "r['evidence_files']=[{'R1':'02_round1/R1_cashflows.md','R2':'02_round1/R2_valuation.md','R3':'02_round1/R3_external.md','R4':'02_round1/R4_upside.md','R5':'02_round1/R5_diversification.md'}[role] for role in links if role in ['R1','R2','R3','R4','R5']]+[")
s=s.replace('**已核事实：**','**已核披露（事实/指引按原文区分）：**')
s=s.replace("(B/'06_final/最终20家公司投资研究.md').write_text(text,encoding='utf-8')", "text=re.sub('。{2,}','。',text)\n(B/'06_final/最终20家公司投资研究.md').write_text(text,encoding='utf-8')")
p.write_text(s,encoding='utf-8')
