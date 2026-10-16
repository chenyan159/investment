import json, pathlib, hashlib, math, datetime
R=pathlib.Path(__file__).resolve().parents[1]
P=R/'04_verification/V2_models.json'
D=json.loads(P.read_text(encoding='utf-8-sig'))
checks=[]
def check(t,b,k,actual,expected):
    if actual is None or expected is None: return
    ok=math.isfinite(actual) and abs(actual-expected)<=max(1e-7,abs(expected)*1e-9)
    checks.append(dict(ticker=t,branch=b,field=k,stored=actual,independent=expected,ok=ok))
def capital(i,p):
    if p<i['preferred_initial_price']: rate=i['preferred_max_rate']
    elif p<i['preferred_threshold_price']: rate=1000/p
    else: rate=i['preferred_min_rate']
    n=i['base_common_plus_employee_shares_m']+i['preferred_units_m']*rate
    debt=i['remaining_bank_debt_m']
    for note in i['convertible_notes']:
        if p>note['strike']: n+=note['principal_m']/note['strike']
        else: debt+=note['principal_m']
    return n,debt
def warr(i,p):
    strikes=[s for s in i['warrant_strikes'] if p>s]
    cash=i['warrant_cash_per_tranche_m']*len(strikes)
    n=i['base_shares_m']+sum(i['warrant_cash_per_tranche_m']/s for s in strikes)
    return n,cash
def bisect(fn):
    lo=1e-8; hi=1000000
    for _ in range(180):
        mid=(lo+hi)/2
        if fn(mid)>0: hi=mid
        else: lo=mid
    return (lo+hi)/2
for c in D['companies']:
    t=c['ticker']; typ=c['model_type']
    for s in c['scenario_inputs']:
        i=s['inputs']; out=s['result']; b=s['branch']; n=i.get('shares_m'); derived={}
        if typ=='EV_NopAT':
            ebit=i['revenue_m']*(i['gross_margin']-i['economic_opex_rate'])
            nopat=ebit*(1-i['tax_rate']); ev=nopat*i['multiple']
            eq=ev-i['net_debt_m']-i.get('other_claims_m',0)
            derived=dict(ebit_m=ebit,nopat_m=nopat,enterprise_value_m=ev,equity_value_m=eq,price=max(0,eq/n))
        elif typ=='EV_NOPAT_endogenous_convertibles_and_preferred':
            ebit=i['revenue_m']*i['gross_margin']-i['economic_opex_m']; nopat=ebit*(1-i['tax_rate']); ev=nopat*i['multiple']
            p=bisect(lambda p: p*capital(i,p)[0]+capital(i,p)[1]+i['preferred_dividends_PV_m']-ev-i['cash_m'])
            n,debt=capital(i,p); eq=ev+i['cash_m']-debt-i['preferred_dividends_PV_m']
            derived=dict(ebit_m=ebit,nopat_m=nopat,enterprise_value_m=ev,remaining_debt_m=debt,equity_value_m=eq,price=p)
            check(t,b,'endogenous_shares',i['shares_m'],n)
        elif typ=='economic_parent_EPS_PE_plus_incremental_option':
            ebit=i['revenue_m']*i['gross_margin']-i['economic_opex_m']
            ni=(ebit-i['net_interest_cost_m'])*(1-i['tax_rate'])*(1-i['nci_fraction'])-i['preferred_distribution_m']
            core=max(0,ni*i['PE']); eq=core+i['incremental_option_value_m']
            derived=dict(ebit_m=ebit,economic_parent_net_income_m=ni,economic_EPS=ni/n,core_equity_m=core,equity_value_m=eq,price=eq/n)
        elif typ=='EV_Sales_with_profit_crosscheck':
            ebit=i['revenue_m']*i['gross_margin']-i['economic_opex_m']; nopat=ebit*(1-i['tax_rate']); ev=i['revenue_m']*i['sales_multiple']; eq=ev-i['net_debt_m']
            derived=dict(ebit_m=ebit,nopat_m=nopat,enterprise_value_m=ev,equity_value_m=eq,price=max(0,eq/n),implied_EV_NOPAT=ev/nopat if nopat>0 else None)
        elif typ=='EV_EBITDA_with_maintenance_FCF_crosscheck':
            ebitda=i['revenue_m']*i['gross_margin_before_DA']-i['cash_opex_including_SBC_equivalent_m']; ebit=ebitda-i['DA_m']; ev=ebitda*i['multiple']; eq=ev-i['net_debt_m']-i.get('remaining_environment_legal_cash_PV_m',0)
            fcf=ebitda-max(0,ebit)*i['tax_rate']-i['maintenance_capex_m']
            derived=dict(EBITDA_m=ebitda,EBIT_m=ebit,unlevered_maintenance_FCF_m=fcf,enterprise_value_m=ev,equity_value_m=eq,price=max(0,eq/n))
        elif typ.startswith('conditional_owned_asset_SOTP'):
            ev=sum(i['risk_adjusted_asset_values_m'].values()); cash=i['net_cash_m']
            if 'cash_bridge_EUR' in i:
                x=i['cash_bridge_EUR']; cash=(x['opening_EUR_m']-x['research_operating_investing_burn_EUR_m']-x['buyback_EUR_m'])*x['EURUSD_assumption']
                check(t,b,'EUR_cash_conversion',i['net_cash_m'],cash)
            derived=dict(enterprise_value_m=ev,equity_value_m=ev+cash,price=(ev+cash)/n)
        elif typ=='discounted_expansion_SOTP_endogenous_warrants':
            expansion=max(0,i['mature_incremental_NOPAT_m']*i['mature_multiple']/(1+i['discount_rate'])**i['years_to_mature']*i['conditional_execution_discount']-i['remaining_unfunded_capital_PV_m'])
            ev=i['existing_trade_EV_m']+expansion
            p=bisect(lambda p:p*warr(i,p)[0]-ev-i['net_cash_before_warrants_m']-warr(i,p)[1])
            n,proceeds=warr(i,p); eq=ev+i['net_cash_before_warrants_m']+proceeds
            derived=dict(expansion_EV_m=expansion,enterprise_value_m=ev,warrant_proceeds_m=proceeds,equity_value_m=eq,price=p)
            check(t,b,'endogenous_warrant_shares',i['shares_m'],n)
        elif typ=='project_equity_waterfall':
            ev=i['project_NOI_m']*i['NOI_multiple']; eq=max(0,ev-i['project_net_debt_m'])*i['parent_economic_ownership']+i['ChronoScale_owned_equity_m']-i['mother_net_debt_preferred_other_claims_m']
            derived=dict(project_EV_m=ev,parent_equity_m=eq,price=max(0,eq/n))
        else: raise ValueError(typ)
        for k,val in derived.items(): check(t,b,k,out.get(k),val)
        check(t,b,'return_pct',s['return_pct'],(derived['price']/c['price']-1)*100)
    i=c['scenario_inputs'][2]['inputs']; inv=c['two_x_inverse']; p=2*c['price']; n=i['shares_m']; wanted={}
    check(t,'inverse','target_price',inv['target_price'],p)
    if typ=='EV_NopAT':
        ev=p*n+i['net_debt_m']+i.get('other_claims_m',0); nopat=ev/i['multiple']
        wanted=dict(required_EV_m=ev,required_NOPAT_m=nopat,required_revenue_m=nopat/((i['gross_margin']-i['economic_opex_rate'])*(1-i['tax_rate'])))
    elif typ=='EV_NOPAT_endogenous_convertibles_and_preferred':
        n,debt=capital(i,p); ev=p*n+debt+i['preferred_dividends_PV_m']-i['cash_m']; nopat=ev/i['multiple']
        wanted=dict(shares_m=n,remaining_debt_m=debt,required_EV_m=ev,required_NOPAT_m=nopat,required_revenue_m=(nopat/(1-i['tax_rate'])+i['economic_opex_m'])/i['gross_margin'])
    elif typ=='economic_parent_EPS_PE_plus_incremental_option':
        ni=(p*n-i['incremental_option_value_m'])/i['PE']; r=((ni+i['preferred_distribution_m'])/(1-i['nci_fraction'])/(1-i['tax_rate'])+i['net_interest_cost_m']+i['economic_opex_m'])/i['gross_margin']
        wanted=dict(required_parent_NI_m=ni,required_EPS=ni/n,required_revenue_m=r)
    elif typ=='EV_Sales_with_profit_crosscheck':
        ev=p*n+i['net_debt_m']; wanted=dict(required_EV_m=ev,required_revenue_m=ev/i['sales_multiple'],required_sales_multiple_at_branch_revenue=ev/i['revenue_m'])
    elif typ=='EV_EBITDA_with_maintenance_FCF_crosscheck':
        ebitda=(p*n+i['net_debt_m']+i.get('remaining_environment_legal_cash_PV_m',0))/i['multiple']; wanted=dict(required_EBITDA_m=ebitda,required_revenue_m=(ebitda+i['cash_opex_including_SBC_equivalent_m'])/i['gross_margin_before_DA'])
    elif typ.startswith('conditional_owned_asset_SOTP'):
        wanted=dict(required_owned_pipeline_and_franchise_EV_m=p*n-i['net_cash_m'])
    elif typ=='discounted_expansion_SOTP_endogenous_warrants':
        n,proceeds=warr(i,p); ev=p*n-i['net_cash_before_warrants_m']-proceeds
        ni=(ev-i['existing_trade_EV_m']+i['remaining_unfunded_capital_PV_m'])*(1+i['discount_rate'])**i['years_to_mature']/i['mature_multiple']/i['conditional_execution_discount']
        wanted=dict(shares_m=n,required_EV_m=ev,required_mature_incremental_NOPAT_m=ni)
    elif typ=='project_equity_waterfall':
        noi=((p*n-i['ChronoScale_owned_equity_m']+i['mother_net_debt_preferred_other_claims_m'])/i['parent_economic_ownership']+i['project_net_debt_m'])/i['NOI_multiple']; wanted=dict(required_project_NOI_m=noi)
    for k,v in wanted.items(): check(t,'inverse',k,inv.get(k),v)
    for bridge in c['target_cash_bridge'].get('branches',[]):
        x=bridge['starting_net_cash_m']+sum(bridge['movements_m'].values())
        check(t,'cash_bridge '+bridge['branch'],'conditional_cash_total',bridge['calculated_ending_net_cash_m'],x)
failed=[x for x in checks if not x['ok']]
report=dict(verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),model_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),companies=len(D['companies']),scenarios=sum(len(c['scenario_inputs']) for c in D['companies']),checks=len(checks),failures=failed,scope='Root independently reimplemented arithmetic from input JSON, without copying V2 calculation code. This verifies identities only, not likelihood, completeness of financing or valuation appropriateness.',details=checks)
out=R/'04_verification/控制器_模型独立复算.json'; out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'04_verification/控制器_模型独立复算.md').write_text('# 控制器独立复算\n\n模型 SHA256：`'+report['model_sha256']+'`。\n\n38 家、152 个四情景，独立实现八类公式、反解翻倍门槛、转换证券价格一致性、欧元换算和已提供的条件现金桥。共 '+str(len(checks))+' 项数值比对，失败 '+str(len(failed))+' 项。没有复制 V2 计算程序。\n\n这是算术与输入一致性检查，不把假设认证为预测，也不把未闭合的融资与权益合同写成已验证。全部逐项结果在同名 JSON。\n\n'+json.dumps(failed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
