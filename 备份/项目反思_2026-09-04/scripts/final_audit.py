from pathlib import Path
import re,json,hashlib,sys,platform
import pandas as pd,numpy as np,requests
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data'
f=ROOT/'00_项目反思与问题诊断.md';t=f.read_text(encoding='utf-8');t=t.replace('远小于一般实际交易摩擦','且尚未计入交易摩擦，不能据此确认存在实际净超额');f.write_text(t,encoding='utf-8')
f=ROOT/'evidence/decisions_问题审计.md';t=f.read_text(encoding='utf-8');t=t.replace('研究方案_2026-07-15_未来经营与再投资传导升级前.md:97','研究方案_2026-07-15_未来经营与再投资传导升级前.md:111');f.write_text(t,encoding='utf-8')
bad=[];blank=[];link_count=0
for f in ROOT.rglob('*.md'):
    if '原文摘录' in f.name:continue
    text=f.read_text(encoding='utf-8-sig')
    assert not re.search(r'\{\{[A-Z_]+\}\}',text),str(f)
    for path,ln in re.findall(r'\]\(<?(D:[^>\n]*?)(?::(\d+))?>?\)',text):
        link_count+=1;p=Path(path)
        if not p.exists():bad.append((str(f),path,ln))
        elif ln:
            ls=p.read_text(encoding='utf-8-sig').splitlines();i=int(ln)
            if not 1<=i<=len(ls):bad.append((str(f),path,ln))
            elif not ls[i-1].strip():blank.append((str(f),path,ln))
assert not bad,bad
assert not blank,blank
co=pd.read_csv(D/'company_returns.csv');r=pd.read_csv(D/'historical_rankings.csv',dtype={'list_id':str});obs=pd.read_csv(D/'company_observations_by_source_date.csv');dec=pd.read_csv(D/'decisions_historical.csv');cells=pd.read_csv(D/'decisions_matrix_cells.csv');p=pd.read_csv(D/'daily_prices.csv')
assert len(co)==192 and co.ticker.nunique()==192
assert len(r)==5376 and r.groupby('list_id').size().eq(192).all()
assert len(obs)==768 and obs.groupby('layer').size().eq(192).all()
assert len(cells)==3840
assert not p.duplicated(['symbol','date']).any()
assert set(co.ticker)==set(dec.ticker)==set(r.ticker)
sources=[]
for filename,pc,hc in [('upstream_company_inventory.csv','path','sha256'),('historical_rankings_source_audit.csv','source_path','sha256'),('decisions_historical.csv','scenario_path','scenario_sha256'),('decisions_historical.csv','evaluation_path','evaluation_sha256')]:
    x=pd.read_csv(D/filename)
    for _,row in x.iterrows():sources.append((row[pc],row[hc]))
checked={}
for path,expected in sources:
    if path in checked:continue
    actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    checked[path]={'expected':expected,'actual':actual,'unchanged':expected.lower()==actual.lower()}
assert all(x['unchanged'] for x in checked.values()),'Source changed during audit'
pd.DataFrame([{'path':k,**v} for k,v in checked.items()]).to_csv(D/'source_hash_recheck.csv',index=False,encoding='utf-8-sig')
stats={'companies':192,'rank_lists':28,'rank_rows':5376,'source_date_observations':768,'matrix_cells':3840,'price_rows':len(p),'local_links_checked':link_count,'invalid_links':len(bad),'empty_line_citations':len(blank),'unique_source_hashes_rechecked':len(checked),'source_hash_changes':0,'python':sys.version,'pandas':pd.__version__,'numpy':np.__version__,'requests':requests.__version__,'os':platform.platform()}
(D/'final_validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False,indent=2))
