import math, json, copy
P0 = 493.78
N = 7.45
C0 = 76.843
MINC = 25.0
DEBT = 46.136
K = [1, 3, 7, 10, 15]
UNITS = ['Azure', 'M365云', '生产力与服务器许可', '行业解决方案', 'Frontier与支持', '搜索与广告', 'Xbox', 'Windows与设备']
R0 = [101.938, 100.299, 37.285, 20.345, 8.26, 24.835, 21.79, 17.087]
S = {'受损': dict(p=0.25, rev=[[140, 160, 180, 170, 145], [111, 122, 132, 135, 130], [35, 29, 20, 15, 10], [21.5, 23, 25, 26, 25], [9, 9, 10, 10, 10], [26, 26, 26, 25, 23], [20, 18, 16, 14, 12], [13.5, 13, 12, 11, 9]], mar=[[0.28, 0.23, 0.24, 0.22, 0.2], [0.58, 0.54, 0.49, 0.46, 0.43], [0.68, 0.64, 0.55, 0.5, 0.45], [0.38, 0.35, 0.33, 0.32, 0.3], [0.18, 0.16, 0.15, 0.15, 0.15], [0.36, 0.33, 0.3, 0.28, 0.26], [0.12, 0.1, 0.08, 0.08, 0.08], [0.29, 0.27, 0.25, 0.23, 0.21]], cap=[170, 130, 85, 65, 50], da=[53, 74, 64, 52, 39], asset=20, divg=0, g=0.0, roic=0.1), '基准': dict(p=0.45, rev=[[155, 255, 460, 580, 720], [118, 155, 230, 280, 340], [36, 33, 27, 23, 20], [23, 29, 45, 60, 80], [9.3, 11, 15, 18, 23], [27.5, 33, 43, 49, 57], [22, 24, 28, 31, 35], [14, 14.5, 16, 17, 19]], mar=[[0.35, 0.37, 0.39, 0.38, 0.36], [0.61, 0.62, 0.62, 0.6, 0.58], [0.7, 0.69, 0.65, 0.6, 0.55], [0.42, 0.45, 0.48, 0.48, 0.46], [0.2, 0.21, 0.23, 0.23, 0.23], [0.4, 0.41, 0.42, 0.42, 0.4], [0.16, 0.18, 0.2, 0.21, 0.2], [0.32, 0.33, 0.34, 0.34, 0.32]], cap=[175, 190, 210, 225, 250], da=[53, 84, 135, 160, 195], asset=120, divg=0.07, g=0.03, roic=0.16), '乐观': dict(p=0.23, rev=[[160, 290, 600, 850, 1200], [123, 180, 310, 405, 560], [36, 34, 30, 27, 22], [24, 34, 62, 85, 125], [9.5, 12, 18, 23, 32], [28, 36, 52, 65, 85], [22, 26, 35, 40, 50], [14, 15.5, 19, 22, 26]], mar=[[0.36, 0.41, 0.44, 0.43, 0.41], [0.61, 0.64, 0.65, 0.64, 0.61], [0.7, 0.7, 0.67, 0.63, 0.58], [0.43, 0.48, 0.52, 0.53, 0.5], [0.21, 0.23, 0.26, 0.26, 0.25], [0.4, 0.43, 0.46, 0.46, 0.43], [0.17, 0.21, 0.25, 0.25, 0.23], [0.32, 0.35, 0.37, 0.37, 0.34]], cap=[178, 225, 300, 370, 450], da=[55, 90, 175, 235, 310], asset=190, divg=0.1, g=0.03, roic=0.18), '突破': dict(p=0.07, rev=[[162, 315, 780, 1200, 2000], [125, 200, 440, 640, 1000], [36, 33, 26, 22, 16], [24, 38, 95, 150, 270], [9.5, 12.5, 22, 31, 48], [28, 36, 50, 65, 85], [22, 24, 29, 32, 38], [14, 14.5, 16, 18, 21]], mar=[[0.34, 0.4, 0.47, 0.47, 0.44], [0.6, 0.64, 0.68, 0.68, 0.63], [0.7, 0.69, 0.65, 0.6, 0.55], [0.42, 0.48, 0.56, 0.56, 0.53], [0.2, 0.23, 0.28, 0.28, 0.26], [0.4, 0.41, 0.42, 0.42, 0.4], [0.16, 0.18, 0.2, 0.21, 0.2], [0.32, 0.33, 0.34, 0.34, 0.32]], cap=[190, 280, 440, 620, 950], da=[55, 104, 245, 360, 620], asset=300, divg=0.12, g=0.03, roic=0.18)}

def interp(a, t):
    if t <= 1:
        return a[0]
    for i in range(1, len(K)):
        if t <= K[i]:
            return a[i - 1] + (a[i] - a[i - 1]) * (t - K[i - 1]) / (K[i] - K[i - 1])
    return a[-1]
LP = [4.29, 4.95, 5.4, 5.6, 6.2, 6.6, 6.5, 6.0, 5.5, 5.0, 4.0, 3.0, 2.0, 1.0, 0.554]
assert abs(sum(LP) - 66.594) < 1e-09

def model(s, ke=0.095, terminal_g=None, extra_cap=0, margin_delta=0, cash_cap=100):
    rows = []
    cash = C0
    debt = DEBT
    lease = 66.594
    prev = sum(R0) * 1.045
    divcum = 0
    for t in range(1, 16):
        rr = [interp(a, t) for a in s['rev']]
        mm = [interp(a, t) for a in s['mar']]
        op = [r * (m + margin_delta) for r, m in zip(rr, mm)]
        rev = sum(rr)
        ebit = sum(op)
        tax = 0.18 + min(t - 1, 6) / 6 * 0.02 if t <= 7 else 0.2 + min(t - 7, 8) / 8 * 0.02
        if s is S['受损']:
            tax = 0.2
        intdebt = 1.7 + (debt - DEBT) * 0.055
        intlease = lease * 0.045
        cap = interp(s['cap'], t) + extra_cap
        da = interp(s['da'], t)
        nw = 0.01 * (rev - prev)
        prev = rev
        fcfe = (ebit - intdebt - intlease) * (1 - tax) + da - cap - nw - LP[t - 1]
        if t == 1:
            fcfe -= 1.1
        ordinary = 3.92 * (1 + s['divg']) ** (t - 1)
        interest_cash = max(cash - MINC, 0) * 0.03
        cash_pre = cash + fcfe + interest_cash - ordinary * N
        special = max(0, cash_pre - cash_cap) / N
        div = ordinary + special
        cash_pre -= special * N
        issue = max(0, MINC - cash_pre)
        cash = cash_pre + issue
        debt += issue
        lease -= LP[t - 1]
        divcum += div
        rows.append(dict(t=t, rev=rev, rr=rr, mm=mm, op=op, ebit=ebit, tax=tax, cap=cap, da=da, nwc=nw, interest=intdebt + intlease, lp=LP[t - 1], fcfe=fcfe, cash=cash, debt=debt, newdebt=issue, ordinary=ordinary, special=special, div=div, divcum=divcum, netcash=cash - debt))
    g = s['g'] if terminal_g is None else terminal_g
    last = rows[-1]
    termcf = last['ebit'] * (1 + g) * (1 - 0.22) * (1 - g / s['roic']) - (1.7 + (last['debt'] - DEBT) * 0.055) * (1 - 0.22)
    tv = termcf / (ke - g) + last['cash'] - MINC + s['asset'] * 1.08 ** 15

    def value(h):
        eq = sum((r['div'] * N / (1 + ke) ** (r['t'] - h) for r in rows if r['t'] > h)) + tv / (1 + ke) ** (15 - h)
        c = C0 if h == 0 else rows[h - 1]['cash']
        dv = 0 if h == 0 else rows[h - 1]['divcum']
        oper = eq - (c - MINC) - s['asset'] * 1.08 ** h
        v = eq / N
        wealth = v + dv
        return dict(h=h, oper=oper, equity=eq, price=v, div=dv, wealth=wealth, total=wealth / P0 - 1, cagr=(wealth / P0) ** (1 / h) - 1 if h else None, tvshare=tv / (1 + ke) ** (15 - h) / eq)
    vals = {h: value(h) for h in [0, 1, 3, 7]}
    return dict(rows=rows, values=vals, tv=tv, termcf=termcf, ke=ke)

def all_results():
    return {k: model(s) for k, s in S.items()}
for name, result in all_results().items():
    print(name)
    for h, v in result['values'].items():
        print(h, v['equity'], v['price'], v['div'], v['total'], v['cagr'])
    for h in [1, 3, 7]:
        check = sum((result['rows'][i - 1]['div'] / 1.095 ** i for i in range(1, h + 1)))
        check += result['values'][h]['price'] / 1.095 ** h
        assert abs(check - result['values'][0]['price']) < 1e-09