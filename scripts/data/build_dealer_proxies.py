#!/usr/bin/env python3
"""Build the public-company dealer-proxy panel for the Deere FY2026 Q3 forecast.

PROXY LABELLING (critical -- do not conflate):
  TITN  Titan Machinery  = CNH Industrial (Case IH / New Holland) dealer.
        AG-EQUIPMENT CHANNEL proxy. NOT a Deere dealer. FY ends 31 January.
  CERV  Cervus Equipment = genuine John Deere dealer (Canada/AU/NZ), TSX-listed
        until Brandt acquired it in 2021. HISTORICAL CALIBRATION ONLY. FY = calendar.
  TSCO  Tractor Supply   = rural-lifestyle RETAILER. Farmer/rural discretionary
        spending proxy ONLY. Not an equipment dealer. FY = calendar (52/53wk).
  DE    Deere & Company  = one cross-check datapoint from its own Q2 FY2026 call.

Inputs (all in the scratch dir): titn_series.csv (SEC XBRL), titn_releases.csv
(8-K EX-99.1 parses), tsco_comps.csv, plus hand-entered Cervus figures sourced
from dated press releases (URLs carried in the notes column).
"""
import csv, os, sys, datetime as dt
from collections import defaultdict

SCRATCH = sys.argv[1]
OUT = sys.argv[2]

rows = []
def add(series_id, period_end, fy, fq, entity, metric, value, units,
        source_type, source, notes=''):
    if value is None or value == '':
        return                      # missing data is an absent row, never a zero
    rows.append(dict(series_id=series_id, period_end=period_end, fiscal_year=fy,
                     fiscal_quarter=fq, entity=entity, metric=metric,
                     value=(round(value, 4) if isinstance(value, float) else value),
                     units=units, source_type=source_type, source=source, notes=notes))

def titn_fy(pe):
    d = dt.date.fromisoformat(pe)
    return {4: (d.year + 1, 'Q1'), 7: (d.year + 1, 'Q2'),
            10: (d.year + 1, 'Q3'), 1: (d.year, 'Q4')}.get(d.month, (None, None))

def cal_fq(pe):
    d = dt.date.fromisoformat(pe)
    return d.year, 'Q%d' % ((d.month - 1) // 3 + 1)

TITN_NOT = 'TITN is a CNH Industrial dealer (Case IH/New Holland), NOT a Deere dealer; ag-equipment channel proxy only'

# ---------------------------------------------------------------- TITN XBRL
xb = defaultdict(dict)
xsrc = {}
for r in csv.DictReader(open(os.path.join(SCRATCH, 'titn_series.csv'))):
    xb[r['metric']][r['period_end']] = float(r['value'])
    xsrc[(r['metric'], r['period_end'])] = f"SEC XBRL companyfacts CIK0001409171 ({r['concept']}, {r['form']} filed {r['filed']})"

XBRL_MAP = [('revenue_total', 'revenue', 'USD_thousands'),
            ('gross_profit', 'gross_profit', 'USD_thousands'),
            ('operating_income', 'operating_income', 'USD_thousands'),
            ('net_income', 'net_income', 'USD_thousands'),
            ('inventory_net', 'inventory_total', 'USD_thousands'),
            ('inventory_parts', 'inventory_parts', 'USD_thousands'),
            ('receivables_net', 'receivables_net', 'USD_thousands'),
            ('total_assets', 'total_assets', 'USD_thousands'),
            ('stockholders_equity', 'stockholders_equity', 'USD_thousands')]
for src_m, out_m, unit in XBRL_MAP:
    for pe, v in sorted(xb[src_m].items()):
        if pe < '2011-01-01':
            continue
        fy, fq = titn_fy(pe)
        if fy is None:
            continue
        add(f'titn_{out_m}', pe, fy, fq, 'Titan Machinery (TITN)', out_m, v / 1000.0,
            unit, 'sec_xbrl', xsrc[(src_m, pe)], TITN_NOT)

# derived: equipment (machinery) inventory = total - parts - work in process
for pe in sorted(xb['inventory_net']):
    if pe in xb['inventory_parts'] and pe in xb['inventory_equipment_wip']:
        fy, fq = titn_fy(pe)
        if fy is None: continue
        eq = xb['inventory_net'][pe] - xb['inventory_parts'][pe] - xb['inventory_equipment_wip'][pe]
        add('titn_inventory_equipment', pe, fy, fq, 'Titan Machinery (TITN)',
            'inventory_equipment', eq / 1000.0, 'USD_thousands', 'derived',
            'SEC XBRL CIK0001409171: InventoryNet minus InventoryPartsAndComponentsNetOfReserves minus InventoryWorkInProcessNetOfReserves',
            TITN_NOT + '; equipment/machinery inventory derived by subtraction')

# ---------------------------------------------------- TITN press releases
rel = {}
for r in csv.DictReader(open(os.path.join(SCRATCH, 'titn_releases.csv'))):
    pe = r['period_end']
    # a mid-quarter pre-announcement can duplicate a period end; keep the fuller record
    if pe in rel and sum(1 for v in rel[pe].values() if v) >= sum(1 for v in r.values() if v):
        continue
    rel[pe] = r

def f(r, k):
    v = r.get(k)
    try:
        return float(v) if v not in (None, '') else None
    except ValueError:
        return None

PR = 'SEC 8-K EX-99.1 earnings release, CIK0001409171 ({})'
for pe, r in sorted(rel.items()):
    fy, fq = titn_fy(pe)
    if fy is None: continue
    s = PR.format(r['source'])
    for line in ('equipment', 'parts', 'service', 'rental_other'):
        rv, cv = f(r, f'rev_{line}'), f(r, f'cogs_{line}')
        # press-release figures are already stated in USD thousands -- do NOT rescale
        if rv: add(f'titn_revenue_{line}', pe, fy, fq, 'Titan Machinery (TITN)',
                   f'revenue_{line}', rv, 'USD_thousands', 'sec_filing', s, TITN_NOT)
        if rv and cv:
            add(f'titn_gross_margin_{line}_pct', pe, fy, fq, 'Titan Machinery (TITN)',
                f'gross_margin_{line}_pct', 100.0 * (rv - cv) / rv, 'percent', 'derived',
                s, TITN_NOT + '; (revenue-COGS)/revenue for this product line')
    rt, ct = f(r, 'rev_total'), f(r, 'cogs_total')
    if rt and ct:
        add('titn_gross_margin_total_pct', pe, fy, fq, 'Titan Machinery (TITN)',
            'gross_margin_total_pct', 100.0 * (rt - ct) / rt, 'percent', 'derived', s, TITN_NOT)
    for k, m, u in (('floorplan_interest_expense', 'floorplan_interest_expense', 'USD_thousands'),
                    ('other_interest_expense', 'other_interest_expense', 'USD_thousands'),
                    ('floorplan_payable', 'floorplan_payable', 'USD_thousands')):
        v = f(r, k)
        if v: add(f'titn_{m}', pe, fy, fq, 'Titan Machinery (TITN)', m, v, u,
                  'sec_filing', s, TITN_NOT)
    if f(r, 'floorplan_interest_expense') and rt:
        add('titn_floorplan_interest_pct_of_revenue', pe, fy, fq, 'Titan Machinery (TITN)',
            'floorplan_interest_pct_of_revenue',
            100.0 * f(r, 'floorplan_interest_expense') / rt, 'percent', 'derived', s,
            TITN_NOT + '; carrying cost of channel inventory as a share of sales')
    for seg in ('agriculture', 'construction', 'europe', 'australia', 'international'):
        v = f(r, f'sss_{seg}')
        if v is not None:
            add(f'titn_same_store_sales_{seg}_pct', pe, fy, fq, 'Titan Machinery (TITN)',
                f'same_store_sales_{seg}_pct', v, 'percent_yoy', 'sec_filing', s,
                TITN_NOT + '; same-store sales disclosed per segment; blank quarters were not disclosed')
        v = f(r, f'segrev_{seg}')
        if v: add(f'titn_segment_revenue_{seg}', pe, fy, fq, 'Titan Machinery (TITN)',
                  f'segment_revenue_{seg}', v, 'USD_thousands', 'sec_filing', s, TITN_NOT)

# --------------------------------------- TITN equipment inventory turns (TTM)
eq_cogs = {pe: f(r, 'cogs_equipment') for pe, r in rel.items() if f(r, 'cogs_equipment')}
eq_inv = {}   # in USD thousands, to match the press-release COGS units
for pe in xb['inventory_net']:
    if pe in xb['inventory_parts'] and pe in xb['inventory_equipment_wip']:
        eq_inv[pe] = (xb['inventory_net'][pe] - xb['inventory_parts'][pe]
                      - xb['inventory_equipment_wip'][pe]) / 1000.0
ends = sorted(eq_cogs)
for i, pe in enumerate(ends):
    if i < 3: continue
    window = ends[i - 3:i + 1]
    # require a genuinely contiguous four-quarter window: first-to-last end spans 3 quarters (~273d)
    d0, d1 = dt.date.fromisoformat(window[0]), dt.date.fromisoformat(window[-1])
    if not (245 <= (d1 - d0).days <= 300): continue
    if pe not in eq_inv: continue
    fy, fq = titn_fy(pe)
    ttm = sum(eq_cogs[w] for w in window)
    add('titn_equipment_inventory_turns_ttm', pe, fy, fq, 'Titan Machinery (TITN)',
        'equipment_inventory_turns_ttm', ttm / eq_inv[pe], 'turns_per_year', 'derived',
        'SEC 8-K EX-99.1 equipment COGS (TTM) over derived period-end equipment inventory (SEC XBRL CIK0001409171)',
        TITN_NOT + '; TTM equipment cost of revenue divided by period-end equipment inventory')

# ------------------------------- TITN forward guidance (channel expectation)
GSRC = ('SEC 8-K EX-99.1 earnings release, CIK0001409171 '
        '(afy27q1ex991earningsrelease.htm, filed 2026-06-09) - FY2027 modeling assumptions, reaffirmed')
GNOT = (TITN_NOT + '; FORWARD GUIDANCE, not an actual. TITN fiscal 2027 runs Feb 2026 - Jan 2027, '
        'so it straddles Deere FY2026 Q2-Q4 and Deere FY2027 Q1.')
for m, v, u, extra in [
    ('guidance_segment_revenue_agriculture_yoy_low_pct', -20.0, 'percent_yoy', 'low end of the Down 15%-20% range'),
    ('guidance_segment_revenue_agriculture_yoy_high_pct', -15.0, 'percent_yoy', 'high end of the Down 15%-20% range'),
    ('guidance_segment_revenue_construction_yoy_low_pct', 0.0, 'percent_yoy', 'low end of the Flat to Up 5% range'),
    ('guidance_segment_revenue_construction_yoy_high_pct', 5.0, 'percent_yoy', 'high end of the Flat to Up 5% range'),
    ('guidance_equipment_gross_margin_pct', 8.4, 'percent', 'full-year consolidated equipment margin guidance, vs 7.3% actual in FY2026 (from the Q1 FY2027 earnings call, 2026-06-09)')]:
    add(f'titn_{m}', '2027-01-31', 2027, 'FY', 'Titan Machinery (TITN)', m, v, u,
        'sec_filing' if 'equipment_gross_margin' not in m else 'web',
        GSRC if 'equipment_gross_margin' not in m
        else 'https://www.fool.com/earnings/call-transcripts/2026/06/09/titan-machinery-titn-q1-2027-earnings-transcript/ (published 2026-06-09)',
        GNOT + '; ' + extra)

# --------------------------------------------------------------- CERVUS
# Genuine John Deere dealer. Figures transcribed from dated press releases (CAD).
CERV_NOT = ('Cervus Equipment: genuine John Deere dealer (largest Deere dealer group in Canada, '
            'plus AU/NZ Deere branches); TSX-listed until the Brandt acquisition closed in 2021. '
            'HISTORICAL CALIBRATION ONLY - not a current signal. Reported in CAD, calendar fiscal year. '
            'Group also carried Peterbilt (Transportation) and Bobcat/JCB (Industrial), so consolidated '
            'figures are not pure Deere-ag.')
C2019 = 'https://www.newswire.ca/news-releases/cervus-announces-2019-results-and-quarterly-dividend-845807347.html (published 2020-03-11)'
C2020 = 'https://www.newswire.ca/news-releases/cervus-announces-40-million-increase-in-2020-adjusted-income-before-tax-and-increase-to-quarterly-dividend-801578751.html (published 2021-03-10)'

CERV = [
 # (period_end, fy, metric, value, units, source)
 ('2018-12-31', 2018, 'revenue',                 1350.036, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'revenue_equipment',       1041.835, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'revenue_product_support',  308.201, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'gross_profit',             209.078, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'gross_margin_total_pct',    15.5,   'percent',      C2019),
 ('2018-12-31', 2018, 'inventory_impairment',      11.513, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'income_before_tax',         34.102, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'net_income',                24.777, 'CAD_millions', C2019),
 ('2018-12-31', 2018, 'eps_basic',                  1.58,  'CAD_per_share',C2019),
 ('2018-12-31', 2018, 'net_finance_costs',          5.498, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'revenue',                 1139.034, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'revenue_equipment',        813.393, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'revenue_product_support',  325.641, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'gross_profit',             169.351, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'gross_margin_total_pct',    14.9,   'percent',      C2019),
 ('2019-12-31', 2019, 'inventory_impairment',      24.006, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'income_before_tax',        -10.446, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'net_income',                -8.618, 'CAD_millions', C2019),
 ('2019-12-31', 2019, 'eps_basic',                 -0.56,  'CAD_per_share',C2019),
 ('2019-12-31', 2019, 'net_finance_costs',         12.369, 'CAD_millions', C2019),
 ('2020-12-31', 2020, 'revenue',                 1227.9,   'CAD_millions', C2020),
 ('2020-12-31', 2020, 'revenue_equipment',        891.9,   'CAD_millions', C2020),
 ('2020-12-31', 2020, 'revenue_product_support',  336.0,   'CAD_millions', C2020),
 ('2020-12-31', 2020, 'gross_profit',             202.3,   'CAD_millions', C2020),
 ('2020-12-31', 2020, 'gross_margin_total_pct',    16.5,   'percent',      C2020),
 ('2020-12-31', 2020, 'net_income',                25.1,   'CAD_millions', C2020),
 ('2020-12-31', 2020, 'eps_basic',                  1.62,  'CAD_per_share',C2020),
 ('2020-12-31', 2020, 'adjusted_income_before_tax',27.7,   'CAD_millions', C2020),
]
for pe, fy, m, v, u, s in CERV:
    add(f'cerv_{m}', pe, fy, 'FY', 'Cervus Equipment (TSX:CERV)', m, v, u,
        'press_release', s, CERV_NOT)

# The single most transferable Deere-dealer health metric Cervus disclosed.
TURN_NOT = (CERV_NOT + ' | USED-EQUIPMENT TURNOVER is the calibration anchor: Cervus '
            'stated an internal target of 2.50x. <2x = stressed Deere dealer; ~2.9x = healthy.')
for pe, fy, fq, v, s in [
    ('2019-06-30', 2019, 'Q2', 1.62, C2019),
    ('2019-12-31', 2019, 'FY', 1.78, C2019),
    ('2020-12-31', 2020, 'FY', 2.87, C2020)]:
    add('cerv_ag_used_equipment_turnover_ttm', pe, fy, fq, 'Cervus Equipment (TSX:CERV)',
        'ag_used_equipment_turnover_ttm', v, 'turns_per_year', 'press_release', s, TURN_NOT)
add('cerv_ag_used_equipment_turnover_target', '2020-12-31', 2020, 'FY',
    'Cervus Equipment (TSX:CERV)', 'ag_used_equipment_turnover_target', 2.50,
    'turns_per_year', 'press_release', C2020,
    "Company-stated internal target for agriculture used-equipment turnover")
for pe, fy, fq, v, s, n in [
    ('2019-06-30', 2019, 'Q2', 181.0, C2019, 'Agriculture segment used-equipment inventory at the cycle peak'),
    ('2019-12-31', 2019, 'Q4', 114.0, C2019, 'Agriculture segment used-equipment inventory, -37% vs the June 2019 peak')]:
    add('cerv_ag_used_equipment_inventory', pe, fy, fq, 'Cervus Equipment (TSX:CERV)',
        'ag_used_equipment_inventory', v, 'CAD_millions', 'press_release', s, CERV_NOT + ' | ' + n)

# ---------------------------------------------------------------- TSCO
TSCO_NOT = ('Tractor Supply is a RURAL-LIFESTYLE RETAILER, not an equipment dealer. '
            'Use only as a farmer/rural discretionary spending proxy. Its basket is consumables, '
            'animal feed, apparel and small tools - it carries no combines or high-hp tractors '
            'and no floorplan exposure, so it says nothing about dealer inventory or Deere shipments.')
for r in csv.DictReader(open(os.path.join(SCRATCH, 'tsco_comps.csv'))):
    pe = r['period_end']; fy, fq = cal_fq(pe)
    s = f"SEC 8-K EX-99.1 earnings release, CIK0000916365 ({r['source']})"
    for k, m, u in (('comp_sales_pct', 'comparable_store_sales_pct', 'percent_yoy'),
                    ('comp_transactions_pct', 'comparable_transactions_pct', 'percent_yoy'),
                    ('comp_ticket_pct', 'comparable_avg_ticket_pct', 'percent_yoy')):
        v = r.get(k)
        if v: add(f'tsco_{m}', pe, fy, fq, 'Tractor Supply (TSCO)', m, float(v), u,
                  'sec_filing', s, TSCO_NOT)
# quarters recovered individually from narrative / comparative columns
for pe, v, s in [
    ('2022-12-31', 8.6, 'SEC 8-K EX-99.1 CIK0000916365 (tsco_2023-01-26_0000916365-23-000006.txt)'),
    ('2023-12-30', -4.2, 'SEC 8-K EX-99.1 CIK0000916365 (tsco_2024-02-01_0000916365-24-000005.txt)'),
    ('2024-09-28', -0.2, 'SEC 8-K EX-99.1 CIK0000916365 (tsco_2025-10-23_0000916365-25-000157.txt, prior-year comparative column)'),
    ('2024-12-28', 0.6, 'SEC 8-K EX-99.1 CIK0000916365 (tsco_2025-01-30_0000916365-25-000008.txt)')]:
    fy, fq = cal_fq(pe)
    add('tsco_comparable_store_sales_pct', pe, fy, fq, 'Tractor Supply (TSCO)',
        'comparable_store_sales_pct', v, 'percent_yoy', 'sec_filing', s, TSCO_NOT)
for r in csv.DictReader(open(os.path.join(SCRATCH, 'tsco_series.csv'))):
    if r['metric'] not in ('revenue_total', 'gross_profit') or r['period_end'] < '2022-01-01':
        continue
    fy, fq = cal_fq(r['period_end'])
    add(f"tsco_{r['metric'].replace('_total','')}", r['period_end'], fy, fq,
        'Tractor Supply (TSCO)', r['metric'].replace('_total', ''),
        float(r['value']) / 1000.0, 'USD_thousands', 'sec_xbrl',
        f"SEC XBRL companyfacts CIK0000916365 ({r['concept']}, {r['form']} filed {r['filed']})", TSCO_NOT)

# ------------------------------------------- Deere's own cross-check datapoint
add('de_jdf_trade_wholesale_used_portfolio_yoy_pct', '2026-05-03', 2026, 'Q2',
    'Deere & Company (DE)', 'jdf_trade_wholesale_used_portfolio_yoy_pct', -15.0, 'percent_yoy',
    'corpus', 'challenge/offline-data/deere/call-transcripts/2026-05-21__de-us-20260521-call-qna__1042775.md line 137',
    'Deere management, Q2 FY2026 call: John Deere Financial trade-wholesale portfolio (used equipment '
    'financed on DEERE dealer lots) "down over 15%" y/y. Directional floor, not an exact figure. '
    'This is the only quantitative Deere-dealer used-inventory datapoint located; it corroborates the '
    'TITN/channel destock read but is Deere-specific.')

rows.sort(key=lambda r: (r['entity'], r['metric'], r['period_end']))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cols = ['series_id','period_end','fiscal_year','fiscal_quarter','entity','metric',
        'value','units','source_type','source','notes']
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow(r)
print(f'{len(rows)} rows -> {OUT}')
