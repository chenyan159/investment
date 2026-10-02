import json, copy, math
from pathlib import Path
P0 = 222.27
S0 = 24.25
NWC0 = 85.0
CASH0 = 56.586
DEBT0 = 34.352
KEYS = ['C', 'N', 'X', 'G', 'P']
NODES = [1, 3, 7, 15]
DATA = {'受损': dict(p=0.25, rev=[[320, 77, 10, 30, 3], [244, 61, 13, 29, 3], [220, 54, 24, 28, 4], [160, 42, 30, 23, 5]], mar=[[0.53, 0.5, 0.05, 0.27, -0.2], [0.4, 0.42, 0.1, 0.25, -0.1], [0.35, 0.38, 0.2, 0.24, 0.05], [0.3, 0.33, 0.25, 0.22, 0.1]], wc=0.26, cap=0.035, da=0.02, g=0.0, roic=0.15, assets=25.0, invrecover=0.5, loss={1: 15, 2: 20, 3: 12, 4: 10, 5: 10, 6: 5, 7: 3}, buy=0.2), '基准': dict(p=0.45, rev=[[410, 100, 20, 36, 4], [575, 153, 48, 37, 7], [700, 190, 100, 42, 18], [860, 240, 210, 50, 40]], mar=[[0.64, 0.6, 0.15, 0.32, -0.1], [0.61, 0.58, 0.3, 0.31, 0.1], [0.54, 0.52, 0.4, 0.3, 0.2], [0.44, 0.44, 0.43, 0.28, 0.25]], wc=0.2, cap=0.035, da=0.02, g=0.025, roic=0.2, assets=60.0, invrecover=0.8, loss={1: 2, 2: 3, 3: 3, 4: 2, 5: 2, 6: 2, 7: 2}, buy=0.4), '乐观': dict(p=0.23, rev=[[450, 116, 24, 36, 4], [775, 224, 73, 39, 9], [1090, 320, 190, 48, 32], [1300, 390, 380, 65, 65]], mar=[[0.66, 0.62, 0.18, 0.33, -0.1], [0.64, 0.61, 0.35, 0.33, 0.15], [0.59, 0.57, 0.47, 0.32, 0.25], [0.5, 0.5, 0.48, 0.3, 0.28]], wc=0.18, cap=0.04, da=0.025, g=0.03, roic=0.23, assets=85.0, invrecover=1.0, loss={1: 1, 2: 1, 3: 1}, buy=0.4), '突破': dict(p=0.07, rev=[[465, 118, 27, 36, 4], [940, 260, 150, 40, 10], [1450, 420, 520, 55, 55], [1850, 550, 1200, 85, 115]], mar=[[0.66, 0.62, 0.18, 0.33, -0.1], [0.64, 0.6, 0.38, 0.33, 0.15], [0.59, 0.56, 0.5, 0.32, 0.28], [0.52, 0.5, 0.54, 0.3, 0.32]], wc=0.2, cap=0.05, da=0.03, g=0.03, roic=0.25, assets=100.0, invrecover=1.0, loss={1: 1, 2: 2, 3: 2, 4: 2}, buy=0.35)}

def interp(rows, y):
    if y <= 1:
        return rows[0][:]
    for i in range(1, len(NODES)):
        if y <= NODES[i]:
            w = (y - NODES[i - 1]) / (NODES[i] - NODES[i - 1])
            return [a + (b - a) * w for a, b in zip(rows[i - 1], rows[i])]
    return rows[-1][:]

def model(name, rate=0.11, data=None, revscale=1.0, margindelta=0.0, delay=False, buypricefactor=1.0):
    d = copy.deepcopy(data or DATA[name])
    rows = []
    nwc = NWC0
    opreserve = 20.0
    for y in range(1, 16):
        nodeyear = max(1, y - 1) if delay and y > 1 else y
        rev = [x * revscale for x in interp(d['rev'], nodeyear)]
        mar = [x + margindelta for x in interp(d['mar'], nodeyear)]
        R = sum(rev)
        E = sum((x * m for x, m in zip(rev, mar)))
        tax = 0.18
        nwcnew = R * d['wc']
        dwc = nwcnew - nwc
        nwc = nwcnew
        da = R * d['da']
        cap = R * d['cap']
        loss = d['loss'].get(y, 0.0)
        fcf = E * (1 - tax) + da - cap - dwc - loss
        inv = {1: 21.0, 2: 2.0, 3: 2.0}.get(y, 0.0)
        acq = 11.9 if y == 1 else 0.0
        newreserve = max(20.0, 0.04 * R)
        dreserve = newreserve - opreserve
        opreserve = newreserve
        adjfcf = fcf - inv * (1 - d['invrecover']) - acq - dreserve
        rows.append(dict(y=y, rev=rev, mar=mar, R=R, E=E, tax=E * tax, da=da, cap=cap, dwc=dwc, loss=loss, fcf=fcf, inv=inv, acq=acq, dreserve=dreserve, adjfcf=adjfcf))
    last = rows[-1]
    term = last['E'] * 0.82 * (1 + d['g']) * (1 - d['g'] / d['roic']) / (rate - d['g'])
    ev = []
    for t in range(16):
        ev.append(sum((row['adjfcf'] / (1 + rate) ** (row['y'] - t) for row in rows if row['y'] > t)) + term / (1 + rate) ** (15 - t))
    cash = CASH0
    debt = DEBT0
    assets = d['assets']
    shares = S0
    divcum = 0.0
    buycum = 0.0
    mincash = cash
    minreserve = cash - 20.0
    v0 = (ev[0] + cash - 20.0 + assets - debt) / shares
    prevreserve = 20.0
    for row in rows:
        y = row['y']
        debt_before = debt
        cash_before = cash
        principal = {1: 1.986, 2: 4.75, 3: 3.5, 4: 1.5, 5: 5.25, 7: 3.5, 10: 4.0}.get(y, 0.0)
        principal = min(principal, debt)
        interest = debt * 0.045 * 0.82
        cashinterest = max(0, cash - prevreserve) * 0.03
        owner = row['fcf'] - row['inv'] - row['acq'] - interest + cashinterest - principal
        assets += row['inv'] * d['invrecover']
        debt -= principal
        divps = 0.75 if y == 1 else 1.0
        olddiv = S0 * 0.25 if y == 1 else 0.0
        div = divps * shares
        divcum += divps
        reserve = max(20.0, 0.04 * row['R'])
        buy = max(0.0, owner - div - olddiv) * d['buy']
        available = cash + owner - div - olddiv - reserve
        buy = min(buy, max(0.0, available))
        cashpre = cash + owner - div - olddiv
        eqpre = ev[y] + cashpre - reserve + assets - debt
        buyprice = eqpre / shares * buypricefactor
        retired = buy / buyprice if buyprice > 0 else 0.0
        shares -= retired
        cash = cashpre - buy
        buycum += buy
        equity = ev[y] + cash - reserve + assets - debt
        value = equity / shares
        row.update(EV=ev[y], cash=cash, reserve=reserve, debt=debt, assets=assets, shares=shares, buy=buy, buycum=buycum, divps=divps, divcum=divcum, olddiv=olddiv, principal=principal, interest=interest, cashinterest=cashinterest, owner=owner, equity=equity, value=value, wealth=value + divcum, ret=(value + divcum) / P0 - 1, cagr=((value + divcum) / P0) ** (1 / y) - 1, buyprice=buyprice)
        assert abs(cash - (cash_before + owner - div - olddiv - buy)) < 1e-08
        assert cash >= reserve - 1e-08 and shares > 0 and (debt >= -1e-08)
        mincash = min(mincash, cash)
        minreserve = min(minreserve, cash - reserve)
        prevreserve = reserve
    v0 -= 0.25
    return dict(name=name, p=d['p'], rate=rate, v0=v0, ev0=ev[0], terminal=term, terminalshare=term / (1 + rate) ** 15 / ev[0], post7share=(sum((r['adjfcf'] / (1 + rate) ** r['y'] for r in rows if r['y'] > 7)) + term / (1 + rate) ** 15) / ev[0], rows=rows, mincash=mincash, minreserve=minreserve)

def summarize(m):
    return dict(name=m['name'], v0=round(m['v0'], 2), tvshare=round(m['terminalshare'], 3), post7=round(m['post7share'], 3), targets=[{k: round(m['rows'][i - 1][k], 3) for k in ['y', 'R', 'E', 'fcf', 'cash', 'debt', 'shares', 'equity', 'value', 'divcum', 'ret', 'cagr']} for i in [1, 3, 7]])
if __name__ == '__main__':
    out = {k: model(k) for k in DATA}
    for m in out.values():
        print(json.dumps(summarize(m), ensure_ascii=False))
    print('weighted v0', sum((x['p'] * x['v0'] for x in out.values())))
    for t in [1, 3, 7]:
        w = sum((x['p'] * x['rows'][t - 1]['wealth'] for x in out.values()))
        print('weighted horizon', t, w, w / P0 - 1, (w / P0) ** (1 / t) - 1)