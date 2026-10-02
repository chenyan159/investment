import json, math, copy
from datetime import date
from pathlib import Path
ROOT = Path.cwd()
P0 = 434.67
SH = 25.9324 / 5
TAX = 0.18
CASH0 = 108.0
DEBT = 32.34
MINCASH = 18.0
OLD_DIV = 7 * 25.9324 / 32
OTHER = 3.0
START = date(2026, 9, 19)
END = date(2041, 1, 1)
names = ['受损', '基准', '乐观', '突破']
probs = [0.2, 0.5, 0.25, 0.05]
common = ([86, 39, 24, 26], [0.66, 0.6, 0.4, 0.48], 62, 26, 20)
anchors = {'受损': {2026: common, 2027: ([94, 37, 22, 26], [0.5, 0.54, 0.25, 0.3], 63, 32, 20), 2029: ([90, 38, 20, 29], [0.43, 0.51, 0.2, 0.25], 45, 38, 20), 2033: ([111, 42, 18, 37], [0.46, 0.5, 0.2, 0.28], 43, 38, 23), 2036: ([119, 43, 17, 42], [0.43, 0.48, 0.18, 0.26], 43, 38, 25), 2040: ([125, 44, 16, 46], [0.4, 0.45, 0.16, 0.24], 44, 40, 28)}, '基准': {2026: common, 2027: ([115, 43, 25, 35], [0.64, 0.6, 0.36, 0.47], 77, 32, 24), 2029: ([172, 50, 26, 52], [0.66, 0.62, 0.35, 0.46], 95, 48, 34), 2033: ([257, 62, 26, 80], [0.62, 0.58, 0.3, 0.42], 111, 70, 60), 2036: ([302, 68, 25, 96], [0.58, 0.55, 0.26, 0.4], 117, 85, 80), 2040: ([340, 74, 24, 112], [0.52, 0.5, 0.24, 0.36], 125, 99, 100)}, '乐观': {2026: common, 2027: ([125, 44, 25, 40], [0.67, 0.61, 0.37, 0.5], 81, 33, 25), 2029: ([203, 54, 27, 65], [0.68, 0.63, 0.37, 0.5], 108, 52, 40), 2033: ([340, 72, 29, 116], [0.65, 0.6, 0.32, 0.46], 150, 90, 82), 2036: ([420, 81, 28, 146], [0.62, 0.57, 0.29, 0.44], 177, 113, 110), 2040: ([499, 90, 27, 178], [0.57, 0.53, 0.26, 0.4], 199, 140, 145)}, '突破': {2026: common, 2027: ([131, 43, 25, 43], [0.67, 0.6, 0.36, 0.51], 86, 34, 25), 2029: ([234, 51, 26, 85], [0.7, 0.61, 0.34, 0.53], 134, 60, 45), 2033: ([467, 64, 26, 184], [0.67, 0.57, 0.28, 0.5], 226, 125, 105), 2036: ([605, 70, 24, 249], [0.63, 0.54, 0.25, 0.47], 285, 174, 155), 2040: ([750, 76, 22, 317], [0.58, 0.5, 0.22, 0.43], 324, 220, 210)}}
terminal = {'受损': (0.01, 0.1), '基准': (0.025, 0.16), '乐观': (0.03, 0.18), '突破': (0.03, 0.2)}

def annual(name, changed=None):
    a = copy.deepcopy(anchors[name] if changed is None else changed)
    out = {}
    keys = sorted(a)
    for y in range(2026, 2041):
        l = max((k for k in keys if k <= y))
        u = min((k for k in keys if k >= y))
        f = (y - l) / (u - l) if u > l else 0

        def interp(v, w):
            if isinstance(v, list):
                return [interp(x, z) for x, z in zip(v, w)]
            return v + (w - v) * f
        rv, mg, cap, da, dv = [interp(v, w) for v, w in zip(a[l], a[u])]
        rev = sum(rv)
        op = sum((x * z for x, z in zip(rv, mg)))
        prev = sum(common[0]) if y == 2026 else out[y - 1]['rev']
        nwc = 0.08 * (rev - prev) if y > 2026 else 4.2
        lease = 0.18 * (rev / 175)
        minority = 0.005 * op * (1 - TAX)
        jv = {2026: 0.2, 2027: 0.6, 2028: 0.7, 2029: 0.38}.get(y, 0)
        jvc = 0 if y < 2030 else {'受损': 0.04, '基准': 0.15, '乐观': 0.23, '突破': 0.3}[name]
        fcff = op * (1 - TAX) + da - cap - nwc - lease - minority - jv + jvc
        out[y] = dict(rv=rv, mg=mg, rev=rev, op=op, cap=cap, da=da, nwc=nwc, lease=lease, minority=minority, jv=jv, jvc=jvc, fcff=fcff, div=dv)
    return out

def pieces(start, end):
    cur = start
    while cur < end:
        nxt = date(cur.year + 1, 1, 1) if cur.month == 12 else date(cur.year, cur.month + 1, 1)
        stop = min(nxt, end)
        days = (stop - cur).days
        year_days = (date(cur.year + 1, 1, 1) - date(cur.year, 1, 1)).days
        yield (cur.year, days / year_days, ((cur - START).days + days / 2) / 365.25, days / 365.25)
        cur = stop

def value(name, h=0, w=0.095, gdelta=0, changed=None, capshift=0, opshift=0):
    a = annual(name, changed)
    target = date(2026 + h, 9, 19)
    for y, z in a.items():
        if y >= 2027:
            z['fcff'] += z['rev'] * (opshift * (1 - TAX) - capshift)
            z['op'] += z['rev'] * opshift
            z['cap'] += z['rev'] * capshift
    schedule = [(date(2026, 9, 16), date(2026, 10, 8), OLD_DIV)]
    for yy in range(2027, 2042):
        for mm, dd, em, ed in [(1, 7, 12, 10), (4, 8, 3, 16), (7, 9, 6, 11), (10, 8, 9, 16)]:
            ey = yy - 1 if mm == 1 else yy
            amount = 7 * 25.9324 / 32 if yy == 2027 and mm == 1 else a[min(yy, 2040)]['div'] / 4
            schedule.append((date(ey, em, ed), date(yy, mm, dd), amount))
    cash = CASH0
    div = 0
    cumfcff = 0
    mincash = cash
    totalint = 0
    for y, f, t, dt in pieces(START, target):
        z = a[y]
        earn = cash * 0.025 * dt
        interest = DEBT * 0.035 * (1 - TAX) * dt
        pay = sum((v for ex, pd, v in schedule if t - dt / 2 <= (pd - START).days / 365.25 < t + dt / 2))
        cash += z['fcff'] * f - pay + earn - interest
        cumfcff += z['fcff'] * f
        mincash = min(mincash, cash)
        totalint += interest
    reserve = MINCASH
    owed = sum((v for ex, pd, v in schedule if ex <= target < pd))
    div = sum((v for ex, pd, v in schedule if ex >= START and pd <= target)) / SH
    receivable = sum((v for ex, pd, v in schedule if START <= ex <= target < pd)) / SH
    equity_bridge = cash - DEBT - reserve - OTHER - owed
    ev = 0
    future = []
    ht = (target - START).days / 365.25
    for y, f, t, dt in pieces(target, END):
        pv = a[y]['fcff'] * f / (1 + w) ** (t - ht)
        ev += pv
        future.append((t, pv))
    g, roic = terminal[name]
    g += gdelta
    nop = a[2040]['op'] * (1 - TAX) * 0.995
    terminal_cf = nop * (1 + g) * (1 - g / roic) - a[2040]['lease'] * (1 + g) + a[2040]['jvc']
    tv = terminal_cf / (w - g)
    tvpv = tv / (1 + w) ** ((END - target).days / 365.25)
    ev += tvpv
    eq = ev + equity_bridge
    px = eq / SH
    total = (px + div + receivable) / P0 - 1
    wealth = px + div + receivable
    return dict(name=name, h=h, w=w, eq=eq, px=px, div=div, total=total, cagr=(wealth / P0) ** (1 / h) - 1 if h else None, wealth=wealth, ev=ev, tvshare=tvpv / ev, cash=cash, reserve=reserve, bridge=equity_bridge, owed=owed, receivable=receivable, mincash=mincash, cumfcff=cumfcff, interest=totalint, terminal_cf=terminal_cf)

def main():
    results = {n: {h: value(n, h) for h in [0, 1, 3, 7]} for n in names}
    bands = {n: {h: [value(n, h, 0.11, -0.005), value(n, h, 0.085, 0.005)] for h in [0, 1, 3, 7]} for n in names}
    data = dict(annual={n: annual(n) for n in names}, results=results, bands=bands)
    pass
    for n in names:
        print(n, [(h, round(results[n][h]['px'], 1), round(results[n][h]['div'], 1), round(results[n][h]['total'] * 100, 1), [round(x['total'] * 100, 1) for x in bands[n][h]]) for h in [0, 1, 3, 7]])
    for h in [0, 1, 3, 7]:
        v = sum((p * results[n][h]['wealth'] for p, n in zip(probs, names)))
        print('MEAN', h, round(v, 2), 'CAGR', round(((v / P0) ** (1 / h) - 1) * 100, 2) if h else None, 'P12', round(v / 1.12 ** h, 2))
if __name__ == '__main__':
    main()