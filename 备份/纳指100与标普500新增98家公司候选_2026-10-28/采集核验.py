"""Read-only source collection for the 2026-10-28 research candidate proposal."""
import concurrent.futures
import io
import json
import re
from pathlib import Path
import requests
import openpyxl
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent.parent
TICKERS = '''AAPL INTU ADP PAYX WDAY ADSK ROP VEEV ACN FTNT APP NFLX DIS TTWO SHOP MELI UBER BKNG
V MA AXP JPM BAC GS MS SCHW IBKR BLK BX KKR SPGI MCO MSCI CME ICE BRK.B AJG AON
LLY JNJ ABBV MRK AMGN GILD ABT SYK BSX MDT EW DXCM RMD IDXX ZTS UNH MCK HCA
PG KO PEP MDLZ MNST MCD CMG SBUX HD LOW ORLY AZO NKE CL
CTAS GWW FAST ITW AME HWM TDG RTX LMT NOC URI OTIS
UNP CSX ODFL UPS XOM CVX COP SLB WMB NEE FCX SHW PLD WELL AMT O'''.split()
assert len(TICKERS) == len(set(TICKERS)) == 98
# Transcribed from Nasdaq's official company table, read via web on 2026-10-28.
# Only selected candidates are retained; cross-checked against Slickcharts live components.
NDX_SELECTED = set('AAPL INTU ADP PAYX WDAY ADSK ROP FTNT APP NFLX TTWO SHOP MELI BKNG AMGN GILD DXCM IDXX PEP MDLZ MNST SBUX ORLY CTAS FAST CSX ODFL'.split())
SPY_URL = 'https://www.ssga.com/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx'
INDEX_URL = 'https://www.nasdaq.com/articles/global-indexes/nasdaq-100-index'

def collect_profile(ticker):
    slug = ticker.lower().replace('.', '-')
    url = f'https://stockanalysis.com/stocks/{slug}/company/'
    target = ROOT / 'sources' / f'{ticker}.json'
    if target.exists():
        cached = json.loads(target.read_text(encoding='utf-8'))
        if cached.get('description'):
            return cached
    result = {'ticker': ticker, 'url': url, 'access_date': '2026-10-28'}
    try:
        response = requests.get(url, timeout=(10, 20))
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        main = soup.find('main')
        text = main.get_text(' ', strip=True) if main else ''
        section = text.split('Company Description', 1)[-1]
        # Store a bounded excerpt for provenance, not a redistribution of full profiles.
        result['description'] = ' '.join(section.split()[:160]) if 'Company Description' in text else ''
        result['title'] = soup.title.get_text() if soup.title else ''
        result['last_updated'] = re.findall(r'Last updated: (.{0,35})', text)
    except Exception as exc:
        result['error'] = f'{type(exc).__name__}: {exc}'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

def main():
    (ROOT / 'sources').mkdir(exist_ok=True)
    response = requests.get(SPY_URL, timeout=(10, 40))
    response.raise_for_status()
    sheet = openpyxl.load_workbook(io.BytesIO(response.content), data_only=True).active
    values = list(sheet.values)
    members = {row[1]: row[0] for row in values[5:] if isinstance(row[1], str) and re.fullmatch(r'[A-Z][A-Z.\-]*', row[1])}
    current = (WORKSPACE / '基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig')
    existing = set(re.findall(r'^\|\s*([A-Z][A-Z0-9.\-]*)\s*\|', current, re.M))
    duplicate = sorted(set(TICKERS) & existing)
    outside = sorted(set(TICKERS) - set(members) - NDX_SELECTED)
    assert not duplicate, duplicate
    assert not outside, outside
    summary = {'access_date': '2026-10-28', 'spy_holdings_date': values[2][1], 'spy_source': SPY_URL, 'ndx_source': INDEX_URL,
        'existing_company_count': len(existing), 'candidate_count': len(TICKERS), 'duplicates_with_project': duplicate, 'outside_verified_union': outside,
        'candidates': [{'ticker': t, 'sp500_proxy': t in members, 'nasdaq100': t in NDX_SELECTED, 'spy_name': members.get(t)} for t in TICKERS]}
    (ROOT / '指数与去重核验.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(collect_profile, TICKERS))
    errors = [r['ticker'] for r in results if not r.get('description')]
    print(json.dumps({'count': len(TICKERS), 'existing': len(existing), 'spy_date': values[2][1], 'sp500': sum(t in members for t in TICKERS), 'nasdaq100': len(NDX_SELECTED), 'profile_ok': len(results)-len(errors), 'profile_errors': errors}, ensure_ascii=False))

if __name__ == '__main__':
    main()
