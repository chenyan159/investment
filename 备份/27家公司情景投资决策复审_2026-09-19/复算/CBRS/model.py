import json, math, copy
from pathlib import Path
P0 = 198.37
S = {'D': dict(p=0.25, H=[0.35, 0.36, 0.38, 0.38, 0.36, 0.34, 0.32, 0.3, 0.28, 0.26], O=[0.65, 1.3, 2.0, 2.1, 1.9, 1.6, 1.3, 1.05, 0.85, 0.7], A=[0.25, 0.32, 0.4, 0.46, 0.5, 0.5, 0.48, 0.46, 0.44, 0.42], W=[0.03, 0.08, 0.15, 0.2, 0.25, 0.25, 0.24, 0.23, 0.22, 0.2], gm=[0.34, 0.36, 0.38, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32], fixed=0.48, var=0.22, repl=0.22, growth=1.1, n=0.282, g=0, roic=0.12), 'B': dict(p=0.4, H=[0.36, 0.4, 0.45, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6], O=[1.4, 2.9, 4.1, 4.8, 4.7, 4.5, 4.3, 4.15, 4.0, 3.9], A=[0.38, 0.65, 1.0, 1.4, 1.75, 2.1, 2.45, 2.7, 2.95, 3.2], W=[0.12, 0.3, 0.65, 1.0, 1.3, 1.55, 1.8, 2.0, 2.2, 2.4], gm=[0.43, 0.46, 0.49, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], fixed=0.54, var=0.21, repl=0.18, growth=0.85, n=0.29, g=0.02, roic=0.14), 'O': dict(p=0.2, H=[0.38, 0.43, 0.49, 0.53, 0.56, 0.59, 0.62, 0.65, 0.68, 0.7], O=[1.75, 3.65, 5.1, 6.2, 7.1, 7.8, 8.2, 8.5, 8.7, 8.9], A=[0.44, 0.85, 1.55, 2.45, 3.4, 4.3, 5.2, 6.1, 7.0, 7.8], W=[0.18, 0.55, 1.15, 2.0, 2.85, 3.6, 4.3, 4.9, 5.5, 6.0], gm=[0.46, 0.49, 0.52, 0.54, 0.54, 0.54, 0.54, 0.54, 0.54, 0.54], fixed=0.58, var=0.205, repl=0.16, growth=0.75, n=0.301, g=0.025, roic=0.17), 'X': dict(p=0.1, H=[0.36, 0.4, 0.45, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6], O=[1.55, 3.3, 5.3, 7.3, 9.4, 11.3, 12.0, 12.4, 12.7, 13.0], A=[0.48, 1.15, 2.55, 4.7, 7.7, 11.5, 15.5, 19.0, 22.5, 25.0], W=[0.2, 0.7, 1.6, 3.1, 5.0, 7.2, 9.5, 11.5, 13.5, 15.0], gm=[0.45, 0.49, 0.53, 0.55, 0.57, 0.58, 0.58, 0.58, 0.58, 0.58], fixed=0.62, var=0.22, repl=0.15, growth=0.8, n=0.311, g=0.025, roic=0.18)}

def run(key, rate=0.13, g_override=None, cap_mult=1.0, gm_delta=0.0, revenue_mult=1.0, cfg=None):
    s = copy.deepcopy(cfg or S[key])
    n = s['n']
    cash = 6.9
    debt = 0.7
    reserve = 0.5
    rows = []
    nol = 0.8
    lastrev = 0.86
    prev_rec = 0.5
    for k in ['H', 'O', 'A', 'W']:
        a = s[k]
        if key == 'D':
            a += [a[-1] * 0.8 ** j for j in range(1, 6)]
        else:
            end = s['g']
            start = a[-1] / a[-2] - 1
            for j in range(1, 6):
                a.append(a[-1] * (1 + start + (end - start) * j / 5))
    for j in range(5):
        s['gm'].append(s['gm'][9] - (0.04 if key != 'D' else 0.06) * (j + 1) / 5)
    for i in range(15):
        t = i + 1
        parts = {k: s[k][i] * revenue_mult for k in ['H', 'O', 'A', 'W']}
        rev = sum(parts.values())
        rec = rev - parts['H']
        gms = {'H': (0.35 if key == 'D' else 0.4) + gm_delta, 'O': s['gm'][i] + gm_delta, 'A': s['gm'][i] - 0.04 + gm_delta, 'W': s['gm'][i] + 0.08 + gm_delta}
        gp = sum((parts[k] * gms[k] for k in parts))
        gm = gp / rev
        fixed = s['fixed'] * (1.03 ** i if key != 'D' else 1.0 if t <= 4 else max(0.18, 0.65 * 0.85 ** (t - 5)))
        opex = fixed + s['var'] * rev
        ebit = gp - opex
        use = min(nol, max(ebit, 0) * 0.8)
        nol = max(0, nol - use) + max(-ebit, 0)
        tax = max(0, ebit - use) * 0.23 + 0.002
        da = (0.17 if key == 'D' else 0.14) * rec + 0.015
        if i < 10:
            nextrec = sum((s[k][min(i + 1, 14)] for k in ['O', 'A', 'W'])) * revenue_mult
            growth = s['growth'] * max(nextrec - rec, 0)
            replacement = (0.1 if key == 'D' and t >= 5 else s['repl']) * rec + 0.025
            cap = (growth + replacement) * cap_mult
            dnwc = 0.08 * (rev - lastrev)
        else:
            growth_rate = max(0, rev / lastrev - 1)
            reinvest = max(0, ebit - tax) * growth_rate / s['roic']
            cap = (da + reinvest * 0.85) * cap_mult
            dnwc = reinvest * 0.15
        exit_cost = 0.25 if key == 'D' and t in [2, 3] else 0
        fcf = ebit - tax + da - cap - dnwc - exit_cost
        repay = min(debt, 0.55 if t == 1 else 0.15)
        debt -= repay
        raise_equity = 0
        interest = 0.06 * (debt + repay / 2)
        quarters = []
        for q, (rw, cw) in enumerate(zip([0.18, 0.22, 0.27, 0.33], [0.35, 0.3, 0.2, 0.15])):
            qfcf = (gp - s['var'] * rev) * rw - fixed / 4 - tax / 4 + da / 4 - cap * cw - dnwc * rw - exit_cost / 4
            cash += qfcf - repay / 4 - interest / 4 + max(cash - reserve, 0) * 0.03 / 4
            newfund = 0
            if cash < reserve:
                newfund = reserve - cash + 0.5
                price = s.get('issueprice', 150)
                n += newfund / price
                cash += newfund
                raise_equity += newfund
            quarters.append(dict(t=i + (q + 1) / 4, FCF=qfcf, cash=cash, newfund=newfund))
        rows.append(dict(t=t, R=rev, **parts, GMS=gms, GM=gm, OPEX=opex, EBIT=ebit, tax=tax, DA=da, capex=cap, NWC=dnwc, exit=exit_cost, FCF=fcf, cash=cash, debt=debt, N=n, raise_equity=raise_equity, quarters=quarters))
        lastrev = rev
        prev_rec = rec
    g = s['g'] if g_override is None else g_override
    terminal = 0.3 if key == 'D' else max(0, rows[-1]['EBIT'] * 0.77) * (1 + g) * (1 - g / s['roic']) / (rate - g)
    finaln = rows[-1]['N']

    def value(t):
        remaining = sum((x['FCF'] / (1 + rate) ** (x['t'] - t) for x in rows if x['t'] > t))
        futurefund = sum((q['newfund'] / (1 + rate) ** (q['t'] - t) for x in rows for q in x['quarters'] if q['t'] > t))
        tv = terminal / (1 + rate) ** (15 - t)
        ct = 6.9 if t == 0 else rows[t - 1]['cash']
        dt = 0.7 if t == 0 else rows[t - 1]['debt']
        eq = max(0, remaining + tv + ct - reserve - dt + futurefund)
        return dict(t=t, EV=remaining + tv, eq=eq, n=finaln, price=eq / finaln, ret=eq / finaln / P0 - 1, cagr=(eq / finaln / P0) ** (1 / t) - 1 if t else None, terminal_fraction=tv / eq if eq else 0)
    return dict(rows=rows, values={str(t): value(t) for t in [0, 1, 3, 7]}, mincash=min((q['cash'] for x in rows for q in x['quarters'])), fund=sum((x['raise_equity'] for x in rows)), terminal=terminal)

def main():
    out = {k: run(k) for k in S}
    for k in S:
        lo = run(k, rate=0.15, g_override=max(0, S[k]['g'] - 0.005), cap_mult=1.1, gm_delta=-0.02)
        hi = run(k, rate=0.11, g_override=S[k]['g'] + 0.005 if k != 'D' else 0, cap_mult=0.9, gm_delta=0.02)
        out[k]['range'] = {t: [lo['values'][t]['price'], hi['values'][t]['price']] for t in ['0', '1', '3', '7']}
        print(k, 'fund', round(out[k]['fund'], 3), 'mincash', round(out[k]['mincash'], 3))
        for t, v in out[k]['values'].items():
            print(t, {x: round(v[x], 3) for x in ['eq', 'n', 'price', 'ret', 'terminal_fraction']}, [round(a, 2) for a in out[k]['range'][t]])
    out['F'] = {'p': 0.05, 'values': {str(t): {'price': 3.0 / 1.13 ** max(3 - t, 0)} for t in [0, 1, 3, 7]}}
    out['weighted'] = {str(t): sum((S[k]['p'] * out[k]['values'][str(t)]['price'] for k in S)) + 0.05 * out['F']['values'][str(t)]['price'] for t in [0, 1, 3, 7]}
    print('weighted', out['weighted'])
    pass
if __name__ == '__main__':
    main()