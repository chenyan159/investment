import json, math, copy
from pathlib import Path
PRICE = 1015.8
N0 = 1.15
C0 = 30.2
R0 = [16, 60, 49.312, 20.8, 18.972, 0.74]
PRODUCTS = ['HBM', '服务器DRAM', '其他DRAM', '企业NAND产品', '其他NAND', 'NOR等']
NODES = [1, 3, 7, 12]
S = {'悲观': dict(q=[[1.25, 1.7, 2.4, 3.0], [1.08, 1.35, 1.8, 2.3], [0.97, 1.0, 1.15, 1.3], [1.1, 1.6, 2.5, 3.4], [0.98, 1.0, 1.2, 1.4], [1, 1, 1, 1]], price=[[0.95, 0.65, 0.48, 0.4], [0.85, 0.45, 0.29, 0.25], [0.82, 0.35, 0.23, 0.2], [0.9, 0.5, 0.33, 0.28], [0.82, 0.34, 0.22, 0.18], [1, 0.9, 0.8, 0.75]], m=[[0.5, 0.25, 0.25, 0.22], [0.68, 0.25, 0.2, 0.18], [0.63, 0.1, 0.12, 0.1], [0.6, 0.25, 0.22, 0.2], [0.55, 0.05, 0.08, 0.08], [0.15, 0.1, 0.08, 0.08]], cap=[44, 27, 22, 24], da=[12, 17, 19, 22]), '基准': dict(q=[[1.6, 2.5, 4, 5.5], [1.18, 1.65, 2.5, 3.3], [1.03, 1.13, 1.4, 1.6], [1.3, 2.2, 4, 5.8], [1.04, 1.2, 1.6, 2], [1, 1.05, 1.15, 1.25]], price=[[1.15, 0.95, 0.7, 0.62], [1.08, 0.72, 0.45, 0.4], [1.03, 0.62, 0.35, 0.32], [1.08, 0.75, 0.5, 0.42], [1.03, 0.6, 0.32, 0.26], [1, 0.95, 0.85, 0.8]], m=[[0.64, 0.58, 0.47, 0.42], [0.8, 0.57, 0.38, 0.33], [0.8, 0.48, 0.25, 0.2], [0.77, 0.57, 0.4, 0.35], [0.74, 0.38, 0.2, 0.15], [0.2, 0.15, 0.12, 0.1]], cap=[46, 44, 36, 39], da=[12, 18, 28, 35]), '乐观': dict(q=[[1.8, 3.1, 5.3, 7.4], [1.22, 1.85, 3.0, 4.1], [1.04, 1.18, 1.5, 1.75], [1.4, 2.6, 5.0, 7.4], [1.04, 1.25, 1.7, 2.2], [1, 1.08, 1.2, 1.35]], price=[[1.3, 1.12, 0.85, 0.75], [1.13, 0.9, 0.63, 0.54], [1.06, 0.76, 0.45, 0.38], [1.15, 0.9, 0.67, 0.55], [1.06, 0.7, 0.4, 0.32], [1, 1, 0.9, 0.85]], m=[[0.7, 0.65, 0.56, 0.49], [0.82, 0.69, 0.52, 0.44], [0.81, 0.6, 0.38, 0.3], [0.8, 0.67, 0.52, 0.45], [0.77, 0.5, 0.32, 0.25], [0.22, 0.2, 0.16, 0.12]], cap=[50, 57, 52, 56], da=[12, 20, 36, 46]), '突破': dict(q=[[1.85, 3.9, 8, 12], [1.22, 1.85, 3.2, 4.7], [1.04, 1.18, 1.5, 1.75], [1.4, 3.0, 7, 11], [1.04, 1.25, 1.7, 2.2], [1, 1.08, 1.2, 1.35]], price=[[1.35, 1.28, 1.08, 0.93], [1.13, 0.92, 0.65, 0.57], [1.06, 0.76, 0.45, 0.38], [1.15, 0.98, 0.78, 0.64], [1.06, 0.7, 0.4, 0.32], [1, 1, 0.9, 0.85]], m=[[0.72, 0.7, 0.64, 0.56], [0.82, 0.7, 0.53, 0.46], [0.81, 0.6, 0.38, 0.3], [0.8, 0.7, 0.58, 0.5], [0.77, 0.5, 0.32, 0.25], [0.22, 0.2, 0.16, 0.12]], cap=[53, 72, 78, 90], da=[12, 23, 47, 69])}

def ip(a, t):
    if t <= 1:
        return a[0]
    for j in range(1, 4):
        if t <= NODES[j]:
            f = (t - NODES[j - 1]) / (NODES[j] - NODES[j - 1])
            return a[j - 1] + f * (a[j] - a[j - 1])

def run(s, r=0.115, g=0.02, shock=0, capmult=1, crisis=False, initcash=C0):
    cash = initcash
    debt = 0.0
    shares = N0
    ppe = 63.8
    nwc = 34.2
    rows = []
    for t in range(1, 13):
        qs = [ip(a, t) for a in s['q']]
        ps = [ip(a, t) for a in s['price']]
        ms = [ip(a, t) for a in s['m']]
        rev = [R0[k] * qs[k] * ps[k] for k in range(6)]
        cost = [rev[k] * (1 - ms[k]) for k in range(6)]
        if shock and t >= 2:
            rev = [x * (1 - shock) for x in rev]
        ops = [rev[k] - cost[k] for k in range(6)]
        cap = ip(s['cap'], t) * capmult
        da = ip(s['da'], t)
        extra = 1.0 if t <= 3 else 0.5
        newnwc = 0.18 * sum(rev)
        if crisis:
            rr = [50, 45, 65, 75, 82, 88, 94, 100, 105, 110, 115, 120][t - 1]
            mm = [-0.15, -0.2, 0.08, 0.12, 0.15, 0.17, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18][t - 1]
            rev = [rr * x / sum(rev) for x in rev]
            ops = [x * mm for x in rev]
            cap = [46, 32, 20, 18, 18, 19, 20, 21, 22, 23, 24, 25][t - 1]
            da = [12, 14, 15, 15, 15, 16, 17, 18, 19, 20, 21, 22][t - 1]
            newnwc = max(0.18 * rr, 34.2 if t <= 2 else 20)
        ebit = sum(ops)
        tax = max(0, ebit) * 0.18
        fcf = ebit - tax + da - cap - (newnwc - nwc) - extra
        interest = cash * 0.035 - debt * 0.08
        available = cash + fcf + interest
        borrow = 0.0
        raised = 0.0
        newshares = 0.0
        repay = 0.0
        if available < 0:
            borrow = min(2 - debt, -available)
            debt += borrow
            available += borrow
            if available < 0:
                raised = -available + 5
                issueprice = 60 if t == 1 else 45
                newshares = raised / (0.97 * issueprice)
                shares += newshares
                available += raised
        if available > 5 and debt > 0:
            repay = min(debt, available - 5)
            debt -= repay
            available -= repay
        div = max(0, available - C0)
        cash = available - div
        ppe += cap - da
        rows.append(dict(t=t, rev=sum(rev), ebit=ebit, tax=tax, da=da, cap=cap, nwc=newnwc, dnwc=newnwc - nwc, other=extra, fcf=fcf, cash=cash, debt=debt, shares=shares, div=div, dps=div / shares, borrow=borrow, repay=repay, raised=raised, newshares=newshares, ppe=ppe, products=[dict(r=rev[k], op=ops[k], q=qs[k], p=ps[k], m=ms[k]) for k in range(6)]))
        nwc = newnwc
    last = rows[-1]
    ic = last['ppe'] + last['nwc']
    nopat = last['ebit'] - last['tax']
    tfcf = nopat * (1 + g) - g * ic - 0.5
    tv = max(0, tfcf / (r - g))
    terminal = (tv + last['cash'] - last['debt']) / last['shares']
    vals = {}
    wealth = {}
    ds = {}
    for h in [0, 1, 3, 7, 12]:
        val = sum((x['dps'] / (1 + r) ** (x['t'] - h) for x in rows if x['t'] > h)) + terminal / (1 + r) ** (12 - h)
        dp = sum((x['dps'] for x in rows if x['t'] <= h))
        vals[h] = val
        ds[h] = dp
        wealth[h] = val + dp
    return dict(rows=rows, v=vals, dps=ds, wealth=wealth, terminal=terminal, tv=tv, tfcf=tfcf, roic=nopat / ic, terminal_weight=terminal / (1 + r) ** 12 / vals[0], after7_weight=(sum((x['dps'] / (1 + r) ** x['t'] for x in rows if x['t'] > 7)) + terminal / (1 + r) ** 12) / vals[0])
if __name__ == '__main__':
    out = {name: run(s) for name, s in S.items()}
    for name, s in S.items():
        out[name]['low'] = run(s, 0.13, 0.01)['v']
        out[name]['high'] = run(s, 0.1, 0.03)['v']
    out['危机'] = run(S['悲观'], crisis=True)
    w = {'悲观': 0.24, '基准': 0.43, '乐观': 0.21, '突破': 0.07, '危机': 0.05}
    out['weights'] = w
    for name, z in list(out.items()):
        if name == 'weights':
            continue
        print(name, 'V', {h: round(z['v'][h]) for h in [0, 1, 3, 7]}, 'D', {h: round(z['dps'][h]) for h in [1, 3, 7]}, 'R', [round(z['rows'][i - 1]['rev']) for i in [1, 3, 7, 12]], 'FCF', [round(z['rows'][i - 1]['fcf']) for i in [1, 3, 7, 12]], 'ROIC', round(z['roic'], 3), 'TVweight', round(z['terminal_weight'], 3))
    out['expected'] = {h: sum((w[n] * out[n]['wealth'][h] for n in w)) for h in [0, 1, 3, 7]}
    out['expected_v'] = {h: sum((w[n] * out[n]['v'][h] for n in w)) for h in [0, 1, 3, 7]}
    out['ordinary'] = run(S['基准'], shock=0.1, capmult=1.1)
    hbm = copy.deepcopy(S['基准'])
    for key in ['q', 'price', 'm']:
        hbm[key][0] = S['突破'][key][0]
    hbm['cap'] = [51, 58, 54, 58]
    hbm['da'] = [12, 21, 36, 49]
    out['hbm_only'] = run(hbm)
    durable = copy.deepcopy(S['基准'])
    durable['price'] = [[a[0], a[0] * 0.95, a[0] * 0.8, a[0] * 0.7] for a in durable['price']]
    durable['m'] = [[a[0], max(a[0] - 0.1, 0.1), max(a[0] - 0.2, 0.1), max(a[0] - 0.25, 0.1)] for a in durable['m']]
    durable['cap'] = [46, 49, 47, 50]
    durable['da'] = [12, 19, 32, 42]
    out['durability'] = run(durable)
    out['durability_params'] = durable
    for n in ['ordinary', 'hbm_only']:
        print(n, {h: round(out[n]['wealth'][h]) for h in [0, 1, 3, 7]})
    print('EXPECTED', out['expected'])