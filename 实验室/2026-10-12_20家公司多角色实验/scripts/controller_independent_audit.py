"""Independent read-only recalculation of V2 inputs; no import of its model builder.
Writes only the audit artifact inside this experiment. Conditional inputs are not verified facts.
"""
import json, math, hashlib
from decimal import Decimal as D
from pathlib import Path
from datetime import datetime, timezone
R=Path(__file__).resolve().parents[1]
P=R/'04_verification/V2_models.json'
o=json.loads(P.read_text(encoding='utf-8-sig'))
universe={x['ticker'] for x in json.loads((R/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))}
quotes={x['ticker']:x['close'] for x in json.loads((R/'04_verification/controller_web_quote_checks.json').read_text(encoding='utf-8-sig'))['records']}
rows=[]
def dec(v): return D(str(v))
def price(c,s):
    x=s['inputs']; k=c['model_type']; d=lambda key: dec(x[key])
    if k=='economic EPS x PE':
        operating=d('revenue_B')*d('economic_gross_margin')-d('opex_ex_SBC_B')-d('SBC_expense_B')
        net=(operating-d('net_interest_expense_B'))*(1-d('tax_rate'))+d('other_after_tax_B')-d('preferred_dividend_B')
        return max(D(0),net/d('FD_shares_B')*d('PE'))
    if k in ('EV/EBITDA','EV/Sales'):
        return max(D(0),(d('revenue_B')*d('economic_margin')*d('multiple')-d('net_debt_B')-d('other_senior_claims_B'))/d('FD_shares_B'))
    if k=='FCFE multiple':
        inc=sum(d(i) for i in ['legacy_EBITDA_B','Cogentrix_EBITDA_B','incremental_Meta_EBITDA_B'])
        out=sum(d(i) for i in ['SBC_B','maintenance_capex_B','cash_interest_B','cash_tax_B','preferred_dividend_B','growth_capex_B','asset_closure_other_B'])
        return (inc-out)/d('FD_shares_B')*d('FCFE_multiple')
    if k=='economicFCFE multiple':return (d('CFO_minus_capex_after_interest_B')-d('SBC_B'))/d('FD_shares_B')*d('equity_cash_multiple')
    if k=='underwritingEPS multiple':return (d('net_premiums_earned_B')*(1-d('combined_ratio'))+d('investment_other_income_B'))*(1-d('tax_rate'))/d('FD_shares_B')*d('PE')
    if k=='RMB economicEPS convertedonce':
        ni=(d('adjusted_EBITA_RMB_B')-d('SBC_RMB_B')-d('economic_recurring_cost_RMB_B'))*(1-d('tax_rate'))+d('net_attributable_other_RMB_B')
        return ni*d('ordinary_per_ADS')/d('ordinary_shares_B')/d('RMB_per_USD')*d('PE')
    if k=='pipeline rNPV plusremainingfinancialassets':
        pipeline=D(0)
        for z in x['branches']:
            b=lambda key: dec(z[key])
            if 'success_sales_B' in z:
                income=b('success_sales_B')*b('ownership')*b('after_tax_margin')
                factor=b('discount_factor')
            else:
                if 'US_profit_share' in z:
                    us=b('US_global_sales_fraction')*b('pre_partner_operating_margin')*b('US_profit_share')
                    rest=b('other_licensed_global_sales_fraction')*(b('pre_partner_operating_margin')-b('exUS_sales_royalty_rate'))
                    income=b('success_global_product_sales_B')*(us+rest)*(1-b('tax_rate'))
                else:
                    income=b('success_global_product_sales_B')*b('licensed_global_sales_fraction')*(b('pre_partner_operating_margin')-b('sales_royalty_rate'))*b('profit_share')*(1-b('tax_rate'))
                assert abs(income-b('success_BNTX_net_income_B'))<D('1e-10')
                factor=1/(1+b('discount_rate'))**int(z['years_to_terminal'])
                assert abs(factor-b('discount_factor'))<D('1e-10')
            branch=income*b('terminal_PE')*factor*b('subjective_success_probability')
            assert abs(branch-b('rNPV_B'))<D('1e-10')
            pipeline+=branch
        return (d('start_financial_assets_EUR_B')*d('USD_per_EUR')-d('burn_to_observation_USD_B')+pipeline-d('post_observation_development_PV_B'))/d('ADS_B')
    if k=='financedclinical rNPV':
        shares=d('current_shares_B')+d('awards_other_B')+d('net_equity_raise_B')/(1-d('issuance_fee'))/d('issue_price')
        assert abs(shares-d('FD_shares_B'))<D('1e-12')
        pv=d('SPS_success_after_tax_income_B')*d('PE')/(1+d('discount_rate'))**int(x['years_to_success_earnings'])*d('subjective_probability')
        return max(D(0),(pv+d('other_pipeline_net_rNPV_B')+d('remaining_cash_B')-d('debt_B')-d('post_observation_development_PV_B'))/shares)
    if k=='EVsales + cash minusdilutiveoptionvalue':
        p=s['price']; sig=x['volatility']; rate=x['risk_free_rate']
        def option(z):
            t=z['remaining_years']; strike=z['strike_USD']; sd=sig*math.sqrt(t)
            a=(math.log(p/strike)+(rate+sig*sig/2)*t)/sd; b=a-sd
            return z['shares_B']*(p*.5*math.erfc(-a/math.sqrt(2))-strike*math.exp(-rate*t)*.5*math.erfc(-b/math.sqrt(2)))
        claim=sum(option(z) for z in x['tranches'])
        residual=p*x['base_awards_future_SBC_shares_B']+claim-(x['sales_B']*x['EV_sales']+x['remaining_net_cash_B'])
        assert abs(residual)<1e-6, residual
        assert abs(sum(z['shares_B'] for z in x['tranches'])-.078734968)<1e-10
        return dec(p)
    if k=='retainedrevenueEV withcash/profitcrosscheck':
        sales=sum(d(drug+'_paid_years')*d(drug+'_net_price')/D('1e9') for drug in ['TRYNGOLZA','DAWNZERA','ZANVASTRO'])
        royalty=d('SPINRAZA_gross_royalty_B')*d('SPINRAZA_retention')+sum(d(drug+'_partner_sales_B')*d(rate) for drug,rate in [('WAINUA_PN','WAINUA_royalty'),('bepirovirsen','bepirovirsen_royalty'),('sefaxersen','sefaxersen_royalty'),('ulefnersen','ulefnersen_royalty')])
        total=sales+royalty+d('other_retained_revenue_B')+d('collaboration_revenue_B')
        return max(D(0),(total*d('EV_retained_sales')-d('net_debt_B'))/d('FD_shares_B'))
    raise ValueError(k)
for c in o['companies']:
    assert c['ticker'] in universe
    assert c['observation_date']=='2028-04-12' and c['reference_price_date']=='2026-10-12'
    assert c['reference_price']==quotes[c['ticker']]
    assert c['currency']['trading']==c['currency']['model']=='USD'
    assert [s['scenario'] for s in c['scenarios']]==['bear','base','bull']
    prices=[]
    for s in c['scenarios']:
        p=float(price(c,s)); ret=100*(p/c['reference_price']-1)
        assert abs(p-s['price'])<1e-5,(c['ticker'],s['scenario'],p,s['price'])
        assert abs(ret-s['return_pct'])<2e-5,(c['ticker'],s['scenario'],ret,s['return_pct'])
        rows.append(dict(ticker=c['ticker'],scenario=s['scenario'],independent_price=p,recorded_price=s['price'],absolute_price_difference=abs(p-s['price']),independent_return_pct=ret,status='PASS'))
        prices.append(p)
    assert prices==sorted(prices)
assert len(rows)==87 and len({c['ticker'] for c in o['companies']})==29
result=dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),model_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),companies=29,scenarios=87,method='Separately implemented Decimal formulas; option model verified with erfc equation residual; no V2 builder imported or executed',limitations='Arithmetic, identity, units and date controls only. Business forecasts, clinical probabilities, economic margins, funding and valuation multiples remain conditional. A bear price is not a maximum loss.',rows=rows)
(R/'04_verification/controller_independent_model_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
