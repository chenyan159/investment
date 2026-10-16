from pathlib import Path
import json,math,re,hashlib
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'04_verification/V2_models.json').read_text(encoding='utf-8'))
checks=[]
def eq(a,b,label):
    ok=math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7); checks.append({'check':label,'ok':ok,'expected':a,'stored':b});assert ok,(label,a,b)
for m in d['companies']:
    t=m['ticker']; f=m['model_type']; prev=-1
    for s in m['scenario_inputs']:
        x=s['inputs']; n=x['shares_m'];v=s['result'];label=t+':'+s['branch'];
        if f=='EV_NopAT': value=max(0,(x['revenue_m']*(x['gross_margin']-x['economic_opex_rate'])*(1-x['tax_rate'])*x['multiple']-x['net_debt_m']-x.get('other_claims_m',0))/n)
        elif f=='economic_parent_EPS_PE_plus_incremental_option':
            ni=(x['revenue_m']*x['gross_margin']-x['economic_opex_m']-x['net_interest_cost_m'])*(1-x['tax_rate'])*(1-x['nci_fraction'])-x['preferred_distribution_m'];value=(max(0,ni*x['PE'])+x['incremental_option_value_m'])/n
        elif f=='EV_Sales_with_profit_crosscheck':value=max(0,(x['revenue_m']*x['sales_multiple']-x['net_debt_m'])/n)
        elif f=='EV_EBITDA_with_maintenance_FCF_crosscheck':value=max(0,((x['revenue_m']*x['gross_margin_before_DA']-x['cash_opex_including_SBC_equivalent_m'])*x['multiple']-x['net_debt_m']-x.get('remaining_environment_legal_cash_PV_m',0))/n)
        elif f.startswith('conditional_owned_asset'):value=(sum(x['risk_adjusted_asset_values_m'].values())+x['net_cash_m'])/n
        elif f.startswith('discounted_expansion'):
            ev=x['existing_trade_EV_m']+max(0,x['mature_incremental_NOPAT_m']*x['mature_multiple']/(1+x['discount_rate'])**x['years_to_mature']*x['conditional_execution_discount']-x['remaining_unfunded_capital_PV_m'])
            itm=[k for k in x['warrant_strikes'] if v['price']>k]; nn=x['base_shares_m']+sum(500/k for k in itm);value=(ev+x['net_cash_before_warrants_m']+500*len(itm))/nn;eq(nn,n,label+':warrant_shares')
        elif f.startswith('EV_NOPAT_endogenous'):
            p=v['price'];pr=x['preferred_max_rate'] if p<x['preferred_initial_price'] else 1000/p if p<=x['preferred_threshold_price'] else x['preferred_min_rate']; nn=x['base_common_plus_employee_shares_m']+x['preferred_units_m']*pr; dd=x['remaining_bank_debt_m']
            for no in x['convertible_notes']:
                if p>no['strike']:nn+=no['principal_m']/no['strike']
                else:dd+=no['principal_m']
            eq(nn,n,label+':conversion_shares');ev=(x['revenue_m']*x['gross_margin']-x['economic_opex_m'])*(1-x['tax_rate'])*x['multiple'];value=(ev+x['cash_m']-dd-x['preferred_dividends_PV_m'])/nn
        else:value=max(0,(max(0,x['project_NOI_m']*x['NOI_multiple']-x['project_net_debt_m'])*x['parent_economic_ownership']+x['ChronoScale_owned_equity_m']-x['mother_net_debt_preferred_other_claims_m'])/n)
        eq(value,v['price'],label+':price');eq((value/m['price']-1)*100,s['return_pct'],label+':return');assert value>=prev;prev=value
        if t=='BNTX':
            b=x['cash_bridge_EUR'];eq((b['opening_EUR_m']-b['research_operating_investing_burn_EUR_m']-b['buyback_EUR_m'])*b['EURUSD_assumption'],x['net_cash_m'],label+':FX_cash')
    for b in m['target_cash_bridge'].get('branches',[]):eq(b['starting_net_cash_m']+sum(b['movements_m'].values()),b['target_net_cash_m'],t+':'+b['branch']+':cash_bridge')
    z=m['two_x_inverse'];x=m['scenario_inputs'][2]['inputs'];n=z['shares_m'];target=z['target_price']
    if f=='EV_NopAT':q=(z['required_revenue_m']*(x['gross_margin']-x['economic_opex_rate'])*(1-x['tax_rate'])*x['multiple']-x['net_debt_m']-x.get('other_claims_m',0))/n
    elif f=='economic_parent_EPS_PE_plus_incremental_option':q=(((z['required_revenue_m']*x['gross_margin']-x['economic_opex_m']-x['net_interest_cost_m'])*(1-x['tax_rate'])*(1-x['nci_fraction'])-x['preferred_distribution_m'])*x['PE']+x['incremental_option_value_m'])/n
    elif f=='EV_Sales_with_profit_crosscheck':q=(z['required_revenue_m']*x['sales_multiple']-x['net_debt_m'])/n
    elif f=='EV_EBITDA_with_maintenance_FCF_crosscheck':q=(z['required_EBITDA_m']*x['multiple']-x['net_debt_m']-x.get('remaining_environment_legal_cash_PV_m',0))/n
    elif f.startswith('conditional_owned_asset'):q=(z['required_owned_pipeline_and_franchise_EV_m']+x['net_cash_m'])/n
    elif f.startswith('discounted_expansion'):q=(x['existing_trade_EV_m']+z['required_mature_incremental_NOPAT_m']*x['mature_multiple']/(1+x['discount_rate'])**x['years_to_mature']*x['conditional_execution_discount']-x['remaining_unfunded_capital_PV_m']+x['net_cash_before_warrants_m']+500*z['warrant_tranches_in_money'])/n
    elif f.startswith('EV_NOPAT_endogenous'):q=((z['required_revenue_m']*x['gross_margin']-x['economic_opex_m'])*(1-x['tax_rate'])*x['multiple']+x['cash_m']-z['remaining_debt_m']-x['preferred_dividends_PV_m'])/n
    else:q=((z['required_project_NOI_m']*x['NOI_multiple']-x['project_net_debt_m'])*x['parent_economic_ownership']+x['ChronoScale_owned_equity_m']-x['mother_net_debt_preferred_other_claims_m'])/n
    eq(q,target,t+':inverse_replug')
# Check price against dated controller quotes where its stored row text is parseable.
history={}
for p in (R/'07_logs').glob('controller_history_close_*.json'):
    j=json.loads(p.read_text(encoding='utf-8-sig'))
    if isinstance(j,list):
        for v in j:
            if isinstance(v,dict) and 'ticker'in v:history[v['ticker']]=json.dumps(v,ensure_ascii=False)
for m in d['companies']:
    h=history.get(m['ticker'],''); found=[]
    for ln in h.split('\\n'):
        if 'Oct 12, 2026' in ln:
            mo=re.search(r'Oct 12, 2026\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)\s*\|\s*([\d,.]+)',ln)
            if mo:found.append(float(mo[4].replace(',','')))
    if found:eq(found[0],m['price'],m['ticker']+':controller_close')
summary={'company_count':len(d['companies']),'scenario_count':sum(len(m['scenario_inputs'])for m in d['companies']),'checks':len(checks),'failed':sum(not c['ok'] for c in checks),'max_price_delta':max(abs(c['expected']-c['stored']) for c in checks if c['check'].endswith(':price')),'coverage_scope':'formula/return/inverse/FX/warrants/conditional cash arithmetic only; NOT finance-truth certification','details':checks}
(R/'07_logs/V2_recalculation_audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
paths=['04_verification/V2_models.json','04_verification/V2_models.csv','04_verification/V2_numeric_verification.md','07_logs/V2_sources.json','07_logs/V2_reading_notes.md','07_logs/V2_build.py','07_logs/V2_verify.py','07_logs/V2_recalculation_audit.json']
paths+=['04_verification/V2_chair_revision.md','07_logs/V2_chair_addendum.py']
manifest={'role':'V2','sealed':True,'coverage':38,'scenario_rows':152,'audit_failed':summary['failed'],'files':[{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'bytes':(R/p).stat().st_size}for p in paths]}
(R/'07_logs/V2_seal_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='details'},ensure_ascii=False))
