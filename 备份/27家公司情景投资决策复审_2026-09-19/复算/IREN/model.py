import json, math, copy
from pathlib import Path
P0 = 46.68
CFG = {'受损': dict(mw=[220, 390, 470, 470, 440, 410, 390, 370, 350, 330, 310, 290, 270, 250, 230], price=[16, 14, 12, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], growth=[13, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], margin=0.66, sg=0.35, rate=0.105, ke=0.16, issue=[22, 18, 18, 20, 20, 20, 20, 20], loan=0.4, ms=[1.1, 1.65, 1.8, 1.8, 1.4, 0.6, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1], nv=[0.2, 0.5, 0.6, 0.6, 0.5, 0.3, 0.25, 0.2, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], soft=[0.08, 0.1, 0.1, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0, 0], maint=6.8), '基准': dict(mw=[300, 650, 900, 1080, 1220, 1370, 1475, 1550, 1600, 1625, 1650, 1650, 1650, 1650, 1650], price=[20, 19, 18, 17, 16, 15.5, 15, 14.5, 14, 13.5, 13, 13, 13, 13, 13], growth=[23.5, 11.5, 8, 5, 4, 3, 2, 1.5, 1, 0.5, 0, 0, 0, 0, 0], margin=0.78, sg=0.45, rate=0.085, ke=0.14, issue=[40, 44, 48, 50, 52, 55, 55, 55], loan=0.65, ms=[1.7, 1.94, 1.94, 1.94, 1.7, 1.2, 1.15, 1.1, 1.05, 1, 0.95, 0.9, 0.9, 0.9, 0.9], nv=[0.4, 0.68, 0.68, 0.68, 0.68, 0.5, 0.45, 0.42, 0.4, 0.38, 0.35, 0.35, 0.35, 0.35, 0.35], soft=[0.12, 0.16, 0.22, 0.28, 0.34, 0.4, 0.45, 0.48, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], maint=6.0), '乐观': dict(mw=[340, 780, 1200, 1550, 1850, 2100, 2300, 2450, 2550, 2600, 2650, 2650, 2650, 2650, 2650], price=[22, 22, 21, 20, 19, 18, 17.5, 17, 16.5, 16, 15.5, 15, 15, 15, 15], growth=[26, 18, 15, 12, 10, 8, 6, 4, 3, 2, 1, 0, 0, 0, 0], margin=0.8, sg=0.5, rate=0.075, ke=0.13, issue=[52, 65, 80, 90, 100, 110, 110, 110], loan=0.72, ms=[1.85, 1.94, 1.94, 1.94, 1.8, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25, 1.2, 1.2, 1.2, 1.2], nv=[0.48, 0.68, 0.68, 0.68, 0.68, 0.6, 0.55, 0.52, 0.5, 0.48, 0.45, 0.45, 0.45, 0.45, 0.45], soft=[0.15, 0.23, 0.35, 0.5, 0.65, 0.8, 0.9, 1, 1.1, 1.15, 1.2, 1.2, 1.2, 1.2, 1.2], maint=5.6), '突破': dict(mw=[350, 850, 1400, 2000, 2600, 3100, 3500, 3800, 4000, 4100, 4200, 4200, 4200, 4200, 4200], price=[23, 23, 23, 22, 22, 21, 20, 19.5, 19, 18.5, 18, 17.5, 17, 17, 17], growth=[27, 23, 24, 23, 20, 17, 13, 10, 7, 5, 3, 0, 0, 0, 0], margin=0.81, sg=0.65, rate=0.07, ke=0.13, issue=[60, 85, 110, 130, 150, 170, 170, 170], loan=0.75, ms=[1.85, 1.94, 1.94, 1.94, 1.8, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25, 1.2, 1.2, 1.2, 1.2], nv=[0.5, 0.68, 0.68, 0.68, 0.68, 0.6, 0.55, 0.52, 0.5, 0.48, 0.45, 0.45, 0.45, 0.45, 0.45], soft=[0.15, 0.25, 0.5, 0.9, 1.5, 2.1, 2.8, 3.2, 3.5, 3.8, 4, 4.1, 4.2, 4.2, 4.2], maint=5.4)}
CONV = [(4, 0.233389, 13.64, 20.98, 0.035), (4, 0.21231, 16.81, 25.86, 0.0325), (5, 1, 85.63, 120.18, 0), (6, 1.15, 51.4, 82.24, 0.0025), (7, 1.15, 51.4, 82.24, 0.01), (8, 3, 73.07, 110.3, 0.01)]

def model(name, price_factor=1, cap_factor=1, ke_delta=0, loan_delta=0, cash_delta=0, software=None, issue_factor=1, renew_factor=1, forward=True):
    c = copy.deepcopy(CFG[name])
    n = 0.394058648
    cash = 4.8256 + cash_delta
    restricted = 1.2
    loans = [dict(balance=2.353746, repay=2.353746 / 4, rate=0.075)]
    conv = copy.deepcopy(CONV)
    advances = []
    taxloss = 1.0
    rows = []
    nvidia = False
    for i in range(15):
        y = i + 1
        mw = c['mw'][i]
        ip = c['issue'][min(i, 7)] * issue_factor
        ms = c['ms'][i]
        nv = c['nv'][i]
        ms_mw = min(200, ms / 1.94 * 200) if y == 1 else 200
        nv_mw = min(60, nv / 0.68 * 60) if y == 1 else 60
        other = max(0, mw - ms_mw - nv_mw) * c['price'][i] / 1000 * price_factor
        soft = software[i] if software is not None else c['soft'][i]
        mining = 0.06 if y == 1 else 0
        revenue = ms + nv + other + soft + mining
        corp = c['sg'] + 0.03 * (ms + nv + other)
        ebitda = (ms + nv + other) * c['margin'] + soft * 0.3 + mining * 0.4 - corp
        ramp = [0.12, 0.2, 0.4, 0.65, 0.85, 1][min(i, 5)]
        maintenance = mw * c['maint'] / 1000 * ramp * cap_factor * renew_factor
        growth = c['growth'][i] * cap_factor
        capex = maintenance + growth
        da = (mw * 0.0065 + soft * 0.05) * cap_factor
        grant = 0.018198656 / 4 if y <= 4 else 0
        othergrant = 0.004 if y <= 4 else n * 0.01
        grant += othergrant
        sbc = grant * ip
        n += grant
        if y == 4 and forward:
            n -= 0.014519103
        ebit = ebitda - da - sbc
        interest = sum((x['balance'] * x['rate'] for x in loans)) + sum((f * cp for _, f, k, h, cp in conv))
        principal = 0
        for l in loans:
            r = min(l['balance'], l['repay'])
            principal += r
            l['balance'] -= r
        draw = growth * 0.72 * max(0, c['loan'] + loan_delta)
        mac = min(2.4, draw) if y == 1 else 0
        if mac:
            loans.append(dict(balance=mac, repay=mac / 2.5, rate=0.09))
        if draw > mac:
            loans.append(dict(balance=draw - mac, repay=(draw - mac) / 5, rate=c['rate']))
        interest += mac * 0.09 * 0.5 + (draw - mac) * c['rate'] * 0.5
        adv = growth * 0.72 * (0.2 if name == '受损' else 0.25)
        offsets = (1.102546 / 4 if y <= 4 else 0) + (1.94 / 3 if 3 <= y <= 5 else 0)
        offsets += sum((a / 4 for yr, a in advances if 1 <= y - yr <= 4))
        advances.append((y, adv))
        taxable = ebit - interest
        tax = max(0, taxable - taxloss) * 0.25
        taxloss = max(0, taxloss - taxable)
        wc = max(0, revenue - (rows[-1]['rev'] if rows else 0.9)) * 0.025
        netconv = 0
        callcash = 0
        convshares = 0
        for due, f, k, h, cp in list(conv):
            if due == y:
                netconv += f
                if ip > k:
                    convshares += f / k
                    n += f / k
                    callcash += f / k * max(0, min(ip, h) - k)
                else:
                    principal += f
                conv.remove((due, f, k, h, cp))
        nv_cash = 0
        if y <= 5 and (not nvidia) and (ip > 70):
            nv_cash = 2.1
            n += 0.03
            nvidia = True
        optioncash = 0
        if y == 5 and ip > 75:
            optioncash = 0.36
            n += 0.0048
        release = restricted if y == 1 else 0
        restricted -= release
        free = ebitda - interest - tax - capex - wc + adv - offsets
        before = cash + free + draw - principal + callcash + nv_cash + optioncash + release
        floor = max(0.75, revenue * 0.08)
        eq = max(0, floor - before)
        newshares = eq / (ip * 0.98)
        n += newshares
        cash = before + eq
        sweep = 0
        if y >= 4:
            sweep = min(max(0, cash - floor), sum((l['balance'] for l in loans)))
            left = sweep
            for l in loans:
                paid = min(left, l['balance'])
                l['balance'] -= paid
                left -= paid
            cash -= sweep
            principal += sweep
        div = 0
        if y >= 8:
            div = max(0, cash - floor)
            cash -= div
        debt = sum((l['balance'] for l in loans)) + sum((f for _, f, k, h, cp in conv))
        defbal = 3.042546 + sum((a for _, a in advances)) - sum((r['offset'] for r in rows)) - offsets
        rows.append(dict(y=y, mw=mw, ms=ms, nv=nv, other=other, soft=soft, mining=mining, rev=revenue, ebitda=ebitda, corp=corp, sbc=sbc, da=da, ebit=ebit, tax=tax, interest=interest, capex=capex, growth=growth, maint=maintenance, wc=wc, advance=adv, offset=offsets, deferred=defbal, fcfe=free, draw=draw, repay=principal, equity=eq, issue=ip, n=n, cash=cash, debt=debt, div=div, dps=div / n, pre_eq_cash=before, callcash=callcash, convshares=convshares, nv_cash=nv_cash, optioncash=optioncash, release=release))
        if name == '受损' and y == 2:
            rows[-1]['unfunded'] = eq - 1.0
            rows[-1]['equity'] = 1.0
            rows[-1]['n'] -= max(0, eq - 1.0) / (ip * 0.98)
            rows[-1]['cash'] -= max(0, eq - 1.0)
            return dict(name=name, ke=c['ke'] + ke_delta, rows=rows, values=[0.0] * 16, terminal=0.0, terminal_fraction=0.0, default_year=2)
    r = rows[-1]
    terminal_cash = max(0, r['ebitda'] - 0.25 * max(0, r['ebitda'] - r['da'] - r['sbc']) - r['maint'])
    ke = c['ke'] + ke_delta
    terminal = terminal_cash / r['n'] / (ke + 0.01)
    vals = [0.0] * 16
    vals[15] = terminal
    for y in range(14, -1, -1):
        vals[y] = (vals[y + 1] + rows[y]['dps']) / (1 + ke)
    return dict(name=name, ke=ke, rows=rows, values=vals, terminal=terminal, terminal_fraction=terminal / (1 + ke) ** 15 / max(vals[0], 1e-09))

def summary(m):
    return dict(name=m['name'], now=m['values'][0], terminal_fraction=m['terminal_fraction'], equity=sum((r['equity'] for r in m['rows'])), points=[dict(y=t, value=m['values'][t], wealth=m['values'][t] + sum((r['dps'] for r in m['rows'][:t])), ret=(m['values'][t] + sum((r['dps'] for r in m['rows'][:t]))) / P0 - 1, annual=((m['values'][t] + sum((r['dps'] for r in m['rows'][:t]))) / P0) ** (1 / t) - 1, n=m['rows'][t - 1]['n'], equityvalue=m['values'][t] * m['rows'][t - 1]['n'], cash=m['rows'][t - 1]['cash'], debt=m['rows'][t - 1]['debt'], rev=m['rows'][t - 1]['rev'], ebit=m['rows'][t - 1]['ebit']) for t in (1, 3, 7) if t <= len(m['rows'])])
if __name__ == '__main__':
    for k in CFG:
        print(json.dumps(summary(model(k)), ensure_ascii=False))