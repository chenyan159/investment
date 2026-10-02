import json, math
from pathlib import Path
P0 = 199.39
N0 = 1.261224648
C0 = 12.5433
R0 = 12.6
PROBS = [0.25, 0.45, 0.23, 0.07]
NAMES = ['受损', '基准', '乐观', '突破']
R = {'受损': [[7.5, 7.2, 7.3, 7.5, 7.7, 7.85, 8], [3.8, 3.3, 3.3, 3.4, 3.5, 3.5, 3.5], [1.4, 1.45, 1.55, 1.65, 1.75, 1.85, 2], [0, 0, 0, 0, 0, 0, 0]], '基准': [[8.7, 9.7, 10.7, 11.65, 12.6, 13.5, 14.4], [5, 6.7, 8.5, 10.2, 11.8, 13.4, 15], [1.65, 2.1, 2.65, 3.2, 3.8, 4.45, 5.1], [0, 0.05, 0.2, 0.4, 0.7, 1, 1.4]], '乐观': [[9, 10.3, 11.6, 13, 14.4, 15.8, 17.2], [5.8, 8.3, 11.4, 14.8, 18.2, 21.7, 25], [1.75, 2.3, 3, 3.8, 4.7, 5.7, 6.8], [0.02, 0.15, 0.6, 1.2, 2, 3, 4.2]], '突破': [[8.7, 9.7, 10.7, 11.65, 12.6, 13.5, 14.4], [5.8, 8.8, 13, 18, 24, 30, 36], [1.65, 2.1, 2.65, 3.2, 3.8, 4.45, 5.1], [0.05, 0.4, 1.5, 3.5, 6, 9, 12]]}
M = {'受损': [(0.42, 0.35), (0.36, 0.25), (0.2, 0.24), (0.35, 0.3)], '基准': [(0.47, 0.44), (0.46, 0.4), (0.25, 0.33), (0.4, 0.4)], '乐观': [(0.48, 0.46), (0.48, 0.44), (0.27, 0.36), (0.43, 0.44)], '突破': [(0.47, 0.44), (0.47, 0.43), (0.25, 0.33), (0.42, 0.43)]}
G8 = {'受损': 0.025, '基准': 0.09, '乐观': 0.12, '突破': 0.14}
GT = {'受损': 0.01, '基准': 0.03, '乐观': 0.035, '突破': 0.035}
MT = {'受损': [0.32, 0.23, 0.24, 0.3], '基准': [0.4, 0.35, 0.32, 0.35], '乐观': [0.42, 0.38, 0.34, 0.38], '突破': [0.4, 0.37, 0.32, 0.38]}
FIX = {'受损': (0.2, 0.05), '基准': (0.2, 0.28), '乐观': (0.22, 0.4), '突破': (0.3, 0.7)}
WC = {'受损': 0.2, '基准': 0.16, '乐观': 0.18, '突破': 0.22}
SHOCK = {'受损': {1: 3.0, 2: 1.0, 3: -1.0, 4: -1.0, 5: -0.5}, '基准': {1: 1.0, 2: 0.5, 3: -0.5, 4: -0.5, 5: -0.5}, '乐观': {1: 1.2, 2: 0.5, 3: -0.4, 4: -0.5, 5: -0.8}, '突破': {1: 1.5, 2: 1.0, 3: 0.5, 4: -0.5, 5: -0.5, 6: -1, 7: -1}}
LOSS = {'受损': {1: 0.8, 2: 0.4}, '基准': {}, '乐观': {}, '突破': {}}

def model(name, r=0.105, gshift=0, d=0.01, revscale=1, mdelta=0, ai_from=None, up_from=None, delay=False, late_ai=1, taxrate=0.2):
    rr = [list(x) for x in R[name]]
    if ai_from:
        rr[1] = list(R[ai_from][1])
    if up_from:
        rr[3] = list(R[up_from][3])
    rr[1] = [x * (1 + (late_ai - 1) * i / 6) for i, x in enumerate(rr[1])]
    wc = max(WC[name], 0.22) if ai_from or up_from else WC[name]
    fixed_pair = FIX[up_from] if up_from else FIX[name]
    if delay:
        rr[1] = [3.5] + rr[1][:-1]
        rr[3] = [0] + rr[3][:-1]
    seq = []
    prevR = R0
    cash = C0
    shares = N0
    g = GT[name] + gshift
    for t in range(1, 16):
        if t <= 7:
            rev = [x[t - 1] * revscale for x in rr]
            margins = [a + (b - a) * (t - 1) / 6 + mdelta for a, b in M[name]]
            fix = fixed_pair[0] + (fixed_pair[1] - fixed_pair[0]) * (t - 1) / 6
        else:
            growth = G8[name] + (g - G8[name]) * (t - 8) / 7
            rev = [x * (1 + growth) for x in seq[-1]['business_rev']]
            margins = [M[name][k][1] + (MT[name][k] - M[name][k][1]) * (t - 7) / 8 + mdelta for k in range(4)]
            fix = seq[-1]['fixed_up'] * (1 + growth)
        op = [rev[k] * margins[k] - (fix if k == 3 else 0) for k in range(4)]
        sales = sum(rev)
        operating = sum(op) - LOSS[name].get(t, 0)
        sbc = 0.04 * sales
        tax = taxrate * max(operating, 0)
        da = 0.007 * sales
        capex = 0.015 * sales + (0.12 if t == 1 else 0)
        dwc = wc * (sales - prevR) + SHOCK[name].get(t, 0)
        reserve = 0.12 * (sales - prevR)
        fcf = operating - tax + sbc + da - capex - dwc - reserve
        cash = cash * 1.03 + fcf
        shares *= 1 + d
        seq.append(dict(t=t, business_rev=rev, business_op=op, rev=sales, op=operating, sbc=sbc, tax=tax, da=da, capex=capex, dwc=dwc, reserve=reserve, fcf=fcf, cash=cash, shares=shares, fixed_up=fix))
        prevR = sales
    z = seq[-1]
    r16 = z['rev'] * (1 + g)
    op16 = z['op'] * (1 + g)
    f16 = op16 * (1 - taxrate) + 0.04 * r16 - 0.008 * r16 - (wc + 0.12) * (r16 - z['rev'])
    reff = (1 + r) * (1 + d) - 1
    terminal = f16 / (reff - g)
    out = {}
    for h in [0, 1, 3, 7]:
        nh = N0 * (1 + d) ** h
        rem = sum((x['fcf'] * (nh / x['shares']) / (1 + r) ** (x['t'] - h) for x in seq if x['t'] > h))
        tv = terminal * (nh / z['shares']) / (1 + r) ** (15 - h)
        ch = C0 if h == 0 else seq[h - 1]['cash']
        equity = ch + rem + tv
        price = equity / nh
        out[h] = dict(price=price, equity=equity, cash=ch, shares=nh, remaining=rem + tv, tv=tv, tv_pct=tv / (rem + tv), ret=price / P0 - 1, cagr=(price / P0) ** (1 / h) - 1 if h else None)
    return dict(seq=seq, values=out, terminal=terminal, f16=f16)

def weighted(results, probs=PROBS):
    return {h: sum((p * results[n]['values'][h]['price'] for p, n in zip(probs, NAMES))) for h in [0, 1, 3, 7]}
for n in NAMES:
    print(n, model(n)['values'])
print(weighted({n: model(n) for n in NAMES}))