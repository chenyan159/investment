from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import yfinance as yf

OUT = Path(__file__).parent
SYMBOLS = ['SPCX', '4062.T', '3037.TW', '6954.T', '6506.T', 'SYM', 'ASTS', 'PL']

def fetch(symbol):
    t = yf.Ticker(symbol)
    row = {'symbol': symbol, 'retrieved_at': datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()}
    try:
        q = t.info
        fields = ['symbol','shortName','longName','quoteType','exchange','currency','financialCurrency','regularMarketPrice','regularMarketTime','trailingPE','forwardPE','trailingEps','forwardEps','marketCap','sharesOutstanding','firstTradeDateMilliseconds']
        row['quote'] = {k: q.get(k) for k in fields}
    except Exception as e:
        row['quote_error'] = str(e)
    try:
        h = t.history(start='2025-09-01', end='2026-09-10', auto_adjust=False)
        row['history'] = [{'date': str(i.date()), 'close': float(v.Close), 'dividend': float(v.get('Dividends', 0)), 'split':float(v.get('Stock Splits', 0))} for i,v in h.iterrows()]
        if len(h):
            endpoint = row['history'][-1]
            row['endpoint'] = endpoint
            row['returns'] = {}
            for key, target in [('3m','2026-06-09'),('6m','2026-03-09'),('1y','2025-09-09')]:
                candidates = [v for v in row['history'] if v['date'] <= target]
                if candidates and endpoint['date'] == '2026-09-09':
                    a = candidates[-1]
                    row['returns'][key] = {'anchor':a,'percent':100*(endpoint['close']/a['close']-1)}
                else:
                    row['returns'][key] = None
    except Exception as e:
        row['history_error'] = str(e)
    return row

if __name__ == '__main__':
    data = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(fetch,t) for t in SYMBOLS]):
            row = future.result()
            data.append(row)
            print(json.dumps({k:v for k,v in row.items() if k != 'history'}, ensure_ascii=False), flush=True)
    (OUT/'补充公司行情.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
