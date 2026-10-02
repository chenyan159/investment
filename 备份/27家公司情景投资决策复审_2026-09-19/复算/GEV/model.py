import json, math
from pathlib import Path
from copy import deepcopy
P0 = 940.33
N0 = 0.27
C0 = 12.0
D0 = 2.905
MINC = 4.0
OTHER = 0.5
TAX = 0.25
KNOTS = [1, 3, 7, 14]
NAMES = ['燃机设备', '燃机服务', '成熟核电水电', '传统电网', '风电', '新供电架构', 'SMR', 'SOFC及探索']
DATA = {'悲观': {'p': 0.2, 'div0': 1, 'divgrowth': 0, 'q': [18, 21, 20, 16], 'asp': [0.46, 0.49, 0.45, 0.43], 'svc': [12.5, 13.8, 15.5, 17], 'mature': [4.3, 4.5, 4.8, 5.3], 'grid': [15.8, 18, 20, 23], 'wind': [7.2, 6.3, 5.0, 4.5], 'arch': [0, 0.08, 0.4, 0.5], 'smr': [0.04, 0.08, 0.2, 0.3], 'sofc': [0, 0, 0, 0], 'em': [0.08, 0.1, 0.07, 0.06], 'sm': [0.24, 0.24, 0.23, 0.22], 'gm': [0.15, 0.15, 0.13, 0.13], 'we': [-0.9, -0.5, 0, 0.1], 'ae': [-0.12, -0.1, 0.02, 0.03], 'ne': [-0.08, -0.1, -0.08, -0.03], 'fe': [-0.12, -0.1, -0.05, 0], 'cap': [2.0, 1.8, 1.7, 1.9], 'da': [1.05, 1.15, 1.25, 1.45], 'nw': [-0.25, -0.18, -0.13, -0.12], 'corp': [0.7, 0.75, 0.8, 0.9], 'g': 0.02, 'roc': 0.12}, '基准': {'p': 0.5, 'q': [21, 27, 30, 27], 'asp': [0.48, 0.56, 0.63, 0.62], 'svc': [13.0, 15.2, 21, 27], 'mature': [4.6, 5.0, 5.8, 7.1], 'grid': [16.6, 21, 27.5, 35], 'wind': [7.3, 6.8, 7.0, 8], 'arch': [0.05, 0.55, 2.6, 4.0], 'smr': [0.05, 0.2, 0.9, 2], 'sofc': [0, 0, 0.15, 0.7], 'em': [0.12, 0.19, 0.2, 0.16], 'sm': [0.26, 0.28, 0.29, 0.28], 'gm': [0.18, 0.21, 0.21, 0.18], 'we': [-0.4, 0.1, 0.42, 0.56], 'ae': [-0.1, -0.03, 0.39, 0.64], 'ne': [-0.08, -0.06, 0.09, 0.32], 'fe': [-0.12, -0.12, -0.07, 0.03], 'cap': [2.2, 2.6, 3.0, 3.5], 'da': [1.1, 1.4, 1.8, 2.5], 'nw': [-0.33, -0.29, -0.21, -0.16], 'corp': [0.7, 0.8, 1.0, 1.2], 'g': 0.025, 'roc': 0.15}, '乐观': {'p': 0.23, 'q': [22, 29, 34, 32], 'asp': [0.49, 0.61, 0.73, 0.71], 'svc': [13.3, 16, 23.5, 32], 'mature': [4.7, 5.3, 6.3, 8], 'grid': [17.2, 23, 33, 44], 'wind': [7.5, 7.5, 8.5, 10], 'arch': [0.08, 0.9, 4.2, 7], 'smr': [0.06, 0.35, 1.6, 3.5], 'sofc': [0, 0.03, 0.5, 1.6], 'em': [0.14, 0.23, 0.25, 0.22], 'sm': [0.27, 0.3, 0.32, 0.3], 'gm': [0.19, 0.24, 0.25, 0.23], 'we': [-0.15, 0.45, 0.85, 1.0], 'ae': [-0.1, 0.1, 0.84, 1.4], 'ne': [-0.08, -0.03, 0.24, 0.63], 'fe': [-0.12, -0.14, 0, 0.18], 'cap': [2.4, 3.2, 4, 4.9], 'da': [1.1, 1.5, 2.2, 3.5], 'nw': [-0.35, -0.32, -0.24, -0.18], 'corp': [0.72, 0.85, 1.1, 1.45], 'g': 0.025, 'roc': 0.17}, '突破': {'p': 0.07, 'q': [22, 30, 38, 38], 'asp': [0.49, 0.63, 0.78, 0.76], 'svc': [13.4, 16.5, 26, 38], 'mature': [4.7, 5.4, 6.5, 8.5], 'grid': [17.3, 24, 37, 54], 'wind': [7.3, 6.8, 7, 8], 'arch': [0.1, 1.5, 7.5, 14], 'smr': [0.06, 0.4, 2, 5], 'sofc': [0, 0.05, 1.2, 4], 'em': [0.14, 0.24, 0.28, 0.24], 'sm': [0.27, 0.31, 0.34, 0.32], 'gm': [0.19, 0.25, 0.28, 0.25], 'we': [-0.4, 0.1, 0.42, 0.56], 'ae': [-0.1, 0.2, 1.65, 3.36], 'ne': [-0.08, -0.04, 0.3, 1.0], 'fe': [-0.12, -0.17, 0.06, 0.6], 'cap': [2.6, 4.0, 5.6, 7.3], 'da': [1.1, 1.7, 3, 5], 'nw': [-0.35, -0.32, -0.24, -0.18], 'corp': [0.75, 1.0, 1.5, 2], 'g': 0.025, 'roc': 0.18}}

def interp(v, t):
    for i in range(3):
        if t <= KNOTS[i + 1]:
            return v[i] + (v[i + 1] - v[i]) * (t - KNOTS[i]) / (KNOTS[i + 1] - KNOTS[i])
    return v[-1]

def operating(d):
    rows = []
    prev = -16.735
    for t in range(1, 15):
        x = {k: interp(v, t) for k, v in d.items() if isinstance(v, list)}
        rv = [x['q'] * x['asp'], x['svc'], x['mature'], x['grid'], x['wind'], x['arch'], x['smr'], x['sofc']]
        eb = [rv[0] * x['em'], rv[1] * x['sm'], rv[2] * 0.14, rv[3] * x['gm'], x['we'], x['ae'], x['ne'], x['fe']]
        rev = sum(rv)
        ebit = sum(eb) - x['corp']
        wc = rev * x['nw']
        dw = wc - prev
        prev = wc
        tax = TAX * (sum((max(0, z) for z in eb)) - x['corp'] + min(0, eb[4]) * 0.5)
        nci = 0.15 * max(0, eb[2]) * (1 - TAX) + 0.03 * max(0, eb[3]) * (1 - TAX) + 0.4 * max(0, eb[6]) * (1 - TAX)
        fcf = ebit - tax - nci + x['da'] - x['cap'] - dw
        rows.append(dict(t=t, rev=rev, ebit=ebit, tax=tax, nci=nci, fcf=fcf, wc=wc, dwc=dw, rv=rv, eb=eb, **x))
    return rows

def calc(d, r=0.1, g=None, buy=0.3, price=P0, initcash=C0, fcf_shock=None):
    rows = operating(d)
    g = d['g'] if g is None else g
    if fcf_shock:
        for z in rows:
            z['fcf'] += fcf_shock(z['t'])
    last = rows[-1]
    nop = last['ebit'] - last['tax'] - last['nci']
    term = nop * (1 + g) * (1 - g / d['roc']) / (r - g)
    cash = initcash
    debt = D0
    n = N0
    dist = 0
    rep = 0
    val0 = sum((z['fcf'] / (1 + r) ** z['t'] for z in rows)) + term / (1 + r) ** 14 + cash - MINC - debt - OTHER
    out = []
    for z in rows:
        t = z['t']
        dps = d.get('div0', 2) * (1 + d.get('divgrowth', 0.08)) ** (t - 1)
        div = n * dps
        interest = debt * 0.049 * (1 - TAX)
        repayment = 0.6 if t == 5 else 1.0 if t == 10 else 0
        available = z['fcf'] - interest + max(0, cash - MINC) * 0.03 - div - repayment
        budget = max(0, available) * buy
        if cash + available - budget < MINC:
            budget = 0
        cash += available - budget
        debt -= repayment
        rep += budget
        n -= budget / (price * 1.06 ** (t - 0.5))
        extra = max(0, cash - 12.0)
        cash -= extra
        dps += extra / n
        dist += dps
        remaining = sum((j['fcf'] / (1 + r) ** (j['t'] - t) for j in rows if j['t'] > t)) + term / (1 + r) ** (14 - t)
        equity = remaining + cash - MINC - debt - OTHER
        out.append(dict(t=t, cash=cash, debt=debt, n=n, dist=dist, dps=dps, buyback=rep, opvalue=remaining, equity=equity, per=equity / n, total=(equity / n + dist) / price - 1, cagr=((equity / n + dist) / price) ** (1 / t) - 1))
    terminal_per = out[-1]['per']
    for a in out:
        t = a['t']
        a['asset_per'] = a['per']
        a['per'] = sum((j['dps'] / (1 + r) ** (j['t'] - t) for j in out if j['t'] > t)) + terminal_per / (1 + r) ** (14 - t)
        a['equity'] = a['per'] * a['n']
        a['opvalue'] = a['equity'] - a['cash'] + MINC + a['debt'] + OTHER
        a['total'] = (a['per'] + a['dist']) / price - 1
        a['cagr'] = (1 + a['total']) ** (1 / t) - 1
    v0 = sum((a['dps'] / (1 + r) ** a['t'] for a in out)) + terminal_per / (1 + r) ** 14
    return dict(v0=v0, asset_v0=val0 / N0, ev0=val0 - initcash + MINC + D0 + OTHER, termshare=terminal_per / (1 + r) ** 14 / v0, rows=rows, capital=out)

def run():
    result = {k: calc(d) for k, d in DATA.items()}
    for k, z in result.items():
        print(k, 'v0', round(z['v0'], 1), 'terminal%', round(z['termshare'] * 100, 1))
        for t in [1, 3, 7]:
            a = z['capital'][t - 1]
            b = z['rows'][t - 1]
            print(t, 'revenue/EBIT/FCF', *[round(b[v], 2) for v in ['rev', 'ebit', 'fcf']], 'value/div/return/cagr', *[round(a[v], 2) for v in ['per', 'dist', 'total', 'cagr']], 'cash/debt/shares', *[round(a[v], 3) for v in ['cash', 'debt', 'n']])
    for t in [0, 1, 3, 7]:
        wealth = sum((DATA[k]['p'] * (z['v0'] if t == 0 else z['capital'][t - 1]['per'] + z['capital'][t - 1]['dist']) for k, z in result.items()))
        print('WEIGHTED', t, wealth, (wealth / P0) ** (1 / t) - 1 if t else '')
    return result
if __name__ == '__main__':
    run()