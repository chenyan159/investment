import json, math, copy
from pathlib import Path
PRICE = 349.54
N0 = 12.23
KEYS = ['搜索', 'YouTube广告', 'Network', '订阅平台设备', 'Cloud服务', 'TPU外销', 'Waymo']
ANCH = [1, 3, 7, 15]
PARAM = {'悲观': dict(p=0.25, r=0.1, g=0.01, roic=0.1, rev=[[270, 48, 26, 58, 105, 25, 1.2], [260, 52, 20, 65, 140, 25, 2], [240, 60, 12, 78, 180, 20, 4], [200, 65, 5, 90, 220, 15, 3]], mar=[[0.42, 0.25, 0.1, 0.2, 0.25, 0.15, -1], [0.36, 0.24, 0.07, 0.2, 0.23, 0.12, -0.5], [0.32, 0.25, 0.05, 0.21, 0.24, 0.1, 0], [0.3, 0.25, 0.03, 0.22, 0.25, 0.08, 0]], common=[32, 34, 32, 30], other=[4, 3, 2, 1], cap=[225, 180, 125, 135], dep=[53, 90, 90, 100], nwc=0.09, inv=[115, 110, 115, 130], extra=[20, 15, 5, 0], rate=0.065), '基准': dict(p=0.45, r=0.095, g=0.025, roic=0.15, rev=[[290, 51, 28, 62, 120, 35, 2], [350, 65, 25, 85, 195, 55, 6], [460, 95, 20, 135, 340, 80, 22], [600, 135, 12, 210, 540, 105, 48]], mar=[[0.46, 0.28, 0.12, 0.23, 0.31, 0.2, -1], [0.46, 0.3, 0.1, 0.25, 0.32, 0.19, -0.35], [0.45, 0.32, 0.08, 0.28, 0.34, 0.17, 0.12], [0.43, 0.32, 0.06, 0.29, 0.34, 0.15, 0.16]], common=[32, 43, 60, 85], other=[4, 4, 4, 4], cap=[245, 255, 260, 315], dep=[55, 100, 165, 250], nwc=0.07, inv=[180, 195, 225, 280], extra=[7, 5, 2, 0], rate=0.055), '乐观': dict(p=0.23, r=0.095, g=0.03, roic=0.18, rev=[[300, 53, 28, 65, 130, 40, 2], [385, 72, 27, 100, 225, 70, 8], [570, 115, 23, 175, 450, 120, 38], [810, 180, 16, 300, 820, 165, 95]], mar=[[0.47, 0.29, 0.12, 0.24, 0.33, 0.22, -1], [0.48, 0.32, 0.11, 0.28, 0.35, 0.22, -0.2], [0.48, 0.34, 0.1, 0.31, 0.37, 0.2, 0.17], [0.45, 0.34, 0.08, 0.32, 0.36, 0.17, 0.2]], common=[34, 49, 78, 120], other=[4, 5, 6, 8], cap=[260, 285, 335, 470], dep=[56, 108, 210, 375], nwc=0.065, inv=[200, 235, 310, 470], extra=[7, 5, 2, 0], rate=0.0525), '突破': dict(p=0.07, r=0.1, g=0.03, roic=0.2, rev=[[300, 53, 28, 65, 135, 45, 2], [390, 74, 26, 110, 290, 90, 10], [620, 125, 22, 220, 700, 180, 55], [980, 225, 14, 410, 1400, 240, 150]], mar=[[0.47, 0.29, 0.12, 0.24, 0.33, 0.22, -1], [0.49, 0.33, 0.11, 0.29, 0.37, 0.24, -0.1], [0.49, 0.35, 0.09, 0.34, 0.4, 0.23, 0.2], [0.45, 0.35, 0.07, 0.34, 0.38, 0.19, 0.22]], common=[37, 65, 125, 210], other=[5, 7, 10, 15], cap=[280, 365, 495, 750], dep=[58, 130, 300, 630], nwc=0.065, inv=[210, 250, 360, 550], extra=[8, 7, 3, 0], rate=0.0575)}

def interp(a, t):
    if t <= 1:
        return a[0]
    for i in range(1, len(ANCH)):
        if t <= ANCH[i]:
            z = (t - ANCH[i - 1]) / (ANCH[i] - ANCH[i - 1])
            if isinstance(a[0], list):
                return [x + (y - x) * z for x, y in zip(a[i - 1], a[i])]
            return a[i - 1] + (a[i] - a[i - 1]) * z
    return a[-1]

def run(name, override=None, dr=0, dg=0):
    q = copy.deepcopy(PARAM[name])
    q.update(override or {})
    cash, debt, shares, inv = (120.0, 101.1, N0, 175.0)
    out = []
    cumulative = 0.0
    sold = 0.0
    prevrev = 495.0
    for t in range(1, 16):
        rev = interp(q['rev'], t)
        mar = interp(q['mar'], t)
        profit = [a * b for a, b in zip(rev, mar)]
        common, other = (interp(q['common'], t), interp(q['other'], t))
        ebit = sum(profit) - common - other
        attributable = ebit - 0.3 * profit[-1]
        total = sum(rev)
        da = interp(q['dep'], t)
        cap = interp(q['cap'], t)
        minimum = 40 + 0.02 * max(total - 495, 0)
        oldminimum = 40 + 0.02 * max(prevrev - 495, 0)
        dminimum = minimum - oldminimum
        dnwc = q['nwc'] * (total - prevrev) + dminimum
        extra = interp(q['extra'], t) if t <= 7 else 0
        if name == '悲观' and t == 2:
            extra += 20
        wprev = interp(q['rev'], max(t - 1, 1))[-1] if t > 1 else 1.0
        wda = rev[-1] * 0.15
        wcap = rev[-1] * 0.4
        wnw = 0.03 * (rev[-1] - wprev)
        wfcf = profit[-1] * 0.8 + wda - wcap - wnw
        groupfcf = ebit * 0.8 + da - cap - dnwc - extra
        fcf = groupfcf - 0.3 * wfcf
        interest = debt * q['rate'] * 0.8
        pref = 1.203125 if t < 3 else 1.203125 * 8 / 12 if t == 3 else 0.0
        if t == 3:
            shares += 0.05445825
        div = 0.88 * 1.05 ** (t - 1)
        if name == '悲观' and t >= 2:
            div = 0.44
        cash += fcf + dminimum - interest + max(cash - oldminimum, 0) * 0.03 - pref - div * shares
        borrowing = issuance = sale = repay = 0.0
        inv = interp(q['inv'], t) - sold
        if cash < minimum:
            borrowing = min(minimum - cash, max(0, 1.5 * (max(attributable, 0) + da) - debt))
            cash += borrowing
            debt += borrowing
        if cash < minimum:
            sale = min(minimum - cash, max(inv, 0) * 0.5)
            cash += sale
            inv -= sale
            sold += sale
        if cash < minimum:
            issuance = minimum - cash
            issueprice = PRICE * 0.6 * (total / 495) ** 0.5
            shares += issuance / issueprice
            cash += issuance
        if cash > minimum + 50 and debt > 20:
            repay = min(cash - minimum - 50, debt - 20)
            cash -= repay
            debt -= repay
        cumulative += div
        out.append(dict(t=t, rev=total, byrev=rev, byprofit=profit, ebit=ebit, attr=attributable, da=da, cap=cap, dnwc=dnwc, extra=extra, fcf=fcf, groupfcf=groupfcf, wfcf=wfcf, cash=cash, debt=debt, shares=shares, inv=inv, div=div, cumdiv=cumulative, borrow=borrowing, issue=issuance, sale=sale, repay=repay, interest=interest, pref=pref, minimum=minimum))
        prevrev = total
    r = q['r'] + dr
    g = q['g'] + dg
    terminal = out[-1]['attr'] * 0.8 * (1 + g) * (1 - g / q['roic']) / (r - g)
    vals = {}
    for h in [0, 1, 3, 7]:
        ev = sum((x['fcf'] / (1 + r) ** (x['t'] - h) for x in out if x['t'] > h)) + terminal / (1 + r) ** (15 - h)
        z = out[h - 1] if h else dict(cash=120, debt=101.1, shares=N0, inv=175, minimum=40, cumdiv=0)
        n = z['shares'] + (0.05445825 if h < 3 else 0)
        prefreserve = sum((x['pref'] / (1 + r) ** (x['t'] - h) for x in out if x['t'] > h))
        eq = ev + z['cash'] - z['minimum'] + z['inv'] - z['debt'] - prefreserve
        v = eq / n
        wealth = v + z['cumdiv']
        ret = wealth / PRICE - 1
        vals[h] = dict(ev=ev, eq=eq, n=n, v=v, dist=z['cumdiv'], ret=ret, annual=(wealth / PRICE) ** (1 / h) - 1 if h else None, terminal_share=terminal / (1 + r) ** (15 - h) / ev)
    return dict(rows=out, values=vals, terminal=terminal)

def all_results():
    result = {}
    for name in PARAM:
        z = run(name)
        lo = run(name, dr=0.01, dg=-0.005)
        hi = run(name, dr=-0.01, dg=0.005)
        for h in z['values']:
            z['values'][h]['low'] = lo['values'][h]['v']
            z['values'][h]['high'] = hi['values'][h]['v']
        result[name] = z
    return result
if __name__ == '__main__':
    d = all_results()
    pass
    for name, z in d.items():
        print(name)
        for h, v in z['values'].items():
            print(h, {k: round(x, 2) for k, x in v.items() if x is not None})
        print('finance', [(x['t'], round(x['fcf'], 1), round(x['cash'], 1), round(x['debt'], 1), round(x['issue'], 1)) for x in z['rows'][:7]])
    for h in [0, 1, 3, 7]:
        wealth = sum((PARAM[n]['p'] * (z['values'][h]['v'] + z['values'][h]['dist']) for n, z in d.items()))
        print('E', h, wealth, 'CAGR', (wealth / PRICE) ** (1 / h) - 1 if h else 0)
for n, z in all_results().items():
    p = z['terminal']
    for x in reversed(z['rows']):
        p = (p + x['fcf']) / (1 + PARAM[n]['r'])
    assert abs(p - z['values'][0]['ev']) < 1e-08