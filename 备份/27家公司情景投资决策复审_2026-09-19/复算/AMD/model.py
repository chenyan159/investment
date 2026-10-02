import math, json, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parent
PRICE = 559.82
ANCHORS = [0, 1, 3, 7, 12]
BUS = ['GPU', 'CPU', 'Client', 'Gaming', 'Embedded', 'Network', 'New']
START = [16, 16, 12.5, 3, 4, 0.8, 0]
START_M = [0.22, 0.34, 0.2, 0.12, 0.37, 0.1, 0]
P = {'damaged': dict(p=0.2, N=1.72, g=0.005, roic=0.12, nwc=0.22, cap=0.04, r=[[16, 20, 12, 2.6, 4.1, 0.8, 0], [20, 23, 13, 4, 4.8, 1.2, 0], [18, 25, 14, 3.5, 5.5, 1.5, 0], [15, 27, 15, 3, 6, 2, 0]], m=[[0.12, 0.3, 0.16, 0.08, 0.32, 0.08, 0], [0.16, 0.31, 0.17, 0.13, 0.34, 0.12, 0], [0.12, 0.29, 0.16, 0.11, 0.33, 0.12, 0], [0.1, 0.28, 0.16, 0.1, 0.32, 0.12, 0]], central=[1.2, 1.1, 1.2, 1.4], invest=[1, 0.5, 0], recover=1, loss=[2, 1, 0], acq=1.5), 'base': dict(p=0.41, N=1.86, g=0.025, roic=0.2, nwc=0.18, cap=0.035, r=[[32, 24, 13.2, 3, 4.4, 1.2, 0], [65, 44, 16, 5, 6, 2.5, 0.5], [100, 70, 20, 5, 9, 5, 0.7], [130, 90, 24, 5, 12, 7, 1]], m=[[0.28, 0.36, 0.2, 0.12, 0.38, 0.15, 0], [0.33, 0.38, 0.22, 0.16, 0.39, 0.22, 0.05], [0.3, 0.37, 0.22, 0.15, 0.38, 0.25, 0.1], [0.27, 0.34, 0.2, 0.14, 0.36, 0.24, 0.1]], central=[1.2, 1.4, 1.8, 2.3], invest=[2, 2, 1], recover=5, loss=[0, 0, 0], acq=1.5), 'upside': dict(p=0.22, N=1.98, g=0.03, roic=0.25, nwc=0.18, cap=0.04, r=[[46, 29, 14, 3.2, 4.6, 1.6, 0], [105, 85, 17, 5.5, 7, 4, 1], [190, 140, 23, 6, 12, 9, 3], [270, 175, 29, 6, 16, 14, 5]], m=[[0.32, 0.38, 0.22, 0.14, 0.39, 0.18, 0], [0.38, 0.41, 0.24, 0.18, 0.41, 0.27, 0.15], [0.37, 0.4, 0.24, 0.18, 0.4, 0.3, 0.2], [0.33, 0.36, 0.22, 0.16, 0.38, 0.28, 0.18]], central=[1.3, 1.7, 2.5, 3.3], invest=[2, 2, 1], recover=7, loss=[0, 0, 0], acq=1.5), 'breakthrough': dict(p=0.08, N=1.98, g=0.03, roic=0.25, nwc=0.2, cap=0.045, r=[[57, 24, 13.2, 3, 4.4, 1.8, 0], [150, 44, 16, 5, 6, 5, 4], [320, 70, 20, 5, 9, 12, 16], [470, 90, 24, 5, 12, 20, 30]], m=[[0.33, 0.36, 0.2, 0.12, 0.38, 0.18, 0], [0.42, 0.38, 0.22, 0.16, 0.39, 0.3, 0.2], [0.43, 0.37, 0.22, 0.15, 0.38, 0.33, 0.3], [0.37, 0.34, 0.2, 0.14, 0.36, 0.3, 0.25]], central=[1.5, 2, 3.5, 5], invest=[2, 2, 1], recover=7, loss=[0, 0, 0], acq=1.5), 'tail': dict(p=0.05, N=1.68, g=0, roic=0.1, nwc=0.27, cap=0.035, r=[[6, 15, 10, 2, 3.5, 0.6, 0], [5, 18, 11, 3, 4, 0.7, 0], [3, 20, 12, 3, 4.5, 0.8, 0], [2, 21, 12, 2.5, 5, 1, 0]], m=[[-0.25, 0.25, 0.12, 0.05, 0.28, 0, 0], [-0.05, 0.27, 0.14, 0.1, 0.3, 0.08, 0], [-0.05, 0.26, 0.14, 0.09, 0.3, 0.08, 0], [-0.05, 0.25, 0.14, 0.09, 0.29, 0.08, 0]], central=[1.4, 1.1, 1.1, 1.2], invest=[1, 0, 0], recover=0, loss=[6.1, 2, 0], acq=1.5)}
P['joint'] = copy.deepcopy(P['breakthrough'])
for j in range(4):
    P['joint']['r'][j][1] = P['upside']['r'][j][1]
    P['joint']['m'][j][1] = P['upside']['m'][j][1]
P['joint'].update(p=0.04, cap=0.05, central=[2, 3, 5, 7])

def interp(points, t):
    if t == 0:
        return points[0]
    for j in range(1, len(ANCHORS)):
        if t <= ANCHORS[j]:
            a, b = ANCHORS[j - 1:j + 1]
            f = (t - a) / (b - a)
            if isinstance(points[0], list):
                return [x + (y - x) * f for x, y in zip(points[j - 1], points[j])]
            return points[j - 1] + (points[j] - points[j - 1]) * f

def model(k, w=0.11, gshift=0, gpu_scale=1, margin_shift=0, delay=0, shares=None, ramp=False, sbc_rate=0.04, nwc_shift=0, extra_cost=0, terminal_roic=None, cash_shift=0, acq_shift=0):
    s = copy.deepcopy(P[k])
    N = s['N'] if shares is None else shares
    s['nwc'] += nwc_shift
    if terminal_roic is not None:
        s['roic'] = terminal_roic
    C = 13.111 - 4 + cash_shift
    D = 3.25
    nwc0 = 12.0
    R0 = sum(START)
    prev_nwc = nwc0
    prev_R = R0
    rows = []
    loan = 0
    issues = 0
    minC = C
    old_extra_assets = 2.0
    quarters = []
    peakloan = 0
    for t in range(1, 13):
        r = interp([START] + s['r'], t)
        m = interp([START_M] + s['m'], t)
        if delay and t >= 1:
            rt = interp([START] + s['r'], max(0, t - delay))
            r[0] = rt[0]
        scale = 1 + (gpu_scale - 1) * min((t - 1) / 6, 1) if ramp else gpu_scale
        r[0] *= scale
        m[0] += margin_shift
        R = sum(r)
        op = [a * b for a, b in zip(r, m)]
        corp = interp([1] + s['central'], t) + extra_cost
        sbc = sbc_rate * R
        loss = s['loss'][t - 1] if t <= 3 else 0
        EBIT = sum(op) - corp - sbc - loss
        tax = 0.16 if t <= 3 else 0.18 if t <= 7 else 0.2
        cash_tax = max(EBIT, 0) * tax
        da = 0.02 * R
        cap = s['cap'] * R
        nwc = s['nwc'] * R
        if k == 'tail' and t == 1:
            nwc = max(nwc, nwc0 + 3)
        dnwc = nwc - prev_nwc
        mincashchange = 0.02 * (R - prev_R)
        strategic = s['invest'][t - 1] if t <= 3 else 0
        acquisition = s['acq'] + acq_shift if t == 1 else 0
        recovery = s['recover'] if t == 7 else 0
        fcff = EBIT - cash_tax + da - cap - dnwc - mincashchange - strategic - acquisition + recovery
        scheduled = {1: 0.875, 2: 0.625, 4: 0.75, 6: 0.5}.get(t, 0)
        afterinterest = draw = equity = repayloan = 0
        front = {'damaged': [-5, -2, 3], 'base': [-4, -1, 5], 'upside': [-6, -2, 5], 'breakthrough': [-7, -3, 4], 'tail': [-10, -5, 1], 'joint': [-8, -4, 5]}
        qfs = front.get(k, front['base']) + [fcff - sum(front.get(k, front['base']))] if t == 1 else [fcff / 4] * 4
        for q, qf in enumerate(qfs, 1):
            interest = ((D - loan) * 0.04 + loan * 0.07) / 4
            ai = interest * (1 - tax) if EBIT > 0 else interest
            afterinterest += ai
            debtpayment = scheduled if q == 1 else 0
            C = C * 1.035 ** 0.25 + qf - ai - debtpayment
            D -= debtpayment
            dr = eq = rep = 0
            if C < 0:
                dr = min(-C, max(0, 5 - loan))
                C += dr
                D += dr
                loan += dr
                draw += dr
                if C < 0:
                    eq = -C + 1
                    issues += eq / 50
                    N += eq / 50
                    C += eq
                    equity += eq
            elif loan > 0 and C > 2:
                rep = min(C - 2, loan)
                C -= rep
                D -= rep
                loan -= rep
                repayloan += rep
            minC = min(minC, C)
            peakloan = max(peakloan, loan)
            if t == 1:
                quarters.append(dict(q=q, F=qf, C=C, D=D, loan=loan, draw=dr, equity=eq, repayloan=rep))
        rows.append(dict(t=t, r=r, m=m, R=R, op=op, corp=corp, sbc=sbc, loss=loss, EBIT=EBIT, tax=cash_tax, da=da, capex=cap, dnwc=dnwc, dcash=mincashchange, invest=strategic, acq=acquisition, recovery=recovery, F=fcff, C=C, D=D, interest=afterinterest, repay=scheduled, draw=draw, equity=equity, repayloan=repayloan, N=N))
        prev_nwc = nwc
        prev_R = R
    g = max(-0.005, s['g'] + gshift)
    terminal_nopat = rows[-1]['EBIT'] * 0.8 * (1 + g)
    terminal_F = terminal_nopat * (1 - g / s['roic'])
    TV = terminal_F / (w - g)
    values = {}
    for h in [0, 1, 3, 7]:
        ev = sum((row['F'] / (1 + w) ** (row['t'] - h) for row in rows if row['t'] > h)) + TV / (1 + w) ** (12 - h)
        ch = 9.111 + cash_shift if h == 0 else rows[h - 1]['C']
        dh = 3.25 if h == 0 else rows[h - 1]['D']
        fundingPV = sum((row['equity'] / (1 + w) ** (row['t'] - h) for row in rows if row['t'] > h))
        eq = ev + ch + old_extra_assets - dh + fundingPV
        value = max(0, eq / N)
        values[h] = dict(EV=ev, E=eq, V=value, C=ch, D=dh, N=N, TR=value / PRICE - 1, CAGR=(value / PRICE) ** (1 / h) - 1 if h else None, TVshare=TV / (1 + w) ** (12 - h) / ev)
    return dict(rows=rows, values=values, TV=TV, terminal_F=terminal_F, minC=minC, issues=issues, quarters=quarters, peakloan=peakloan)

def all_outputs():
    out = {k: model(k) for k in P}
    for k, o in out.items():
        lo = model(k, w=0.13, gshift=-0.005)
        hi = model(k, w=0.09, gshift=0.005)
        o['range'] = {h: [lo['values'][h]['V'], hi['values'][h]['V']] for h in [0, 1, 3, 7]}
    return out
if __name__ == '__main__':
    out = all_outputs()
    pass
    for k, o in out.items():
        print(k, 'V', [(h, round(v['V'], 1), [round(x, 1) for x in o['range'][h]], round(v['TVshare'] * 100, 1)) for h, v in o['values'].items()])
        print('R EBIT F C D N', [(x['t'], *[round(x[a], 2) for a in ['R', 'EBIT', 'F', 'C', 'D', 'N']]) for x in o['rows'] if x['t'] in [1, 3, 7, 12]])
    for h in [0, 1, 3, 7]:
        v = sum((P[k]['p'] * o['values'][h]['V'] for k, o in out.items()))
        print('EXPECTED', h, round(v, 2), 'ANNUAL', None if h == 0 else round((v / PRICE) ** (1 / h) - 1, 4))