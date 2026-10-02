import math, json, copy
from pathlib import Path
P0 = 317.36
S0 = 0.2024
C0 = 1.637
D0 = 3.25
R0 = [6.5, 1.75, 0.1, 0]
K = [1, 3, 7, 12]
DATA = {'受损': {'r': [[7.4, 7.0, 6.3, 5.8], [1.65, 1.6, 1.65, 1.7], [0.15, 0.3, 0.5, 0.5], [0.01, 0.04, 0.08, 0.1]], 'm': [[0.22, 0.2, 0.18, 0.16], [0.12, 0.12, 0.13, 0.13], [-0.4, -0.1, 0.1, 0.1], [-2, -0.5, 0, 0.05]], 'g': 0.0, 'roic': 0.09}, '基准': {'r': [[8.9, 11.8, 16, 19.5], [1.8, 2, 2.3, 2.6], [0.35, 1.5, 4, 5.5], [0.05, 0.3, 1, 1.5]], 'm': [[0.25, 0.26, 0.23, 0.21], [0.16, 0.17, 0.17, 0.16], [-0.1, 0.18, 0.25, 0.23], [-0.5, 0.1, 0.22, 0.2]], 'g': 0.025, 'roic': 0.15}, '乐观': {'r': [[9.7, 14, 21, 26], [1.85, 2.1, 2.5, 2.9], [0.55, 2.6, 7, 10], [0.06, 0.5, 2.5, 4]], 'm': [[0.27, 0.29, 0.27, 0.24], [0.17, 0.18, 0.18, 0.17], [0, 0.24, 0.29, 0.26], [-0.4, 0.15, 0.25, 0.23]], 'g': 0.03, 'roic': 0.18}, '突破': {'r': [[9.8, 14.3, 23, 30], [1.8, 2, 2.3, 2.6], [0.65, 3.5, 14, 22], [0.05, 0.3, 1.2, 2]], 'm': [[0.27, 0.3, 0.28, 0.25], [0.16, 0.17, 0.17, 0.16], [0, 0.25, 0.32, 0.28], [-0.5, 0.1, 0.22, 0.2]], 'g': 0.03, 'roic': 0.2}}
CAP = [[0.2, 0.12, 0.085, 0.075], [0.06, 0.06, 0.06, 0.06], [0.35, 0.2, 0.12, 0.1], [0.8, 0.4, 0.16, 0.13]]
DEP = [[0.04, 0.055, 0.06, 0.06], [0.045, 0.045, 0.045, 0.045], [0.05, 0.06, 0.06, 0.06], [0.04, 0.05, 0.06, 0.06]]
WC = [0.2, 0.16, 0.25, 0.25]
WEIGHTS = {'受损': 0.2, '基准': 0.45, '乐观': 0.2, '突破': 0.1, '清偿': 0.05}

def interp(vals, t):
    if t <= 1:
        return vals[0]
    for a, b in zip(range(3), range(1, 4)):
        if t <= K[b]:
            u = (t - K[a]) / (K[b] - K[a])
            return vals[a] * (1 - u) + vals[b] * u
    return vals[-1]

def model(name, wacc=0.115, gshift=0, override=None, margin_shift=0, cap_shift=0, thermal_own=0.85, delay_c=False):
    d = copy.deepcopy(DATA[name] if override is None else override)
    rows = []
    prev = R0[:]
    cash = C0
    debt = D0
    shares = S0
    reserve = 0.65
    max_extra = 0
    drawn = 0
    equity = 0
    for t in range(1, 13):
        rr = [interp(v, t) for v in d['r']]
        mm = [interp(v, t) + margin_shift for v in d['m']]
        if delay_c:
            effective = 0 if t <= 2 else t - 2 if t <= 7 else 5 + (t - 7) * 7 / 5
            rr[2] = 0.1 if effective == 0 else interp(d['r'][2], effective)
            mm[2] = -0.8 if effective == 0 else interp(d['m'][2], effective) + margin_shift
        rev = sum(rr)
        corp = 0.15 + 0.007 * rev
        eb = [r * m for r, m in zip(rr, mm)]
        ebit = sum(eb) - corp
        da = [r * interp(v, t) for r, v in zip(rr, DEP)]
        caps = copy.deepcopy(CAP)
        if name == '受损':
            caps[0] = [0.15, 0.08, 0.065, 0.06]
        cap = [r * (interp(v, t) + cap_shift) for r, v in zip(rr, caps)]
        if delay_c and t <= 2:
            cap[2] = max(cap[2], 0.06)
        nwc = [(r - p) * v for r, p, v in zip(rr, prev, WC)]
        extra = 0.15 if t == 1 else 0
        damage = {1: 0.35, 2: 0.15}.get(t, 0) if name == '受损' else 0
        newreserve = max(0.65, 0.06 * rev)
        dr = newreserve - reserve
        taxes = max(ebit, 0) * 0.21
        rawfcff = ebit - taxes + sum(da) - sum(cap) - sum(nwc) - extra - damage
        thermal_cf = eb[3] * (1 - 0.21) + da[3] - cap[3] - nwc[3]
        minority = (1 - thermal_own) * thermal_cf + 0.005
        restricted_credit = 0.06 if t <= 7 else 0.033 if t == 8 else 0
        fcff = rawfcff - minority - dr + restricted_credit
        bridge_fee = {'受损': 0, '基准': 0.012, '乐观': 0.022, '突破': 0.03}[name] if t <= 2 else 0
        interest = debt * (0.075 if name == '受损' else 0.06) * 0.79 + bridge_fee
        cash_interest = max(cash - reserve, 0) * 0.033
        pre = cash + fcff + dr - interest + cash_interest
        principal = {1: 0.008, 2: 0.034, 3: 1.16, 4: 1.05, 5: 0.998}.get(t, 0)
        principal = min(debt, principal)
        pre -= principal
        debt -= principal
        need = max(newreserve - pre, 0)
        newdebt = min(need, max(0.664 - drawn, 0))
        drawn += newdebt
        debt += newdebt
        pre += newdebt
        issue = max(newreserve - pre, 0)
        if issue:
            price = 80 if name == '受损' else 200
            shares += issue / 0.97 / price
            equity += issue / 0.97
            pre += issue
        cash = pre
        if t >= 6 and debt > 0:
            repay = min(debt, max(cash - newreserve, 0))
            debt -= repay
            cash -= repay
            principal += repay
        max_extra = max(max_extra, drawn + equity)
        rows.append(dict(t=t, rev=rev, unit_r=rr, unit_ebit=eb, ebit=ebit, corp=corp, tax=taxes, da=sum(da), cap=sum(cap), nwc=sum(nwc) + extra, damage=damage, minority=minority, dr=dr, restricted_credit=restricted_credit, fcff=fcff, cash=cash, reserve=newreserve, debt=debt, shares=shares, interest=interest, cashinterest=cash_interest, principal=principal, newdebt=newdebt, issue=issue / 0.97))
        prev = rr
        reserve = newreserve
    g = d['g'] + gshift
    terminal_nopat = (rows[-1]['ebit'] - (1 - thermal_own) * rows[-1]['unit_ebit'][3]) * 0.79 - 0.005
    terminal_fcf = terminal_nopat * (1 + g) * (1 - g / d['roic'])
    tv = terminal_fcf / (wacc - g)
    values = {}
    termshares = {}
    for h in [0, 1, 3, 7]:
        ev = sum((z['fcff'] / (1 + wacc) ** (z['t'] - h) for z in rows if z['t'] > h)) + tv / (1 + wacc) ** (12 - h)
        if h == 0:
            c, rs, dn, sh = (C0, 0.65, D0, S0)
        else:
            z = rows[h - 1]
            c, rs, dn, sh = (z['cash'], z['reserve'], z['debt'], z['shares'])
        eq = max(ev + c - rs - dn, 0)
        values[h] = {'ev': ev, 'eq': eq, 'p': eq / sh, 'cash': c, 'debt': dn, 'shares': sh, 'ret': eq / sh / P0 - 1, 'ann': (eq / sh / P0) ** (1 / h) - 1 if h else None, 'tv_pct': tv / (1 + wacc) ** (12 - h) / ev}
    return dict(rows=rows, values=values, terminal_fcf=terminal_fcf, tv=tv, max_extra=max_extra, drawn=drawn, equity=equity)

def quarterly_liquidity(name):
    z = model(name)
    cash = C0
    debt = D0
    draw = 0
    minimum = C0
    for j in range(2):
        row = z['rows'][j]
        for q in range(4):
            cash += (row['ebit'] - row['tax'] + row['da']) * [0.18, 0.22, 0.27, 0.33][q]
            cash -= row['cap'] * [0.3, 0.27, 0.23, 0.2][q] + row['nwc'] * [0.4, 0.3, 0.2, 0.1][q]
            cash -= row['damage'] * (q == 0) + row['minority'] / 4
            cash -= debt * (0.075 if name == '受损' else 0.06) * 0.79 / 4
            cash -= {'受损': 0, '基准': 0.012, '乐观': 0.022, '突破': 0.03}[name] / 4
            principal = [0.008, 0.034][j] / 4
            cash -= principal
            debt -= principal
            reserve = max(0.65, 0.06 * row['rev'])
            gap = max(reserve - cash, 0)
            cash += gap
            debt += gap
            draw += gap
            minimum = min(minimum, cash)
    return {'peak_draw': draw, 'minimum_cash': minimum}

def run():
    out = {k: model(k) for k in DATA}
    for k, z in out.items():
        print(k, 'values', {h: round(v['p'], 2) for h, v in z['values'].items()}, 'fund', round(z['max_extra'], 3), 'shares', round(z['rows'][6]['shares'] * 1000, 2))
        print('quarterly', quarterly_liquidity(k))
        for t in [1, 2, 3, 7, 12]:
            r = z['rows'][t - 1]
            print(t, *[round(r[q], 3) for q in ['rev', 'ebit', 'fcff', 'cash', 'debt', 'cap', 'nwc']])
    pass
    for h in [0, 1, 3, 7]:
        ep = sum((WEIGHTS[k] * out[k]['values'][h]['p'] for k in DATA))
        print('EXPECTED', h, round(ep, 2), round(ep / P0 - 1, 4), (ep / P0) ** (1 / h) - 1 if h else '')
    return out
if __name__ == '__main__':
    run()