import json, math, copy
from pathlib import Path
ROOT = Path(__file__).parent
PRICE = 223.54
N0 = 308.721154
BONDS = [('Jun29', 0.1, 0.02, 3, 1.175, 51.45), ('Jun31', 0.1, 0.03, 5, 1.225, 51.45), ('Sep30', 1.58125, 0.01, 4, 1.15, 138.75), ('Sep32', 1.58125, 0.0275, 6, 1.15, 138.75), ('Mar31', 2.5875, 0.0125, 5, 1.2, 183.22), ('Mar33', 1.75, 0.02625, 7, 1.2, 180.31), ('Aug30', 3.45, 0.005, 4, 1.1, 313.46), ('Aug34', 2.3, 0.045, 8, 1.25, 324.65)]
PATHS = {'悲观': dict(p=0.15, D=[4.8, 6, 6.5, 6.5, 6, 6, 6, 6, 6, 6, 6, 6], C=[1.5, 2.5, 3, 3.5, 4, 4.5, 5, 5, 5, 5, 5, 5], S=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.5, 0.5], cap=[14, 6, 3, 3, 3.2, 3.5, 3.7, 4, 4, 4, 4, 4], mD=0.48, mC=0.5, mS=0.6, fixed=0.25, other=-0.2, pre=[1, 0, -2, -2, -2, -1, 0, 0, 0, 0, 0, 0], borrow=[3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], issue=25, exit=1.0, g=0), '基准': dict(p=0.45, D=[5.2, 7, 8.5, 9.5, 10.5, 11, 11.5, 12, 12.3, 12.6, 12.8, 13], C=[2.4, 5.8, 9, 12, 15, 17.5, 20, 22, 24, 25.5, 27, 28], S=[0.15, 0.4, 0.8, 1.3, 2, 2.7, 3.5, 4.2, 5, 5.8, 6.5, 7], cap=[20, 15, 12, 12, 13, 14, 15, 15, 15, 15.5, 16, 16], mD=0.54, mC=0.55, mS=0.68, fixed=0.35, other=-0.23, pre=[4, 2, 1, 0, -2, -2, -2, -1, 0, 0, 0, 0], borrow=[5, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], issue=160, exit=3.0, g=0.02), '乐观': dict(p=0.23, D=[5.5, 8, 10, 12, 14, 16, 17, 18, 19, 20, 21, 22], C=[3, 7.5, 13, 18, 23, 28, 33, 37, 41, 44, 47, 50], S=[0.2, 0.7, 1.5, 2.7, 4.2, 6, 8, 10, 12, 14, 16, 18], cap=[22, 19, 17, 17, 19, 21, 23, 24, 25, 26, 27, 28], mD=0.57, mC=0.59, mS=0.72, fixed=0.45, other=-0.23, pre=[5, 4, 2, 1, -2, -3, -3, -3, -1, 0, 0, 0], borrow=[6, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], issue=230, exit=4, g=0.025), '突破': dict(p=0.07, D=[5.3, 7.5, 9, 10.5, 12, 13, 14, 15, 16, 17, 18, 19], C=[2.6, 6.5, 11, 16, 22, 28, 34, 40, 46, 51, 56, 60], S=[0.2, 1, 3, 6, 10, 15, 21, 27, 33, 39, 45, 50], cap=[21, 18, 17, 19, 22, 25, 28, 30, 32, 34, 36, 38], mD=0.55, mC=0.6, mS=0.76, fixed=0.65, other=-0.23, pre=[4, 3, 2, 1, -1, -2, -2, -2, -2, -1, 0, 0], borrow=[5, 5, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], issue=230, exit=3, g=0.03)}
PATHS['悲观']['p'] = 0.25

def simulate(cfg, r=0.14, capmult=1, rev_mult=1, margin_shift=0, startcash=11.0, force=None, min_cash=1.0, terminal_roic=0.15):
    choices = set() if force is None else set(force)
    option_exercise = False
    for iteration in range(32):
        cash = startcash
        shares = N0
        loan = 0.775
        arrears = 0
        loss_pool = 0.8
        rows = []
        cohorts = []
        deferred = 8.0
        previous_rev = 3.0
        equity_total = 0
        default = False
        refinance_cohorts = []
        for i in range(1, 13):
            D = cfg['D'][i - 1] * rev_mult
            C = cfg['C'][i - 1] * rev_mult
            S = cfg['S'][i - 1] * rev_mult
            rev = D + C + S + 0.05
            sbc = max(0.25, 0.03 * rev)
            other = cfg['other'] if i <= 4 else -0.05
            ebitda = D * (cfg['mD'] + margin_shift) + C * (cfg['mC'] + margin_shift) + S * cfg['mS'] - cfg['fixed'] + other - sbc
            cap = cfg['cap'][i - 1] * capmult
            da = (3.5 if i <= 4 else 0) + 0.25
            for j, v in cohorts:
                age = i - j
                da += v * 0.85 / 5 * (1 if age < 5 else 0.5 if age == 5 else 0)
                da += v * 0.15 / 15
            da += cap * (0.85 / 5 + 0.15 / 15) * 0.5
            cohorts.append((i, cap))
            ebit = ebitda - da
            intbond = sum((a * c for n, a, c, t, ac, k in BONDS if t >= i))
            rate = 0.11 if cfg['issue'] == 25 else 0.08
            repay = (0.775 if i == 5 else 0) + sum((cfg['borrow'][j - 1] / 5 for j in range(1, i) if 2 <= i - j <= 6)) + sum((v / 7 for j, v in refinance_cohorts if 1 <= i - j <= 7))
            interest = intbond + rate * loan
            intcash = 0.035 * max(cash, 0)
            taxable = ebit - interest + intcash
            if taxable < 0:
                loss_pool -= taxable
                tax = 0
            else:
                used = min(loss_pool, taxable * 0.8)
                loss_pool -= used
                tax = (taxable - used) * 0.25
            dpre = cfg['pre'][i - 1]
            deferred += dpre
            assert deferred >= -1e-08
            dwork = 0.025 * (rev - previous_rev)
            previous_rev = rev
            fcff = ebitda - tax - cap - dwork + dpre
            convert = 0
            redeemed = 0
            for n, a, c, t, ac, k in BONDS:
                if t == i:
                    if n in choices:
                        convert += a * 1000 / k
                    else:
                        redeemed += a * ac
            shares += convert + (6.234091 / 4 if i <= 4 else 0)
            option_cash = 0
            if i == 4 and option_exercise:
                shares += 6.7406
                option_cash = 6.7406 * 88.65 / 1000
            refill = min(0.75 * redeemed, max(0, 2 * max(ebitda, 0) - (loan - repay + cfg['borrow'][i - 1])))
            refinance_cohorts.append((i, refill))
            newloan = cfg['borrow'][i - 1] + refill
            loan += newloan - repay
            assert loan >= -1e-08
            asset_exit = cfg['exit'] if i == 5 else 0
            before = cash + fcff - interest + intcash + newloan - repay - redeemed + asset_exit + option_cash
            minimum = max(min_cash, rev * 0.06)
            eq = max(0, minimum - before)
            shares += eq * 1000 / cfg['issue']
            equity_total += eq
            cash = before + eq
            dividend = 0
            if i >= 8:
                dividend = max(0, cash - minimum)
                cash -= dividend
            rows.append(dict(t=i, D=D, C=C, S=S, R=rev, EBITDA=ebitda, SBC=sbc, DA=da, EBIT=ebit, tax=tax, capex=cap, dWC=dwork - dpre, Fstar=fcff, interest=interest, interest_cash=intcash, pre=dpre, deferred=deferred, newdebt=newloan, repay=repay, redeem=redeemed, convshares=convert, option_cash=option_cash, equity=eq, shares=shares, cash=cash, loan=loan, dividend=dividend, divps=dividend * 1000 / shares, exit=asset_exit, lowcash=before))
        last = rows[-1]
        g = cfg['g']
        mature_nopat = max(0, (last['EBIT'] - rate * last['loan']) * 0.75)
        terminal_fcf = mature_nopat * (1 + g) * (1 - max(g, 0) / terminal_roic)
        terminal = terminal_fcf / (r - g)
        prices = [0.0] * 13
        prices[12] = terminal * 1000 / last['shares']
        for i in range(11, -1, -1):
            prices[i] = (prices[i + 1] + rows[i]['divps']) / (1 + r)
        updated = {n for n, a, c, t, ac, k in BONDS if prices[t] > ac * k}
        option_update = prices[4] > 88.65
        if force is not None or (updated == choices and option_update == option_exercise):
            break
        choices = updated
        option_exercise = option_update
    else:
        raise ValueError('conversion iteration did not converge')
    default_t = None
    if cfg['issue'] == 25:
        default_t = next((x['t'] for x in rows if x['equity'] > 2), None)
        if default_t is not None:
            prices = [0.0] * 13
            terminal = 0
            terminal_fcf = 0
            equity_total = 0
            for x in rows:
                if x['t'] >= default_t:
                    for c in ['R', 'D', 'C', 'S', 'EBIT', 'EBITDA', 'DA', 'SBC', 'capex', 'Fstar', 'cash', 'shares', 'loan', 'dividend', 'divps', 'equity', 'newdebt', 'repay', 'redeem', 'interest', 'interest_cash', 'tax', 'dWC', 'pre', 'exit', 'option_cash']:
                        x[c] = 0.0
    for row in rows:
        row['price'] = prices[row['t']]
        row['equityvalue'] = row['price'] * row['shares'] / 1000
        row['debt_cash_maturity_claim'] = row['loan'] + sum((a * ac for n, a, c, t, ac, k in BONDS if t > row['t']))
    return dict(prices=prices, rows=rows, conversions=sorted(choices), new_equity=equity_total, terminal=terminal, terminal_fcf=terminal_fcf, terminal_share=terminal * 1000 / last['shares'] / (1 + r) ** 12 / max(prices[0], 1e-10) if default_t is None else 0, r=r, iterations=iteration + 1, default_t=default_t)
if __name__ == '__main__':
    result = {k: simulate(v) for k, v in PATHS.items()}
    pass
    for k, v in result.items():
        print(k, 'prices=', [round(v['prices'][i], 2) for i in [0, 1, 3, 7]], 'raises=', round(v['new_equity'], 2), 'conv=', v['conversions'], 'terminal%', round(v['terminal_share'] * 100, 1))
        for x in v['rows']:
            print(x['t'], *(round(x[c], 2) for c in ['R', 'EBIT', 'capex', 'Fstar', 'equity', 'cash', 'shares', 'price']))