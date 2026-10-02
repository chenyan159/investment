import math, json, copy
from pathlib import Path
PRICE = 249.39
SHARES = 0.393
CASH0 = 3.45
DEBT0 = 2.9672
MIN0 = 0.8
REV0 = [4.65, 4.15, 2.25, 2.65, 0.0]
NAMES = ['电力', '热管理', 'IT与预制净额', '服务备件', 'UIG']
KNOTS = [1, 3, 7, 14]
SPEC = {'受损': dict(p=0.2, rev=[[4.7, 3.9, 1.9, 2.7, 0.2], [4.4, 3.5, 1.6, 2.8, 0.22], [5.1, 4.4, 2.1, 3.7, 0.35], [6.0, 5.2, 2.5, 4.5, 0.45]], mar=[[22, 21, 13, 25, 10], [18, 16, 10, 25, 12], [19, 18, 12, 25, 16], [19, 18, 12, 25, 16]], hq=0.018, cap=0.035, nwc=0.14, g=0.02, roic=0.15, earn=[0, 0], shock=[0.8, 0.5, 0], restruct=[0.15, 0.1, 0]), '基准': dict(p=0.5, rev=[[5.25, 4.75, 2.35, 3.0, 0.35], [6.9, 6.6, 3.5, 4.25, 0.7], [9.4, 9.9, 5.8, 6.65, 1.25], [12.5, 12.8, 8.0, 9.0, 1.6]], mar=[[26, 26, 18, 30, 22], [27, 28, 21, 31, 25], [27, 28, 22, 32, 25], [24, 24, 19, 29, 22]], hq=0.015, cap=0.04, nwc=0.1, g=0.03, roic=0.2, earn=[0.3, 0.4], shock=[0.25, 0.1, 0], restruct=[0.03, 0, 0]), '乐观': dict(p=0.23, rev=[[5.5, 5.1, 2.6, 3.15, 0.4], [7.7, 8.0, 4.7, 4.9, 1.1], [12.0, 14.5, 9.0, 8.8, 2.6], [16.0, 20.0, 13.0, 13.0, 4.0]], mar=[[27, 28, 20, 31, 25], [29, 30, 24, 33, 28], [29, 30, 25, 34, 28], [25, 26, 22, 30, 25]], hq=0.014, cap=0.045, nwc=0.1, g=0.03, roic=0.22, earn=[0.5, 0.575], shock=[0.15, 0, 0], restruct=[0.03, 0, 0]), '突破': dict(p=0.07, rev=[[5.55, 5.25, 2.7, 3.2, 0.45], [8.2, 9.8, 6.1, 5.2, 1.6], [13.0, 18.0, 12.0, 10.0, 5.0], [19.0, 25.0, 20.0, 17.0, 9.0]], mar=[[27, 28, 20, 31, 25], [30, 33, 27, 34, 30], [30, 32, 28, 35, 30], [26, 27, 24, 32, 27]], hq=0.015, cap=0.055, nwc=0.12, g=0.03, roic=0.22, earn=[0.575, 0.575], shock=[0.2, 0, 0], restruct=[0.05, 0, 0])}

def interp(nodes, t, geometric=False):
    for j, k in enumerate(KNOTS):
        if t <= k:
            if j == 0:
                return nodes[0][:]
            f = (t - KNOTS[j - 1]) / (k - KNOTS[j - 1])
            return [a * (b / a) ** f if geometric and a > 0 else a + (b - a) * f for a, b in zip(nodes[j - 1], nodes[j])]
    raise ValueError(t)

def run(spec, r=0.105, gshift=0, close=True, revscale=1, marginshift=0, capshift=0):
    rows = []
    cash = CASH0
    debt = DEBT0
    minimum = MIN0
    prev = sum(REV0)
    for t in range(1, 15):
        rev = [x * revscale for x in interp(spec['rev'], t, True)]
        if not close:
            rev[4] = 0
        margins = [x / 100 + marginshift for x in interp(spec['mar'], t)]
        op = [x * m for x, m in zip(rev, margins)]
        total = sum(rev)
        hq = total * spec['hq']
        re = spec['restruct'][t - 1] if t <= 3 else 0
        ebit = sum(op) - hq - re
        dep = total * 0.014
        caprate = spec['cap'] if t <= 7 else spec['cap'] + (0.032 - spec['cap']) * (t - 7) / 7
        cap = total * (caprate + capshift) + sum((a * b for a, b in zip(rev, spec.get('extra_cap', [0] * 5))))
        nwc = spec['nwc'] * (total - prev) + (spec['shock'][t - 1] if t <= 3 else 0)
        fcff = ebit * 0.77 + dep - cap - nwc
        newmin = max(0.8, total * 0.05)
        dmin = newmin - minimum
        pay = ((1.45 + 0.04 if close else 0.02) if t == 1 else 0) + (0.2346 if t == 1 else 0)
        if close and t in (2, 3):
            pay += spec['earn'][t - 2]
        flow = fcff - dmin - pay
        coupon = 0.85 * 0.04125 + 0.6 * 0.0485 + 0.5 * (0.0565 + 0.058 + 0.0595) + 0.0172 * 0.03
        if t == 3:
            coupon -= 0.85 * 0.04125 * (308 / 365)
        if t >= 4:
            coupon -= 0.85 * 0.04125
        if t == 10:
            coupon -= (0.6 * 0.0485 + 0.0172 * 0.03) * (188 / 365)
        if t >= 11:
            coupon -= 0.6 * 0.0485 + 0.0172 * 0.03
        principal = (0.85 if t == 3 else 0) + (0.6172 if t == 10 else 0)
        div = 0.25 * SHARES
        cashyield = max(0, cash - minimum) * 0.03
        cash += fcff - pay - coupon * 0.77 + cashyield - div - principal
        debt -= principal
        borrow = max(0, newmin - cash)
        cash += borrow
        debt += borrow
        rows.append(dict(t=t, rev=rev, op=op, R=total, E=ebit, hq=hq, restruct=re, dep=dep, cap=cap, nwc=nwc, F=fcff, pay=pay, flow=flow, cash=cash, debt=debt, mincash=newmin, borrow=borrow, div=0.25, coupon=coupon, cashyield=cashyield))
        minimum = newmin
        prev = total
    g = spec['g'] + gshift
    term = rows[-1]['E'] * 0.77 * (1 + g) * (1 - g / spec['roic']) / (r - g)
    vals = {}
    for t in [0, 1, 3, 7]:
        rem = sum((x['flow'] / (1 + r) ** (x['t'] - t) for x in rows if x['t'] > t)) + term / (1 + r) ** (14 - t)
        c = CASH0 if t == 0 else rows[t - 1]['cash']
        d = DEBT0 if t == 0 else rows[t - 1]['debt']
        m = MIN0 if t == 0 else rows[t - 1]['mincash']
        eq = rem + c - m - d
        v = eq / SHARES
        wealth = v + 0.25 * t
        vals[t] = dict(EV=rem, equity=eq, V=v, cash=c, debt=d, mincash=m, distribution=0.25 * t, total=wealth / PRICE - 1, cagr=(wealth / PRICE) ** (1 / t) - 1 if t else None, terminal_fraction=term / (1 + r) ** (14 - t) / rem)
    return dict(rows=rows, values=vals, terminal=term, r=r, g=g)

def expected(results, weights=None):
    weights = weights or {k: s['p'] for k, s in SPEC.items()}

    def v(k, mode, t):
        z = results[k][mode]['values']
        return z[t if t in z else str(t)]['V']
    return {t: sum((weights[k] * (0.95 * v(k, 'close', t) + 0.05 * v(k, 'noclose', t)) for k in SPEC)) for t in [0, 1, 3, 7]}

def main():
    results = {k: dict(close=run(s), noclose=run(s, close=False), low=run(s, r=0.115, gshift=-0.005), high=run(s, r=0.095, gshift=0.005)) for k, s in SPEC.items()}
    out = Path(__file__).parent
    pass
    for k, z in results.items():
        print(k)
        for t, v in z['close']['values'].items():
            lo = z['low']['values'][t]['V']
            hi = z['high']['values'][t]['V']
            print(t, 'V', round(v['V'], 2), 'range', round(lo, 2), round(hi, 2), 'return', round(v['total'] * 100, 1), 'CAGR', round((v['cagr'] or 0) * 100, 1), 'cash', round(v['cash'], 2), 'TV%', round(v['terminal_fraction'] * 100, 1))
    for w in [None, {'受损': 0.15, '基准': 0.4, '乐观': 0.32, '突破': 0.13}, {'受损': 0.3, '基准': 0.5, '乐观': 0.17, '突破': 0.03}]:
        print('EXPECTED', w, expected(results, w))
if __name__ == '__main__':
    main()
for name, spec in SPEC.items():
    z = run(spec)
    ev = z['terminal']
    for a in reversed(z['rows']):
        ev = (ev + a['flow']) / (1 + z['r'])
    assert abs(ev - z['values'][0]['EV']) < 1e-09
    for a in z['rows']:
        assert abs(a['E'] - (sum(a['op']) - a['hq'] - a['restruct'])) < 1e-09
        assert a['cash'] >= a['mincash']