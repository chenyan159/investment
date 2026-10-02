import copy, json, math
from pathlib import Path
P0 = 152.71
KNOTS = [1, 3, 7, 12, 20]
DATA = {'D': {'C': ([20, 24, 29, 30, 27], [0.3, 0.27, 0.23, 0.2, 0.16]), 'D': ([0.1, 0.4, 1.5, 2, 2], [-3, -1, 0.05, 0.1, 0.1]), 'S': ([4, 4.5, 5, 5, 4], [0.22, 0.22, 0.2, 0.18, 0.15]), 'G': ([22, 24, 25, 20, 15], [0.15, 0.12, 0.1, 0.08, 0.07]), 'A': ([4, 5, 7, 7, 6], [-0.75, -0.3, 0.05, 0.07, 0.05]), 'O': ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]), 'rd': [10, 5, 3, 2, 1], 'cap': [48, 18, 12, 9, 7], 'da': [16, 19, 12, 9, 7], 'g': 0.0, 'issue': 20}, 'B': {'C': ([23.648, 33.8, 50.04, 62.984, 69.8], [0.35, 0.35, 0.32, 0.3, 0.28]), 'D': ([0.3, 2, 9, 18, 22], [-1, 0.05, 0.3, 0.32, 0.28]), 'S': ([5, 8, 15, 25, 30], [0.3, 0.32, 0.33, 0.3, 0.27]), 'G': ([40, 70, 110, 150, 180], [0.32, 0.3, 0.25, 0.23, 0.2]), 'A': ([6, 13, 32, 60, 85], [-0.2, 0.1, 0.25, 0.3, 0.27]), 'O': ([0, 0.1, 1, 4, 6], [0, -2, 0.05, 0.15, 0.15]), 'rd': [13, 17, 22, 26, 28], 'cap': [60, 65, 75, 88, 90], 'da': [18, 30, 52, 64, 70], 'g': 0.025, 'issue': 60}, 'U': {'C': ([25, 40, 84, 112, 135], [0.38, 0.39, 0.38, 0.36, 0.32]), 'D': ([0.4, 4, 18, 40, 55], [-0.75, 0.2, 0.35, 0.38, 0.32]), 'S': ([5.5, 10, 24, 38, 45], [0.32, 0.38, 0.4, 0.36, 0.32]), 'G': ([48, 105, 220, 330, 410], [0.37, 0.38, 0.34, 0.3, 0.26]), 'A': ([7, 20, 65, 135, 200], [0, 0.22, 0.34, 0.36, 0.32]), 'O': ([0, 0.2, 5, 18, 30], [0, -1, 0.15, 0.25, 0.23]), 'rd': [15, 22, 32, 45, 52], 'cap': [65, 95, 130, 160, 180], 'da': [19, 38, 83, 115, 145], 'g': 0.025, 'issue': 90}, 'X': {'C': ([25, 41, 81, 115, 140], [0.38, 0.39, 0.38, 0.36, 0.32]), 'D': ([0.4, 3, 25, 60, 90], [-0.75, 0.1, 0.4, 0.42, 0.35]), 'S': ([5.5, 11, 28, 60, 85], [0.32, 0.38, 0.45, 0.4, 0.35]), 'G': ([48, 110, 260, 520, 760], [0.37, 0.38, 0.38, 0.35, 0.3]), 'A': ([8, 25, 100, 300, 530], [0.05, 0.25, 0.4, 0.42, 0.36]), 'O': ([0, 0.3, 12, 120, 300], [0, -1, 0.15, 0.32, 0.3]), 'rd': [16, 25, 50, 90, 145], 'cap': [70, 110, 220, 390, 560], 'da': [19, 40, 110, 255, 440], 'g': 0.03, 'issue': 100}}

def ip(a, t):
    if t <= 1:
        return a[0]
    for j in range(1, len(KNOTS)):
        if t <= KNOTS[j]:
            f = (t - KNOTS[j - 1]) / (KNOTS[j] - KNOTS[j - 1])
            return a[j - 1] * (1 - f) + a[j] * f
    return a[-1]

def run(key, ke=0.12, gshift=0, capmult=1, cloudmult=1, orb=None, cash0=88, issue_mult=1, extra_cap=None, nol0=12, rdmult=1, apps=None):
    d = copy.deepcopy(DATA[key])
    if orb:
        other = DATA[orb]
        d['O'] = other['O']
    if apps:
        d['A'] = DATA[apps]['A']
    cash = cash0
    debt = 39.0
    shares = 14.25
    nol = nol0
    lastrev = 40.0
    cumdiv = 0.0
    out = []
    for t in range(1, 21):
        rev = {k: ip(d[k][0], t) * (cloudmult if k == 'G' else 1) for k in 'CDSGAO'}
        op = {k: rev[k] * ip(d[k][1], t) for k in rev}
        op['G'] = ip(d['G'][0], t) * ip(d['G'][1], t) + ip(d['G'][0], t) * (cloudmult - 1) * 0.8
        rd = ip(d['rd'], t) * rdmult
        cap = ip(d['cap'], t) * capmult
        base_da = ip(d['da'], t)
        depreciation_shift = base_da * (capmult - 1) * min(t / 5, 1)
        da = base_da + depreciation_shift
        if orb:
            rd += ip([0, 1, 5, 12, 20], t)
            cap += ip([0, 3, 18, 75, 140], t)
            da += ip([0, 0, 6, 40, 95], t)
        if extra_cap:
            cap += ip(extra_cap, t)
        if apps:
            rd += ip([1, 3, 8, 20, 40], t)
            cap += ip([1, 3, 12, 40, 80], t)
            da += ip([0, 1, 7, 25, 55], t)
        revenue = sum(rev.values())
        ebit = sum(op.values()) - rd - depreciation_shift
        interest = 0.062 * debt
        cashint = 0.032 * cash
        taxable = ebit - interest + cashint
        use = min(nol, max(taxable, 0) * 0.8)
        nol -= use
        if taxable < 0:
            nol += -taxable
        tax = 0.23 * max(taxable - use, 0)
        wc = 0.035 * (revenue - lastrev)
        lastrev = revenue
        spectrum = 0.8 if t == 1 else 8.913 if t == 2 else 0.0
        if t == 2:
            shares += 0.2618
        principal = min(debt, {1: 2.7, 2: 3.1, 3: 3.5, 4: 3.7, 5: 8.0, 7: 6.0, 10: 6.0, 20: 2.5}.get(t, 0))
        debt -= principal
        fcfe = ebit + da - tax - cap - wc - interest + cashint - spectrum - principal
        cash_pre = cash + fcfe
        floor = 10 + 0.05 * revenue
        need = max(0, floor - cash_pre)
        issuepx = d['issue'] * issue_mult
        shares += need / issuepx
        cash = cash_pre + need
        div = max(0, cash - floor) if t >= 11 else 0.0
        cash -= div
        divps = div / shares
        cumdiv += divps
        out.append(dict(t=t, R=revenue, rev=rev, op=op, rd=rd, EBIT=ebit, DA=da, tax=tax, cap=cap, wc=wc, interest=interest, cashint=cashint, spectrum=spectrum, principal=principal, FCFE=fcfe, Cpre=cash_pre, C=cash, D=debt, N=shares, raise_=need, div=div, divps=divps, cumdiv=cumdiv, nol=nol))
    z = out[-1]
    g = d['g'] + gshift
    nopat = z['EBIT'] * (1 + g) * 0.77
    fcf = nopat * (1 - g / 0.12)
    ev = fcf / (ke - g)
    debt_tail = sum((z['D'] * 0.0665 * 0.77 / (1 + ke) ** n for n in range(1, 11))) + z['D'] / (1 + ke) ** 10
    terminal = max(0, ev + z['C'] - debt_tail) / z['N']
    prices = {20: terminal}
    for t in range(19, -1, -1):
        prices[t] = (prices[t + 1] + out[t]['divps']) / (1 + ke)
    pvterm = terminal / (1 + ke) ** 20
    return dict(key=key, ke=ke, rows=out, prices=prices, terminal=terminal, tvshare=pvterm / prices[0], equity0=prices[0] * 14.25)

def brief(m):
    print(m['key'], 'P0', round(m['prices'][0], 2), 'TV%', round(m['tvshare'] * 100, 1), 'raise', round(sum((x['raise_'] for x in m['rows'])), 2))
    for t in [1, 2, 3, 7, 12, 20]:
        x = m['rows'][t - 1]
        v = m['prices'][t]
        w = v + x['cumdiv']
        print(t, *[round(x[k], 2) for k in ['R', 'EBIT', 'FCFE', 'C', 'D', 'N', 'raise_']], 'p', round(v, 2), 'div', round(x['cumdiv'], 2), 'ret', round(w / P0 - 1, 3))
for key in DATA:
    brief(run(key))