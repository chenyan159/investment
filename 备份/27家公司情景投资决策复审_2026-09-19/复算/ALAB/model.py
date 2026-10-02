from pathlib import Path
import json, math, copy
PRICE = 303.25
N0 = (173.485104 + 1.693 + 9.18 + 0.375) / 1000
X0 = 1.252958 - 0.35
K = 0.115
NODES = [1, 3, 7, 10, 14]
P = [0.25, 0.45, 0.23, 0.07]
CFG = {'受损': dict(rev=[[0.8, 0.85, 0.025, 0], [0.65, 0.65, 0.025, 0.005], [0.5, 0.55, 0.025, 0.025], [0.42, 0.42, 0.02, 0.02], [0.35, 0.3, 0.015, 0.015]], gm0=[0.65, 0.63, 0.5, 0.35], gm14=[0.58, 0.55, 0.48, 0.35], rdv=[0.15, 0.2, 0.35, 0.3], fixed=[0.09, 0.12, 0.045, 0.06], fg=-0.08, w=2.316175, g=-0.02, roic=0.15), '基准': dict(rev=[[1.1, 1.3, 0.08, 0.02], [1.35, 2.7, 0.3, 0.2], [1.55, 5.0, 0.85, 1.2], [1.5, 6.0, 1.1, 1.6], [1.4, 6.5, 1.3, 1.8]], gm0=[0.72, 0.71, 0.65, 0.45], gm14=[0.64, 0.65, 0.61, 0.54], rdv=[0.14, 0.18, 0.25, 0.22], fixed=[0.09, 0.1, 0.04, 0.09], fg=0.04, w=5.578474, g=0.025, roic=0.25), '乐观': dict(rev=[[1.2, 1.55, 0.1, 0.05], [1.6, 3.65, 0.45, 0.4], [2.0, 7.5, 1.3, 2.2], [2.1, 9.5, 1.7, 3.2], [2.1, 11.0, 2.0, 4.0]], gm0=[0.73, 0.73, 0.66, 0.48], gm14=[0.66, 0.68, 0.64, 0.57], rdv=[0.14, 0.17, 0.24, 0.21], fixed=[0.1, 0.12, 0.05, 0.11], fg=0.06, w=5.578474, g=0.03, roic=0.28), '突破': dict(rev=[[1.2, 1.65, 0.12, 0.03], [1.6, 4.8, 0.7, 0.9], [1.9, 12.0, 2.0, 5.0], [1.8, 16.0, 3.0, 8.0], [1.6, 20.0, 4.0, 11.0]], gm0=[0.73, 0.74, 0.66, 0.46], gm14=[0.64, 0.68, 0.63, 0.58], rdv=[0.15, 0.18, 0.24, 0.22], fixed=[0.11, 0.16, 0.07, 0.17], fg=0.08, w=5.578474, g=0.03, roic=0.25)}

def interp(y, nodes):
    if y <= 1:
        return list(nodes[0])
    for j in range(1, len(NODES)):
        if y <= NODES[j]:
            f = (y - NODES[j - 1]) / (NODES[j] - NODES[j - 1])
            return [a + (b - a) * f for a, b in zip(nodes[j - 1], nodes[j])]
    raise ValueError(y)

def model(c, k=K, gdelta=0, gmshift=0, scale=1, delay=False):
    n = N0 + c['w'] / 1000
    rows = []
    cash = X0
    prior = 1.75
    for y in range(1, 15):
        rr = [v * scale for v in interp(max(1, y - 1) if delay else y, c['rev'])]
        gm = [a + (b - a) * (y - 1) / 13 + gmshift for a, b in zip(c['gm0'], c['gm14'])]
        rd = [rr[i] * c['rdv'][i] + c['fixed'][i] * (1 + c['fg']) ** (y - 1) for i in range(4)]
        contribution = [rr[i] * gm[i] - rd[i] for i in range(4)]
        rev = sum(rr)
        shared = 0.07 * rev + 0.05 * 1.03 ** (y - 1)
        ebit = sum(contribution) - shared
        taxrate = [0.15, 0.18, 0.2][y - 1] if y <= 3 else 0.21
        tax = max(ebit, 0) * taxrate
        da = 0.02 * rev
        capex = 0.05 * rev
        dnwc = 0.12 * (rev - prior)
        dreserve = 0.02 * (rev - prior)
        legacy = [0.32, 0.22, 0.06][y - 1] if y <= 3 else 0
        fcff = ebit - tax + da - capex - dnwc - dreserve + legacy
        startcash = cash
        cash = cash * 1.03 + fcff
        rows.append(dict(y=y, rr=rr, rev=rev, gm=gm, rd=rd, contribution=contribution, shared=shared, ebit=ebit, tax=tax, da=da, capex=capex, dnwc=dnwc, dreserve=dreserve, legacy=legacy, fcff=fcff, cash=cash, startcash=startcash))
        prior = rev
    g = c['g'] + gdelta
    terminal = rows[-1]['ebit'] * (1 + g) * 0.79 * (1 - max(g, 0) / c['roic']) / (k - g)
    values = {}
    for t in [0, 1, 3, 7]:
        pv = sum((x['fcff'] / (1 + k) ** (x['y'] - t) for x in rows if x['y'] > t))
        tv = terminal / (1 + k) ** (14 - t)
        cx = X0 if t == 0 else rows[t - 1]['cash']
        eq = pv + tv + cx
        values[t] = dict(ev=pv + tv, equity=eq, price=eq / n, cash=cx, shares=n, tvshare=tv / eq, total=eq / n / PRICE - 1, cagr=(eq / n / PRICE) ** (1 / t) - 1 if t else None)
    return dict(rows=rows, values=values, n=n, terminal=terminal)

def results():
    out = {}
    for name, c in CFG.items():
        m = model(c)
        low = model(c, k=K + 0.02, gdelta=-0.01)
        high = model(c, k=K - 0.02, gdelta=0.01)
        m['range'] = {t: [low['values'][t]['price'], high['values'][t]['price']] for t in [0, 1, 3, 7]}
        out[name] = m
    return out

def expectations(out, weights=P):
    return {t: sum((p * out[n]['values'][t]['price'] for p, n in zip(weights, CFG))) for t in [0, 1, 3, 7]}
if __name__ == '__main__':
    out = results()
    for name, m in out.items():
        print(name, 'VALUE', {t: round(v['price'], 2) for t, v in m['values'].items()}, 'RANGE', {t: [round(x, 2) for x in v] for t, v in m['range'].items()})
        print('NODE', [(x['y'], round(x['rev'], 3), round(x['ebit'], 3), round(x['fcff'], 3), round(x['cash'], 3)) for x in m['rows'] if x['y'] in NODES])
    print('WEIGHTED', expectations(out))
    pass