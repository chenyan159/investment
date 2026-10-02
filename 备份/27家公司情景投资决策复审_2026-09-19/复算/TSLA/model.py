import math, json, copy
from datetime import date
from pathlib import Path
ROOT = Path(__file__).parent
P0 = 364.27
NODES = [0, 1, 3, 7, 12, 20]
START = dict(v=1.75, asp=40, am=0.075, e=50, ep=0.21, em=0.16, s=17, sm=0.07, f=1.3, fp=1.05, fm=0.6, r=0.001, mi=30, fare=1.2, own=1.0, take=0.2, rm=0.2, o=0, op=40, installed=0, fee=2, om=0, over=10, extra=17)
DATA = {'D': dict(v=[1.55, 1.35, 1.2, 1.1, 0.9], asp=[37, 34, 31, 30, 30], am=[0.02, 0.03, 0.04, 0.04, 0.03], e=[52, 65, 90, 105, 110], ep=[0.185, 0.15, 0.115, 0.095, 0.08], em=[0.09, 0.1, 0.09, 0.08, 0.07], s=[17, 17, 16, 15, 14], sm=[0.04, 0.05, 0.05, 0.05, 0.04], f=[1.4, 1.8, 2, 1.8, 1.5], fp=[0.95, 0.9, 0.8, 0.75, 0.7], fm=[0.45, 0.5, 0.5, 0.45, 0.4], r=[0.002, 0.006, 0.01, 0.01, 0.005], mi=[20, 23, 25, 25, 25], fare=[1.2, 1.1, 1, 1, 1], own=[1, 0.8, 0.5, 0.5, 0.5], take=[0.2] * 5, rm=[0.05, 0.1, 0.15, 0.15, 0.1], o=[0, 0.0001, 0.002, 0.003, 0.003], op=[40, 35, 30, 25, 22], installed=[0, 0.0002, 0.008, 0.012, 0.015], fee=[2] * 5, om=[0, 0, 0.05, 0.05, 0.05], over=[10, 6.5, 4, 3.5, 3], extra=[12, 3, 1, 0.5, 0.3]), 'B': dict(v=[1.85, 2.2, 2.8, 3.1, 3.0], asp=[39, 37, 35, 34, 33], am=[0.07, 0.09, 0.1, 0.09, 0.08], e=[63, 95, 180, 270, 360], ep=[0.195, 0.17, 0.13, 0.105, 0.085], em=[0.14, 0.16, 0.16, 0.15, 0.13], s=[19, 23, 30, 37, 42], sm=[0.08, 0.1, 0.11, 0.11, 0.1], f=[1.8, 3.2, 7, 11, 13], fp=[1.05, 1.0, 0.95, 0.9, 0.8], fm=[0.6, 0.65, 0.68, 0.68, 0.65], r=[0.006, 0.1, 0.6, 2, 4], mi=[27, 32, 40, 43, 45], fare=[1.2, 1.1, 1.05, 1, 0.9], own=[1, 0.65, 0.35, 0.25, 0.2], take=[0.2] * 5, rm=[0.18, 0.25, 0.35, 0.4, 0.42], o=[0.0002, 0.006, 0.12, 0.6, 1.0], op=[40, 35, 25, 22, 18], installed=[0.0003, 0.012, 0.35, 2, 4.5], fee=[2, 2, 2, 1.8, 1.5], om=[-0.2, 0.05, 0.15, 0.18, 0.18], over=[10.8, 11, 12, 14, 16], extra=[17, 7, 3, 2, 1]), 'U': dict(v=[2, 2.6, 3.8, 4.5, 4.5], asp=[39.5, 38, 36, 34, 32], am=[0.085, 0.11, 0.13, 0.12, 0.1], e=[70, 120, 250, 400, 550], ep=[0.2, 0.175, 0.135, 0.11, 0.085], em=[0.17, 0.2, 0.2, 0.18, 0.15], s=[20, 27, 39, 50, 60], sm=[0.09, 0.12, 0.14, 0.14, 0.12], f=[2.1, 4.5, 11, 20, 25], fp=[1.08, 1.05, 1, 0.9, 0.8], fm=[0.63, 0.68, 0.72, 0.72, 0.68], r=[0.015, 0.25, 2, 6, 10], mi=[30, 36, 44, 47, 48], fare=[1.2, 1.12, 1.05, 0.95, 0.85], own=[0.9, 0.55, 0.25, 0.2, 0.2], take=[0.22, 0.22, 0.22, 0.2, 0.18], rm=[0.2, 0.3, 0.44, 0.46, 0.43], o=[0.0005, 0.025, 0.7, 3, 5], op=[40, 32, 24, 20, 17], installed=[0.001, 0.04, 1.8, 10, 22], fee=[2, 2, 2, 1.8, 1.5], om=[-0.1, 0.1, 0.2, 0.23, 0.2], over=[11.5, 13, 18, 24, 29], extra=[18, 9, 5, 3, 1.5]), 'X': dict(v=[1.95, 2.4, 3.3, 4, 4.5], asp=[39, 37, 34, 32, 30], am=[0.08, 0.1, 0.11, 0.1, 0.09], e=[66, 105, 210, 350, 500], ep=[0.195, 0.17, 0.13, 0.105, 0.085], em=[0.15, 0.17, 0.18, 0.17, 0.15], s=[20, 26, 37, 48, 58], sm=[0.09, 0.11, 0.13, 0.13, 0.11], f=[2, 4.5, 13, 25, 30], fp=[1.05, 1.05, 1, 0.85, 0.7], fm=[0.62, 0.68, 0.73, 0.72, 0.68], r=[0.02, 0.5, 8, 20, 30], mi=[30, 38, 50, 55, 60], fare=[1.2, 1.12, 0.95, 0.85, 0.8], own=[0.9, 0.5, 0.2, 0.2, 0.2], take=[0.22, 0.22, 0.22, 0.2, 0.18], rm=[0.2, 0.32, 0.5, 0.52, 0.47], o=[0.0008, 0.05, 4, 12, 20], op=[38, 30, 22, 18, 15], installed=[0.001, 0.08, 8, 38, 80], fee=[2, 2, 2, 1.8, 1.5], om=[-0.1, 0.1, 0.24, 0.26, 0.23], over=[12, 15, 25, 40, 50], extra=[20, 12, 8, 5, 3])}
PROB = {'D': 0.28, 'B': 0.42, 'U': 0.2, 'X': 0.08, 'T': 0.02}
DATA['D']['am'] = [0.035, 0.045, 0.055, 0.05, 0.04]
DATA['D']['over'] = [7, 3.5, 2.5, 2, 1.5]
TERMS = {'D': (0, 0.1, 0), 'B': (0.02, 0.15, 0), 'U': (0.025, 0.18, 1), 'X': (0.03, 0.2, 3)}
DATA['T'] = copy.deepcopy(DATA['X'])
for k in ['r', 'o', 'installed']:
    DATA['T'][k] = [x * (1 + (3 - 1) * min(i / 2, 1)) for i, x in enumerate(DATA['T'][k])]
DATA['T']['over'] = [x * 1.4 for x in DATA['X']['over']]
DATA['T']['extra'] = [x * 1.7 for x in DATA['X']['extra']]
TERMS['T'] = (0.03, 0.2, 8)

def interp(vals, t):
    for i in range(1, len(NODES)):
        if t <= NODES[i]:
            w = (t - NODES[i - 1]) / (NODES[i] - NODES[i - 1])
            return vals[i - 1] * (1 - w) + vals[i] * w
    return vals[-1]

def run(name, rate=0.11, override=None, delay=0, capmult=1.0, pricecut=0.0, terminalg=None, issue_factor=1.0):
    data = copy.deepcopy(DATA[name])
    data.update(override or {})
    g, roic, tranches = TERMS[name]
    if terminalg is not None:
        g = terminalg
    rows = []
    cash = 38.0
    debt = 9.36
    shares = 3.6
    loss = 0.0
    prev = None
    raises = []
    for t in range(21):
        a = {k: interp([START[k]] + v, max(0, t - delay) if k in ['r', 'o', 'installed'] else t) for k, v in data.items()}
        a['asp'] *= 1 - pricecut
        rev = {'A': a['v'] * a['asp'], 'E': a['e'] * a['ep'] + 2, 'S': a['s'], 'F': a['f'] * a['fp'], 'R': a['r'] * a['mi'] * a['fare'] * (a['own'] + (1 - a['own']) * a['take']), 'O': a['o'] * a['op'] + a['installed'] * a['fee']}
        profit = {k: rev[k] * a[m] for k, m in zip(['A', 'E', 'S', 'F', 'R', 'O'], ['am', 'em', 'sm', 'fm', 'rm', 'om'])}
        profit['A'] -= a['v'] * (interp([START['asp']] + data['asp'], t) * pricecut) * (1 - a['am']) * 0.75
        profit['G'] = -a['over']
        ebit = sum(profit.values())
        R = sum(rev.values())
        da = 0.035 * rev['A'] + 0.04 * rev['E'] + 0.04 * rev['S'] + 0.06 * rev['F'] + a['r'] * a['own'] * 32 / 5 + 0.05 * rev['O'] + 2
        if t == 0:
            prev = (rev, a, R)
            continue
        delta = {k: max(0, rev[k] - prev[0][k]) for k in rev}
        growth = 0.35 * delta['A'] + 0.4 * delta['E'] + 0.3 * delta['S'] + 0.08 * delta['F'] + 0.45 * delta['O'] + max(0, a['r'] * a['own'] - prev[1]['r'] * prev[1]['own']) * 32 + 0.08 * delta['R']
        capex = da + (growth + a['extra']) * capmult
        nwc = 0.06 * (R - prev[2])
        taxable = max(0, ebit - loss)
        tax = 0.24 * taxable
        loss = max(0, loss - ebit)
        fcff = ebit - tax + da - capex - nwc
        principal = min(debt, [0, 6.2, 1.2, 0.5, 0.5, 0.3, 0.3, 0.36][t] if t <= 7 else debt)
        debtinterest = debt * 0.05 * (0.76 if ebit > 0 else 1)
        netinterest = max(0, cash + 0.5 * (fcff - principal - debtinterest)) * 0.032 - debtinterest
        cashbefore = cash
        cash += fcff + netinterest - principal
        debt -= principal
        issue = max(0, 15 - cash)
        issueprice = {'D': 60, 'B': 180, 'U': 280, 'X': 300, 'T': 300}[name] * issue_factor
        before = shares
        if issue > 0:
            shares += issue / issueprice
            cash += issue
            raises.append((t, issue, shares - before, shares))
        dividend = max(0, cash - 15) if t >= 8 else 0.0
        cash -= dividend
        rows.append(dict(t=t, rev=rev, profit=profit, ebit=ebit, revenue=R, da=da, capex=capex, nwc=nwc, tax=tax, fcff=fcff, cash=cash, debt=debt, shares=shares, issue=issue, issueprice=issueprice, principal=principal, netinterest=netinterest, cashbefore=cashbefore, dividend=dividend, inputs=a))
        prev = (rev, a, R)
    terminal = rows[-1]['ebit'] * 0.76 * (1 + g) * (1 - g / roic) / (rate - g)
    other = 3.5
    residual = terminal + other + rows[-1]['cash'] - 15 - rows[-1]['debt']
    eq9 = sum((x['dividend'] / (1 + rate) ** (x['t'] - 9) for x in rows if x['t'] >= 9)) + residual / (1 + rate) ** 11
    award = tranches * 0.035311992
    p9 = (eq9 + award * 334.09) / (rows[8]['shares'] + award)
    award_net = award * max(0, 1 - 334.09 / max(p9, 1e-09))
    assert all((x['issue'] == 0 for x in rows[9:])), 'Extend grant solver for financing after vest'
    for x in rows:
        x['diluted_shares'] = x['shares'] + (award_net if x['t'] >= 9 else 0)

    def calc(h):
        ev = sum((x['fcff'] / (1 + rate) ** (x['t'] - h) for x in rows if x['t'] > h)) + terminal / (1 + rate) ** (20 - h)
        ch = 38 if h == 0 else rows[h - 1]['cash']
        dh = 9.36 if h == 0 else rows[h - 1]['debt']
        nh = 3.6 if h == 0 else rows[h - 1]['shares']
        tail_per_share = residual / rows[-1]['diluted_shares'] / (1 + rate) ** (20 - h)
        price = sum((x['dividend'] / x['diluted_shares'] / (1 + rate) ** (x['t'] - h) for x in rows if x['t'] > h)) + tail_per_share
        equity = price * nh
        years = (date(2026 + h, 9, 19) - date(2026, 9, 19)).days / 365.25 if h else 0
        return dict(ev=ev, equity=equity, price=price, econ_shares=nh, cash=ch, debt=dh, base_shares=nh, terminal_pct=tail_per_share / price, ret=price / P0 - 1, cagr=(price / P0) ** (1 / years) - 1 if h else None)
    return dict(rows=rows, values={h: calc(h) for h in [0, 1, 3, 7]}, terminal=terminal, raises=raises, rate=rate)
if __name__ == '__main__':
    out = {k: run(k) for k in DATA}
    pass
    for k, m in out.items():
        print(k, 'values', [(h, round(v['price'], 1), round(v['ret'] * 100, 1)) for h, v in m['values'].items()], 'raises', [(t, round(a, 2)) for t, a, n, p in m['raises']])
        for t in [1, 3, 7, 12, 20]:
            x = m['rows'][t - 1]
            print(t, *[round(x[f], 2) for f in ['revenue', 'ebit', 'capex', 'fcff', 'cash', 'shares']])