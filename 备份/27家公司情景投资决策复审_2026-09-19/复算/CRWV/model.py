"""Independent conditional USD-billion model; all forecasts are research assumptions."""
from pathlib import Path
import json, copy, math
ROOT = Path(__file__).parent
P0 = 81.36
S0 = 0.551536602
SC = {'受损': dict(A=[17, 22, 25, 27, 28, 28, 28, 27, 26, 25, 24, 23], B=[0.25, 0.4, 0.5, 0.6, 0.65, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], C=[0.45, 0.6, 0.7, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8], ma=0.6, mb=0.35, mc=0.35, da=0.35, db=0.26, dc=0.07, growth=[16, 8, 5, 4, 3, 2, 2, 2, 2, 2, 2, 2], maint=[3, 5, 7, 8, 9, 10, 10, 10, 10, 9, 9, 9], wc=[0, -1, -1, -0.5, -0.5, 0, 0, 0, 0, 0, 0, 0], rate=0.105, eqprice=30, leverage=0.65, g=0.0, ke=0.15, wacc=0.12), '基准': dict(A=[20.7, 32.4, 40.8, 47.2, 51.6, 54, 55, 56, 56.8, 57.6, 58.4, 59.2], B=[0.55, 1.15, 2, 3, 4, 5, 6, 6.8, 7.5, 8, 8.5, 9], C=[0.75, 1.3, 2, 2.7, 3.4, 4.2, 5, 5.6, 6.2, 6.8, 7.4, 8], ma=0.63, mb=0.48, mc=0.52, da=0.42, db=0.28, dc=0.07, growth=[30, 28, 20, 14, 11, 8, 7, 6, 5, 5, 5, 5], maint=[3, 5, 8, 12, 16, 20, 22, 23, 24, 24, 24, 25], wc=[3, 2, 1, 0, -1, -1, -0.5, 0, 0, 0, 0, 0], rate=0.085, eqprice=70, leverage=0.78, g=0.025, ke=0.15, wacc=0.105), '乐观': dict(A=[25.3, 42, 58, 73, 85, 95, 102, 108, 114, 120, 125, 130], B=[0.8, 2, 4, 6.5, 9, 12, 15, 18, 21, 24, 27, 30], C=[0.9, 1.8, 3, 4.6, 6.5, 9, 12, 14, 16, 18, 20, 22], ma=0.68, mb=0.54, mc=0.58, da=0.36, db=0.25, dc=0.06, growth=[37, 38, 32, 27, 24, 21, 18, 16, 14, 13, 12, 12], maint=[3, 6, 11, 18, 25, 31, 37, 42, 46, 49, 52, 55], wc=[4, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0], rate=0.075, eqprice=100, leverage=0.8, g=0.025, ke=0.15, wacc=0.105), '突破': dict(A=[21.6, 33.6, 42, 49, 54, 57, 60, 62, 64, 66, 68, 70], B=[0.8, 2.5, 6, 10, 15, 20, 26, 32, 38, 44, 50, 56], C=[0.9, 2, 4, 6.5, 9.5, 13, 17, 21, 25, 29, 33, 37], ma=0.64, mb=0.6, mc=0.7, da=0.4, db=0.2, dc=0.04, growth=[32, 32, 28, 24, 22, 20, 18, 17, 16, 16, 16, 16], maint=[3, 5, 9, 14, 19, 24, 29, 33, 37, 41, 45, 49], wc=[3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0], rate=0.08, eqprice=90, leverage=0.78, g=0.025, ke=0.15, wacc=0.105)}

def once(p, ke=None, wacc=None, opening_debt=43.0, opening_cash=5.0, price_scale=1.0, cost_extra=0.0, cap_scale=1.0, eq_scale=1.0, eqcap=8.0, conv_prices=None):
    p = copy.deepcopy(p)
    ke = ke or p['ke']
    wacc = wacc or p['wacc']
    debt = opening_debt
    cash = opening_cash
    ppe = 55.5
    shares = S0
    rows = []
    div = []
    nol = 4.0
    for j in range(12):
        t = j + 1
        A = p['A'][j] * price_scale
        B = p['B'][j]
        C = p['C'][j]
        R = A + B + C
        ebitda = p['A'][j] * p['ma'] + (A - p['A'][j]) + B * p['mb'] + C * p['mc'] - cost_extra * R - (1.0 if p['g'] == 0 and t == 1 else 0.0)
        da = (p['A'][j] * p['da'] + B * p['db'] + C * p['dc']) * (1 + (cap_scale - 1) * min(t / 6, 1))
        sbc = 0.7 + R * 0.012
        ebit = ebitda - da - sbc
        interest = debt * p['rate']
        cap = (p['growth'][j] + p['maint'][j]) * cap_scale
        debt0 = debt
        cash0 = cash
        s_old = shares
        amort = min(debt, [7.5, 7, 8, 8, 9, 11, 12, 12, 12, 12, 12, 12][j])
        if t == 1:
            conv = 3.7
            fees = 0.5543
        else:
            conv = 0.0
            fees = 0.0
        jv = 0.8 if t == 1 else 0.0
        ppe1 = ppe + cap - da - jv
        debt_limit = max(0.0, p['leverage'] * ppe1)
        for _ in range(10):
            taxable = max(0, ebit - interest)
            tax = 0.01 * R + 0.23 * max(0, taxable - nol)
            op = ebitda - interest - tax + p['wc'][j]
            need = max(0.0, 3.0 - (cash0 + op - cap - amort + conv - fees))
            credit_cap = [23, 22, 18, 16, 15, 16, 17, 17, 17, 17, 17, 17][j]
            borrow = min(need, max(0.0, debt_limit - (debt0 - amort + conv)), credit_cap - conv)
            interest = debt0 * p['rate'] + 0.5 * (borrow + conv - amort) * p['rate']
        taxable = max(0, ebit - interest)
        nol = max(0, nol - taxable) + max(0, -ebit + interest)
        equity = max(0.0, need - borrow)
        issue = p['eqprice'] * 1.04 ** j * eq_scale
        shares += equity / (issue * 0.98)
        existing = (0.024 / 2 if t <= 2 else 0) + (0.029 / 4 if t <= 4 else 0)
        new_awards = (0.005 if t >= 2 else 0) + (0.008 if t >= 5 else 0)
        shares += existing + new_awards
        conv_dilution = 0.0
        if conv_prices:
            for when, face, strike, cap_price in [(6, 2.588, 107.8, 215.6), (7, 4.0, 119.6, 230.0), (7, 3.7, 97.85, 199.7)]:
                if t == when:
                    quote = conv_prices.get(t, 0)
                    conv_dilution += face / strike * max(0, 1 - cap_price / quote) if quote > 0 else 0
            shares += conv_dilution
        option_cash = 0.024 / 2 * 1.84 if t <= 2 else 0
        debt = debt0 - amort + conv + borrow
        cash = cash0 + op - cap - amort + conv - fees + borrow + equity + option_cash
        extra_repay = min(max(0, cash - 3), max(0, debt - 2.0 * ebitda))
        debt -= extra_repay
        cash -= extra_repay
        distribution = max(0, cash - 3.0) if t >= 5 else 0.0
        cash -= distribution
        dps = distribution / shares
        div.append(dps)
        rows.append(dict(t=t, R=R, A=A, B=B, C=C, EBITDA=ebitda, DA=da, SBC=sbc, EBIT=ebit, interest=interest, tax=tax, wc=p['wc'][j], op=op, cap=cap, growth=p['growth'][j] * cap_scale, maint=p['maint'][j] * cap_scale, fcff=op + interest - cap, amort=amort + extra_repay, borrow=borrow + conv, equity=equity, issue=issue, fees=fees, shares=shares, debt=debt, cash=cash, ppe=ppe1, distribution=distribution, dps=dps, existing=existing, new_awards=new_awards, option_cash=option_cash, conv_dilution=conv_dilution, jv=jv))
        assert abs(cash - (cash0 + op - cap - rows[-1]['amort'] + rows[-1]['borrow'] - fees + equity + option_cash - distribution)) < 1e-08
        assert ppe1 >= 0 and cash >= 3 - 1e-08 and (debt >= -1e-08)
        ppe = ppe1
        if equity > eqcap:
            return dict(rows=rows, values={h: dict(value=0.0, paid=0.0, wealth=0.0, total=-1.0, annual=-1.0 if h else None, eq=0.0) for h in range(13)}, terminal_ev=0.0, terminal_equity=0.0, terminal_ps=0.0, terminal_fcff=0.0, terminal_fraction=0.0, equity_total=0.0, debt_peak=debt0, failed=True, unfunded_equity_need=equity, failure_t=t)
    last = rows[-1]
    g = p['g']
    revenue = last['R'] * (1 + g)
    eb = (last['EBITDA'] - last['DA'] - last['SBC']) * (1 + g)
    nopat = eb * 0.75
    reinvest = max(0, nopat * g / 0.12)
    terminal_fcff = nopat - reinvest
    terminal_ev = max(0, terminal_fcff / (wacc - g))
    terminal_equity = max(0, terminal_ev - debt + max(0, cash - 3))
    terminal_ps = terminal_equity / shares
    vals = {}
    for h in range(13):
        value = sum((div[i] / (1 + ke) ** (i + 1 - h) for i in range(h, 12))) + terminal_ps / (1 + ke) ** (12 - h)
        paid = sum(div[:h])
        wealth = value + paid
        vals[h] = dict(value=value, paid=paid, wealth=wealth, total=wealth / P0 - 1, annual=(wealth / P0) ** (1 / h) - 1 if h else None, eq=value * (S0 if h == 0 else rows[h - 1]['shares']))
    return dict(rows=rows, values=vals, terminal_ev=terminal_ev, terminal_equity=terminal_equity, terminal_ps=terminal_ps, terminal_fcff=terminal_fcff, terminal_fraction=terminal_ps / (1 + ke) ** 12 / max(vals[0]['value'], 1e-12), equity_total=sum((x['equity'] for x in rows)), debt_peak=max((x['debt'] for x in rows)), failed=False)

def run(p, **kwargs):
    prices = {6: 0.0, 7: 0.0}
    for _ in range(60):
        out = once(p, conv_prices=prices, **kwargs)
        new = {t: out['values'][t]['value'] for t in [6, 7]}
        err = max((abs(new[t] - prices[t]) for t in new))
        prices = new
        if err < 1e-09:
            break
    return out
if __name__ == '__main__':
    out = {n: run(p) for n, p in SC.items()}
    pass
    for n, x in out.items():
        print(n, 'V', {h: round(x['values'][h]['value'], 2) for h in [0, 1, 3, 7, 12]}, 'div7', round(x['values'][7]['paid'], 2), 'eq_raise', round(x['equity_total'], 2), 'peakD', round(x['debt_peak'], 2), 'tail%', round(x['terminal_fraction'] * 100, 1))
        print('rows', [(r['t'], round(r['EBIT'], 1), round(r['debt'], 1), round(r['shares'], 3), round(r['equity'], 1), round(r['dps'], 1)) for r in x['rows']])