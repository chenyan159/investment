import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r'D:\investment\备份\公司调研财报后验检验_2026-09-30')
SOURCE = ROOT / 'report_inventory.json'
inventory = json.loads(SOURCE.read_text(encoding='utf-8-sig'))
DATE = re.compile(r'(20\d{2})\s*(?:年|[-/.])\s*(\d{1,2})\s*(?:月|[-/.])\s*(\d{1,2})(?:日)?')
CUTOFF = re.compile(r'(?:研究|信息|资料|数据)(?:的)?(?:截止|截至)(?:日期|时间|日|于)?|研究日期')
DRAFT = re.compile(r'成稿(?:日期|时间)?|写作与最终核验跨入|定稿(?:日期|时间)?|报告完成(?:日期|时间)?|本文于|本次交付于')
PARTIAL_DATE = re.compile(r'(?<!\d)(\d{1,2})\s*月\s*(\d{1,2})\s*日')
QUARTER = re.compile(r'(?:FY\s*20?\d{2}\s*)?Q[1-4]|(?:20\d{2}年?|FY\s*20?\d{2})(?:第)?[一二三四1234]季度|(?:下一|下个|未来[一两二12]个?)季度|近[一两二12]季', re.I)
INDEPENDENT = re.compile(r'本研究|研究(?:估计|估算|预测|推演|路径|区间|范围|判断)|工作路径|独立(?:判断|估计|预测)|参考(?:路径|模型|范围|算例)|条件(?:算例|预测|路径)|本报告(?:估计|预测|判断)|中心(?:路径|范围)')
METRIC = re.compile(r'收入|营收|营业|经营|毛利|利润|现金|出货|交付|资本开支|CapEx|FCF|EPS|销量', re.I)
NUM = re.compile(r'\d[\d,.]*(?:\s*[—–~～至±-]\s*\d[\d,.]*)?\s*(?:亿|万|百万|十亿|%|美元|亿元|B\b|M\b)', re.I)
FORWARD_YEAR = re.compile(r'FY\s*(?:202[7-9]|2[7-9])|202[7-9]年|203\d|未来[两三五十]年', re.I)
HUMAN = {
    # Deliberately selected examples, not a random sample or an exhaustive semantic classification.
    'ALAB': ('direct_quarter_or_segment_path', [289,291], 'Q3工作点550、Q4研究估算620及560—660范围，并给对应成本。'),
    'MRVL': ('direct_quarter_or_segment_path', [359], 'FY27 Q3 3.12B、Q4 3.6229B，明确与指引差异和联合变化。'),
    'NVDA': ('direct_quarter_or_segment_path', [309], 'FY27 Q3 106—110、Q4 116—126；区分公司指引与研究工作范围。'),
    'FN': ('direct_quarter_or_segment_path', [162], 'DCI分支FY27四季2.7/3.0/3.4/3.4亿美元；属于分支路径，不是集团季度全集。'),
    'RMBS': ('direct_quarter_or_segment_path', [323], '研究Q4产品116—126、royalties67—75、其他24—30。'),
    'SIMO': ('direct_quarter_or_segment_path', [296], '年度工作路径显式取Q3 530、Q4 556.894，条件化季度收入。'),
    'WDC': ('direct_quarter_or_segment_path', [293], 'FY27 Q1工作路径收入40.94亿美元、GAAP附近毛利55%，对照公司指引。'),
    'BELFB': ('direct_quarter_or_segment_path', [339], 'Q3中心215、Q4独立估计195—220，年度与季度相连。'),
    'COHR': ('direct_quarter_or_segment_path', [357], 'FY27代表季度收入23.0/25.5/28.0/30.5亿美元，有兑现条件。'),
    'GLW': ('direct_quarter_or_segment_path', [371], 'Q3约50亿、Q4研究估计52亿美元，明确指引与估计。'),
    'AXTI': ('direct_quarter_or_segment_path', [296], '研究Q3 63—69、Q4 68—80，并保留许可及交付前提。'),
    'ROG': ('direct_quarter_or_segment_path', [276], 'Q3为指引233—243，Q4研究季节性假设212—230。'),
    'TTMI': ('direct_quarter_or_segment_path', [328], '工作路径Q3 1.12B、Q4 1.28B，说明低于管理层的利润理由。'),
    'ICHR': ('direct_quarter_or_segment_path', [22,243], 'Q4条件收入350—395；FY27有代表季度序列。'),
    'TSEM': ('direct_quarter_or_segment_path', [284], 'Q4研究范围5.50亿—6.20亿美元，区别Q3公司指引。'),
    'UCTT': ('direct_quarter_or_segment_path', [269], 'Q4研究条件范围720—850，区别Q3指引。'),
    'BESIY': ('direct_quarter_or_segment_path', [298], 'Q4交付收入270—338为研究判断。'),
    'FORM': ('direct_quarter_or_segment_path', [271], 'Q4研究估算297.6，明确10.2%环比和验收驱动。'),
    'ONTO': ('direct_quarter_or_segment_path', [284], '工作范围由Q3 380—400、Q4 400—445构成。'),
    'POWL': ('direct_quarter_or_segment_path', [299], 'Q4收入320—370、经营利润65—82，明确研究估计。'),
    'CLS': ('required_quarter_or_illustration', [276,278], 'Q4 63.544亿是全年目标需达到的值，代表点一致不构成独立验证。'),
    'AAOI': ('required_quarter_or_illustration', [23], 'Q4 4.67—5.02亿美元是11亿美元年度路径所需门槛。'),
    'STX': ('required_quarter_or_illustration', [298], '四季相容序列明确不是公司季度预测、不构成独立证据。'),
    'LITE': ('required_quarter_or_illustration', [331], '季度收入为相容示例，展示全年路径需要的交付跃迁。'),
    'ASMIY': ('required_quarter_or_illustration', [319], 'Q4 1.214bn为年度目标与Q3指引中点形成的必要桥接。'),
    'MU': ('annual_multiyear_dominant_summary', [19,380,384,398,449], '当前核心数值为FY27/FY28；Q4指引检验与FY27工作预测分开。'),
    'JBL': ('annual_multiyear_dominant_summary', [3,5,26,422], 'FY26在报告日前已经结束且沿用指引；未来自主工作预测主要为FY27。'),
    'AVGO': ('annual_multiyear_dominant_summary', [9,21,334], '主结论为FY27经营与FY28事件概率，近期Q4另有公司指引。'),
    'TSM': ('annual_multiyear_dominant_summary', [23,25], '核心合并工作点是2026/2027/2028全年及年度事件概率。'),
    'MSFT': ('annual_multiyear_dominant_summary', [25,27], '核心工作点为FY27/FY28，关键联合事件也为FY28全年。'),
    'OKLO': ('annual_multiyear_dominant_summary', [9,22,228], '主要路径为2028—2030首次售电与2035规模，近期现金指引用于承受力。'),
}
rows = []
for company in inventory['companies']:
    p = Path(company['path'])
    raw = p.read_bytes()
    body = raw.decode('utf-8-sig')
    lines = body.splitlines()
    file_dates = DATE.findall(p.stem)
    filename_date = '-'.join([file_dates[-1][0], file_dates[-1][1].zfill(2), file_dates[-1][2].zfill(2)]) if file_dates else None
    cutoff_evidence, draft_evidence = [], []
    for n, line in enumerate(lines[:60], 1):
        cleaned = line.replace('*', '').replace('`', '')
        for label, bucket in [(CUTOFF, cutoff_evidence), (DRAFT, draft_evidence)]:
            m = label.search(cleaned)
            if not m:
                continue
            tail = cleaned[m.end():m.end()+(110 if bucket is cutoff_evidence else 25)]
            dm = DATE.search(tail)
            if dm:
                bucket.append({'line': n, 'date': f'{dm[1]}-{int(dm[2]):02d}-{int(dm[3]):02d}', 'text': line})
            elif bucket is draft_evidence:
                partial = PARTIAL_DATE.search(tail)
                if partial and cutoff_evidence:
                    bucket.append({'line': n, 'date': f"{cutoff_evidence[0]['date'][:4]}-{int(partial[1]):02d}-{int(partial[2]):02d}", 'year_from_cutoff': True, 'text': line})
    # These are machine candidates for inspection, never quality scores.
    quarter_hits, own_quarter_candidates, own_year_candidates = [], [], []
    for i, line in enumerate(lines):
        if QUARTER.search(line):
            quarter_hits.append({'line': i+1, 'text': line})
            window = '\n'.join(lines[max(0,i-2):min(len(lines),i+3)])
            if INDEPENDENT.search(window) and METRIC.search(window) and (NUM.search(window) or re.search(r'\d', line)):
                own_quarter_candidates.append({'line': i+1, 'text': line, 'context': window})
        if INDEPENDENT.search(line) and FORWARD_YEAR.search(line) and METRIC.search(line):
            own_year_candidates.append({'line': i+1, 'text': line})
    cutoff_date = cutoff_evidence[0]['date'] if cutoff_evidence else None
    review = HUMAN.get(company['symbol'])
    rows.append({
        'symbol': company['symbol'], 'category': company['category'], 'path': str(p),
        'inventory_report_date': company['report_date'], 'filename_date': filename_date,
        'body_cutoff_date': cutoff_date, 'body_cutoff_evidence': cutoff_evidence,
        'draft_date_evidence': draft_evidence,
        'cross_day_completion_without_exact_date': [
            {'line': n+1, 'text': line} for n,line in enumerate(lines[:10])
            if re.search(r'跨日完成|整理完成时的日期变化|截止日后完成', line)
        ],
        'sha256_frozen': company['sha256'], 'sha256_current': hashlib.sha256(raw).hexdigest(),
        'hash_matches_frozen': hashlib.sha256(raw).hexdigest() == company['sha256'],
        'filename_matches_body_cutoff': filename_date == cutoff_date,
        'inventory_matches_body_cutoff': company['report_date'] == cutoff_date,
        'quarter_token_count': len(quarter_hits),
        'quarter_hits': quarter_hits,
        'independent_quarter_candidates': own_quarter_candidates,
        'independent_annual_multiyear_candidates': own_year_candidates,
        'human_classification': review[0] if review else 'not_reviewed',
        'human_evidence': [{'line': n, 'text': lines[n-1]} for n in review[1]] if review else [],
        'human_note': review[2] if review else None,
    })

result = {
    'source_inventory': str(SOURCE), 'source_inventory_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'cutoff_local': inventory.get('cutoff_local'),
    'method': 'Full UTF-8 text traversal of frozen inventory files; opening-date extraction plus regex candidate screening. Machine flags are not proof of forecast horizon or quality. Human classifications distinguish management guidance from independent predictions.',
    'counts': {
        'reports': len(rows), 'hash_mismatches': sum(not r['hash_matches_frozen'] for r in rows),
        'unresolved_cutoff': sum(r['body_cutoff_date'] is None for r in rows),
        'filename_cutoff_mismatches': sum(not r['filename_matches_body_cutoff'] for r in rows),
        'inventory_cutoff_mismatches': sum(not r['inventory_matches_body_cutoff'] for r in rows),
        'explicit_draft_date_candidates': sum(bool(r['draft_date_evidence']) for r in rows),
        'machine_independent_quarter_candidates': sum(bool(r['independent_quarter_candidates']) for r in rows),
        'machine_independent_annual_multiyear_candidates': sum(bool(r['independent_annual_multiyear_candidates']) for r in rows),
        'human_selected_review': dict(Counter(r['human_classification'] for r in rows)),
        'cutoff_dates': dict(Counter(r['body_cutoff_date'] for r in rows)),
    },
    'reports': rows,
}
(ROOT / 'cross_report_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result['counts'], ensure_ascii=False, indent=2))
print('DATE EXCEPTIONS')
for r in rows:
    if not r['filename_matches_body_cutoff'] or not r['inventory_matches_body_cutoff'] or r['body_cutoff_date'] is None:
        print(json.dumps({k:r[k] for k in ['symbol','filename_date','inventory_report_date','body_cutoff_date','body_cutoff_evidence']}, ensure_ascii=False))
print('QUARTER CANDIDATES')
print(' '.join(r['symbol'] + ':' + str(len(r['independent_quarter_candidates'])) for r in rows if r['independent_quarter_candidates']))
