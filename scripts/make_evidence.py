#!/usr/bin/env python3
import csv
import json
import sqlite3
import re
from pathlib import Path
from collections import Counter

OUT_DIR = Path("out/evidence")
DB_PATH = "data/raw/database.sqlite"
OUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

tables = [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
).fetchall()]

def get_cols(table):
    return [r[1] for r in conn.execute(f'PRAGMA table_info("{table}")').fetchall()]

def score_table(table):
    cols = [c.lower() for c in get_cols(table)]
    score = 0
    if "match" in table.lower():
        score += 5
    for key in ["winner", "loser", "surface", "date", "score", "round"]:
        if any(key in c for c in cols):
            score += 2
    return score

match_table = sorted(tables, key=score_table, reverse=True)[0]
cols = get_cols(match_table)

def pick(*names):
    for n in names:
        for c in cols:
            if c.lower() == n.lower():
                return c
    for n in names:
        for c in cols:
            if n.lower() in c.lower():
                return c
    return None

date_col = pick("date", "match_date", "tourney_date")
surface_col = pick("surface")
winner_col = pick("winner_name", "winner")
loser_col = pick("loser_name", "loser")
round_col = pick("round")
score_col = pick("score")
id_col = pick("match_id", "id")

selected_cols = [c for c in [date_col, surface_col, winner_col, loser_col, round_col, score_col, id_col] if c]
sql_cols = ", ".join(['"{}"'.format(c) for c in selected_cols])
query = 'SELECT {} FROM "{}"'.format(sql_cols, match_table)
rows = conn.execute(query).fetchall()
total_rows = len(rows)

def parse_year(v):
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    if re.match(r"^\d{8}$", s):
        y = int(s[:4]); m = int(s[4:6]); d = int(s[6:8])
        if 1 <= m <= 12 and 1 <= d <= 31:
            return y
        return None
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        y = int(s[:4]); m = int(s[5:7]); d = int(s[8:10])
        if 1 <= m <= 12 and 1 <= d <= 31:
            return y
        return None
    if re.match(r"^\d{4}$", s):
        y = int(s)
        if 1800 <= y <= 2100:
            return y
    return None

def write_csv(path, fieldnames, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data)

winner_counts = Counter()
surface_counts = Counter()
year_counts = Counter()
flag_counts = Counter()
missing_counts = Counter()
seen_ids = set()
duplicate_id_rows = 0
invalid_date_rows = 0
invalid_surface_rows = 0
unknown_surface_rows = 0

VALID_SURFACES = {"Hard", "Clay", "Grass", "Carpet"}
UNKNOWN_VALUES = {"", "unknown", "unk", "na", "n/a", "null", "none", "?"}

for r in rows:
    date_val = r[date_col] if date_col else None
    surface_val = r[surface_col] if surface_col else None
    winner_val = r[winner_col] if winner_col else None
    loser_val = r[loser_col] if loser_col else None
    round_val = r[round_col] if round_col else None
    score_val = r[score_col] if score_col else None
    id_val = r[id_col] if id_col else None

    values = {
        "date": date_val,
        "surface": surface_val,
        "winner": winner_val,
        "loser": loser_val,
        "round": round_val,
        "score": score_val,
        "id": id_val,
    }

    for k, v in values.items():
        if v is None or str(v).strip() == "":
            missing_counts[k] += 1

    if winner_val is not None and str(winner_val).strip():
        winner_counts[str(winner_val).strip()] += 1

    if surface_val is not None:
        s = str(surface_val).strip()
        if s:
            surface_counts[s] += 1
            if s.lower() in UNKNOWN_VALUES:
                unknown_surface_rows += 1
            elif s not in VALID_SURFACES:
                invalid_surface_rows += 1

    yr = parse_year(date_val)
    if yr is not None:
        year_counts[yr] += 1
    elif date_val is not None and str(date_val).strip() != "":
        invalid_date_rows += 1

    txt = " ".join([str(x).lower() for x in [round_val, score_val] if x is not None])
    if "ret" in txt or "retired" in txt:
        flag_counts["retirement_match"] += 1
    if "w/o" in txt or "walkover" in txt:
        flag_counts["walkover_match"] += 1
    if "def" in txt:
        flag_counts["default_match"] += 1

    if id_col and id_val is not None and str(id_val).strip():
        v = str(id_val).strip()
        if v in seen_ids:
            duplicate_id_rows += 1
        else:
            seen_ids.add(v)

top_players = [
    {"rank": i + 1, "winner": name, "win_count": cnt}
    for i, (name, cnt) in enumerate(winner_counts.most_common(20))
]
write_csv(
    OUT_DIR / "decision_top20_winners.csv",
    ["rank", "winner", "win_count"],
    top_players
)

cohort_rows = []
for s in ["Hard", "Clay"]:
    cnt = surface_counts.get(s, 0)
    cohort_rows.append({
        "cohort_surface": s,
        "match_count": cnt,
        "share_of_total_matches": round(cnt / total_rows, 6) if total_rows else ""
    })
write_csv(
    OUT_DIR / "decision_cohort_hard_vs_clay.csv",
    ["cohort_surface", "match_count", "share_of_total_matches"],
    cohort_rows
)

trend_rows = [{"year": y, "match_count": year_counts[y]} for y in sorted(year_counts)]
write_csv(
    OUT_DIR / "decision_trend_matches_by_year.csv",
    ["year", "match_count"],
    trend_rows
)

rule_rows = []
for k, v in sorted(flag_counts.items()):
    rule_rows.append({
        "flag_rule": k,
        "row_count": v,
        "share_of_total_rows": round(v / total_rows, 6) if total_rows else ""
    })
if not rule_rows:
    rule_rows = [{
        "flag_rule": "no_matches_found_by_rules",
        "row_count": 0,
        "share_of_total_rows": 0
    }]
write_csv(
    OUT_DIR / "decision_rule_flags.csv",
    ["flag_rule", "row_count", "share_of_total_rows"],
    rule_rows
)

trust_rows = []
for field in ["date", "surface", "winner", "loser", "round", "score", "id"]:
    trust_rows.append({
        "check_name": f"missing_{field}",
        "count": missing_counts.get(field, 0),
        "rate": round(missing_counts.get(field, 0) / total_rows, 6) if total_rows else ""
    })
trust_rows.append({
    "check_name": "invalid_date_rows",
    "count": invalid_date_rows,
    "rate": round(invalid_date_rows / total_rows, 6) if total_rows else ""
})
trust_rows.append({
    "check_name": "invalid_surface_rows",
    "count": invalid_surface_rows,
    "rate": round(invalid_surface_rows / total_rows, 6) if total_rows else ""
})
trust_rows.append({
    "check_name": "duplicate_id_rows",
    "count": duplicate_id_rows,
    "rate": round(duplicate_id_rows / total_rows, 6) if total_rows else ""
})
write_csv(
    OUT_DIR / "trust_data_quality_checks.csv",
    ["check_name", "count", "rate"],
    trust_rows
)

assumption_rows = [
    {"metric": "distinct_surface_values", "value": len(surface_counts)},
    {"metric": "unknown_surface_rows", "value": unknown_surface_rows},
    {"metric": "invalid_surface_rows", "value": invalid_surface_rows},
    {"metric": "hard_surface_rows", "value": surface_counts.get("Hard", 0)},
    {"metric": "clay_surface_rows", "value": surface_counts.get("Clay", 0)},
]
write_csv(
    OUT_DIR / "assumption_surface_field_cleanliness.csv",
    ["metric", "value"],
    assumption_rows
)

manifest = {
    "database_path": DB_PATH,
    "detected_match_table": match_table,
    "columns_used": {
        "date_col": date_col,
        "surface_col": surface_col,
        "winner_col": winner_col,
        "loser_col": loser_col,
        "round_col": round_col,
        "score_col": score_col,
        "id_col": id_col
    },
    "total_rows_scanned": total_rows,
    "evidence_files": sorted([p.name for p in OUT_DIR.glob("*") if p.is_file()])
}

with open(OUT_DIR / "manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Done.")
print(json.dumps(manifest, indent=2))
