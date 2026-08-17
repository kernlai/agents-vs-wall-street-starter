#!/usr/bin/env python3
"""Parse Titan Machinery (TITN) earnings press releases into a tidy quarterly table.
TITN sells CNH Industrial (Case IH / New Holland) equipment. It is an AG-EQUIPMENT
CHANNEL proxy, NOT a Deere dealer.  Fiscal year ends 31 January.
Emits: revenue & COGS by product line, gross margins by line, segment revenue,
same-store sales, inventories, floorplan payable, floorplan interest expense.
"""
import re, glob, os, sys, csv, datetime as dt

MONTHS = {m: i for i, m in enumerate(
    ['January','February','March','April','May','June','July','August',
     'September','October','November','December'], 1)}

def num(s):
    s = s.strip().replace(',', '').replace('$', '').strip()
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()').strip()
    if not re.fullmatch(r'-?\d+(\.\d+)?', s):
        return None
    v = float(s)
    return -v if neg else v

def first_nums(line, k):
    """Return the first k numeric cells on a tab-separated statement line."""
    out = []
    for cell in line.split('\t'):
        v = num(cell)
        if v is not None:
            out.append(v)
        if len(out) >= k:
            break
    return out

def period_end(txt):
    m = re.search(r'Three Months Ended (\w+) (\d{1,2}),', txt)
    if not m:
        m = re.search(r'quarter ended (\w+) (\d{1,2}), (\d{4})', txt)
        if m:
            return dt.date(int(m.group(3)), MONTHS[m.group(1)], int(m.group(2))).isoformat()
        return None
    mon, day = MONTHS[m.group(1)], int(m.group(2))
    # the year row directly beneath the header carries the two comparative years
    tail = txt[m.end():m.end() + 400]
    yrs = re.findall(r'\b(20\d{2})\b', tail)
    if not yrs:
        return None
    return dt.date(int(yrs[0]), mon, day).isoformat()

def fiscal(pe):
    """TITN fiscal year ends 31 Jan; FY label = calendar year in which it ends."""
    d = dt.date.fromisoformat(pe)
    if d.month == 4:  return (d.year + 1, 'Q1')
    if d.month == 7:  return (d.year + 1, 'Q2')
    if d.month == 10: return (d.year + 1, 'Q3')
    if d.month == 1:  return (d.year, 'Q4')
    return (None, None)

LINES = {
    'Equipment': 'equipment', 'Parts': 'parts', 'Service': 'service',
    'Rental and other': 'rental_other',
}

def parse(path):
    txt = open(path).read()
    pe = period_end(txt)
    if not pe:
        return None
    fy, fq = fiscal(pe)
    if fy is None:
        return None
    rec = {'period_end': pe, 'fiscal_year': fy, 'fiscal_quarter': fq,
           'source': os.path.basename(path)}
    lines = txt.split('\n')

    # --- income statement: Revenue block then Cost of Revenue block ---
    for block, prefix in (('Revenue', 'rev'), ('Cost of Revenue', 'cogs')):
        try:
            i = next(j for j, l in enumerate(lines)
                     if l.strip() == block or l.strip() == block + '\t')
        except StopIteration:
            continue
        for l in lines[i + 1:i + 8]:
            lab = l.split('\t')[0].strip()
            if lab in LINES:
                v = first_nums(l, 1)
                if v:
                    rec[f'{prefix}_{LINES[lab]}'] = v[0]
            if lab.startswith('Total'):
                v = first_nums(l, 1)
                if v:
                    rec[f'{prefix}_total'] = v[0]
                break

    # --- floorplan interest expense (income statement line) ---
    m = re.search(r'^Floorplan interest expense\t(.*)$', txt, re.M)
    if m:
        v = first_nums(m.group(1), 1)
        if v:
            rec['floorplan_interest_expense'] = abs(v[0])
    m = re.search(r'^Other interest expense\t(.*)$', txt, re.M)
    if m:
        v = first_nums(m.group(1), 1)
        if v:
            rec['other_interest_expense'] = abs(v[0])

    # --- balance sheet ---
    m = re.search(r'^Inventories,? net ?\t(.*)$', txt, re.M | re.I)
    if m:
        v = first_nums(m.group(1), 1)
        if v: rec['inventories_net'] = v[0]
    m = re.search(r'^Floorplan payable ?\t(.*)$', txt, re.M | re.I)
    if m:
        v = first_nums(m.group(1), 1)
        if v: rec['floorplan_payable'] = v[0]
    m = re.search(r'^Total stockholders.? equity ?\t(.*)$', txt, re.M | re.I)
    if m:
        v = first_nums(m.group(1), 1)
        if v: rec['stockholders_equity'] = v[0]

    # --- narrative: equipment inventory change ---
    m = re.search(r'Equipment inventor(?:y|ies) (increased|decreased) by \$([\d.]+) million', txt)
    if m:
        rec['equipment_inventory_change_musd'] = (
            float(m.group(2)) * (1 if m.group(1) == 'increased' else -1))

    # --- segment revenue + same-store sales ---
    for seg in ('Agriculture', 'Construction', 'International', 'Europe', 'Australia'):
        m = re.search(seg + r' Segment[^\n]*?same-store sales (decrease|increase) of ([\d.]+)%', txt)
        if m:
            rec[f'sss_{seg.lower()}'] = float(m.group(2)) * (-1 if m.group(1) == 'decrease' else 1)
    m = re.search(r'^(Agriculture|Construction|International|Europe|Australia)\t(.*)$', txt, re.M)
    # segment revenue table
    try:
        i = next(j for j, l in enumerate(lines) if l.strip() == 'Revenue' and
                 any('Segment Results' in x for x in lines[max(0, j - 12):j]))
        for l in lines[i + 1:i + 8]:
            lab = l.split('\t')[0].strip()
            if lab in ('Agriculture', 'Construction', 'International', 'Europe', 'Australia'):
                v = first_nums(l, 1)
                if v: rec[f'segrev_{lab.lower()}'] = v[0]
            if lab.startswith('Total'):
                break
    except StopIteration:
        pass
    return rec

def main(indir, out):
    recs = [r for r in (parse(p) for p in sorted(glob.glob(os.path.join(indir, 'rel_*.txt')))) if r]
    recs.sort(key=lambda r: r['period_end'])
    cols = []
    for r in recs:
        for k in r:
            if k not in cols: cols.append(k)
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in recs: w.writerow(r)
    print(f'{len(recs)} quarters -> {out}')
    return recs

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
