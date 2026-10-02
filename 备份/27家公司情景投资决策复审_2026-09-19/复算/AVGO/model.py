import math, json, copy
from pathlib import Path
P = 357.61
N0 = 4.773629865
C0 = 22.475
D0 = 59.579
KNOTS = [0, 1, 2, 3, 5, 7, 10, 15]
PARAM = {'受损': dict(p=0.25, x=[43, 54, 58, 53, 46, 40, 34, 26], net=[15, 21, 24, 23, 21, 20, 18, 15], old=[17, 16, 15, 14, 13, 12, 11, 10], sw=[31, 33, 33, 32, 30, 29, 28, 26], mx=[0.58, 0.49, 0.43, 0.43, 0.44, 0.43, 0.42, 0.4], mn=[0.65, 0.61, 0.58, 0.56, 0.55, 0.54, 0.52, 0.5], mo=[0.5, 0.45, 0.43, 0.42, 0.41, 0.4, 0.39, 0.38], ms=[0.82, 0.79, 0.75, 0.73, 0.72, 0.71, 0.7, 0.68], sbc=[9, 9, 9, 8.5, 8, 7.5, 7, 6], nwc=0.2, cap=0.025, g=0.005, roic=0.12, loss={1: 8, 2: 15, 3: 7}), '基准': dict(p=0.45, x=[43, 74, 112, 138, 161, 177, 192, 200], net=[15, 25, 36, 42, 49, 53, 58, 60], old=[17, 17.5, 18, 18.5, 19, 19, 18.5, 18], sw=[31, 36, 39, 42, 47, 51, 55, 60], mx=[0.58, 0.56, 0.54, 0.52, 0.5, 0.48, 0.46, 0.44], mn=[0.65, 0.64, 0.63, 0.62, 0.6, 0.59, 0.58, 0.56], mo=[0.5, 0.5, 0.5, 0.49, 0.48, 0.47, 0.46, 0.44], ms=[0.82, 0.81, 0.8, 0.79, 0.78, 0.77, 0.75, 0.73], sbc=[9, 10, 11, 12, 13, 14, 15, 16], nwc=0.16, cap=0.025, g=0.02, roic=0.15, loss={1: 1, 2: 2, 3: 2, 4: 1}), '乐观': dict(p=0.2, x=[43, 86, 161, 195, 243, 276, 312, 350], net=[15, 28, 49, 60, 72, 79, 88, 100], old=[17, 17.5, 18, 18.5, 19, 19, 18.5, 18], sw=[31, 36, 39, 42, 47, 51, 55, 60], mx=[0.58, 0.58, 0.57, 0.56, 0.54, 0.52, 0.5, 0.48], mn=[0.65, 0.65, 0.65, 0.64, 0.63, 0.62, 0.6, 0.58], mo=[0.5, 0.5, 0.5, 0.49, 0.48, 0.47, 0.46, 0.44], ms=[0.82, 0.81, 0.8, 0.79, 0.78, 0.77, 0.75, 0.73], sbc=[9, 10.5, 12, 13, 15, 17, 19, 22], nwc=0.15, cap=0.027, g=0.02, roic=0.17, loss={1: 1, 2: 2, 3: 2, 4: 1}), '突破': dict(p=0.05, x=[43, 92, 185, 245, 355, 440, 540, 600], net=[15, 29, 55, 75, 100, 120, 145, 160], old=[17, 17.5, 18, 18.5, 19, 19, 18.5, 18], sw=[31, 36, 39, 42, 47, 51, 55, 60], mx=[0.58, 0.58, 0.58, 0.58, 0.56, 0.54, 0.51, 0.48], mn=[0.65, 0.65, 0.65, 0.65, 0.64, 0.63, 0.61, 0.58], mo=[0.5, 0.5, 0.5, 0.49, 0.48, 0.47, 0.46, 0.44], ms=[0.82, 0.81, 0.8, 0.79, 0.78, 0.77, 0.75, 0.73], sbc=[9, 11, 13, 15, 19, 23, 28, 34], nwc=0.18, cap=0.035, g=0.025, roic=0.18, loss={1: 1, 2: 3, 3: 4, 4: 3, 5: 2}), '尾部': dict(p=0.05, x=[43, 40, 18, 20, 24, 25, 24, 20], net=[15, 17, 12, 13, 15, 15, 14, 12], old=[17, 15, 13, 12, 11, 10, 9, 8], sw=[31, 31, 28, 26, 25, 24, 23, 22], mx=[0.58, 0.4, 0.15, 0.25, 0.35, 0.37, 0.36, 0.34], mn=[0.65, 0.55, 0.4, 0.44, 0.48, 0.48, 0.47, 0.45], mo=[0.5, 0.43, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33], ms=[0.82, 0.75, 0.67, 0.65, 0.65, 0.64, 0.63, 0.62], sbc=[9, 9, 8, 7, 6.5, 6, 5.5, 5], nwc=0.28, cap=0.02, g=0, roic=0.1, loss={1: 35, 2: 48, 3: 10})}
BUS = ['x', 'net', 'old', 'sw']
MARG = ['mx', 'mn', 'mo', 'ms']

def interp(vals, t):
    for j in range(1, len(KNOTS)):
        if t <= KNOTS[j]:
            f = (t - KNOTS[j - 1]) / (KNOTS[j] - KNOTS[j - 1])
            return vals[j - 1] + f * (vals[j] - vals[j - 1])
    return vals[-1]

def run(name, r=0.105, par=None, gshift=0, margin_shift=0, cash_yield=0.035):
    q = copy.deepcopy(par or PARAM[name])
    rows = []
    c, d, n = (C0, D0, N0)
    sched = {1: 0.752, 2: 5.127, 3: 2.405, 4: 6.406, **{t: 5 for t in range(5, 13)}, 13: 4.889}
    prev = sum((q[b][0] for b in BUS))
    prevfloor = 8
    for t in range(1, 16):
        revs = [interp(q[b], t) for b in BUS]
        margins = [interp(q[m], t) + margin_shift for m in MARG]
        rev = sum(revs)
        sbc = interp(q['sbc'], t)
        opb = [v * m for v, m in zip(revs, margins)]
        op = sum(opb) - sbc
        tax = 0.16 if t <= 3 else 0.18
        nop = op * (1 - tax)
        wc = q['nwc'] * (rev - prev) * (1 if rev >= prev else 0.35)
        da = 0.009 * rev
        capex = (q['cap'] + 0.009) * rev
        loss = q['loss'].get(t, 0) + (0.005 * revs[0] if t >= 4 and name not in ['受损', '尾部'] else 0)
        floor = max(8, 0.05 * rev)
        dfloor = floor - prevfloor
        fcf = nop + da - capex - wc - loss - dfloor
        interest = d * (0.05 if name != '尾部' else 0.07) * (1 - tax)
        pay = min(d, sched.get(t, 0))
        income = max(0, c - prevfloor) * cash_yield
        cpre = c + fcf + dfloor + income - interest - pay
        div = min(2.6 * 1.05 ** (t - 1) * n, max(0, cpre - floor))
        if name == '尾部' and t <= 3:
            div = 0
        borrow = 0
        equity = 0
        issue = 0
        if cpre - div < floor:
            gap = floor - (cpre - div)
            drawn = sum((z['borrow'] for z in rows))
            borrow = min(gap, max(0, 7.5 - drawn))
            gap -= borrow
            if gap > 0:
                equity = gap
                issue = equity / 15.0
        d = d - pay + borrow
        c = cpre - div + borrow + equity
        oldn = n
        n += issue
        rows.append(dict(t=t, rev=rev, revs=revs, opb=opb, sbc=sbc, op=op, tax=tax, nop=nop, da=da, capex=capex, wc=wc, loss=loss, dfloor=dfloor, fcf=fcf, interest=interest, income=income, repay=pay, borrow=borrow, equity=equity, issue=issue, cash=c, debt=d, shares=n, div=div, dps=div / oldn, floor=floor))
        prev = rev
        prevfloor = floor
    g = q['g'] + gshift
    last = rows[-1]
    reserve = 0.005 * last['revs'][0] * (1 + g) if name not in ['受损', '尾部'] else 0
    terminal = (last['nop'] * (1 + g) * (1 - g / q['roic']) - reserve) / (r - g)
    out = {}
    for h in [0, 1, 3, 7]:
        ev = sum((z['fcf'] / (1 + r) ** (z['t'] - h) for z in rows if z['t'] > h)) + terminal / (1 + r) ** (15 - h)
        if h == 0:
            cash, debt, n, floor = (C0, D0, N0, 8)
        else:
            z = rows[h - 1]
            cash, debt, n, floor = (z['cash'], z['debt'], z['shares'], z['floor'])
        eq = ev + cash - floor - debt
        price = max(0, eq / n)
        future_issues = [z for z in rows if z['t'] > h and z['equity'] > 0]
        if future_issues:
            finaln = rows[-1]['shares']
            finalfloor = rows[-1]['floor']
            finalcash = rows[-1]['cash'] - finalfloor
            endpoint = max(0, (terminal + finalcash - rows[-1]['debt']) / finaln)
            price = endpoint / (1 + r) ** (15 - h) + sum((z['dps'] / (1 + r) ** (z['t'] - h) for z in rows if z['t'] > h))
            eq = price * n
        cum = sum((z['dps'] for z in rows if z['t'] <= h))
        wealth = price + cum
        out[h] = dict(ev=ev, eq=eq, price=price, dist=cum, wealth=wealth, ret=wealth / P - 1, ann=(wealth / P) ** (1 / h) - 1 if h else None, shares=n, cash=cash, debt=debt, floor=floor, terminal_share=terminal / (1 + r) ** (15 - h) / ev)
    return dict(rows=rows, values=out, terminal=terminal, r=r)

def all_results():
    res = {k: run(k) for k in PARAM}
    for k in res:
        res[k]['low'] = run(k, 0.12, gshift=-0.005)['values']
        res[k]['high'] = run(k, 0.095, gshift=0.005)['values']
    return res
for name in PARAM:
    out = run(name)
    print(name, out['values'])
print('weighted', {h: sum((PARAM[k]['p'] * run(k)['values'][h]['wealth'] for k in PARAM)) for h in [0, 1, 3, 7]})