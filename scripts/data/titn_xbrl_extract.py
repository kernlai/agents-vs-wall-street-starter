#!/usr/bin/env python3
"""Extract Titan Machinery (TITN) quarterly series from SEC XBRL companyfacts.
TITN fiscal year ends 31 Jan. Note: TITN is a CNH Industrial (Case IH / New Holland)
dealer, NOT a Deere dealer. Channel proxy only.
Usage: python3 titn_xbrl_extract.py <companyfacts.json> <out.csv>
"""
import json, sys, csv, datetime as dt

CONCEPTS = {
 'Revenues':'revenue_total',
 'RevenueFromContractWithCustomerExcludingAssessedTax':'revenue_total',
 'GrossProfit':'gross_profit',
 'CostOfRevenue':'cost_of_revenue',
 'InventoryNet':'inventory_net',
 'InterestExpense':'interest_expense_total',
 'FinancingInterestExpense':'floorplan_and_other_interest_expense',
 'OperatingIncomeLoss':'operating_income',
 'NetIncomeLoss':'net_income',
 'Assets':'total_assets',
 'StockholdersEquity':'stockholders_equity',
 'ReceivablesNetCurrent':'receivables_net',
 'AccountsReceivableNetCurrent':'receivables_net',
 'InventoryPartsAndComponentsNetOfReserves':'inventory_parts',
 'InventoryWorkInProcessNetOfReserves':'inventory_equipment_wip',
}

def days(a,b):
    return (dt.date.fromisoformat(b)-dt.date.fromisoformat(a)).days

def main(src, out):
    d = json.load(open(src))
    gaap = d['facts']['us-gaap']
    rows = {}   # (metric, end, form_kind) -> record
    for concept, metric in CONCEPTS.items():
        if concept not in gaap: continue
        for unit, facts in gaap[concept]['units'].items():
            for f in facts:
                end = f['end']; start = f.get('start')
                if start:
                    n = days(start, end)
                    if not (80 <= n <= 100):   # quarterly durations only
                        continue
                    dur = 'Q'
                else:
                    dur = 'I'   # instant
                key = (metric, end)
                rec = {'metric':metric,'end':end,'val':f['val'],'unit':unit,
                       'fy':f.get('fy'),'fp':f.get('fp'),'form':f.get('form'),
                       'filed':f.get('filed'),'frame':f.get('frame'),'dur':dur,
                       'accn':f.get('accn'),'concept':concept}
                prev = rows.get(key)
                # prefer the most recently filed value (restatements), prefer 10-Q/10-K
                if prev is None or (f.get('filed','') > prev['filed']):
                    rows[key] = rec
    recs = sorted(rows.values(), key=lambda r:(r['metric'], r['end']))
    with open(out,'w',newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['metric','period_end','value','unit','duration','fy','fp','form','filed','concept'])
        for r in recs:
            w.writerow([r['metric'],r['end'],r['val'],r['unit'],r['dur'],r['fy'],r['fp'],r['form'],r['filed'],r['concept']])
    print(f'wrote {len(recs)} rows to {out}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
