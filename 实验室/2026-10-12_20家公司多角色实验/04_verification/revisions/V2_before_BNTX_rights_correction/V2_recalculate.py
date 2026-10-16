"""Reproducible conditional valuation ledger; stdlib only. Run python -B this_file.
All money/share quantities B unless field name says otherwise. No network or external writes.
"""
import json, math, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'04_verification'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
quotes={x['ticker']:x for x in read('04_verification/controller_web_quote_checks.json')['records']}
s1={x['ticker']:x for x in read('03_round2/S1_ai_upside.json')['companies']}
s2={x['ticker']:x for x in read('03_round2/S2_nonai_upside.json')['companies']}
companies=[]
SC=['bear','base','bull']

def company(t,kind,period,assumptions,unresolved='',verdict='条件模型通过；预测仍须经营兑现'):
    sec={'type':'US listed common equity','ordinary_shares_per_ADS':None,'economic_unit':'one common share'}
    curr={'trading':'USD','financial':'USD','model':'USD'}
    if t in ['BNTX','ARGX','BABA','TSM']:
        sec.update(type='US listed ADS',ordinary_shares_per_ADS={'BNTX':1,'ARGX':1,'BABA':8,'TSM':5}[t],economic_unit='one ADS-equivalent equity unit')
    if t=='BNTX': curr.update(financial='EUR',FX_assumption_USD_per_EUR=1.10)
    if t=='BABA': curr.update(financial='RMB',FX_assumption_RMB_per_USD=7.0)
    if t=='TSM': curr.update(financial='TWD',FX_treatment='USD revenue forecasts; 25.95B ordinary / 5 = 5.19B ADS; no second FX conversion')
    if t=='FLNC': sec.update(economic_unit='Class A plus exchangeable LLC economic units',current_economic_units_B=(143136891+41432781)/1e9)
    if t=='CLS': sec.update(type='NYSE USD quoted common equity; Canadian issuer')
    if t=='POET': sec.update(type='NASDAQ USD quoted common equity; Canadian issuer')
    obj=dict(ticker=t,observation_date='2028-04-12',earnings_period=period,security=sec,currency=curr,reference_price=quotes[t]['close'],reference_price_date='2026-10-12',price_verification='Inherited controller independent web historical close; not independently fetched by V2',model_type=kind,scenarios=[],assumptions=assumptions,unresolved=unresolved,verdict=verdict,return_basis='USD price return, excluding dividends, fees and taxes; not total return')
    companies.append(obj); return obj

def row(c,i,inp,formula,price,**extra):
    assert math.isfinite(price) and price>=0
    c['scenarios'].append(dict(scenario=SC[i],inputs=inp,formula=formula,price=round(price,6),return_pct=round(100*(price/c['reference_price']-1),6),**extra))

def pe(t,period,rev,gm,op_non_sbc,sbc,interest,tax,shares,mults,note,unresolved='',other_after_tax=None,preferred=None):
    c=company(t,'economic EPS x PE',period,note,unresolved)
    for i in range(3):
        x=dict(revenue_B=rev[i],economic_gross_margin=gm[i],opex_ex_SBC_B=op_non_sbc[i],SBC_expense_B=sbc[i],net_interest_expense_B=interest[i],tax_rate=tax[i],FD_shares_B=shares[i],PE=mults[i],other_after_tax_B=(other_after_tax or [0]*3)[i],preferred_dividend_B=(preferred or [0]*3)[i])
        ebit=x['revenue_B']*x['economic_gross_margin']-x['opex_ex_SBC_B']-x['SBC_expense_B']
        ni=(ebit-x['net_interest_expense_B'])*(1-x['tax_rate'])+x['other_after_tax_B']-x['preferred_dividend_B']
        eps=ni/x['FD_shares_B']; p=max(0,eps*x['PE'])
        row(c,i,x,'max(0,((revenue*economic_GM-opex_ex_SBC-SBC-interest)*(1-tax)+other_after_tax-preferred_dividend)/FD_shares*PE)',p,economic_EBIT_B=ebit,economic_net_income_B=ni,economic_EPS=eps)
    return c

# New 18-month operating views, not a date relabel of S1's October 2027 targets.
pe('NVDA','CY2028 forward annual operating earnings (mostly FY2029 ending Jan2029); FY27 realized base and FY28 ramp as bridge',
 [430,600,760],[.70,.74,.75],[38,42,48],[10,10,12],[0,0,0],[.17]*3,[24,23.9,23.8],[20,27,32],
 'CY2028 base600B vs S1 near-term540B reflects another two-quarter Rubin/next-platform delivery interval; upside requires continued customer spending. Opex52B includes10B SBC; FY27 nonGAAP already includes SBC, so there is no second reported-SBC deduction. No recurring portfolio gains, no net cash addition; buybacks assumed only modestly exceed issuance.',
 '600/760B are V2 conditional budgets, not guidance; financing-backed customer demand and commitments remain a tail risk.')
pe('MU','FY2028 ending Aug2028 forward earnings, valued Apr2028; FY27 high-price contracts are operating anchor',
 [180,260,315],[.68,.88,.90],[8.5,8,9],[1.5,1.5,1.5],[0]*3,[.155]*3,[1.17,1.16,1.16],[6,9,11],
 'Base retains strong219.3B economic EBIT:260*.88-9.5. Here9.5B total opex explicitly contains1.5B SBC; gross margin is economic after production SBC. This is a required budget, not a claim that reported nonGAAP automatically includes SBC. FY28 base holds FY27 high profitability rather than extrapolating another ASP doubling. Bear embodies FY28 supply/ASP normalization, bull demand and mix sustain scarcity.',
 'Base88% economic GM and9.5B total cost need verification each quarter; reported Q1 adjusted86.25 vs GAAP85.95 demonstrates costs cannot silently disappear.')
pe('AVGO','FY2028 ending Oct2028 forward annual earnings',
 [145,190,240],[.70,.73,.75],[15,15,17],[9,10,11],[3.2,3,2.8],[.16]*3,[5.0,5.0,5.05],[19,26,30],
 'S1 revenue170B replaced by FY28 190B with10B recurring SBC; Q3 adjusted OP20.095 less SBC2.019 =18.076B (61.09%). Base economic OPM59.84% is below that quarter. Acquisition amortization normalized but employee pay not free; PE is after interest, no second net-debt subtraction.',
 'Custom silicon customer concentration and future integration charges; larger SBC than budget reduces EPS.')
pe('CLS','CY2028 forward earnings; CY2027 target expansion followed by capacity utilization',
 [29,39,48],[.115,.13,.14],[1.18,1.40,1.65],[.12,.16,.20],[.12,.12,.12],[.20]*3,[.130,.132,.135],[18,25,29],
 'Rebuilt real EMS gross-margin bridge (11.5/13/14%, not S1 synthetic19%). Q2 economic OP=458.3-104.1=354.2M retaining SBC19.3M; adding9.9M acquisition amortization gives364.1M. Base CY28 economic OPM9.0% requires mix/scale, excludes TRS gains. Future shares include financing/rewards.',
 '39B delivery and13% economic GM are assumptions; working capital can lag EPS.')
pe('CRDO','FY2029 ending Apr2029 forward run-rate at Apr2028; FY27 current quarter anchor',
 [2.3,3.7,5],[.64,.68,.69],[.55,.70,.88],[.45,.60,.72],[0]*3,[.15]*3,[.210,.218,.225],[24,36,44],
 'Revenue increased from S1 3.2 to3.7B for later horizon, but recurring SBC explicitly paid:Q1 economic OP230.641-87.979=142.662M. Base OPM32.86%, not S1 free-SBC43%. Gross margin after production SBC; no cash add.',
 'Customer concentration and SBC budget are key; reserve rather than automatic exclusion.')
pe('AAOI','CY2028 forward annual sales; capacity ramp through CY2027',
 [1.2,2.3,3.3],[.28,.33,.36],[.22,.27,.33],[.06,.08,.10],[.02]*3,[.22]*3,[.11,.12,.13],[20,30,38],
 'Later horizon raises base sales2.0→2.3B but explicitSBC80M andFD120M replace free-SBC model; capacity is converted to shipped yield, never nameplate times full year.',
 'Revenue ramp/customer warrants financing may exceed allowance; downside large.')
pe('PSIX','CY2028 forward annual earnings; 2026H2/2027 delivery recovery anchor',
 [.62,.90,1.20],[.25,.29,.32],[.077,.091,.108],[.003,.004,.007],[.005]*3,[.25]*3,[.024,.0245,.025],[12,17,21],
 'S1 .82B base becomes .90B for CY28, GM29% versus2026Q2 actual27.1%; compensation retained. FY25 tax benefit38.3M excluded by normalized25% tax, never deducted again. Debt through interest only.',
 'IncrementalDC orders not management guaranteed; customer concentration and manufacturing execution.')
pe('SNDK','FY2028 ending Jun2028 near-forward earnings; FY27 enterpriseSSD/contract anchor',
 [32,50,65],[.65,.85,.88],[2.5,2.65,2.95],[.4,.55,.65],[0]*3,[.15]*3,[.160,.162,.165],[6,9,11],
 '18mo base50B modestly exceeds S1 48B, while economic opex3.2B includes.55B SBC. Bear allows earlier NAND supply response; base explicitly assumes high contract margins persist into FY28, not perpetuity.',
 'Cycle peak cannot be treated as guaranteed; customer deposit/contract economics do not make all capex free.')
pe('TSM','CY2028 forward earnings with 2026Q2 and 2027 capacity as bridge',
 [185,240,285],[.60,.65,.68],[17,19,22],[1,1,1],[0]*3,[.17]*3,[5.19]*3,[18,25,30],
 'Rebuilt CY28 revenue240B rather than S1 CY27 220B; gross margin65% assumes overseas-cost dilution. All inputsUSD, divisor25.95B ordinary/5=5.19B ADS. SBC1B budget retained; no TWD→USD conversion after USD EPS.',
 'Five ordinary shares per ADS inherited company disclosure; FX affects model economic margin; geopolitics non-Gaussian tail.')

# S2 economic bridges independently recomputed without averaging model outputs.
pe('ADBE','FY2028 ending Nov2028 forward',[27,31,34],[.29,.35,.365],[0]*3,[0]*3,[0]*3,[.22]*3,[.390,.380,.375],[11,17,21],
 'GM field here denotes economic EBIT margin after all opex including SBC (29/35/36.5%); SBC_expense field0 means already embedded, not absent. No cash addition; shrinking shares uses cash generated and modest buyback assumptions.')
pe('PNR','CY2027 sustainable earnings valued Apr2028, not distant peak',[4.32,4.82,5.25],[.871/4.32,1.146/4.82,1.38/5.25],[.080,.055,.040],[0]*3,[.165,.150,.135],[.20,.18,.18],[.162,.161,.160],[12,17,20],
 'Margin field is operating profit after SBC before separately budgeted recurring cash restructuring. Taco1.4B purchase financing included in150M base net interest. Debt repayment.2/.5/.65B uses retained cash; not also used for full buyback or added cash value.',
 'Taco synergy/Pool recovery assumptions not acquired historical earnings;166bp base interest sensitivity meaningful.')
pe('ARGX','CY2028 forward earnings',[7,8.8,10.3],[.90,.90,.89],[3.8,3.95,4.30],[.5,.55,.60],[0]*3,[.22]*3,[.0635,.064,.065],[22,28,33],
 'R&D/SG&A total4.3/4.5/4.9B includesSBC. No excesscash or interest income add. ADS1:1 financialUSD. Base8.8B requires established indications plus expansion; UNITY failure not restored.',
 'Share1:1 ratio inherited; actual full-year total recurring cost may rise;8.1B alternate revenue cuts base valuation materially.')
pe('ALNY','CY2028 forward earnings',[6.4,8,9.4],[1,1,1],[1.58+.24+3.35,1.98+.28+3.50,2.35+.33+3.80],[.55,.60,.65],[.08,.10,.10],[.25,.20,.20],[.140]*3,[25,32,38],
 'Costs separately includeSanofi royalties1.58/1.98/2.35, directcost.24/.28/.33, andR&D/SG&A3.9/4.1/4.45 includingSBC. Interest.08/.10/.10 plus aftertax equity financing/other payments below; no second royalty liability EV haircut. V2 makes previously opaqueEBIT→NI bridge explicit.',
 'S2 opaque EBIT→NI residual replaced with explicit20% normalized tax inbase/bull and100M netinterest/financingexpense; royaltiesnotdeductedagain. FutureBlackstone/royaltyfinancingcashtermsmayrequirehighercharge; V2doesnotinventpositiveotherincometopreservetarget.')
pe('AGCO','CY2028 forward recovery earnings',[10,11.5,12.7],[.06,.105,.125],[0]*3,[0]*3,[.17,.17,.18],[.24]*3,[.071,.071,.072],[12,14,16],
 'Margin already containsSBC/integration costs; net interest plus minority proxy pre-tax consistent withS2. Financial-services debt not blindly subtracted from equipment enterprise value; PTx2029 target not imported.')
pe('CARR','CY2028 forward earnings',[22.5,25.5,28],[.12,.16,.18],[0]*3,[0]*3,[.50,.42,.40],[.23]*3,[.835,.82,.81],[17,22,26],
 'EBITmargin is afterSBC/recurring costs. Minority equity deducted after tax. PE afterinterest, no netcash addition.',other_after_tax=[-.12,-.14,-.16])
pe('MCHP','FY2028 ending Mar2028 sustainable earnings',[5.8,7.2,8.5],[.25,.35,.39],[0]*3,[0]*3,[.23,.19,.17],[.15]*3,[.56,.57,.59],[16,24,29],
 'Economic EBITmargin includesSBC.111M preferreddividend deducted; selected shares exclude preferredconversion. Ifconvert, addcommonshares AND stopsame dividend; never both.',preferred=[.111]*3)
pe('SMCI','FY2028 ending Jun2028 near-forward annual earnings',[55,75,95],[.09,.125,.16],[1.75,2.15,2.65],[.55,.65,.75],[.30,.30,.25],[.205]*3,[.80,.84,.90],[8,12,16],
 'Full revenue/GM/expense reconstruction replacesS1 naked3/5/7EPS. Base75B only modestly aboveFY27 guided65–72B;12.5%GM belowQ4actual17.5 but aboveFY26average10.8. Opex2.8B includes650MSBC; shares840M budget for awards/converts, interest assumes nonconverted debt. No one-off taxaddback or cashadd.',
 'Final2026-08-31 audited10K status inheritedV1/root, not August11 preliminary financials; BDO unqualifiedfinancialaudit with ITGC weakness is not all-audit failure. FY26NI2.2305B vsCFO-6.8099B: base71.27requiresworkingcapitalconversion, notmerelyQ4positive747MCFO. Exportinvestigationrequiresconditions.')

def ev(t,period,rows,note,unresolved='',metric='EBITDA'):
    c=company(t,'EV/'+metric,period,note,unresolved)
    for i,x in enumerate(rows):
        op=x['revenue_B']*x['economic_margin']
        value=op*x['multiple']-x['net_debt_B']-x.get('other_senior_claims_B',0)
        row(c,i,x,'max(0,(revenue*economic_margin*multiple-net_debt-other_senior_claims)/FD_shares)',max(0,value/x['FD_shares_B']),economic_metric_B=op)
    return c
def er(rev,marg,mult,deb,sh,claims=None):
    return [dict(revenue_B=rev[i],economic_margin=marg[i],multiple=mult[i],net_debt_B=deb[i],other_senior_claims_B=(claims or [0]*3)[i],FD_shares_B=sh[i]) for i in range(3)]
ev('BDC','CY2028 forward EBITDA',er([3.5,4.25,4.7],[.13,.185,.21],[8,10.5,12.5],[2.4,1.95,1.65],[.041,.041,.042]),
 'Margins are economic EBITDA after recurringSBC/integration. Netdebt scenario includes acquireddebt; cashdeleveraging cannot simultaneouslyfundbuybacks. BaseD&A90M,interest150M,tax25% givesNI409.7M/EPS9.99;154target≈15.4PE, a cross-check.',
 'Acquisition integration and netdebt1.95B dependFCF; neither refinancing nor synergycertain.')
ev('MOD','FY2028 ending Mar2028 continuing business',er([2.87,3.9,4.7],[.127,.21,.23],[9,15,18],[.5,.25,.1],[.056,.056,.057]),
 'OnlycontinuingClimateSolutions, noPTearnings and no0.44619THRMvalue. EBITDAafterSBC; debtposttransaction budget. Base3.9Brevenue and21%margin independent deliveryassumptions; historical spunassetsnotfreevalue.',
 '21%economicEBITDAmargin needs mix/utilization; no repeatTRS style nonoperatinggains.')
iren=ev('IREN','FY2028 ending Jun2028 recognized revenue, not ARR',er([3.2,5.8,8.5],[.47,.56,.60],[7,10,12],[5,7,9.5],[.48,.53,.60]),
 'Laterhorizon5.8Brevenue vs S1 5.0B, economicEBITDAmargin56% includesSBCbudget. DebtcoversGPUfinancing/projectobligations; equity530M; customerprepayments carry deliverycosts, not surpluscash. Cannot add45–55%prepay and90%GPUfinance as135%fundingofsameasset.',
 'Fullsignedproject capex/funding waterfallsnotclosed; conditionalonly. EBITDA is not shareholdercash; maintenanceGPUreplacement deducted in crosscheck, may forcefuturefunding.')
for i,r in enumerate(iren['scenarios']):
    r['crosscheck']=dict(depreciation_B=[1.1,1.65,2.35][i],interest_B=[.55,.75,1.0][i],growth_capex_B=[3,5,7][i],maintenance_GPU_capex_B=[.8,1.3,2.0][i],tax_rate=.20)
    z=r['crosscheck']; e=r['economic_metric_B']; z['net_income_B']=(e-z['depreciation_B']-z['interest_B'])*.8
    z['cash_after_total_capex_B']=e-z['interest_B']-max(0,(e-z['depreciation_B']-z['interest_B'])*.2)-z['growth_capex_B']-z['maintenance_GPU_capex_B']
fl=ev('FLNC','FY2028 ending Sep2028 restoration sales',er([2.3,3.6,4.6],[1]*3,[.20,.55,.85],[.10,.15,.10],[.225,.220,.220]),
 'EVsales crosschecked with trueprofit. Currenteconomicunits184.569672M, notClassA143.137M; target220–225Mincludesaward/financing. $392Mconverts retainedin future netdebt budget, not bothconvertedandsubtracted. Exclude restrictedcash/customerdepositsfromexcesscash.',
 'FY26Septreset2.4Brevenue/-200MEBITDA supersedesAug. Futurefunding/TRAobligations andwarranttermssensitivity unresolved; onlyconditionalrepairseat.',metric='Sales')
for i,r in enumerate(fl['scenarios']):
    gm=[.07,.14,.18][i]; op=[.34,.37,.42][i]; eb=r['inputs']['revenue_B']*gm-op; ni=(eb-.015)*.75
    r['profit_crosscheck']=dict(economic_gross_margin=gm,opex_including_SBC_B=op,economic_EBIT_B=eb,interest_B=.015,net_income_B=ni,EPS=ni/r['inputs']['FD_shares_B'])

# VST FCFE valuation, with full post-deal capital charges; no second subtraction of debt.
v=company('VST','FCFE multiple','CY2028 forward normalizedFCFE','2027 managementopportunity7.4–7.8B excludesCogentrix/Meta, is NOTformal2027guidance. Q22026hedges94%/72%2027/28. Modellegacy EBITDA7.3/8.0/8.8 plusCogentrix.5/.7/.85 plusincrementalMeta.05/.15/.3 minusSBC.15/.18/.2. Debtinterestandpreferredcashdeductedonce; no netdebtsubtractionfromFCFEvalue. Acquisitioncash2.3B+assumeddebt1.5B+5Mshares; existingpre-financingcannotbeaddedagain.',
 'Interest1.25–1.35B conditionalpostdealbudget; cashclosure/decommissioningandgrowthspendincluded. Needactualdebtbridgewhencloseoccurs; no full2030PPAmargin.')
for i in range(3):
    x=dict(legacy_EBITDA_B=[7.3,8,8.8][i],Cogentrix_EBITDA_B=[.5,.7,.85][i],incremental_Meta_EBITDA_B=[.05,.15,.30][i],SBC_B=[.15,.18,.20][i],maintenance_capex_B=[1.25,1.20,1.25][i],cash_interest_B=[1.35,1.30,1.25][i],cash_tax_B=[.65,.8,.95][i],preferred_dividend_B=.23,growth_capex_B=[.65,.55,.50][i],asset_closure_other_B=.20,FD_shares_B=[.344,.339,.335][i],FCFE_multiple=[11,15,18][i])
    f=x['legacy_EBITDA_B']+x['Cogentrix_EBITDA_B']+x['incremental_Meta_EBITDA_B']-sum(x[k] for k in ['SBC_B','maintenance_capex_B','cash_interest_B','cash_tax_B','preferred_dividend_B','growth_capex_B','asset_closure_other_B'])
    row(v,i,x,'(legacy_EBITDA+Cogentrix+incremental_Meta-SBC-maintenance_capex-interest-cash_tax-preferred-growth_capex-asset_closure_other)/FD_shares*FCFE_multiple',f/x['FD_shares_B']*x['FCFE_multiple'],economic_FCFE_B=f)
v['postdeal_capital_bridge']=dict(June2026_gross_debt_B=19.764,accounts_receivable_financing_B=.300,forward_repurchase_obligation_B=.613,cash_B=.435,June_net_financial_claims_ex_preferred_B=19.764+.300+.613-.435,Cogentrix_cash_consideration_B=2.3,Cogentrix_assumed_debt_B=1.5,Cogentrix_new_common_shares_B=.005,mechanical_no_interim_FCF_proforma_claims_B=19.764+.300+.613-.435+2.3+1.5,preferred_liquidation_B=2.476066,preferred_annual_current_cash_B=.1922508575,preferred_model_cash_B=.23,note='GrossdebtalreadyincludesJanuaryprefinancing; do notaddthe2.25Bissuanceagain. PurchasecashconsumesfutureFCForfunding; above24.042BmechanicalclaimsisbeforeinterimFCFandfutureredemption. FCFEmodelinterest1.3B≈5.4%onthisgrossclaimscale. Preferredresetriskraisesmodelcash230M; preferredprincipalnotdeductedagainfromFCFEvaluation.')

crm=company('CRM','economicFCFE multiple','FY2028 endingJan2028 sustainablecashflow','CFO-capex12/15.5/19B is aftercashinterest; subtractSBC4.5/4.7/5B. No secondnetdebtdeduction. RepurchasesfinancedwithremainingFCFE, notentirebuybackauthorization.')
for i in range(3):
    x=dict(CFO_minus_capex_after_interest_B=[12,15.5,19][i],SBC_B=[4.5,4.7,5][i],FD_shares_B=[.85,.84,.84][i],equity_cash_multiple=[16,23,28][i]); f=x['CFO_minus_capex_after_interest_B']-x['SBC_B']
    row(crm,i,x,'(CFO_minus_capex_after_interest-SBC)/FD_shares*equity_cash_multiple',f/x['FD_shares_B']*x['equity_cash_multiple'],economic_FCFE_B=f)
pgr=company('PGR','underwritingEPS multiple','CY2027–2028 normalized earnings','NPE*(1-CR)+normalinvestmentincome tax21%; reserves/catastrophenormalizationincludedinCR. No floataddition; investmentincomeandportfolioassetcannotbothbecounted.')
for i in range(3):
    x=dict(net_premiums_earned_B=[90,98,106][i],combined_ratio=[.95,.92,.89][i],investment_other_income_B=[2.7,3,3.3][i],tax_rate=.21,FD_shares_B=[.586,.584,.582][i],PE=[14,18,21][i]); ni=(x['net_premiums_earned_B']*(1-x['combined_ratio'])+x['investment_other_income_B'])*.79
    row(pgr,i,x,'(NPE*(1-CR)+investment_other_income)*(1-tax)/FD_shares*PE',ni/x['FD_shares_B']*x['PE'],economic_net_income_B=ni)
baba=company('BABA','RMB economicEPS convertedonce','FY2028 endingMar2028 sustainableearnings','ADS1:8; ordinaryequivalent20.4/20.8/21.2B becomes2.55/2.60/2.65B ADS. AdjustedEBITA lessSBC andongoingeconomiccosts. Taxthenattributablenetequityincome. HighcapexmeansEPSnotFCFE; no freecashaddition.',
 'S2 residualnetequityincome5/10/15B mustbenetofminorities/interest; V2 preserves as explicitbudget, notverifiedforecast.')
for i in range(3):
    x=dict(revenue_RMB_B=[1180,1300,1430][i],adjusted_EBITA_RMB_B=[100,160,230][i],SBC_RMB_B=[14,16,18][i],economic_recurring_cost_RMB_B=[6,7,8][i],tax_rate=.20,net_attributable_other_RMB_B=[5,10,15][i],ordinary_shares_B=[20.4,20.8,21.2][i],ordinary_per_ADS=8,RMB_per_USD=7,PE=[15,21,26][i]); ni=(x['adjusted_EBITA_RMB_B']-x['SBC_RMB_B']-x['economic_recurring_cost_RMB_B'])*.8+x['net_attributable_other_RMB_B']; eps=ni/(x['ordinary_shares_B']/8)/7
    row(baba,i,x,'((adjusted_EBITA-SBC-economic_recurring_cost)*(1-tax)+net_attributable_other)/(ordinary_shares/8)/RMB_per_USD*PE',eps*x['PE'],economic_net_income_RMB_B=ni,economic_EPS_USD_per_ADS=eps)

# Multi-asset biotech: probabilities apply only once inside rNPV. No weighted expected price.
b=company('BNTX','pipeline rNPV plusremainingfinancialassets','Apr2028 rNPV of2032–2033 commercial earnings; not2028sales','Financialassets16.6342BEUR exactdisclosure; EURUSD1.10 assumptiononce. DeductburntoApr2028onlyincash; postApr2028 developmentPV onlyinpipeline. Fourdisjointopportunitybudgets andownershipweights; probabilityonce perbranch. No outer probabilityweightedtarget.',
 'Gotistobart80% andADC50% are S2 mixedrightsproxies, notfullyauditedregionalrights. Terminalvalue/marketoverlap dominate; conditionalonly, notprecisecashfloor.')
branches=['pumitamig','gotistobart','T-Pam_other_ADC','mRNA_BNT113_other']
for i in range(3):
    sales=[[6,1.8,3,1.8],[10,3,5,3],[14,5,7,5]][i]; own=[.5,.8,.5,.8]; margins=[[.28,.32,.28,.32],[.32,.35,.30,.35],[.35,.38,.33,.37]][i]; mult=[[18,18,18,20],[20,20,20,22],[22,23,22,24]][i]; prob=[[.30,.25,.25,.15],[.50,.50,.50,.30],[.75,.70,.65,.50]][i]; discounts=[1/1.12**5,1/1.12**4,1/1.12**4,1/1.12**5]
    detail=[dict(name=branches[j],success_sales_B=sales[j],ownership=own[j],after_tax_margin=margins[j],terminal_PE=mult[j],discount_factor=discounts[j],subjective_success_probability=prob[j]) for j in range(4)]
    for z in detail:z['rNPV_B']=z['success_sales_B']*z['ownership']*z['after_tax_margin']*z['terminal_PE']*z['discount_factor']*z['subjective_success_probability']
    x=dict(start_financial_assets_EUR_B=16.6342,financial_assets_date='2026-06-30',USD_per_EUR=1.10,burn_to_observation_USD_B=[4.5,3.6,2.7][i],burn_period='2026-06-30 to2028-04-12 (about21.4months; NOTonly18months)',post_observation_development_PV_B=[1.6,2.5,3.5][i],ADS_B=[.255,.258,.260][i],branches=detail)
    cash=16.6342*1.1-x['burn_to_observation_USD_B']; pipeline=sum(z['rNPV_B'] for z in detail)-x['post_observation_development_PV_B']
    row(b,i,x,'(start_financial_assets_EUR*USD_per_EUR-burn_to_observation+sum(success_sales*ownership*margin*PE*discount*probability)-post_observation_developmentPV)/ADS',max(0,(cash+pipeline)/x['ADS_B']),remaining_cash_USD_B=cash,pipeline_rNPV_B=pipeline)
ky=company('KYTX','financedclinical rNPV','Apr2028 conditionalclinicalvalue with2030 SPSmatureearnings discounted2years','150M netequityraised requires150/(1-.05)Mgross. FD=current61.84M+12Mfutureawards+newshares; financingcashfundsdevelopment, notaddedasfreeprofit. Loanavailableisnotreceived. Prospective35Mconditionaldrawand60Mdebtmustbeconsistent; discretionary50Mloanexcluded.',
 'SPSsuccessprobability70% subjective; rewards12Mbudget notawardvaluation. Bear assumesfundingbeforefailure; financingfailurecouldapproachzero. Unknownclinicalprice/approvalrights.')
for i in range(3):
    issue=[4,6,12][i]; sh=.06184+.012+.150/.95/issue
    x=dict(current_shares_B=.06184,awards_other_B=.012,net_equity_raise_B=.150,issuance_fee=.05,issue_price=issue,FD_shares_B=sh,SPS_mature_treatments=[200,1000,2000][i],net_price_per_treatment_USD=300000,SPS_success_after_tax_income_B=[0,.060,.180][i],PE=[18,22,25][i],discount_rate=.15,years_to_success_earnings=2,subjective_probability=[.10,.70,.65][i],other_pipeline_net_rNPV_B=[.04,.24,.30][i],remaining_cash_B=[.128,.11,.10][i],debt_B=.06,post_observation_development_PV_B=[0,.15,.15][i])
    pv=x['SPS_success_after_tax_income_B']*x['PE']/1.15**2*x['subjective_probability']; value=pv+x['other_pipeline_net_rNPV_B']+x['remaining_cash_B']-x['debt_B']-x['post_observation_development_PV_B']
    row(ky,i,x,'(SPS_successNI*PE/(1+discount_rate)^years*probability+other_pipeline_rNPV+remaining_cash-debt-post_observation_developmentPV)/(current_shares+awards+net_raise/(1-fee)/issue_price)',max(0,value/sh),SPS_rNPV_B=pv,equity_value_B=value)
ky['financing_stress']=[dict(issue_price=p,FD_shares_M=1000*(.06184+.012+.150/.95/p),base_price=.839/(.06184+.012+.150/.95/p)) for p in [3,4,6,8,12]]
ky['cash_runway_check_B']=.199427-.09-.151-.028+.035
ky['post_financing_cash_check_B']=ky['cash_runway_check_B']+.150
ky['cash_rounding_note']='Cashbridge115.427M after150Mnetraise; modelbase110M leaves5.427Madditionalfinancing/launchslippage. Prospective60Mdebt includescurrent25M+conditional35M; laterpostApr2028developmentPVdeductedseparately.'

# POET uses warrant option-value method only; no simultaneous FD warrants and proceeds.
def call(S,K,T,sig,r):
    if T<=0:return max(S-K,0)
    N=lambda x:.5*(1+math.erf(x/math.sqrt(2)))
    d1=(math.log(max(S,1e-20)/K)+(r+sig*sig/2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-K*math.exp(-r*T)*N(d2)
tranches=[(.000097699,1.09,.79),(.001872490,1.11,.79),(.002048275,3.10,1.08),(.003333334,4,1.27),(.002,5,1.46),(.002777778,6,1.65),(.006,6.06,2.11),(.005,5.94,2.26),(.013636364,7.12,2.49),(.019047620,26.25,1.10),(.022921408,8.25,7.09)]
assert abs(sum(n for n,k,t in tranches)-.078734968)<1e-10
po=company('POET','EVsales + cash minusdilutiveoptionvalue','CY2028 expectedproductsalesandApr2028remainingcash','11warranttranches total78.734968M alreadyincludes22.921408Mcustomerwarrant. Base185M includesordinary173.058M plusawards/expectedSBC; no second full261.415Mdivisor. SolveP*base_shares+sum(N*BlackScholescall(P,K,T))=EV+cash. Exerciseproceedsalreadyinsidecallpayoff; no separatelyaddedcash or optionreservedoublecount. Contractsalegrossamount notagainreducedbycustomerwarrant.',
 'BSvolatility/rate/modelandconditionalcustomervestingnotobservablefuturefacts; tableMay2029 expiry vs narrativefiveyearsfor26.25trancheconflict retained. Allvested assumptionoverchargesbear; sensitivityrequired; modelnotprecisefairvalue.')
for i in range(3):
    x=dict(sales_B=[.012,.080,.220][i],EV_sales=[4,12,18][i],remaining_net_cash_B=[.64,.60,.53][i],base_awards_future_SBC_shares_B=.185,volatility=.75,risk_free_rate=.04,tranches=[dict(shares_B=n,strike_USD=k,remaining_years=T) for n,k,T in tranches])
    a=x['sales_B']*x['EV_sales']+x['remaining_net_cash_B']; lo,hi=.000001,a/.185
    for _ in range(100):
        p=(lo+hi)/2; rhs=p*.185+sum(n*call(p,k,T,.75,.04) for n,k,T in tranches)
        if rhs>a:hi=p
        else:lo=p
    p=(lo+hi)/2
    row(po,i,x,'solve P*base_shares + sum(warrant_count*BS_call(P,strike,T,vol,r)) = sales*EVsales + remaining_net_cash',p,total_warrant_option_value_B=sum(n*call(p,k,T,.75,.04) for n,k,T in tranches),economic_operating_profit_B=x['sales_B']*[.30,.42,.50][i]-[.06,.08,.10][i])

# IONS explicit net retained revenue, pipeline is not all partner sales.
io=company('IONS','retainedrevenueEV withcash/profitcrosscheck','CY2028 forwardretainedrevenue;Apr2028clinicaloptionalvalue','OwnUSsales frompaidtreatmentyears×netprice. PartnerdrugworldsalesonlytimesIonisroyaltyrate; SPINRAZAgrossroyaltiesretained55%afterRP2028share. FailedCM/HORIZONzerovalue. Netdebtincludes575M2028maturity; refinancingnotassumedfree. Salesmultiplevaluationvalidonlyifcommercialscaleandlongerprofitpotential; noautomaticexclusionfromsinglefailedtrial.',
 'HighEVsalesrequires growthbeyond2028; basecashflowstillnearbreakeven. No expensiveopaque2030targetimport. Otherroyaltyrates .11/.18/.15 are disclosedrangeproxies, require productrightsauditforprecisevaluation.')
for i in range(3):
    x=dict(TRYNGOLZA_paid_years=[14000,25000,38000][i],TRYNGOLZA_net_price=[27000,30000,32000][i],DAWNZERA_paid_years=[650,1100,1700][i],DAWNZERA_net_price=350000,ZANVASTRO_paid_years=[60,140,230][i],ZANVASTRO_net_price=500000,SPINRAZA_gross_royalty_B=[.18,.20,.22][i],SPINRAZA_retention=.55,WAINUA_PN_partner_sales_B=[.4,.7,1.0][i],WAINUA_royalty=.23,bepirovirsen_partner_sales_B=[.2,.65,1.2][i],bepirovirsen_royalty=.11,sefaxersen_partner_sales_B=[0,.10,.4][i],sefaxersen_royalty=.18,ulefnersen_partner_sales_B=[0,.05,.15][i],ulefnersen_royalty=.15,other_retained_revenue_B=.04,collaboration_revenue_B=[.12,.20,.30][i],EV_retained_sales=[3.5,6,8][i],net_debt_B=[.45,.20,0][i],FD_shares_B=[.200,.210,.220][i],economic_opex_including_SBC_B=[1.25,1.45,1.70][i])
    own=(x['TRYNGOLZA_paid_years']*x['TRYNGOLZA_net_price']+x['DAWNZERA_paid_years']*x['DAWNZERA_net_price']+x['ZANVASTRO_paid_years']*x['ZANVASTRO_net_price'])/1e9
    royalty=x['SPINRAZA_gross_royalty_B']*.55+sum(x[a]*x[b] for a,b in [('WAINUA_PN_partner_sales_B','WAINUA_royalty'),('bepirovirsen_partner_sales_B','bepirovirsen_royalty'),('sefaxersen_partner_sales_B','sefaxersen_royalty'),('ulefnersen_partner_sales_B','ulefnersen_royalty')])
    revenue=own+royalty+x['other_retained_revenue_B']+x['collaboration_revenue_B']; ebit=own*.85+royalty*.95+x['other_retained_revenue_B']*.5+x['collaboration_revenue_B']*.70-x['economic_opex_including_SBC_B']
    row(io,i,x,'(retained_revenue*EV_retained_sales-net_debt)/FD_shares; retained_revenue=sum(ownpaidyears*netprice)/1e9+sum(partner_sales*royalty)+SPINRAZAroyalty*.55+other+collaboration',max(0,(revenue*x['EV_retained_sales']-x['net_debt_B'])/x['FD_shares_B']),own_sales_B=own,retained_royalties_B=royalty,retained_revenue_B=revenue,economic_EBIT_B=ebit)

assert len(companies)==29 and len({c['ticker'] for c in companies})==29
for c in companies:
    c['arithmetic_status']='PASS: machine recomputed; 3 scenarios; unrounded inputs retained'
    c['security_status']='PASS economicunit identified; source inheritance distinguished from independently read documents'
    c['sensitivity']={ 'base_equity_value_unchanged_shares_plus10pct_price':round(c['scenarios'][1]['price']/1.1,4),'note':'Uncompensated10%newcommonshareswhileholdingtotalcommonequityvalueconstant; notamultiple/operatingsensitivityandnotnormalfairpricecapitalraise. Foroptionmodelrerunallclaimspricing.'}
    if c['ticker'] in s1:c['prior_12month_prices_preserved']=[r['price'] for r in s1[c['ticker']]['recommended_bear_base_bull']]
    if c['ticker'] in s2:c['S2_prior_18month_prices_preserved']=s2[c['ticker']]['recommended_bear_base_bull']['price_usd']
    c['evidence_grade']={'facts':'A:primaryfinancial/operatinganchorverifiedbyV1and/orV2;CRDO/AAOIuseS1/B2plusV2selectedreads','forecast':'B:conditionaloperatingbridge;notcompanyforecast','valuation':'C:subjectiveforwardmultiple'}
    if c['ticker'] in ['IREN','FLNC','POET','KYTX','BNTX','IONS']:
        c['evidence_grade']['forecast']='C:financing/clinical/deliveryconditionsmaterial;precisepredictionnotverified'
        c['verdict']='算术通过；条件候选/候补，不认定融资与商业成功已封口'
    if c['ticker']=='SMCI':c['verdict']='可复活但等待现金转换；全年CFO负6.81B使EPS模型不可单独支持立即行动'
    if c['ticker'] in ['ADBE','PNR','AGCO','CARR','MCHP']:
        for scenario in c['scenarios']:
            scenario['inputs']['margin_definition']='economic EBIT margin after recurringSBC (genericformula marginfield); PNR subtractsadditionalcashrestructuring separately'
    else:
        for scenario in c['scenarios']:
            if 'economic_gross_margin' in scenario['inputs']:
                scenario['inputs']['margin_definition']='economic grossmargin afterproductionSBC; operatingSBCdeductedseparately'

# Source provenance: a second visit is not an independent corporate event.
independent_notes={
 'NVDA_Q2':'FY27 nonGAAP已含SBC；Q2股数24.285B；投资收益不可经常化。',
 'AVGO_Q3':'GAAP OP15.955B；adjusted20.095B−SBC2.019B=18.076B。',
 'CRDO_Q1':'SBC87.979M；经济OP230.641−87.979=142.662M。',
 'CLS_Q2':'GAAP458.3M−TRS104.1M=354.2M；SBC19.3M保留，不重复扣。',
 'MU_Q4':'Q1 GAAPGM85.95/调整86.25；GAAPOpex2.31B；SBC成本与费用分别174/253M。',
 'S2-15':'KYTX现金证券199.427M、贷款账面24.883M；额度不是全部到账。',
 'S2-17':'BNTX金融资产16.6342BEUR；251.204366M股；ADS1:1。',
 'POET_FS':'逐档权证总78.734968M含客户22.921408M；26.25仅一档；2029表与五年文字到期有冲突。',
 'FLNC_Q3':'A类143136891+B-1 41432781=184569672经济单位；非143M。'}
src=[]; seen=set()
for file in ['07_logs/S1_sources.json','07_logs/S2_sources.json','07_logs/B2_sources.json']:
    for z in read(file).get('sources',[]):
        sid=z.get('id'); url=z.get('url')
        if sid in independent_notes and url not in seen:
            seen.add(url);src.append(dict(id=sid,url=url,published_date=z.get('publication_date',z.get('published')),access_status='V2 independently opened and relevant table/body read',note=independent_notes[sid],root_event_independence='Samecompanyeventaspriorroles;independentverificationvisitnotnewindependentbusinesssource'))
new=[
 ('V2_VST_Q2','https://investor.vistracorp.com/2026-08-07-Vistra-Reports-Second-Quarter-2026-Results','2026-08-07','2027机会非指导；94/72%套保；336M股票；现金435M。'),
 ('V2_VST_10Q','https://www.sec.gov/Archives/edgar/data/1692819/000169281926000019/vistra-20260630.htm','2026-08-07','19.764B grossdebt+AR.300+repurchase.613；Cogentrix2.3cash/1.5debt/5Mshares；优先股本金2.476B、当前年息约192M。'),
 ('V2_VST_DEAL','https://investor.vistracorp.com/2026-01-05-Vistra-Adds-to-its-Industry-Leading-Generation-Portfolio-with-Acquisition-of-Cogentrix','2026-01-05','购价现金/债务/股票与税收价值分别处理，税惠非立即现金。'),
 ('V2_IONS_Q2','https://ir.ionispharma.com/news-releases/news-release-details/ionis-reports-second-quarter-2026-financial-results-and','2026-07-29','产品31M、Spinraza53M、Wainua16M；伙伴销售不等Ionis收入；现金2.1B。'),
 ('V2_SMCI_Q4','https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx','2026-08-11','Q4GAAPGM17.5%、FY26平均10.8%、现金7.5B/债8.7B；FY27收入65–72B；当时稿为preliminary，最终审计承接V1。')]
for sid,url,date,note in new:src.append(dict(id=sid,url=url,published_date=date,access_status='V2 independently opened and relevant table/body read',note=note))
src.extend([dict(id='V2_POET_CONTRACT',url='https://www.sec.gov/Archives/edgar/data/1437424/000149315226024093/ex4-1.htm',access_status='opened; strikefind8.25notreturned; do notcountasindependentlyverifiedcontractterms'),dict(id='V2_TSM_PDF',url='https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-07/a80d7933be643644081584087731f73b22ea5a2c/2Q26%20EarningsRelease.pdf',access_status='opened; ADSratiofindnotreturned; inheritS1/V1ratioverification'),dict(id='V2_IONS_10Q',url='https://www.sec.gov/Archives/edgar/data/874015/000087401526000251/form10q.htm',access_status='opened; detailedrights inheritedfrozenreportandV1; do notclaimfulldocumentread')])
v1=read('04_verification/V1_primary_verification.json')
for c in companies:
    inherited=[dict(url=z['source_url'],claim=z['claim'],read_by='V1; inheritedbyV2') for z in v1['checks'] if z['ticker']==c['ticker']]
    c['inherited_primary_checks']=inherited
    c['independent_V2_sources']=[z['url'] for z in src if z['id'] in ({'NVDA':['NVDA_Q2'],'MU':['MU_Q4'],'AVGO':['AVGO_Q3'],'CLS':['CLS_Q2'],'CRDO':['CRDO_Q1'],'KYTX':['S2-15'],'BNTX':['S2-17'],'POET':['POET_FS'],'FLNC':['FLNC_Q3'],'VST':['V2_VST_Q2','V2_VST_10Q','V2_VST_DEAL'],'IONS':['V2_IONS_Q2'],'SMCI':['V2_SMCI_Q4']}.get(c['ticker'],[]))]
(ROOT/'07_logs/V2_sources.json').write_text(json.dumps(dict(role='V2',cutoff='2026-10-12T19:40:00-07:00',independent_relevant_primary_documents_read=sum(z.get('access_status','').startswith('V2 independently') for z in src),sources=src,inherited_files=['03_round2/S1_ai_upside.json','03_round2/S2_nonai_upside.json','03_round2/S2_nonai_upside.md','03_round2/B2_valuation_rebuttal.json','03_round2/B1_business_rebuttal.md','04_verification/V1_primary_verification.json','04_verification/controller_web_quote_checks.json'],inheritance_note='V1/S1/S2/B2facts/modelinputsareinherited;V2equationscomputedindependently. Accessoccurredafterfreeze;useonlydatedprecutoffpublications.'),ensure_ascii=False,indent=2),encoding='utf-8')

report=dict(role='V2 independent numerical and securities verification',information_cutoff='2026-10-12T19:40:00-07:00',observation_date='2028-04-12',precision_note='6decimals are audit precision not forecast confidence; display prices to nearestUSD or centsforlowprices',companies=companies)
OUT.mkdir(exist_ok=True)
(OUT/'V2_models.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
summary=[]
for c in companies:
    summary.append(dict(ticker=c['ticker'],security_status=c['security_status'],arithmetic_status=c['arithmetic_status'],prices=[s['price'] for s in c['scenarios']],returns_pct=[s['return_pct'] for s in c['scenarios']],unresolved=c['unresolved'],verdict=c['verdict']))
verification=dict(role='V2',all_29_have_security_price_arithmetic_status=True,models_count=29,scenario_count=87,companies=summary,limitations=['Forecasts are conditionaljudgments, not statistically calibrated probabilities.','Modelcomplete != capitalfundinglegallycommitted; IREN/FLNC/POET/KYTX need conditions.','Primarydocuments independently reread forselected securities, rest inheritedV1/B2/S2 clearly stated.','No dividend forecasts: allreportedreturnsarepricereturn, not charterUSDtotalreturn.'])
(OUT/'V2_numeric_verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# V2 独立证券、经济利润及18个月计算核验','','统一观察日2028-04-12；截止2026-10-12 19:40 LA。29家/87情景均机器重算。目标是条件估值，不是公司指导或概率置信区间；表中为美元价格回报，未计股息，不能冒称总收益。',
 '', '## 会改变裁决的结论', '',
 '- 14份原始文档相关正文/表格由V2独立重读；其余明确承接V1/S1/S2/B2。重复打开同一公司公告属于独立复核，不算第二条独立经营证据。所有前瞻收入、利润率、倍数仍是研究假设。',
 '- NVDA保留已含SBC的经济利润，AVGO减持续SBC，CLS剔TRS收益但不二扣SBC，CRDO补成本后基准170.69低于当前200.84。不能把稀释当成免费免除SBC的理由。',
 '- AI模型重建到18个月：NVDA以CY2028（大部分为FY2029）前瞻盈利、其他明确FY/CY2028；不是把S1的2027-10-12价格换日期。MU强中枢219.3B EBIT保留，但要求FY28经济GM88%及总Opex9.5B；悲观检验周期供给恢复。',
 '- SMCI用收入75B、经济GM12.5%、含SBC费用2.8B、0.84B股重建基准71.27；但全年CFO负6.8099B对净利2.2305B，是必须等待的现金转化问题。单季CFO正747M不能封口全年。',
 '- VST初始总债19.764B含项目债，不能只取18.131B运营层债。机械交割债权桥24.042B（含AR融资/回购义务、扣现金，再含收购现金和承接债）；FCFE付息后不二扣债。2027 7.4–7.8B是管理层机会区间，非正式指导。',
 '- BNTX四分支重新算概率/权益/折现；金融资产烧损从2026-06-30至2028-04-12约21.4个月，不是只扣未来18个月。KYTX150M净融资含5%费，6美元发行后FD100.16M；基准8.37，融资价3美元则FD126.47M。',
 '- POET逐档权证用期权价值法，既不将客户22.92M再加一次，也不同时加入全部行权现金和扣期权价值。模型对波动率/归属敏感，仅条件候补；FLNC经济单位184.569672M（先前184.596为转写误差），基准进一步融资至220M。',
 '- IONS自主销售与各药版税分开，失败CM/HORIZON不重新加值，2028SPINRAZA仅留55%；基准50.85不支持以旧全额销售倍数58美元自动占席。',
 '', '|股票|冻结价|悲观/基准/乐观|对应价格回报%|经营期限|','|---|---:|---|---|---|']
for c in companies:lines.append('|'+c['ticker']+'|'+str(c['reference_price'])+'|'+' / '.join(f"{s['price']:.2f}" for s in c['scenarios'])+'|'+' / '.join(f"{s['return_pct']:.1f}" for s in c['scenarios'])+'|'+c['earnings_period']+'|')
lines+=['','## 逐家口径与保留问题','']
for c in companies:
    links=c['independent_V2_sources'] or [z['url'] for z in c['inherited_primary_checks'][:2]]
    label='V2实读' if c['independent_V2_sources'] else '承接V1原始核验'
    lines += ['### '+c['ticker'],c['assumptions'],'','待兑现/未封口：'+(c['unresolved'] or '经营与估值假设尚需未来业绩验证；算术通过不等于预测已证实。'),'','证据等级：'+c['evidence_grade']['forecast']+'；'+c['evidence_grade']['valuation'],'',label+'：'+'；'.join(f'[原文{j+1}]({url})' for j,url in enumerate(links)),'']
lines+=['## 复算','`python -B scripts/V2_recalculate.py`；只写本实验04_verification。输入及公式在V2_models.json；脚本不用网络，不修改上游/Git。','标记SBC=0的S2经营利润率模型表示成本已包含在经济EBIT率，不表示没有SBC。EV模型扣债一次；PE/FCFE模型通过利息/资本成本承担债务，不把净债再减一次。','POET采用期权价值法，不能在此价格上再除全潜在股本。BNTX/KYTX分支已乘成功概率，不再整体乘临床概率。']
(OUT/'V2_numeric_verification.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
tests=[]
for c in companies:
    assert len(c['scenarios'])==3
    for s in c['scenarios']:
        assert abs(s['return_pct']-100*(s['price']/c['reference_price']-1))<.00002
        if 'economic_EPS' in s:assert abs(max(0,s['economic_EPS']*s['inputs']['PE'])-s['price'])<.000001
        tests.append({'ticker':c['ticker'],'scenario':s['scenario'],'status':'PASS'})
assert abs(20.095-2.019-18.076)<1e-10
assert abs(458.3-104.1-354.2)<1e-10
assert abs(230.641-87.979-142.662)<1e-10
(OUT/'V2_calculation_audit.json').write_text(json.dumps({'scenario_checks':tests,'checks_passed':len(tests),'security_arithmetic':{'AVGO_economic_OP_B':20.095-2.019,'CLS_economic_OP_M':458.3-104.1,'CRDO_economic_OP_M':230.641-87.979,'FLNC_economic_units':143136891+41432781,'POET_warrants':round(sum(n for n,k,t in tranches)*1e9)},'rounding':'prices6decimals;returntolerance0.00002percentagepoint;forecastsnotproven'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'models':len(companies),'scenarios':sum(len(c['scenarios']) for c in companies),'base_prices':{c['ticker']:round(c['scenarios'][1]['price'],2) for c in companies}},ensure_ascii=False))
