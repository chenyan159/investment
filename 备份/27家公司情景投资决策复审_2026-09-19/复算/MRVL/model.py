"""MRVL independent research model. USD billions; shares billions; rolling Sep-19 years."""
import json, math
from copy import deepcopy
from pathlib import Path
NODES = [1, 2, 3, 5, 7, 10, 15]
CASES = {'悲观': dict(p=0.22, rev=[[3.5, 5.8, 3, 0.0], [3.3, 5.6, 2.9, 0.03], [4, 5.8, 2.8, 0.1], [5.5, 6.2, 2.7, 0.2], [6.2, 6.5, 2.6, 0.3], [6, 6.2, 2.5, 0.3], [5.2, 5.3, 2.3, 0.2]], gm=[0.38, 0.57, 0.54, 0.4], op=[3.1, 3.15, 3.2, 3.4, 3.5, 3.5, 3.3], dilution=0.018, nwc=0.25, capex=0.055, g=0, earn=0, google=[0.2, 0.4, 0.6, 1, 1.2, 1.2, 1.2], extra={1: 1.0, 2: 0.5}), '基准': dict(p=0.48, rev=[[4.6, 6.9, 3.2, 0.02], [6.7, 9.2, 3.3, 0.25], [9.2, 11.1, 3.4, 0.8], [13.8, 14.1, 3.6, 1.8], [17, 16, 3.8, 3.2], [22, 19, 4.1, 5.5], [28, 22, 4.5, 7]], gm=[0.44, 0.64, 0.58, 0.55], op=[3, 3.6, 4.2, 5.4, 6.5, 8.4, 11.5], dilution=0.012, nwc=0.2, capex=0.05, g=0.025, earn=1 / 3, google=[0.5, 1.2, 2.2, 4.2, 6.0, 7, 8], extra={}), '乐观': dict(p=0.23, rev=[[5.2, 7.8, 3.2, 0.05], [8.5, 11, 3.4, 0.5], [12.5, 14, 3.6, 1.4], [21, 19, 3.9, 3.5], [29, 23, 4.2, 6.5], [38, 27, 4.5, 10], [48, 32, 5, 14]], gm=[0.47, 0.66, 0.59, 0.59], op=[3.2, 4.1, 5.1, 7.2, 9.3, 12.5, 17], dilution=0.009, nwc=0.18, capex=0.055, g=0.03, earn=1 / 3, google=[0.7, 2, 4, 7.5, 11, 14, 16], extra={}), '突破': dict(p=0.07, rev=[[5.2, 7.8, 3.2, 0.1], [9, 11, 3.4, 1.2], [15, 14, 3.6, 3.5], [30, 21, 3.9, 8], [46, 27, 4.2, 14], [64, 34, 4.5, 23], [88, 42, 5, 35]], gm=[0.49, 0.65, 0.59, 0.63], op=[3.5, 4.6, 6.3, 10.2, 14.8, 22, 34], dilution=0.009, nwc=0.22, capex=0.065, g=0.03, earn=1, google=[0.7, 2.5, 5.5, 12, 22, 30, 40], extra={})}
S0 = 0.9212
CASH0 = 3.9328
DEBT0 = 4.9999
R0 = 11.8
PRICE = 244.25
R = 0.115
TAX = 0.16
CASHYIELD = 0.035
MATURITY = {2: 1.2499, 3: 0.5, 4: 0.5, 5: 0.75, 7: 0.5, 9: 0.5, 10: 1.0}

def interp(values, t):
    if t <= 1:
        return deepcopy(values[0])
    for i in range(1, len(NODES)):
        if t <= NODES[i]:
            q = (t - NODES[i - 1]) / (NODES[i] - NODES[i - 1])
            a = values[i - 1]
            b = values[i]
            return [x + (y - x) * q for x, y in zip(a, b)] if isinstance(a, list) else a + (b - a) * q
    return deepcopy(values[-1])

def run(c, r=R, g=None, margin_shift=0, delay=0, pf_override=None, retain=7, taxrate=TAX):
    c = deepcopy(c)
    g = c['g'] if g is None else g
    if pf_override is not None:
        c['rev'] = [a[:3] + [b[3]] for a, b in zip(c['rev'], pf_override['rev'])]
        c['op'] = [a + max(0, b[3] - old[3]) * 0.12 for a, b, old in zip(c['op'], pf_override['rev'], CASES['基准']['rev'])]
        c['earn'] = pf_override['earn']
        c['capex'] = max(c['capex'], 0.06)
    google = 0.06 + sum((interp(c['google'], t) for t in range(1, 7))) + 0.36 * interp(c['google'], 7)
    warrant = 0.001360867 + min(240, math.floor(google / 0.5)) * 0.000240042
    warrant = min(warrant, 0.058970907)
    extra_shares = 0
    for iteration in range(100):
        cash = CASH0
        debt = DEBT0
        shares = S0
        prevrev = R0
        rows = []
        for t in range(1, 16):
            rt = max(1, t - delay)
            rv = interp(c['rev'], rt)
            rev = sum(rv)
            op = interp(c['op'], t)
            gp = sum((a * (b + margin_shift) for a, b in zip(rv, c['gm'])))
            ebit = gp - op
            da = 0.03 * rev
            cap = c['capex'] * rev
            dnwc = c['nwc'] * (rev - prevrev)
            interest = 0.05 * debt
            cashinc = CASHYIELD * cash
            tax = max(0, ebit - interest + cashinc) * taxrate
            fcff = ebit * (1 - taxrate) + da - cap - dnwc - c['extra'].get(t, 0)
            cashop = ebit - interest + cashinc - tax + da - cap - dnwc - c['extra'].get(t, 0)
            withholding = 0.01 * rev
            repay = min(debt, MATURITY.get(t, 0))
            debt -= repay
            earncash = 0.233 * c['earn'] if t == 3 else 0
            shares *= 1 + c['dilution']
            if t == 3:
                shares += 0.0224 * c['earn']
            if t == 6:
                shares += 0.0052
            if t == 7:
                shares += extra_shares
            cash += cashop - repay - earncash - withholding
            mincash = max(1.5, 0.1 * rev)
            div = 0.24 * shares if t <= retain else max(0, cash - mincash)
            cash -= div
            rows.append(dict(t=t, units=rv, rev=rev, gp=gp, op=op, ebit=ebit, da=da, cap=cap, dnwc=dnwc, tax=tax, interest=interest, fcff=fcff, cashop=cashop, withholding=withholding, repay=repay, earncash=earncash, cash=cash, debt=debt, shares=shares, div=div, dps=div / shares, mincash=mincash))
            prevrev = rev
        last = rows[-1]
        rev16 = last['rev'] * (1 + g)
        ebit16 = last['ebit'] * (1 + g)
        min16 = max(1.5, 0.1 * rev16)
        income = CASHYIELD * last['cash']
        fcfe16 = (ebit16 + income) * (1 - taxrate) + 0.03 * rev16 - c['capex'] * rev16 - c['nwc'] * (rev16 - last['rev']) - (min16 - last['mincash']) - 0.01 * rev16
        dps16 = fcfe16 / (last['shares'] * (1 + c['dilution']))
        per_growth = (1 + g) / (1 + c['dilution']) - 1
        tv = dps16 / (r - per_growth)
        vals = {15: tv}
        for t in range(14, -1, -1):
            vals[t] = (rows[t]['dps'] + vals[t + 1]) / (1 + r)
        ns = warrant * max(0, 1 - 206.58 / vals[7])
        if abs(ns - extra_shares) < 1e-12:
            break
        extra_shares = (ns + extra_shares) / 2
    return dict(rows=rows, value=vals, tv=tv, terminal_fraction=tv / (1 + r) ** 15 / vals[0], google=google, warrant=warrant, netwarrant=extra_shares, r=r, g=g)

def display(o):
    return dict(value={str(t): round(o['value'][t], 4) for t in [0, 1, 3, 7]}, terminal_fraction=o['terminal_fraction'], google=o['google'], warrant=o['warrant'], netwarrant=o['netwarrant'], rows=[{k: v for k, v in a.items()} for a in o['rows']])
for name, c in CASES.items():
    o = run(c)
    print(name, {t: round(o['value'][t], 2) for t in (0, 1, 3, 7)})
for t in (0, 1, 3, 7):
    expected_price = 0.95 * sum((c['p'] * run(c)['value'][t] for c in CASES.values()))
    expected_dividend = 0.95 * 0.24 * t
    print(t, round(expected_price, 2), round(expected_dividend, 3))