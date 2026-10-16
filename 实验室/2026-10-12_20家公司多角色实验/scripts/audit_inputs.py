import csv,json,re,hashlib
from pathlib import Path
from collections import Counter
OUT=Path(__file__).resolve().parents[1]
U=json.loads((OUT/'01_inputs/universe.json').read_text(encoding='utf-8'))
M=json.loads((OUT/'00_control/input_manifest.json').read_text(encoding='utf-8'))

def num(v):
    v=str(v).replace('$','').replace(',','')
    m=re.fullmatch(r'(-?\d+(?:\.\d+)?)([TBMK]?)',v)
    return float(m[1])*{'':1,'T':1e12,'B':1e9,'M':1e6,'K':1e3}[m[2]] if m else None

def delta(a,b): return abs(a/b-1) if a is not None and b not in [None,0] else None
rows=[]
for r in U:
    q=r['finance'];p=num(q['最新价格']);cap=num(q['市值']);shares=num(q['shares_outstanding']);rev=num(q['ttm_revenue']);eps=num(q['ttm_eps']);feps=num(q['forward_eps']);ps=num(q['P/S'])
    cap_err=delta(p*shares,cap) if p is not None and shares is not None else None
    ttm_pe_err=delta(p/eps,num(q['TTM PE'])) if eps and eps>0 else None
    fwd_pe_err=delta(p/feps,num(q['Forward PE'])) if feps and feps>0 else None
    ps_err=delta(cap/rev,ps) if cap and rev and q['currency']==q['financial_currency'] else None
    flags=[]
    if q['currency']!=q['financial_currency']:flags.append('cross_currency_ps_unusable_without_fx')
    if q['adr_ratio']=='需确认':flags.append('adr_ratio_unconfirmed_in_snapshot')
    if cap_err is not None and cap_err>.05:flags.append('share_class_or_cap_mismatch')
    if q['价格日期']!='2026-10-12':flags.append('stale_price')
    if feps is None or feps<=0:flags.append('no_positive_forward_eps')
    rows.append(dict(ticker=r['ticker'],category=r['category'],price=p,price_date=q['价格日期'],currency=q['currency'],financial_currency=q['financial_currency'],listing_type=q['listing_type'],adr_ratio=q['adr_ratio'],market_cap_check_error=cap_err,ttm_pe_check_error=ttm_pe_err,forward_pe_check_error=fwd_pe_err,ps_same_currency_check_error=ps_err,data_flags=';'.join(flags),source_line=q['source_line'],coverage='screened_financials_and_source_presence_only',disposition='pending_independent_research'))
with (OUT/'00_control/全池245家数据口径审计.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
counts=Counter(flag for row in rows for flag in row['data_flags'].split(';') if flag)
future=[m['path'] for m in M if (max(re.findall(r'202\d-\d{2}-\d{2}',m['path']),default='')>'2026-10-12')]
report={'all_companies':len(rows),'flags':dict(counts),'future_dated_filenames':future,'mismatched_cap_tickers':[r['ticker'] for r in rows if 'share_class_or_cap_mismatch' in r['data_flags']], 'note':'仅检验数据源内部算术一致性。不能证明底层EPS、预测、股数、FX或市值经济口径正确。多股权公司市值差异不自动判为错误。'}
(OUT/'00_control/data_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
