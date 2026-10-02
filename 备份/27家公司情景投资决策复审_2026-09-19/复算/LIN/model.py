"""LIN independent scenario model; USD billions, shares billions. Research assumptions, not guidance."""
import json, math
from pathlib import Path
P0 = 460.4
S0 = 0.46298
D0 = 28.4
CASH = 4.9
RESERVE = 2.0
TAX = 0.24
WACC = 0.085
NODES = [0, 1, 3, 7, 15]
UNITS = ['core', 'electronics', 'new_hydrogen', 'engineering']
START_R = [30.35, 3.5, 0.15, 2.5]
START_M = [0.31, 0.31, 0.1, 0.16]
PARAM = {'受损': dict(p=0.25, g=0.02, roic=0.12, divg=0.02, buyg=0.0, r=[[29.8, 30.5, 33.5, 39.5], [3.6, 4.0, 5.1, 6.5], [0.18, 0.4, 0.85, 1.1], [2.4, 2.4, 2.6, 2.8]], m=[[0.285, 0.29, 0.295, 0.295], [0.28, 0.285, 0.29, 0.29], [0.0, 0.12, 0.21, 0.23], [0.12, 0.13, 0.14, 0.14]], growth=[[0.55, 0.5, 0.65, 0.7, 0.75, 0.8, 0.85], [0.85, 0.75, 0.6, 0.6, 0.6, 0.65, 0.65], [0.75, 0.6, 0.4, 0.35, 0.3, 0.25, 0.2], [0.04] * 7], legal=[0.4, 0.5, 0.3, 0, 0, 0, 0], jv=[-0.1, -0.05, 0, 0.02, 0.04, 0.05, 0.06]), '基准': dict(p=0.5, g=0.0275, roic=0.16, divg=0.05, buyg=0.05, r=[[31.4, 33.8, 39.5, 50.8], [4.0, 5.0, 7.5, 11.8], [0.3, 0.75, 1.65, 2.4], [2.575, 2.73, 3.0, 3.6]], m=[[0.314, 0.322, 0.33, 0.33], [0.31, 0.325, 0.34, 0.33], [0.14, 0.26, 0.3, 0.29], [0.16, 0.16, 0.16, 0.16]], growth=[[0.9, 1.0, 1.05, 1.1, 1.15, 1.2, 1.25], [0.9, 0.95, 1.0, 1.0, 1.0, 1.0, 1.0], [0.8, 0.75, 0.6, 0.5, 0.4, 0.3, 0.25], [0.05] * 7], legal=[0.1, 0.15, 0.1, 0, 0, 0, 0], jv=[-0.08, -0.05, 0, 0.05, 0.09, 0.11, 0.13]), '乐观': dict(p=0.2, g=0.03, roic=0.18, divg=0.07, buyg=0.07, r=[[32.0, 35.8, 44.0, 59.5], [4.15, 5.7, 9.0, 15.0], [0.4, 1.0, 2.1, 3.4], [2.65, 2.9, 3.4, 4.3]], m=[[0.32, 0.335, 0.35, 0.34], [0.32, 0.34, 0.36, 0.35], [0.18, 0.29, 0.32, 0.31], [0.17, 0.175, 0.175, 0.17]], growth=[[1.15, 1.3, 1.45, 1.55, 1.65, 1.7, 1.75], [1.05, 1.15, 1.25, 1.3, 1.3, 1.3, 1.25], [0.85, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4], [0.06] * 7], legal=[0, 0.05, 0, 0, 0, 0, 0], jv=[-0.08, -0.03, 0.04, 0.1, 0.15, 0.19, 0.22]), '突破': dict(p=0.05, g=0.0325, roic=0.18, divg=0.08, buyg=0.09, r=[[31.6, 35.0, 43.0, 58.0], [4.25, 6.4, 12.0, 22.0], [0.4, 1.05, 2.3, 4.5], [2.6, 2.85, 3.5, 5.0]], m=[[0.316, 0.328, 0.34, 0.34], [0.32, 0.345, 0.37, 0.35], [0.17, 0.28, 0.32, 0.31], [0.165, 0.17, 0.18, 0.18]], growth=[[1.0, 1.1, 1.25, 1.35, 1.45, 1.55, 1.65], [1.3, 1.65, 2.0, 2.25, 2.5, 2.6, 2.6], [0.9, 0.85, 0.8, 0.7, 0.65, 0.6, 0.6], [0.07] * 7], legal=[0, 0.05, 0, 0, 0, 0, 0], jv=[-0.12, -0.08, 0.02, 0.12, 0.22, 0.3, 0.38])}

def interpolate(points, t, log=False):
    for a, b in zip(range(4), range(1, 5)):
        if t <= NODES[b]:
            f = (t - NODES[a]) / (NODES[b] - NODES[a])
            return points[a] * (points[b] / points[a]) ** f if log else points[a] + f * (points[b] - points[a])
    raise ValueError(t)

def operations(name, overrides=None):
    import copy
    z = copy.deepcopy(PARAM[name])
    if overrides:
        z.update(overrides)
    out = []
    prev_r = START_R[:]
    prev_n = [r * m * (1 - TAX) for r, m in zip(START_R, START_M)]
    for t in range(1, 16):
        r = [interpolate([START_R[u]] + z['r'][u], t, True) for u in range(4)]
        m = [interpolate([START_M[u]] + z['m'][u], t) for u in range(4)]
        e = [r[u] * m[u] for u in range(4)]
        n = [v * (1 - TAX) for v in e]
        da = [r[u] * [0.078, 0.1, 0.17, 0.025][u] for u in range(4)]
        wc = [0.05 * (r[u] - prev_r[u]) for u in range(4)]
        if t <= 7:
            growth = [z['growth'][u][t - 1] for u in range(4)]
            maint = [1.04 * d for d in da]
            investment = [maint[u] + growth[u] for u in range(4)]
            special = z['legal'][t - 1]
            jv = z['jv'][t - 1]
        else:
            q = (t - 7) / 8
            growth = []
            investment = []
            for u in range(4):
                early = max(0, n[u] - prev_n[u]) / [0.22, 0.16, 0.13, 0.2][u]
                terminal = n[u] * z['g'] / z['roic']
                net = (1 - q) * early + q * terminal
                investment.append(da[u] + net - wc[u])
                growth.append(net - wc[u])
            maint = da[:]
            special = 0
            jv = z['jv'][-1] * 1.03 ** (t - 7)
        unitcf = [n[u] + da[u] - investment[u] - wc[u] for u in range(4)]
        minority = 0.18 * (sum(r) / 36.5)
        fcff = sum(unitcf) + jv - minority - special
        out.append(dict(t=t, r=r, m=m, e=e, n=n, da=da, wc=wc, growth=growth, investment=investment, maint=maint, revenue=sum(r), ebit=sum(e), nopat=sum(n), fcff=fcff, unitcf=unitcf, jv=jv, minority=minority, special=special))
        prev_r, prev_n = (r, n)
    return (z, out)

def capital(z, rows, buy_multiplier=1, repurchase=True):
    debt = D0
    cash = CASH
    shares = S0
    cumdiv = 0
    cumrep = 0
    ans = []
    for row in rows:
        t = row['t']
        net_rate = 0.016 + min(t - 1, 6) * 0.002
        interest = max(0, debt - cash) * net_rate
        dps = 6.4 * (1 + z['divg']) ** t
        div = dps * shares
        surplus = row['fcff'] - interest * (1 - TAX) - div
        buy = 0.6 * max(0, surplus) if repurchase else 0
        if debt - surplus + buy < 10 and repurchase:
            buy = 10 - debt + surplus
        buyprice = P0 * (1 + z['buyg']) ** (t - 0.5) * buy_multiplier
        newshares = shares - buy / buyprice
        newdebt = debt - surplus + buy
        newcash = cash
        if newdebt < 0:
            newcash -= newdebt
            newdebt = 0
        cumdiv += dps
        cumrep += buy
        ans.append(dict(t=t, debt=newdebt, cash=newcash, netdebt=newdebt - newcash, shares=newshares, interest=interest, div=div, dps=dps, cumdiv=cumdiv, buy=buy, buyprice=buyprice, cumrep=cumrep, capital_residual=newdebt - debt - (newcash - cash) - (div + buy + interest * (1 - TAX) - row['fcff'])))
        debt, cash, shares = (newdebt, newcash, newshares)
    return ans

def valuation(z, rows, caps, h=0, w=WACC, g=None, roic=None):
    if g is None:
        g = z['g']
    if roic is None:
        roic = z['roic']
    end = rows[-1]
    terminal = (end['nopat'] * (1 - g / roic) + end['jv'] - end['minority']) * (1 + g) / (w - g)
    near = sum((r['fcff'] / (1 + w) ** (r['t'] - h) for r in rows if r['t'] > h))
    pvterm = terminal / (1 + w) ** (15 - h)
    debt = caps[h - 1]['debt'] if h else D0
    shares = caps[h - 1]['shares'] if h else S0
    cash = caps[h - 1]['cash'] if h else CASH
    equity = near + pvterm + cash - RESERVE - debt
    divs = caps[h - 1]['cumdiv'] if h else 0
    price = equity / shares
    wealth = price + divs
    return dict(h=h, ev=near + pvterm, equity=equity, price=price, divs=divs, wealth=wealth, total=wealth / P0 - 1, cagr=(wealth / P0) ** (1 / h) - 1 if h else None, terminalshare=pvterm / (near + pvterm), pvterm=pvterm, terminal=terminal)

def calc(name, overrides=None, buy_multiplier=1, repurchase=True):
    z, rows = operations(name, overrides)
    caps = capital(z, rows, buy_multiplier, repurchase)
    vals = []
    for h in [0, 1, 3, 7]:
        central = valuation(z, rows, caps, h)
        low = valuation(z, rows, caps, h, 0.0925, z['g'] - 0.005, max(0.1, z['roic'] - 0.02))
        high = valuation(z, rows, caps, h, 0.0775, z['g'] + 0.005, z['roic'] + 0.02)
        vals.append(dict(central=central, low=low, high=high))
    return dict(parameters=z, rows=rows, capital=caps, values=vals)
if __name__ == '__main__':
    allresults = {n: calc(n) for n in PARAM}
    for name, a in allresults.items():
        print(name)
        for v in a['values']:
            q = v['central']
            lo = v['low']
            hi = v['high']
            print(q['h'], 'px', round(q['price'], 2), 'band', round(lo['price']), round(hi['price']), 'div', round(q['divs'], 2), 'ret', round(q['total'] * 100, 1), 'cagr', round((q['cagr'] or 0) * 100, 1), 'TV', round(q['terminalshare'] * 100, 1))
        for t in [1, 3, 7, 15]:
            r = a['rows'][t - 1]
            c = a['capital'][t - 1]
            print(t, *(round(r[k], 3) for k in ['revenue', 'ebit', 'fcff']), 'invest', round(sum(r['investment']), 3), 'ND', round(c['netdebt'], 3), 'shares', round(c['shares'], 6))