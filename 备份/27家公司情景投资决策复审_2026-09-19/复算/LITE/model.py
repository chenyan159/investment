import json, math, copy
from pathlib import Path
PRICE = 930.91
N = 102.0
CASH0 = 2.7384 + 0.18 - 1.5543 - 0.0928
MINCASH0 = 0.6
EXCESS0 = CASH0 - MINCASH0
KEYS = ['激光器', '传输', '模块', 'OCS', '新光源', '工业传感']
PATHS = {'悲观': dict(p=0.2, g=0.0, roic=0.12, r={1: [1.7, 1.3, 1.0, 0.4, 0.15, 0.25], 3: [1.2, 1.2, 0.85, 0.35, 0.2, 0.2], 7: [0.9, 1.1, 0.8, 0.3, 0.3, 0.2], 10: [0.75, 1.0, 0.65, 0.25, 0.25, 0.15]}, m={1: [0.3, 0.3, 0.12, 0.18, -0.1, 0.08], 3: [0.22, 0.25, 0.1, 0.12, 0.05, 0.05], 7: [0.2, 0.23, 0.09, 0.1, 0.1, 0.05], 10: [0.18, 0.22, 0.08, 0.1, 0.1, 0.05]}, cap={1: 0.65, 3: 0.28, 7: 0.2, 10: 0.18}), '基准': dict(p=0.4, g=0.025, roic=0.18, r={1: [2.35, 1.65, 1.5, 0.7, 0.4, 0.3], 3: [3.1, 2.1, 2.4, 1.45, 1.3, 0.35], 7: [3.25, 2.55, 3.0, 2.0, 3.2, 0.4], 10: [3.0, 2.7, 3.2, 2.2, 3.8, 0.4]}, m={1: [0.48, 0.4, 0.27, 0.38, 0.35, 0.12], 3: [0.45, 0.37, 0.25, 0.36, 0.4, 0.12], 7: [0.36, 0.32, 0.22, 0.3, 0.35, 0.12], 10: [0.32, 0.3, 0.2, 0.28, 0.32, 0.12]}, cap={1: 0.95, 3: 1.2, 7: 1.0, 10: 0.95}), '乐观': dict(p=0.25, g=0.03, roic=0.22, r={1: [2.5, 1.7, 1.7, 0.85, 0.55, 0.3], 3: [3.8, 2.5, 3.2, 2.0, 2.2, 0.4], 7: [4.4, 3.2, 4.5, 3.5, 6.0, 0.45], 10: [4.5, 3.5, 5.0, 4.0, 8.0, 0.5]}, m={1: [0.5, 0.42, 0.3, 0.4, 0.4, 0.12], 3: [0.49, 0.4, 0.29, 0.4, 0.46, 0.14], 7: [0.43, 0.36, 0.27, 0.37, 0.43, 0.14], 10: [0.38, 0.34, 0.25, 0.34, 0.4, 0.14]}, cap={1: 1.05, 3: 1.6, 7: 1.7, 10: 1.6}), '突破': dict(p=0.1, g=0.035, roic=0.25, r={1: [2.5, 1.7, 1.7, 0.9, 0.7, 0.3], 3: [3.8, 2.5, 3.2, 2.4, 4.2, 0.4], 7: [4.0, 3.2, 4.0, 6.0, 15.0, 0.5], 10: [3.8, 3.5, 4.2, 7.5, 21.0, 0.55]}, m={1: [0.5, 0.42, 0.3, 0.4, 0.42, 0.12], 3: [0.48, 0.4, 0.28, 0.42, 0.49, 0.14], 7: [0.4, 0.36, 0.25, 0.42, 0.49, 0.15], 10: [0.35, 0.33, 0.23, 0.38, 0.45, 0.15]}, cap={1: 1.2, 3: 2.1, 7: 3.2, 10: 3.1})}
TAIL_P = 0.05

def interp(nodes, t):
    if t in nodes:
        return copy.deepcopy(nodes[t])
    a = max((x for x in nodes if x < t))
    b = min((x for x in nodes if x > t))
    w = (t - a) / (b - a)
    if isinstance(nodes[a], list):
        return [x + (y - x) * w for x, y in zip(nodes[a], nodes[b])]
    return nodes[a] + (nodes[b] - nodes[a]) * w

def run(d, disc=0.105, dg=0, margin_shift=0, cap_scale=1, rev_scale=1, n=N):
    rows = []
    prev = 5.0
    cash = EXCESS0
    pp = 1.3
    for t in range(1, 11):
        rv = [x * rev_scale for x in interp(d['r'], t)]
        R = sum(rv)
        margins = [x + margin_shift for x in interp(d['m'], t)]
        profits = [x * y for x, y in zip(rv, margins)]
        corp = 0.12 + 0.012 * R + (interp(d['extra'], t) if 'extra' in d else 0)
        sbc = R * min(0.03, 0.01 * t)
        ebit = sum(profits) - corp - sbc
        tax = max(0, ebit) * 0.21
        dep = 0.035 * R
        cap = interp(d['cap'], t) * cap_scale
        pp += cap - (0.1814 if t == 1 else 0) - dep
        dnwc = 0.14 * (R - prev)
        dmin = 0.04 * (R - prev)
        fcff = ebit - tax + dep - cap - dnwc - dmin
        cash = cash * 1.03 + fcff
        rows.append(dict(t=t, rv=rv, R=R, profits=profits, corp=corp, sbc=sbc, ebit=ebit, tax=tax, dep=dep, cap=cap, dnwc=dnwc, dmin=dmin, fcff=fcff, cash=cash, mincash=0.6 + 0.04 * (R - 5), pp=pp))
        prev = R
    g = d['g'] + dg
    terminal = rows[-1]['ebit'] * (1 - 0.21) * (1 + g) * (1 - g / d['roic']) / (disc - g)
    values = {}
    for t in [0, 1, 3, 7]:
        remain = sum((z['fcff'] / (1 + disc) ** (z['t'] - t) for z in rows if z['t'] > t)) + terminal / (1 + disc) ** (10 - t)
        cash = EXCESS0 if t == 0 else rows[t - 1]['cash']
        equity = remain + cash
        p = equity * 1000 / n
        values[t] = dict(ev=remain, cash=cash, eq=equity, p=p, ret=p / PRICE - 1, cagr=(p / PRICE) ** (1 / t) - 1 if t else None, tvshare=terminal / (1 + disc) ** (10 - t) / remain)
    return dict(rows=rows, values=values, terminal=terminal)

def all_results():
    out = {}
    for k, d in PATHS.items():
        out[k] = run(d)
        lo = run(d, 0.12, -0.005, margin_shift=-0.03)
        hi = run(d, 0.09, 0.005, margin_shift=0.03)
        out[k]['range'] = {t: [lo['values'][t]['p'], hi['values'][t]['p']] for t in [0, 1, 3, 7]}
    return out
if __name__ == '__main__':
    out = all_results()
    pass
    for k, a in out.items():
        print(k, 'PV', round(a['values'][0]['p'], 1), 'targets', [(t, round(a['values'][t]['p'], 1), [round(x) for x in a['range'][t]], round(a['values'][t]['cagr'] * 100, 1)) for t in [1, 3, 7]])
        print('R/EBIT/FCF/cash/mincash', [(z['t'], *[round(z[x], 3) for x in ['R', 'ebit', 'fcff', 'cash', 'mincash']]) for z in a['rows'] if z['t'] in [1, 3, 7, 10]])
    for t in [0, 1, 3, 7]:
        exp = sum((PATHS[k]['p'] * a['values'][t]['p'] for k, a in out.items()))
        print('Expected', t, round(exp, 2), 'ann', round(((exp / PRICE) ** (1 / t) - 1) * 100, 2) if t else None)