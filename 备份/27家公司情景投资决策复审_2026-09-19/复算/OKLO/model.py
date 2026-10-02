import math, json, copy
from pathlib import Path
T = 62
P0 = 38.0
N0 = 203.0
C0 = 3100.0
BASE = {'B': dict(mw=[0, 0, 75, 150, 225, 375, 600, 825, 1050, 1275, 1500, 1650, 1800, 1950, 2100, 2100, 2100, 2100, 2100, 2100], ppa=145, cf=0.9, op=43, maint=7, k0=8.0, k1=6.5, lev=0.5, rd=0.07, iso=150, fuel=100, eng=80, othercap=500, corp=100), 'O': dict(mw=[0, 75, 150, 300, 600, 900, 1500, 2100, 3000, 3900, 4800, 5700, 6600, 7500, 8400, 9300, 10200, 11100, 12000, 12900], ppa=140, cf=0.92, op=39, maint=6, k0=7.0, k1=5.5, lev=0.6, rd=0.065, iso=350, fuel=500, eng=120, othercap=2100, corp=160), 'T': dict(mw=[0, 75, 225, 525, 1050, 1800, 3000, 4500, 6500, 8500, 11000, 13500, 16000, 18500, 21000, 23500, 26000, 28500, 31000, 33500], ppa=145, cf=0.93, op=36, maint=6, k0=6.0, k1=4.5, lev=0.65, rd=0.06, iso=350, fuel=500, eng=120, othercap=2300, corp=180)}

def run(key, ke=0.12, changes=None, c0=C0, n0=N0):
    c = copy.deepcopy(BASE.get(key, BASE['B']))
    if key == 'L':
        c.update(mw=[0, 0] + c['mw'], delay=2)
    if changes:
        c.update(changes)
    rows = [dict(t=i, year=2026 + i, power=0.0, iso=0.0, fuel=0.0, eng=0.0, rev=0.0, ebit=0.0, da=0.0, capex=0.0, wc=0.0, credit=0.0, draw=0.0, principal=0.0, interest=0.0, debt=0.0, cash=0.0, raise_=0.0, div=0.0, shares=n0, cf=0.0, mw=0.0, tax=0.0, corp=0.0) for i in range(T + 1)]
    rows[0]['cash'] = c0
    if key in ('D', 'X'):
        end = 8 if key == 'D' else 5
        burn = [380, 380, 300, 230, 180, 130, 90, 60] if key == 'D' else [600, 850, 850, 650, 600]
        cash = c0
        for t in range(1, T + 1):
            r = rows[t]
            if t <= end:
                r['eng'] = (18 + 4 * t) * 1.02 ** t
                r['iso'] = max(0, t - 2) * 3 * 1.02 ** t
                r['rev'] = r['eng'] + r['iso']
                r['capex'] = burn[t - 1] * 0.45
                r['ebit'] = -(burn[t - 1] - r['capex'])
                r['cf'] = -burn[t - 1]
                cash = max(0, cash * 1.03 + r['cf'])
                if t == end:
                    r['div'] = cash + (80 if key == 'D' else 0)
                    if key == 'X':
                        r['div'] = 0
                    cash = 0
            r['cash'] = cash
    else:
        mw = c['mw']
        cohorts = []
        for j, total in enumerate(mw, 1):
            size = total - (mw[j - 2] if j > 1 else 0)
            if size <= 0:
                continue
            prev = total - size
            first = max(0, min(size, 150 - prev))
            serial = c['k0'] + (c['k1'] - c['k0']) * min(1, max(0, (j - 3 - c.get('delay', 0)) / 7))
            unit = (first * 12 + (size - first) * serial) / size
            unit *= c.get('capmult', 1)
            costs = []
            for offset, w in [(-2, 0.2), (-1, 0.4), (0, 0.4)]:
                u = max(1, j + offset)
                spend = size * unit * w * 1.02 ** u
                costs.append((u, spend))
                rows[u]['capex'] += spend
                rows[u]['draw'] += spend * c['lev'] * (size - first) / size
            totalcost = sum((x[1] for x in costs))
            debt = totalcost * c['lev'] * (size - first) / size
            startyear = 2026 + max(1, j - 2)
            cr = (0.3 if startyear <= 2033 else 0.225 if startyear == 2034 else 0.15 if startyear == 2035 else 0) * c.get('creditmult', 1)
            rows[j + 1]['credit'] += totalcost * cr * 0.95
            cohorts.append((j, size, totalcost, debt, cr))
            for t in range(j, min(T, j + 40) + 1):
                factor = 0.5 if t in (j, j + 40) else 1.0
                r = rows[t]
                infl = 1.02 ** t
                mwh = size * 8760 * c['cf'] * factor
                r['mw'] += size if t < j + 40 else 0
                price = c['ppa'] * (1 if t - j < 20 else c.get('renewal', 0.85))
                r['power'] += mwh * price * infl / 1000000.0
                r['ebit'] += mwh * (price - c['op'] - c['maint']) * infl / 1000000.0
                r['da'] += totalcost * (1 - cr / 2) / 40 * factor
                r['principal'] += debt / 25 if t < j + 25 else 0
                if t == j + 20:
                    r['capex'] += size * unit * 0.15 * infl
        prevdebt = 0.7
        priorrev = 0.0
        nol = 200.0
        otherassets = []
        for t in range(1, T + 1):
            r = rows[t]
            infl = 1.02 ** t
            fade = 1 if t <= 25 else max(0, (45 - t) / 20)
            r['eng'] = min(c['eng'], 20 + 6 * t) * infl * fade
            r['iso'] = c['iso'] * min(1, max(0, (t - 1) / 9)) ** 1.5 * infl * fade
            r['fuel'] = c['fuel'] * min(1, max(0, (t - 5) / 10)) ** 1.5 * infl * fade
            r['rev'] = r['power'] + r['eng'] + r['iso'] + r['fuel']
            fixed = max(220, c['corp']) if t <= 3 else c['corp']
            r['corp'] = (fixed + r['power'] / infl * 0.015) * infl
            if t > 25:
                r['corp'] *= max(fade, r['mw'] / max(mw))
            r['ebit'] += r['eng'] * 0.18 + r['iso'] * 0.35 + r['fuel'] * 0.3 - r['corp']
            oc = c['othercap'] * {1: 0.12, 2: 0.16, 3: 0.18, 4: 0.18, 5: 0.14, 6: 0.1, 7: 0.07, 8: 0.05}.get(t, 0) * infl
            r['capex'] += oc + 0.025 * (r['eng'] + r['iso'] + r['fuel'])
            if oc:
                otherassets.append((t, oc))
            r['da'] += sum((v / 20 for start, v in otherassets if start <= t < start + 20))
            r['ebit'] -= r['da']
            r['interest'] = (prevdebt + 0.5 * r['draw'] - 0.5 * r['principal']) * c['rd']
            r['debt'] = max(0, prevdebt + r['draw'] - r['principal'])
            if t == 1:
                r['principal'] += 0.7
                r['debt'] = max(0, r['debt'] - 0.7)
            prevdebt = r['debt']
            taxable = r['ebit'] - r['interest']
            used = min(nol, 0.8 * max(0, taxable))
            nol -= used
            if taxable < 0:
                nol -= taxable
            r['tax'] = max(0, taxable - used) * 0.25
            r['wc'] = 0.08 * (r['rev'] - priorrev)
            priorrev = r['rev']
            r['cf'] = r['ebit'] - r['tax'] + r['da'] - r['capex'] - r['wc'] - r['interest'] + r['draw'] - r['principal'] + r['credit']
        cash = c0
        quarters = []
        for t in range(1, T + 1):
            r = rows[t]
            for q in range(1, 5):
                cash = cash * 1.03 ** 0.25 + (r['cf'] - r['credit']) / 4 + (r['credit'] if q == 4 else 0)
                need = max(0, 300 - cash)
                gross = need / 0.985
                cash += need
                r['raise_'] += gross
                dividend = 0.0
                if q == 4:
                    reserve = 300 + sum((max(0, -rows[u]['cf']) for u in range(t + 1, min(T, t + 3) + 1)))
                    if t >= 8 and cash > reserve:
                        dividend = cash - reserve
                        cash = reserve
                    if t == T:
                        dividend += cash
                        cash = 0
                    r['div'] = dividend
                quarters.append(dict(time=t - 1 + q / 4, raise_=gross, div=dividend, cash=cash))
            r['cash'] = cash
    discount = c.get('issue_discount', 0.25)
    if key in ('D', 'X'):
        quarters = [dict(time=i / 4, raise_=0.0, div=rows[i // 4]['div'] if i % 4 == 0 else 0.0) for i in range(1, 4 * T + 1)]
    eq = [0.0] * (4 * T + 1)
    for i in range(4 * T - 1, -1, -1):
        q = quarters[i]
        eq[i] = (eq[i + 1] + q['div'] - q['raise_'] / (1 - discount)) / (1 + ke) ** 0.25
    n = n0
    feasible = True
    dps = 0
    rows[0].update(equity=eq[0], value=max(0, eq[0] / n), dps=0.0, cumdps=0.0)
    for i, q in enumerate(quarters, 1):
        if q['raise_']:
            fraction = q['raise_'] / ((1 - discount) * eq[i]) if eq[i] > 0 else 2
            if not 0 <= fraction < 1:
                feasible = False
                n = float('inf')
            else:
                n = n / (1 - fraction)
        q['shares'] = n
        q['equity'] = eq[i]
        q['dps'] = q['div'] / n
        if i % 4:
            continue
        t = i // 4
        r = rows[t]
        r['shares'] = n
        r['equity'] = eq[i]
        r['value'] = max(0, eq[i] / n)
        r['dps'] = r['div'] / n
        dps += r['dps']
        r['cumdps'] = dps
        if t:
            r['totalreturn'] = (r['value'] + dps) / P0 - 1
            r['annualreturn'] = ((r['value'] + dps) / P0) ** (1 / t) - 1 if r['value'] + dps > 0 else -1
    direct = sum((r['dps'] / (1 + ke) ** r['t'] for r in rows[1:]))
    if feasible and abs(direct - rows[0]['value']) > 1e-06:
        raise AssertionError((key, direct, rows[0]['value']))
    return dict(key=key, params=c, ke=ke, feasible=feasible, rows=rows, quarters=quarters, direct=direct)
if __name__ == '__main__':
    results = {k: run(k) for k in ['X', 'D', 'L', 'B', 'O', 'T']}
    for k, m in results.items():
        print(k, 'feasible', m['feasible'], 'value', round(m['rows'][0]['value'], 2), 'new equity', round(sum((r['raise_'] for r in m['rows'])), 1), 'maxdebt', round(max((r['debt'] for r in m['rows'])), 1))
        for t in [1, 3, 7, 10, 20]:
            r = m['rows'][t]
            print(t, {f: round(r[f], 2) for f in ['mw', 'rev', 'ebit', 'capex', 'cash', 'debt', 'shares', 'value', 'cumdps']})