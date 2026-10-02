import json, math, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent
P0 = 248.92
SH = 0.395
TAX = 0.22
CASH0 = 5.639
MINCASH = 2.0
KNOTS = [0, 1, 3, 7, 10, 15]
START = [11.5, 7.38, 6.45, 0.5, 0.77]
MSTART = [0.49, 0.45, 0.25, -0.4, 0.1]
DATA = {'P': {'p': 0.25, 'g': -0.02, 'rev': [[11, 7.9, 6.8, 0.7, 0.7], [9.8, 8.4, 7, 0.9, 0.55], [7.8, 8.5, 7.2, 1.2, 0.35], [6.8, 8.2, 7, 1.25, 0.25], [5.5, 7.8, 6.7, 1.2, 0.15]], 'mar': [[0.44, 0.43, 0.23, -0.35, 0.08], [0.38, 0.4, 0.2, -0.15, 0.05], [0.32, 0.37, 0.18, 0.05, 0], [0.29, 0.35, 0.17, 0.08, 0], [0.26, 0.33, 0.16, 0.08, 0]], 'central': [1.1, 1.08, 1.0, 0.95, 0.9]}, 'B': {'p': 0.5, 'g': 0.02, 'rev': [[12, 8.4, 7.1, 0.9, 0.7], [12.9, 10.6, 8.6, 2, 0.58], [14.4, 14.8, 11.5, 4.5, 0.4], [14.8, 17, 13.4, 5.7, 0.3], [15.2, 20, 16, 7, 0.2]], 'mar': [[0.49, 0.46, 0.26, -0.2, 0.1], [0.48, 0.47, 0.28, 0.1, 0.09], [0.46, 0.47, 0.3, 0.24, 0.07], [0.44, 0.46, 0.3, 0.27, 0.05], [0.42, 0.44, 0.29, 0.28, 0.02]], 'central': [1.1, 1.25, 1.6, 1.8, 2.1]}, 'O': {'p': 0.2, 'g': 0.025, 'rev': [[12.3, 8.6, 7.3, 1.1, 0.7], [14.2, 11.5, 9.5, 3, 0.6], [17.5, 17, 14, 8, 0.4], [19, 20, 17, 11, 0.3], [21, 24, 21, 15, 0.2]], 'mar': [[0.5, 0.47, 0.27, -0.12, 0.1], [0.51, 0.49, 0.31, 0.2, 0.1], [0.5, 0.5, 0.33, 0.32, 0.08], [0.48, 0.49, 0.33, 0.34, 0.05], [0.46, 0.47, 0.32, 0.34, 0.02]], 'central': [1.12, 1.35, 1.95, 2.35, 2.9]}, 'X': {'p': 0.05, 'g': 0.03, 'rev': [[12.2, 8.6, 7.3, 1.2, 0.7], [13.8, 11.3, 9.5, 4.5, 0.6], [17, 16.5, 14, 15, 0.4], [18.5, 19.5, 17, 23, 0.3], [20, 24, 22, 33, 0.2]], 'mar': [[0.49, 0.46, 0.26, -0.25, 0.1], [0.49, 0.48, 0.3, 0.2, 0.09], [0.48, 0.49, 0.32, 0.36, 0.06], [0.46, 0.48, 0.33, 0.38, 0.04], [0.43, 0.46, 0.32, 0.37, 0.02]], 'central': [1.15, 1.55, 2.7, 3.4, 4.5]}}

def interp(vals, t):
    for j in range(1, len(KNOTS)):
        if t <= KNOTS[j]:
            w = (t - KNOTS[j - 1]) / (KNOTS[j] - KNOTS[j - 1])
            a, b = (vals[j - 1], vals[j])
            if isinstance(a, list):
                return [x + (y - x) * w for x, y in zip(a, b)]
            return a + (b - a) * w

def model(d, r=0.11, g=None, acq=1.0, margin_shift=0.0, revscale=1.0, ai_override=None):
    pay = {1: 1.6, 2: 0.8, 3: 0.75, 4: 2.0, 8: 0.75, 9: 0.5}
    debt = 6.4
    cash = CASH0
    rows = []
    prevR = sum(START)
    for t in range(1, 16):
        rev = interp([START] + d['rev'], t)
        mar = interp([MSTART] + d['mar'], t)
        if ai_override:
            rev[3] = interp([START] + ai_override['rev'], t)[3]
            mar[3] = interp([MSTART] + ai_override['mar'], t)[3]
        rev = [v * revscale for v in rev]
        mar = [m + margin_shift for m in mar]
        central = interp([1.0] + d['central'], t)
        if ai_override:
            central += max(0, interp([1.0] + ai_override['central'], t) - interp([1.0] + DATA['B']['central'], t))
        unit = [a * b for a, b in zip(rev, mar)]
        R = sum(rev)
        ebit = sum(unit) - central
        nopat = ebit * (1 - TAX)
        da = 0.025 * R
        net_fixed = 0.4 * (7 - t) / 6 if t <= 7 else -0.05 * nopat * (t - 7) / 8
        capex = da - net_fixed
        nwc = 0.01 * (R - prevR)
        fcff = nopat + da - capex - nwc
        principal = pay.get(t, 0)
        interest = 0.042 * max(0, debt - principal / 2)
        fcfe = fcff - interest * (1 - TAX) - principal - (acq if t == 1 else 0)
        debt -= principal
        cash = cash + max(0, cash - MINCASH) * 0.03 + fcfe
        rows.append(dict(t=t, rev=rev, mar=mar, unit=unit, central=central, R=R, ebit=ebit, nopat=nopat, da=da, capex=capex, nwc=nwc, fcff=fcff, interest=interest, principal=principal, fcfe=fcfe, cash=cash, debt=debt))
        prevR = R
    if g is None:
        g = d['g']
    terminal = rows[-1]['nopat'] * 0.95 * (1 + g) / (r - g)
    vals = {}
    tvshare = {}
    for h in [0, 1, 3, 7]:
        pv = sum((x['fcfe'] / (1 + r) ** (x['t'] - h) for x in rows if x['t'] > h))
        tv = terminal / (1 + r) ** (15 - h)
        excess = (CASH0 if h == 0 else rows[h - 1]['cash']) - MINCASH
        equity = pv + tv + excess
        vals[h] = dict(equity=equity, price=equity / SH, ret=equity / SH / P0 - 1, cagr=(equity / SH / P0) ** (1 / h) - 1 if h else None, remaining=pv + tv, excess=excess)
        tvshare[h] = tv / equity
    return dict(rows=rows, vals=vals, tvshare=tvshare)

def capital(m, d, r=0.11, g=None, fraction=0.6, buy_multiple=1.0):
    if g is None:
        g = d['g']
    cash = CASH0
    shares = SH
    out = {}
    series = []
    tv = m['rows'][-1]['nopat'] * 0.95 * (1 + g) / (r - g)
    for z in m['rows']:
        t = z['t']
        cash += max(0, cash - MINCASH) * 0.03 + z['fcfe']
        rem = sum((x['fcfe'] / (1 + r) ** (x['t'] - t) for x in m['rows'] if x['t'] > t)) + tv / (1 + r) ** (15 - t)
        before = rem + cash - MINCASH
        bb = min(max(0, z['fcfe']) * fraction, max(0, cash - MINCASH))
        px = before / shares * buy_multiple
        shares -= bb / px
        cash -= bb
        eq = rem + cash - MINCASH
        row = dict(t=t, buyback=bb, cash=cash, shares=shares, equity=eq, price=eq / shares, ret=eq / shares / P0 - 1, cagr=(eq / shares / P0) ** (1 / t) - 1, remaining=rem, debt=z['debt'])
        series.append(row)
        if t in [1, 3, 7]:
            out[t] = row
    return dict(vals=out, series=series)
for key, d in DATA.items():
    m = model(d)
    c = capital(m, d)
    print(key, m['vals'][0], c['vals'])