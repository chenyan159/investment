import json, math, copy
from pathlib import Path
P0 = 175.89
K = [1, 3, 7, 12, 15]
S0 = 187.951918 + 8.3 + 3.1 + 1.7
C0 = 0.764258 + 1.7 * 2.34 / 1000 - 0.25 - 0.01
PROBS = [0.25, 0.45, 0.23, 0.07]
D = {'D': dict(A=[1.65, 1.45, 1.1, 0.8, 0.65], O=[0.3, 0.55, 0.65, 0.55, 0.45], L=[0.12, 0.15, 0.16, 0.13, 0.1], N=[0, 0.03, 0.1, 0.08, 0.06], ma=[0.46, 0.42, 0.36, 0.32, 0.3], mo=[0.25, 0.3, 0.3, 0.27, 0.25], ml=[0.35] * 5, mn=[0.2] * 5, central=[0.12, 0.13, 0.13, 0.12, 0.11], research=[0.08, 0.06, 0.04, 0.03, 0.025], sbc=[0.06, 0.07, 0.08, 0.08, 0.08], nwc=0.28, earn=0, g=-0.03), 'B': dict(A=[2.05, 2.65, 3.2, 3.0, 2.7], O=[0.85, 1.65, 2.5, 3.0, 3.1], L=[0.16, 0.24, 0.35, 0.4, 0.4], N=[0.01, 0.15, 0.65, 1.1, 1.2], ma=[0.55, 0.54, 0.5, 0.46, 0.44], mo=[0.4, 0.44, 0.44, 0.4, 0.38], ml=[0.4] * 5, mn=[0.4] * 5, central=[0.13, 0.16, 0.23, 0.27, 0.28], research=[0.09, 0.11, 0.14, 0.16, 0.16], sbc=[0.06, 0.07, 0.08, 0.08, 0.08], nwc=0.23, earn=1.6, g=0.01), 'U': dict(A=[2.3, 3.5, 4.7, 5.0, 4.6], O=[1.15, 2.9, 5.2, 7.0, 7.5], L=[0.18, 0.3, 0.45, 0.55, 0.6], N=[0.02, 0.4, 1.8, 3.0, 3.5], ma=[0.56, 0.56, 0.53, 0.49, 0.47], mo=[0.44, 0.48, 0.48, 0.44, 0.42], ml=[0.43] * 5, mn=[0.45] * 5, central=[0.14, 0.2, 0.32, 0.44, 0.48], research=[0.11, 0.16, 0.24, 0.32, 0.35], sbc=[0.06, 0.07, 0.08, 0.08, 0.08], nwc=0.23, earn=3.21, g=0.02), 'X': dict(A=[2.3, 3.7, 5.5, 6.0, 5.5], O=[1.2, 3.5, 8.0, 11.0, 12.0], L=[0.18, 0.32, 0.6, 0.8, 0.9], N=[0.03, 0.7, 5.0, 9.0, 11.0], ma=[0.56, 0.57, 0.54, 0.5, 0.48], mo=[0.44, 0.5, 0.51, 0.47, 0.44], ml=[0.43] * 5, mn=[0.46, 0.5, 0.55, 0.52, 0.48], central=[0.15, 0.25, 0.55, 0.85, 1.0], research=[0.14, 0.24, 0.5, 0.75, 0.85], sbc=[0.07, 0.08, 0.09, 0.09, 0.09], nwc=0.25, earn=3.21, g=0.025)}

def interp(a, y):
    if y <= 1:
        return a[0]
    for i in range(1, len(K)):
        if y <= K[i]:
            f = (y - K[i - 1]) / (K[i] - K[i - 1])
            return a[i - 1] * (1 - f) + a[i] * f
    return a[-1]

def calc(d, r=0.125, g=None):
    if g is None:
        g = d['g']
    s = S0 + d['earn']
    c = C0
    oldn = 0.6
    oldm = 0.25
    rows = []
    for y in range(1, 16):
        a = {k: interp(v, y) for k, v in d.items() if isinstance(v, list)}
        rev = sum((a[k] for k in ['A', 'O', 'L', 'N']))
        pools = [a[k] * a['m' + k.lower()] for k in ['A', 'O', 'L', 'N']]
        ebit = sum(pools) - a['central'] - a['research'] - rev * a['sbc']
        tax = 0.15 if y <= 3 else 0.2
        nopat = ebit - max(ebit, 0) * tax
        nw = d['nwc'] * rev + 0.1024
        mc = 0.08 * rev
        capex = 0.03 * rev
        da = 0.01 * rev
        fcf = nopat + da - capex - (nw - oldn) - (mc - oldm)
        if d.get('damagecost', 0) and y == 1:
            fcf -= d['damagecost']
        c = c * 1.04 + fcf
        rows.append(dict(y=y, **a, R=rev, pools=pools, E=ebit, T=max(ebit, 0) * tax, F=fcf, C=c, NWC=nw, MC=mc, capex=capex, da=da, S=s))
        oldn = nw
        oldm = mc
    last = rows[-1]
    tf = last['E'] * 0.8 * (1 + g) - 0.02 * last['R'] * (1 + g) - (d['nwc'] + 0.08) * last['R'] * g
    tv = tf / (r - g)
    values = {}
    for t in [0, 1, 3, 7]:
        ev = sum((z['F'] / (1 + r) ** (z['y'] - t) for z in rows if z['y'] > t)) + tv / (1 + r) ** (15 - t)
        cash = C0 if t == 0 else rows[t - 1]['C']
        eq = ev + cash
        v = eq * 1000 / s
        values[t] = dict(EV=ev, C=cash, EQ=eq, V=v, ret=v / P0 - 1, ann=(v / P0) ** (1 / t) - 1 if t else None)
    return dict(rows=rows, v=values, tv=tv, tvshare=tv / (1 + r) ** 15 / values[0]['EV'], after7=(sum((z['F'] / (1 + r) ** z['y'] for z in rows if z['y'] > 7)) + tv / (1 + r) ** 15) / values[0]['EV'])

def build():
    out = {}
    for name, d in D.items():
        out[name] = calc(d)
        out[name]['low'] = calc(d, 0.145, d['g'] - 0.01)['v']
        out[name]['high'] = calc(d, 0.105, min(0.03, d['g'] + 0.01))['v']
    return out
D['D']['damagecost'] = 0.12
if __name__ == '__main__':
    out = build()
    pass
    for k, z in out.items():
        print(k, 'today', round(z['v'][0]['V'], 2), 'terminal share', round(z['tvshare'], 3), 'after7', round(z['after7'], 3))
        for t in [1, 3, 7]:
            v = z['v'][t]
            print(t, {q: round(v[q], 3) for q in ['V', 'EQ', 'C', 'ret', 'ann']}, 'range', round(z['low'][t]['V'], 2), round(z['high'][t]['V'], 2))
        print('minimum cash', round(min((x['C'] for x in z['rows'])), 3))
    print('Expected values', {t: sum((PROBS[i] * out[k]['v'][t]['V'] for i, k in enumerate(D))) for t in [0, 1, 3, 7]})