import json, math, copy
from pathlib import Path
ROOT = Path('.')
PRICE = 253.71
NODES = [1, 3, 7, 10]
P = [0.25, 0.45, 0.23, 0.07]
S = {'受损': dict(core=[155, 185, 230, 245], cm=[0.35, 0.33, 0.3, 0.29], ai=[34, 43, 70, 83], am=[0.15, 0.17, 0.18, 0.18], ad=[91, 104, 137, 152], dm=[0.36, 0.34, 0.33, 0.31], ret=[590, 650, 745, 790], rm=[0.018, 0.015, 0.015, 0.013], new=[0.5, 1, 3, 3], ne=[-10, -5, -1, -0.5], cap=[210, 125, 135, 130], da=[75, 94, 117, 120], g=0.02, roic=0.1, asset=70), '基准': dict(core=[160, 195, 290, 350], cm=[0.4, 0.4, 0.38, 0.36], ai=[48, 100, 220, 290], am=[0.27, 0.32, 0.34, 0.33], ad=[99, 132, 215, 260], dm=[0.42, 0.43, 0.42, 0.4], ret=[610, 725, 970, 1110], rm=[0.026, 0.031, 0.035, 0.035], new=[1, 3, 10, 17], ne=[-9, -7, -1, 2], cap=[235, 240, 240, 245], da=[78, 124, 196, 213], g=0.03, roic=0.16, asset=450), '乐观': dict(core=[163, 205, 320, 400], cm=[0.41, 0.42, 0.4, 0.38], ai=[60, 145, 375, 530], am=[0.29, 0.35, 0.37, 0.35], ad=[104, 149, 265, 335], dm=[0.44, 0.46, 0.46, 0.43], ret=[621, 756, 1050, 1250], rm=[0.03, 0.04, 0.05, 0.05], new=[1, 3, 10, 17], ne=[-9, -7, -1, 2], cap=[260, 280, 340, 360], da=[80, 137, 251, 300], g=0.035, roic=0.18, asset=750), '突破': dict(core=[160, 195, 290, 350], cm=[0.4, 0.4, 0.38, 0.36], ai=[68, 200, 650, 1050], am=[0.3, 0.38, 0.43, 0.38], ad=[99, 132, 215, 260], dm=[0.42, 0.43, 0.42, 0.4], ret=[610, 725, 970, 1110], rm=[0.026, 0.031, 0.035, 0.035], new=[1, 3, 10, 17], ne=[-9, -7, -1, 2], cap=[285, 370, 520, 650], da=[81, 147, 370, 510], g=0.035, roic=0.18, asset=1200)}

def interp(v, t):
    if t <= 1:
        return v[0]
    for j in range(3):
        if t <= NODES[j + 1]:
            a = (t - NODES[j]) / (NODES[j + 1] - NODES[j])
            return v[j] * (1 - a) + v[j + 1] * a
    return v[-1]

def model(s, r=0.095, g_shift=0, cap_mult=1, margin_delta=0, asset_mult=1):
    rows = []
    cash = 98.0
    debt = 162.0
    shares = 10.79
    ppe = 480.0
    cum = 0
    for t in range(1, 11):
        x = {k: interp(v, t) for k, v in s.items() if isinstance(v, list)}
        rev = sum((x[k] for k in ['core', 'ai', 'ad', 'ret', 'new']))
        e = [x['core'] * x['cm'], x['ai'] * (x['am'] + margin_delta), x['ad'] * x['dm'], x['ret'] * x['rm'], x['ne']]
        ebit = sum(e)
        tax = 0.22 * ebit
        nwc = 0.008 * (rev - (795 if t == 1 else rows[-1]['revenue']))
        cap = x['cap'] * cap_mult
        da = x['da']
        f = ebit - tax + da - cap - nwc
        ppe += cap - da
        invest = 8 if t == 1 else 7 if t == 2 else 0
        acq = 5 if t == 1 else 0
        if t == 1:
            shares += 0.026
        interest = debt * 0.055 * 0.78
        income = max(0, cash - 35) * 0.04 * 0.78
        startcash = cash
        startdebt = debt
        cash += f - invest - acq - interest + income
        borrow = max(0, 35 - cash)
        cash += borrow
        debt += borrow
        repay = min(debt, max(0, cash - 35))
        cash -= repay
        debt -= repay
        cum += f
        assert abs(cash - (startcash + f - invest - acq - interest + income + borrow - repay)) < 1e-08
        rows.append(dict(t=t, revenue=rev, ebit=ebit, ebits=e, nopat=ebit - tax, da=da, cap=cap, nwc=nwc, fcff=f, cash=cash, debt=debt, shares=shares, borrow=borrow, repay=repay, interest=interest, invest=invest, acq=acq, ppe=ppe, cumfcff=cum))
    g = s['g'] + g_shift
    tv = rows[-1]['nopat'] * (1 + g) * (1 - g / s['roic']) / (r - g)
    results = {}
    for t in [0, 1, 3, 7]:
        future = sum((z['fcff'] / (1 + r) ** (z['t'] - t) for z in rows if z['t'] > t))
        ev = future + tv / (1 + r) ** (10 - t)
        asset = s['asset'] * asset_mult / 1.11 ** (10 - t) - sum((z['invest'] / 1.11 ** (z['t'] - t) for z in rows if z['t'] > t))
        acqleft = sum((z['acq'] / (1 + r) ** (z['t'] - t) for z in rows if z['t'] > t))
        z = rows[t - 1] if t else dict(cash=98, debt=162, shares=10.816)
        eq = ev + asset + z['cash'] - 35 - z['debt'] - acqleft
        per = eq / z['shares']
        total = per / PRICE - 1
        results[t] = dict(ev=ev, asset=asset, equity=eq, per=per, total=total, annual=(per / PRICE) ** (1 / t) - 1 if t else None, tvshare=tv / (1 + r) ** (10 - t) / ev)
    return dict(rows=rows, values=results, tv=tv)

def run():
    out = {k: model(v) for k, v in S.items()}
    for k, v in out.items():
        print(k, 'values', [(t, round(q['per'], 2), round(q['total'] * 100, 1), round(q['tvshare'] * 100, 1)) for t, q in v['values'].items()])
        print('cash', [(q['t'], round(q['ebit'], 1), round(q['fcff'], 1), round(q['debt'], 1), round(q['cash'], 1)) for q in v['rows']])
    print('weighted', [(t, round(sum((p * out[k]['values'][t]['per'] for p, k in zip(P, S))), 2)) for t in [0, 1, 3, 7]])
    return out
if __name__ == '__main__':
    run()