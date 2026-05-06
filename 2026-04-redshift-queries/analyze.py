import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import datetime
from statistics import mean


def normalize(query: str) -> str:
    q = query.strip().rstrip(";").lower()
    q = re.sub(r"'[^']*'", "?", q)
    q = re.sub(r"(?<![a-z_])-?\d+(\.\d+)?", "?", q)
    q = re.sub(r"\s+", " ", q)
    return q.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Group Redshift queries by similarity.")
    parser.add_argument("csv_file", nargs="?", help="Input CSV (default: stdin)")
    args = parser.parse_args()

    src = open(args.csv_file, newline="") if args.csv_file else sys.stdin

    try:
        reader = csv.DictReader(src)
        groups: dict[str, list[dict]] = defaultdict(list)
        for row in reader:
            if not row["querytxt"].strip().upper().startswith("SELECT"):
                continue
            key = normalize(row["querytxt"])
            groups[key].append(row)
    finally:
        if args.csv_file:
            src.close()

    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

    def build_row(key: str, rows: list[dict]) -> dict:
        def avg(col):
            vals = [float(r[col]) for r in rows if r.get(col) not in (None, "")]
            return f"{mean(vals):.3f}" if vals else ""

        def total(col):
            vals = [float(r[col]) for r in rows if r.get(col) not in (None, "")]
            return f"{sum(vals):.3f}" if vals else ""

        def most_recent(col):
            vals = [r[col] for r in rows if r.get(col)]
            v = max(vals) if vals else ""
            try:
                return datetime.fromisoformat(v).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return v

        return {
            "count":                 len(rows),
            "userids":               ",".join(sorted({r["userid"] for r in rows if r.get("userid")})),
            "most_recent_starttime": most_recent("starttime"),
            "total_exec_time_s":     total("exec_s"),
            "avg_wall_clock_s":      avg("wall_clock_s"),
            "avg_queue_s":           avg("queue_s"),
            "avg_exec_s":            avg("exec_s"),
            "normalized_key":        key,
            "sample_query":          rows[0]["querytxt"].strip(),
        }

    output_rows = [build_row(key, rows) for key, rows in sorted_groups]

    writer = csv.writer(sys.stdout)
    if output_rows:
        writer.writerow(output_rows[0].keys())
    for row in output_rows:
        writer.writerow(row.values())


if __name__ == "__main__":
    main()
