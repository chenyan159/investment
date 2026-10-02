import json, math, copy
from pathlib import Path
P = 1791.82
N0 = 155.0
X0 = 4.762 - 2.476 - 3.0
A = 1.33
YEARS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def interp(v):
    ks = [1, 3, 7, 12]
    out = []
    for t in YEARS:
        for j in range(3):
            if ks[j] <= t <= ks[j + 1]:
                out.append(v[j] + (v[j + 1] - v[j]) * (t - ks[j]) / (ks[j + 1] - ks[j]))
                break
    return out
spec = {'受损': dict(D=[12, 14, 15, 16], E=[21, 16, 12, 11], C=[2.2, 2, 2, 2], md=[0.72, 0.48, 0.3, 0.25], me=[0.73, 0.4, 0.2, 0.18], mc=[0.4, 0.25, 0.2, 0.18], O=[2.6, 2.8, 3.0, 3.2], H=[0] * 12, hp=[-0.2, -0.2, -0.1] + [0] * 9, cap=0.065, g=0.0, roic=0.1), '基准': dict(D=[19, 29, 40, 46], E=[24, 25, 22, 22], C=[2.5, 2.7, 3, 3.2], md=[0.83, 0.78, 0.56, 0.43], me=[0.83, 0.73, 0.4, 0.3], mc=[0.5, 0.45, 0.32, 0.27], O=[2.7, 3.3, 4.4, 5.2], H=[0, 0, 0.2, 0.5, 0.8, 1.1, 1.5, 1.8, 2, 2.1, 2.2, 2.3], hp=[-0.3, -0.4, -0.4, -0.25, -0.1, 0, 0.15, 0.25, 0.32, 0.35, 0.38, 0.4], cap=0.06, g=0.02, roic=0.15), '乐观': dict(D=[22, 39, 68, 90], E=[25, 29, 35, 38], C=[2.7, 3, 3.8, 4.3], md=[0.85, 0.82, 0.73, 0.6], me=[0.85, 0.79, 0.65, 0.48], mc=[0.55, 0.52, 0.44, 0.35], O=[2.8, 3.6, 5.6, 7.2], H=[0, 0, 0.2, 0.5, 0.8, 1.1, 1.5, 1.8, 2, 2.1, 2.2, 2.3], hp=[-0.3, -0.4, -0.4, -0.25, -0.1, 0, 0.15, 0.25, 0.32, 0.35, 0.38, 0.4], cap=0.06, g=0.025, roic=0.2)}
spec['突破'] = copy.deepcopy(spec['基准'])
spec['突破'].update(largeH=True, H=[0, 0.1, 1.0, 3.5, 8, 13, 20, 24, 27, 29, 30, 31], hp=[-0.5, -0.7, -0.6, 0.1, 1.6, 3.6, 6.4, 8.2, 9.5, 10.2, 10.5, 10.8])

def build(s):
    a = {k: interp(s[k]) for k in ['D', 'E', 'C', 'md', 'me', 'mc', 'O']}
    rows = []
    prev = 5.4
    for i, t in enumerate(YEARS):
        cann = 0.1 * s['H'][i] if s.get('largeH', False) else 0
        d = a['D'][i] - cann
        rev = d + a['E'][i] + a['C'][i] + s['H'][i]
        parts = [d * a['md'][i], a['E'][i] * a['me'][i], a['C'][i] * a['mc'][i], s['hp'][i], -a['O'][i]]
        ebit = sum(parts)
        tax = min(0.21, 0.16 + 0.01 * t)
        nwc = 0.15 * rev
        dn = nwc - prev
        prev = nwc
        hc = [0.3, 0.6, 0.8, 1, 1.3, 1.5, 1.8, 1.8, 1.8, 1.7, 1.6, 1.6][i] if s.get('largeH', False) else 0.1
        cap = s['cap'] * rev + hc
        da = 0.2 + 0.025 * i
        catch = 1.544 if t == 1 else 0
        fcf = ebit * (1 - tax) + da - cap - dn - catch
        rows.append(dict(t=t, D=d, E=a['E'][i], C=a['C'][i], H=s['H'][i], R=rev, parts=parts, EBIT=ebit, tax=tax, DA=da, cap=cap, dNWC=dn, catch=catch, FCF=fcf))
    return rows

def calc(name, r=0.115, gshift=0, variant=None, buy_mult=1, renew=True):
    s = copy.deepcopy(spec[name])
    rows = build(s)
    if variant:
        for z in rows:
            variant(z)
    g = s['g'] + gshift
    term = rows[-1]['EBIT'] * (1 - 0.21) * (1 + g) * (1 - g / s['roic']) / (r - g)

    def ev(t):
        return sum((z['FCF'] / (1 + r) ** (z['t'] - t) for z in rows if z['t'] > t)) + term / (1 + r) ** (12 - t)
    cash = X0
    n = N0
    out = {0: dict(EV=ev(0), EQ=ev(0) + cash + A, N=n, V=(ev(0) + cash + A) * 1000 / n, X=cash, dist=0)}
    for z in rows:
        t = z['t']
        cash += max(cash, 0) * 0.03 + z['FCF']
        b = min(([2, 0] if name == '受损' else [8, 7.5])[t - 1], max(cash, 0)) if t <= 2 else max(z['FCF'], 0) * (0.4 if name == '受损' else 0.8) if renew else 0
        bp = (P * 1.04 ** t if t <= 2 else (ev(t) + cash + A) * 1000 / n) * buy_mult
        cash -= b
        n -= b * 1000 / bp
        assert cash >= -1e-08
        eq = ev(t) + cash + A
        out[t] = dict(EV=ev(t), EQ=eq, N=n, V=eq * 1000 / n, X=cash, buy=b, dist=0, ret=eq * 1000 / n / P - 1, cagr=(eq * 1000 / n / P) ** (1 / t) - 1)
    return (rows, out, term)

def values():
    ans = {}
    for name in spec:
        rows, o, term = calc(name)
        lo = calc(name, 0.135, -0.01)[1]
        hi = calc(name, 0.1, 0.01)[1]
        ans[name] = dict(rows=rows, points={str(t): dict(o[t], low=lo[t]['V'], high=hi[t]['V']) for t in [0, 1, 3, 7]}, terminal_share=term / 1.115 ** 12 / o[0]['EV'])
    return ans
for name in spec:
    rows, points, terminal = calc(name)
    print(name, {t: points[t] for t in (0, 1, 3, 7)})