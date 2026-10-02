import math, json, copy
from pathlib import Path
PRICE = 64.57
S0 = (598350482 + 40951250 + 13095520 + 2607745) / 1000000000.0
C0 = 2.3
K = [1, 3, 7, 15]
P = {'受损': dict(p=0.2, el=[0.27, 0.29, 0.3, 0.27], sy=[0.78, 0.95, 1.5, 2.2], n=[0, 0, 0, 0], net=[1.0, 1.04, 1.1, 1.3], em=[0.1, 0.13, 0.14, 0.12], sm=[-0.03, 0.04, 0.1, 0.12], nm=[-0.28, -0.1, 0, 0], im=[0.27, 0.3, 0.32, 0.33], corp=[0.09, 0.1, 0.11, 0.12], cap=[0.16, 0.1, 0.12, 0.14], close=1, rate=0.095, eq=1.8, issue=25, swap=0.4, g=0.015, roic=0.09), '基准': dict(p=0.4, el=[0.31, 0.39, 0.49, 0.6], sy=[0.88, 1.35, 2.45, 4.2], n=[0.055, 0.33, 0.99, 1.43], net=[1.04, 1.15, 1.5, 2.0], em=[0.17, 0.22, 0.24, 0.23], sm=[0.02, 0.12, 0.18, 0.18], nm=[-0.23, -0.12, 0.18, 0.26], im=[0.32, 0.34, 0.36, 0.34], corp=[0.1, 0.13, 0.2, 0.28], cap=[0.18, 0.23, 0.31, 0.4], close=1, rate=0.075, eq=0.8, issue=55, swap=0.4, g=0.025, roic=0.13), '乐观': dict(p=0.2, el=[0.35, 0.48, 0.65, 0.78], sy=[1.0, 1.8, 4.0, 7.0], n=[0.11, 0.66, 1.8, 3.0], net=[1.08, 1.26, 1.85, 2.9], em=[0.2, 0.25, 0.27, 0.25], sm=[0.05, 0.17, 0.24, 0.24], nm=[-0.21, -0.02, 0.36, 0.75], im=[0.33, 0.37, 0.4, 0.38], corp=[0.11, 0.16, 0.29, 0.43], cap=[0.2, 0.33, 0.52, 0.75], close=1, rate=0.065, eq=0.7, issue=75, swap=0.36, g=0.03, roic=0.16), '突破': dict(p=0.05, el=[0.35, 0.5, 0.72, 0.9], sy=[1.02, 2.0, 5.5, 12.0], n=[0.11, 0.9, 2.7, 5.0], net=[1.08, 1.32, 2.3, 4.3], em=[0.2, 0.25, 0.28, 0.25], sm=[0.05, 0.18, 0.28, 0.28], nm=[-0.21, 0.03, 0.675, 1.5], im=[0.33, 0.38, 0.44, 0.43], corp=[0.11, 0.18, 0.38, 0.7], cap=[0.22, 0.42, 0.82, 1.4], close=1, rate=0.065, eq=1.2, issue=90, swap=0.3, g=0.035, roic=0.18)}
P['独立'] = copy.deepcopy(P['基准'])
P['独立'].update(p=0.1, close=0, eq=0, net=[0] * 4, im=[0] * 4)
P['重组'] = copy.deepcopy(P['受损'])
P['重组'].update(p=0.05)

def interp(v, t):
    if t <= 1:
        return v[0]
    for j in range(1, len(K)):
        if t <= K[j]:
            w = (t - K[j - 1]) / (K[j] - K[j - 1])
            return v[j - 1] * (1 - w) + v[j] * w
    return v[-1]

def run(name, ke=0.12, change=None):
    z = copy.deepcopy(P[name])
    z.update(change or {})
    cash = C0
    debt = 0.018
    shares = S0
    rows = []
    taxloss = 0.6
    funds = 0
    for t in range(1, 16):
        d = {key: interp(z[key], t) for key in ['el', 'sy', 'n', 'net', 'em', 'sm', 'nm', 'im', 'corp', 'cap']}
        f = 0.25 if t == 1 and z['close'] else 1 if z['close'] else 0
        eb_el = d['el'] * d['em']
        eb_sy = d['sy'] * d['sm']
        eb_n = d['nm']
        eb_net = d['net'] * d['im'] * f
        rev = d['el'] + d['sy'] + d['n'] + d['net'] * f
        ebit = eb_el + eb_sy + eb_n + eb_net - d['corp']
        da = 0.045 * (d['el'] + d['sy'] + d['n']) + 0.18 * d['net'] * f
        nc = 0.1 if t <= 4 else 0.57 * z.get('renewal_factor', 1) if t <= 9 else 0.25
        cap = d['cap'] + nc * d['net'] * f
        if name == '受损' and t == 4:
            ebit -= 0.08
        core = d['el'] + d['sy'] + d['n']
        prev = 1.0 if t == 1 else rows[-1]['core']
        wc = 0.14 * (core - prev) + 0.02 * (d['net'] - (0 if t == 1 else interp(z['net'], t - 1))) * f
        ebitcash = ebit
        eq = 0
        event = 0
        newdebt = 0
        if t == 1 and z['close']:
            event = -2.861 - 0.27 - 0.1834 + 0.12
            newdebt = 2.03 + (1.825 - z['eq'])
            debt += newdebt
            eq = z['eq']
            shares += eq / z['issue'] + 0.105956 * z['swap'] + 0.002
        if t == 2:
            event += 0.474
            shares += 0.0074512
        debt_interest = z['rate'] * (debt - newdebt * (0.75 if t == 1 else 0))
        cash_interest = 0.03 * max(cash - 0.4, 0)
        taxable = ebit - debt_interest + cash_interest
        if taxable < 0:
            taxloss -= taxable
            tax = 0
        else:
            offset = min(taxloss, 0.8 * taxable)
            taxloss -= offset
            tax = 0.24 * (taxable - offset)
        tax = max(tax, 0.02 * d['net'] * f)
        fcff = ebit - tax + da - cap - wc
        cf = fcff - debt_interest + cash_interest
        cash += cf + event + eq + (newdebt - 2.03 if t == 1 and z['close'] else 0)
        floor = max(0.4, 0.07 * rev)
        raise_cash = 0
        if cash < floor:
            raise_cash = floor - cash
            cash = floor
            shares += raise_cash / z.get('rescue_price', {'受损': 1, '基准': 5, '乐观': 15, '突破': 25}.get(name, z['issue']))
            funds += raise_cash
        repay = 0
        div = 0
        if t >= 3:
            repay = min(debt, max(0, cash - floor))
            cash -= repay
            debt -= repay
        if t >= 4 and debt < 1e-09:
            div = max(0, cash - floor)
            cash -= div
        rows.append(dict(t=t, rev=rev, core=core, ebit=ebit, el_ebit=eb_el, sy_ebit=eb_sy, n_ebit=eb_n, net_ebit=eb_net, da=da, cap=cap, wc=wc, tax=tax, fcff=fcff, interest=debt_interest, cf=cf, cash=cash, debt=debt, shares=shares, div=div, dps=div / shares, eq=eq, raise_cash=raise_cash, repay=repay, event=event))
    if name == '重组':
        for row in rows:
            row['dps'] = 0
            if row['t'] >= 3:
                for field in ['rev', 'core', 'ebit', 'el_ebit', 'sy_ebit', 'n_ebit', 'net_ebit', 'fcff', 'cash', 'debt', 'div', 'cf', 'eq', 'raise_cash', 'repay']:
                    row[field] = 0
        return dict(name=name, rows=rows, values={0: 0, 1: 0, 3: 0, 7: 0}, wealth={1: 0, 3: 0, 7: 0}, tv=0, terminal_share=0, funds=0)
    last = rows[-1]
    g = z['g']
    normalized = (last['ebit'] - 0.07 * z['net'][-1]) * 0.76 * (1 + g) * (1 - g / z['roic'])
    tv = max(0, normalized / (ke - g) - last['debt'])
    terminal_share = tv / last['shares']
    values = {}
    wealth = {}
    for h in [0, 1, 3, 7]:
        values[h] = sum((r['dps'] / (1 + ke) ** (r['t'] - h) for r in rows if r['t'] > h)) + terminal_share / (1 + ke) ** (15 - h)
        if h:
            wealth[h] = values[h] + sum((r['dps'] for r in rows if r['t'] <= h))
    return dict(name=name, rows=rows, values=values, wealth=wealth, tv=tv, terminal_share=terminal_share, funds=funds)
for name in P:
    a = run(name)
    print(name, a['values'], a['wealth'])