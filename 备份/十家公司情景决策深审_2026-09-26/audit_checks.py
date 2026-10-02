"""Read-only numerical and source audit; writes results only beside this script."""
from pathlib import Path
import re, json, hashlib, datetime

ROOT = Path('D:/investment')
OUT = Path(__file__).resolve().parent
SYMS = ['MU','SNDK','ADBE','SPCX','MSFT','CRWV','TSM','ALAB','CRDO','OKLO']
PRICES = dict(zip(SYMS,[1082.28,1777.80,235.47,148.68,516.17,87.59,450.61,364.62,210.97,38.04]))
TARGETS = dict(zip(SYMS,['2028-10-31','2028-09-29','2028-12-29','2028-12-29','2028-09-29','2028-12-31','2028-12-29','2028-12-31','2028-06-30','2030-12-31']))
source_inventory, reports, return_checks = {}, {}, []
for sym in SYMS:
    paths = sorted((ROOT/'分析报告/公司情景投资决策/结果').glob(f'{sym}_*.md'))
    p = paths[-1]
    txt = p.read_text(encoding='utf-8-sig')
    reports[sym] = {'path': str(p), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes':p.stat().st_size}
    for match in re.finditer(r'基本面[/\\][^`\n|)；]+?\.md', txt):
        rel = match.group(0).replace('\\','/')
        src = ROOT/rel
        item = source_inventory.setdefault(rel, {'path':str(src), 'exists':src.exists(), 'used_by':[]})
        if sym not in item['used_by']: item['used_by'].append(sym)
        if src.exists():
            item['sha256'] = hashlib.sha256(src.read_bytes()).hexdigest()
            item['bytes'] = src.stat().st_size
            # Report hashes are checked only when they appear on the same line as the path.
            line = txt[txt.rfind('\n',0,match.start())+1:txt.find('\n',match.end())]
            cited = re.findall(r'\b[0-9a-fA-F]{64}\b',line)
            if cited: item.setdefault('reported_hash_checks',{})[sym] = cited[-1].lower() == item['sha256']
    for n,line in enumerate(txt.splitlines(),1):
        cells=[v.strip().replace('**','') for v in line.split('|')[1:-1]]
        if len(cells)<5 or not re.match(r'^(悲观|基准|乐观|突破)[／/]', cells[0]): continue
        price_field=cells[2].replace(',','')
        prices=re.findall(r'\d+(?:\.\d+)?',price_field)
        percents=re.findall(r'[+\-−]?\d+(?:\.\d+)?(?=%)',cells[3])
        if len(prices)!=2 or len(percents)!=2: continue
        target=list(map(float,prices))
        observed=[float(v.replace('−','-')) for v in percents]
        computed=[(v/PRICES[sym]-1)*100 for v in target]
        err=max(abs(a-b) for a,b in zip(observed,computed))
        return_checks.append({'symbol':sym,'line':n,'scenario':cells[0], 'target':target,
            'reported_pct':observed,'computed_pct':computed, 'max_error_percentage_points':err,
            'within_rounding_0_06pp':err<=.06})

comparisons = {
 'MU':{'base_current_value':715,'base_target_value':884,'base_target_price':[938,1218]},
 'SNDK':{'base_current_value':1182,'base_target_value':1436,'base_target_price':[1490,2080]},
 'ADBE':{'base_current_value':234,'base_target_value':298.5,'base_target_price':[279,358]},
 'SPCX':{'base_current_value':9.97,'base_target_value':12.76,'base_target_price':[21.12,30.95]},
 'MSFT':{'base_current_value':408.6,'base_target_value':480.4,'base_target_price':[511,662]},
 'CRWV':{'base_current_value':47.02,'base_target_value':64.55,'base_target_price':[45,98]},
 'TSM':{'base_current_value':278,'base_target_value':332,'base_target_price':[330.1,471.6]},
 'ALAB':{'base_current_value':76,'base_target_value':98.22,'base_target_price':[195.62,260.27]},
 'CRDO':{'base_current_value':75.7,'base_target_value':90.6,'base_target_price':[174,278]},
 'OKLO':{'base_current_value':1.06,'base_target_value':1.99,'base_target_price':[1.5,2.6]},
}
for sym,row in comparisons.items():
    row['target_date']=TARGETS[sym]
    row['reference_price']=PRICES[sym]
    row['current_value_to_price']=row['base_current_value']/PRICES[sym]
    row['target_price_to_target_value']=[v/row['base_target_value'] for v in row['base_target_price']]

derived_checks = {
 'hbm_2027': {'specialist_revenue_B':144.9,'memory_fab_revenue_B':186.2,
   'difference_pct':(186.2/144.9-1)*100,'specialist_delivery_billion_GB':6.402,
   'memory_fab_delivery_billion_GB':4.9,'specialist_implied_usd_per_GB':144.9/6.402,
   'memory_fab_usd_per_GB':38},
 'mu_floor_contract_annualized_B':100/4.5,
 'mu_floor_contract_annualized_vs_FY27_base_revenue':100/4.5/210.39,
 'alab_breakthrough_at_26x':2868.8/202.980*26+18.90,
 'alab_breakthrough_at_26x_price_return_pct':((2868.8/202.980*26+18.90)/364.62-1)*100,
 'adbe_upstream_FY29_FCF_less_SBC_B':13.14-2.70,
 'adbe_downstream_FY29_economic_FCFF_B':9.335,
 'adbe_remaining_cash_measure_difference_pct':(9.335/(13.14-2.70)-1)*100,
 'oklo_upper_breakthrough_annualized_pct':((50.3/38.04)**(1/4.263)-1)*100,
 'oklo_required_terminal_price_at_12pct':38.04*1.12**4.263,
 'crwv_capex_improvement_plus_margin_current_value_vs_price_pct':(98.62/87.59-1)*100,
}
result={'scope':'Arithmetic audit, not independent validation of forecasts; inputs copied from cited reports. Derived comparisons are diagnostic, not new fair-value estimates.',
 'reports':reports,'upstream_sources':source_inventory,'return_checks':return_checks,
 'comparisons':comparisons,'derived_checks':derived_checks}
(OUT/'核验底稿.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'reports':len(reports),'upstream_sources':len(source_inventory),
 'missing_sources':[k for k,v in source_inventory.items() if not v['exists']],
 'mismatched_hashes':[(k,s) for k,v in source_inventory.items() for s,b in v.get('reported_hash_checks',{}).items() if not b],
 'return_rows_checked':len(return_checks),'return_rounding_failures':[v for v in return_checks if not v['within_rounding_0_06pp']],
 'upstream_paths':list(source_inventory)},ensure_ascii=False,indent=2))
