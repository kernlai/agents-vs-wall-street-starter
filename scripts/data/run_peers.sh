#!/bin/sh
# End-to-end rebuild of drv_peers.csv. Idempotent; all downloads are cached.
#   usage: sh run_peers.sh <work_dir> <out_csv>
set -e
WORK="${1:?work dir}"
OUT="${2:?output csv}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$WORK"

python3 "$HERE/build_peers.py"  --cache "$WORK/facts" --out "$WORK/peers.csv" \
                                --panel "$WORK/panel.json"
python3 "$HERE/build_kubota.py" --cache "$WORK/kubota_pdf" --out "$WORK/kubota.csv" \
                                --sec-facts "$WORK/facts/0000109821.json"

python3 - "$WORK/peers.csv" "$WORK/kubota.csv" "$OUT" <<'PY'
import csv, sys
hdr = ["series_id", "period_end", "fiscal_year", "fiscal_quarter", "value",
       "units", "source_type", "source", "notes"]
rows = []
for p in sys.argv[1:-1]:
    rows += list(csv.DictReader(open(p)))
rows.sort(key=lambda r: (r["series_id"], r["period_end"], r["fiscal_quarter"]))
with open(sys.argv[-1], "w", newline="") as f:
    w = csv.DictWriter(f, hdr)
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in hdr})
print("merged %d rows -> %s" % (len(rows), sys.argv[-1]))
PY

python3 "$HERE/validate_peers.py" "$OUT"
python3 "$HERE/analyze_peers.py" --csv "$OUT"
