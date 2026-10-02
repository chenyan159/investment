from pathlib import Path
from itertools import combinations
from collections import Counter
from decimal import Decimal
import json, re, csv, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
ROOT=Path('D:/drive/Investment')
manifest=json.loads((OUT/'16份结果清单.json').read_text(encoding='utf-8'))
def words(s): return s.split()

# Manually transcribed from each report's focus table or company cards;
# display order is not interpreted as an investment rank.
focus={
'01': 'ADBE ET MU BABA MSFT PNR ST NVDA SMCI SNDK ASML GOOGL META VISN FLNC DKILY ASGLY DOV MKSI SKHY ACLS GFS AEP DTE TEL EME HUBB HPE CRDO PLAB',
'02': 'MU ADBE MSFT SMCI BABA PNR ST NVDA AVGO TSM META SNPS BWXT QCOM CSCO CDNS CRDO FTV AEP ORCL ET SNDK VST AMZN GOOGL ALAB ANET DELL WDC VRT',
'04': 'ADBE MU MSFT VISN BABA ET PNR DOV ALLE AEP DTE BDC META SMCI DKILY ASGLY NVDA TSM GOOGL QCOM TDY GFS NOK FLNC AMZN NVMI CAMT PLAB KLIC SANM',
'06': 'ADBE MU VISN BABA PNR ET MSFT ST BDC DKILY ASGLY NVDA CRDO AVGO CLS SMCI TSM AMD ALAB SNDK AMZN META AAOI NBIS P COHR MRVL FLEX ENPH FLNC',
'07': 'MU SNDK CLS MRVL CRDO NVDA AVGO FN VRT LITE ANET DELL WDC STX TSM FIX ETN AMD COHR ADBE EME MSFT META ALAB MOD IREN NBIS CRWV SMCI GOOGL',
'N02': 'CRWV IREN NBIS SMCI APLD ORCL WOLF FCEL NVTS AMPX POET LWLG AAOI SMR OKLO CBRS SKHY DELL GOOGL SPACEX MU SNDK NVDA AVGO ALAB CRDO BE VRT GEV ADBE',
'N03': 'MU SNDK CLS KLIC TSM ALAB AVGO LITE MCHP GNRC HPE MKSI EME SMTC NVDA CIEN COHR ONTO VRT NVT MTSI KEYS JBL ETN ANET FN ADBE CRDO AAOI SKHY',
'N06': 'CRDO ALAB MU MRVL NVDA TSEM AAOI LITE COHR AVGO AMD CLS NBIS IREN CRWV MOD VRT BE AMPX AEHR ONTO CAMT RMBS MTSI SITM RKLB POET NVTS APLD OKLO',
'09': 'MU SMCI HPE CLS SANM NVDA TSM META SNDK DELL LITE MRVL IREN ORCL CRWV NBIS VST CEG NOK ET SKHY UMC SIMO WDC STX TER SMTC CRDO VRT ADBE',
'N05': 'ADBE MU ORCL ATKR FLNC CLS ET MSFT BABA SMCI PNR ST NVDA ASML QCOM SNDK SKHY META CRDO AVGO TSM GOOGL ANET DELL VRT GEV POWL HTHIY TEL ACLS',
'E04-A': 'ADBE MU NVDA HPE AVGO TEL DOV MSFT EME HUBB NTAP PLAB ETN QCOM BDC ENS TSM FN CLS META AMZN GOOGL JBL FLEX CRDO COHR VRT LRCX KLAC PNR',
'E05-A': 'ADBE NVDA TEL ALLE ST TSM MSFT DOV FTV EME VST SNDK MU CSCO AVGO NTAP WDC META HPE PNR CLS ENS CRDO AMZN VRT BDC QCOM GOOGL DELL ORCL',
'E06-A': 'ORCL CC WOLF CRWV IREN TE MXL AAON SMCI FLNC APLD NBIS BE PH SITM AMPX COHR FCEL CBRS INTC DELL HPE RKLB ASML AMZN GOOGL NVTS AEHR POET LWLG',
'E04-B': 'ADBE MSFT TEL EME NVDA MU DOV FN NTAP CLS VST DELL HPE BDC SNDK ENS CARR GNRC TSM AVGO ST STX WDC MOD PNR AMAT LRCX GOOGL META ETN',
'E05-B': 'ADBE MSFT TEL NVDA AVGO TSM EME MU NTAP HUBB FN SKHY SNDK WDC ETN VST META STX LRCX AMAT HPE VRT PNR MOD QCOM CRDO CLS DELL GOOGL ORCL',
'E06-B': 'TE COHU MKSI VSH ORCL WOLF FLNC CRWV APLD IREN NBIS SMCI MXL CC AMPX AAON PH SITM INTC FCEL BE SMR OKLO POET LWLG NVTS AAOI AXTI RKLB TSLA',
}
anchors={'01':[170,199],'02':[73,74],'04':[65,65],'06':[69,107],'07':[119,191],'N02':[41,42],'N03':[64,98],'N06':[89,118],'09':[132,821],'N05':[93,118],'E04-A':[81,95],'E05-A':[74,102],'E06-A':[111,140],'E04-B':[204,1215],'E05-B':[158,945],'E06-B':[217,876]}
focus={k:words(v) for k,v in focus.items()}
for k,v in focus.items():
    assert len(v)==len(set(v))==30,(k,len(v))
    a,b=anchors[k]
    excerpt='\n'.join(Path(manifest[k]['report']).read_text(encoding='utf-8').splitlines()[a-1:b])
    assert all(re.search(r'(?<![A-Z])'+re.escape(t)+r'(?![A-Z])',excerpt) for t in v),k

# Separate horizon/view sets: C = conditional research candidate, Y = current-price
# consideration in the report, neither implies a trade or a portfolio.
views={}
def add(key,report,c3,c6,y3='',y6='',r3='',r6='',kind='return_selection'):
    views[key]={'report_id':report,'kind':kind,'c3':words(c3),'c6':words(c6),'y3':words(y3),'y6':words(y6),'research3':words(r3),'research6':words(r6)}
add('01-赔率','01','ADBE ET MU BABA MSFT PNR ST NVDA','ADBE ET MU BABA MSFT PNR ST NVDA SMCI SNDK',r3='ADBE MU MSFT ET PNR DOV TEL EME ST GFS DKILY HUBB AEP DTE PLAB',r6='ADBE MSFT MU ET DOV PNR TEL EME ST GFS DKILY HUBB AEP DTE PLAB')
add('01-基准','01','ADBE ET MU MSFT PNR ST ASML DKILY DOV','ADBE ET MU MSFT PNR ST ASML DKILY DOV AEP DTE',r3='MSFT ADBE MU ET ASML TEL EME DOV PNR ST AEP DKILY GFS HUBB DTE ACLS PLAB',r6='ET ADBE MSFT MU DOV ASML TEL PNR EME ST AEP DKILY HUBB DTE GFS ACLS PLAB')
add('02','02','MU ADBE MSFT SMCI BABA PNR ST','MU MSFT SMCI PNR ADBE ST BABA ET NVDA AVGO TSM')
add('04','04','ADBE MU VISN','ADBE MU VISN DOV ALLE AEP DTE DKILY')
add('06F','06','ADBE MU VISN','ADBE BABA ET MU PNR MSFT VISN ST BDC',r3='ADBE MU VISN BABA PNR ET MSFT ST BDC DKILY ASGLY',r6='ADBE BABA ET MU PNR MSFT VISN ST BDC ASGLY DKILY')
add('06G','06','NVDA MU CRDO AVGO CLS SMCI','NVDA MU TSM AVGO CRDO SMCI AMZN CLS AMD SNDK',r3='NVDA MU CRDO AVGO CLS SMCI TSM AMD ALAB SNDK AMZN MSFT META AAOI NBIS',r6='NVDA MU TSM AVGO CRDO SMCI AMZN CLS AMD SNDK MSFT META AAOI ALAB NBIS')
add('06E','06','ADBE MU P COHR MRVL CLS FLEX','MU ADBE CLS FLNC AAOI P COHR FLEX MRVL BABA VISN',r3='ADBE MU P COHR MRVL CLS FLEX ENPH FLNC AAOI VISN BABA',r6='MU ADBE CLS FLNC AAOI P COHR FLEX MRVL BABA VISN ENPH')
add('07-收入','07','DELL FN STX WDC CLS MU SNDK AVGO NVDA ANET CRDO LITE FIX VRT TSM ETN','DELL FN STX WDC CLS MU SNDK AMD AVGO MRVL NVDA ANET COHR CRDO LITE FIX VRT TSM ETN',r3='MU SNDK CLS MRVL CRDO NVDA AVGO FN VRT LITE ANET DELL WDC STX TSM FIX ETN AMD COHR',r6='NVDA AVGO MU SNDK CLS CRDO MRVL AMD VRT FN LITE COHR TSM ANET DELL WDC STX FIX ETN')
add('07-现金','07','FN CLS MU SNDK AVGO NVDA CRDO FIX VRT EME TSM ETN','DELL FN STX WDC CLS MU SNDK AVGO MRVL NVDA ANET COHR CRDO FIX VRT EME TSM ETN META MSFT','ADBE','ADBE',r3='ADBE MU SNDK AVGO NVDA FN CLS EME ETN TSM VRT FIX CRDO ANET DELL WDC STX MSFT META MRVL COHR',r6='MU SNDK ADBE AVGO NVDA EME FN CLS TSM ETN VRT FIX CRDO ANET MSFT META DELL WDC STX MRVL COHR')
add('N03','N03','MU SNDK CLS KLIC TSM ALAB AVGO LITE MCHP GNRC HPE MKSI EME SMTC NVDA CIEN COHR ONTO VRT NVT MTSI KEYS JBL ETN ANET FN ADBE','MU SNDK CLS KLIC TSM ALAB AVGO LITE MCHP GNRC HPE MKSI EME SMTC NVDA CIEN COHR ONTO VRT NVT MTSI KEYS JBL ETN ANET FN ADBE')
add('N06','N06',' '.join(t for t in focus['N06'] if t not in words('RKLB POET NVTS APLD OKLO')),' '.join(t for t in focus['N06'] if t not in words('RKLB APLD OKLO')),r3=' '.join(focus['N06']),r6='CRDO ALAB TSEM AAOI NBIS IREN MU MRVL COHR LITE AMD NVDA AVGO CLS MOD VRT BE CRWV AMPX AEHR ONTO CAMT RMBS MTSI SITM RKLB POET NVTS APLD OKLO')
add('09','09','MU HPE NVDA META SNDK','MU SMCI HPE SANM NVDA TSM META SNDK NOK ET SIMO',r3='MU SMCI HPE SKHY SNDK NOK SIMO META ET SANM NVDA TSM',r6='MU SMCI SKHY SNDK SIMO META NOK SANM ET NVDA TSM HPE')
add('N05','N05','','SMCI MU ET FLNC PNR ST ADBE MSFT BABA')
add('E04-A','E04-A','DOV TEL MSFT NVDA HUBB EME HPE NTAP PLAB AVGO ETN AMZN JBL LRCX KLAC','DOV MSFT NVDA HUBB EME HPE NTAP PLAB AVGO ETN AMZN JBL LRCX KLAC','','TEL')
add('E05-A','E05-A',' '.join(t for t in focus['E05-A'][:27] if t not in words('ADBE ST')),' '.join(t for t in focus['E05-A'][:27] if t not in words('ADBE ST TEL')),'ADBE ST','ADBE ST TEL',r3=' '.join(focus['E05-A'][:27]),r6='ADBE NVDA TEL TSM ST VST DOV ALLE FTV MSFT EME SNDK MU PNR META CSCO AVGO HPE WDC NTAP CLS AMZN CRDO ENS BDC VRT QCOM')
add('E04-B','E04-B','DELL FN HPE NTAP CLS MU SNDK AVGO NVDA BDC ENS GNRC VST CARR DOV EME AMAT LRCX TSM ST ETN GOOGL META','DELL FN HPE NTAP CLS MU SNDK AVGO NVDA BDC ENS GNRC VST CARR DOV AMAT LRCX TSM ST ETN GOOGL META','ADBE MSFT TEL','ADBE MSFT EME TEL')
add('E05-B','E05-B','MSFT NVDA AVGO TSM EME MU NTAP HUBB FN SKHY VST META PNR','NVDA AVGO TSM VST PNR NTAP MU HUBB META SNDK SKHY FN QCOM MOD HPE EME','ADBE TEL','ADBE MSFT TEL',r3=' '.join(focus['E05-B'][:26]),r6='TEL MSFT ADBE NVDA AVGO TSM EME VST PNR NTAP MU HUBB META SNDK SKHY FN WDC STX LRCX QCOM AMAT MOD ETN HPE VRT CRDO')
add('E06-A','E06-A','ORCL CC CRWV IREN AAON SMCI FLNC APLD NBIS BE PH SITM AMPX COHR INTC DELL HPE RKLB ASML AMZN GOOGL','ORCL CC CRWV IREN AAON SMCI FLNC APLD NBIS BE PH SITM AMPX COHR INTC DELL HPE RKLB ASML AMZN GOOGL',r3=' '.join(focus['E06-A']),r6='TE CRWV IREN WOLF FLNC APLD NBIS SMCI MXL PH AAON BE SITM CC AMPX COHR RKLB ORCL CBRS INTC DELL HPE ASML AMZN GOOGL FCEL NVTS AEHR POET LWLG',kind='risk_review')
add('E06-B','E06-B','COHU MKSI VSH ORCL FLNC CRWV APLD IREN NBIS SMCI MXL CC AMPX AAON PH SITM','COHU MKSI VSH ORCL FLNC CRWV APLD IREN NBIS SMCI MXL CC AMPX AAON PH SITM INTC FCEL BE NVTS AAOI',r3=' '.join(focus['E06-B']),r6='TE CRWV IREN APLD NBIS FLNC WOLF SMCI MXL AMPX ORCL AAON PH CC SITM INTC MKSI VSH FCEL COHU RKLB BE AAOI SMR OKLO NVTS POET AXTI LWLG TSLA',kind='risk_review')

for key,v in views.items():
    for f in ['c3','c6','y3','y6','research3','research6']:
        assert len(v[f])==len(set(v[f])),(key,f)
        assert set(v[f])<=set(focus[v['report_id']]),(key,f,set(v[f])-set(focus[v['report_id']]))
    for h in ['3','6']:
        assert not(set(v['c'+h])&set(v['y'+h])),key
    for f in ['research3','research6']:
        if not v[f]: v[f]=None # not extracted as an ordered set, not an empty result

def overlap(a,b):
    if a is None or b is None: return None
    a,b=set(a),set(b)
    return {'n_a':len(a),'n_b':len(b),'overlap':len(a&b),'union':len(a|b),'jaccard':len(a&b)/len(a|b) if a|b else None,'shared':sorted(a&b),'a_only':sorted(a-b),'b_only':sorted(b-a)}
pairs=[]
for a,b in combinations(focus,2):
    pairs.append({'a':a,'b':b,**overlap(focus[a],focus[b])})
vpairs=[]
for a,b in combinations(views,2):
    if views[a]['kind']!=views[b]['kind']: continue
    vpairs.append({'a':a,'b':b,**{f:overlap(views[a][f],views[b][f]) for f in ['c3','c6','y3','y6','research3','research6']}})
counts=Counter(t for v in focus.values() for t in v)
current_reports={}
for k in focus:
    if k in ['N02','E06-A','E06-B']:continue
    current_reports[k]={h:sorted(set(t for v in views.values() if v['report_id']==k for t in v['y'+h])) for h in ['3','6']}

# Historical validation uses old July rankings, never the September focus sets.
hist_source=ROOT/'备份/会议单一入口与15排序方案复核_2026-09-07/排序证据.json'
old=json.loads(hist_source.read_text(encoding='utf-8'))
rows=list(csv.DictReader((ROOT/'备份/项目反思_2026-09-04/data/company_returns.csv').open(encoding='utf-8-sig')))
daily=list(csv.DictReader((ROOT/'备份/项目反思_2026-09-04/data/daily_prices.csv').open(encoding='utf-8-sig')))
entry={r['symbol']:Decimal(r['open'])*Decimal(r['adj_close'])/Decimal(r['close']) for r in daily if r['date']=='2026-07-14'}
historical=[]
for v in old['ranking_views']:
    field='rank_'+v['list_id']
    selected=sorted(rows,key=lambda x:float(x[field]))[:30]
    mean=sum(Decimal(x['ret_0713']) for x in selected)/Decimal(30)
    assert abs(mean-Decimal(v['top30_return']))<Decimal('0.00000000001'),v['list_id']
    open_mean=sum(Decimal(x['end_adj_close'])/entry[x['vendor_symbol']]-1 for x in selected)/Decimal(30)
    assert abs(open_mean-Decimal(v['top30_next_open_return']))<Decimal('0.00000000001'),v['list_id']
    h={k:v[k] for k in ['list_id','method_name','top30_return','top30_next_open_return','rank_ic','top30_actual_winner30','top30_positive','top30_median','old_result','old_version']}
    by_return=sorted(selected,key=lambda x:float(x['ret_0713']),reverse=True)
    h['top3_return_contributors']=[{'ticker':x['ticker'],'return':x['ret_0713'],'old_rank':x[field]} for x in by_return[:3]]
    h['mean_excluding_top3']=str(sum(Decimal(x['ret_0713']) for x in by_return[3:])/Decimal(27))
    h['old_top30']=[x['ticker'] for x in selected]
    h['width_sensitivity']={}
    all_sorted=sorted(rows,key=lambda x:float(x[field]))
    for n in [10,20,30]:
        s=all_sorted[:n]
        h['width_sensitivity'][str(n)]={'close':str(sum(Decimal(x['ret_0713']) for x in s)/Decimal(n)), 'open':str(sum(Decimal(x['end_adj_close'])/entry[x['vendor_symbol']]-1 for x in s)/Decimal(n))}
    historical.append(h)

hash_ok=all(hashlib.sha256(Path(v['report']).read_bytes()).hexdigest()==v['sha256'] for v in manifest.values())
assert hash_ok
result={'focus':focus,'focus_source_lines':anchors,'views':views,'focus_pairs':pairs,'view_pairs':vpairs,'focus_union_n':len(counts),'focus_counts':dict(counts.most_common()),'current_return_reports':current_reports,'historical':historical,'benchmarks':old['benchmarks'],'pool':old['pool'],'historical_window':old['window'],'N03_old_qualified8':old['N03_qualified8'],'reports_unchanged':hash_ok}
(OUT/'交集与选择及历史核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('focus union',len(counts),'appearances',sum(counts.values()),'same_hashes',hash_ok)
print('focus counts',counts.most_common(25))
print('highest focus overlap')
for x in sorted(pairs,key=lambda x:x['overlap'],reverse=True)[:25]:print(x['a'],x['b'],x['overlap'],'/30','unique',x['a_only'],x['b_only'])
print('current report sets',current_reports)
print('historical')
for x in historical:print(x['list_id'],round(float(x['top30_return'])*100,2),round(float(x['top30_next_open_return'])*100,2),round(float(x['rank_ic']),3),x['top30_actual_winner30'])
