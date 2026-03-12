import pandas as pd
import sqlite3
import os

# -----------------------------
# Create output folder
# -----------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading dataset...")

# -----------------------------
# Load dataset
# Supports CSV or SQLite
# -----------------------------
try:
    df = pd.read_csv("data/matches.csv")
    print("Loaded matches.csv")
except:
    try:
        conn = sqlite3.connect("data/database.sqlite")
        df = pd.read_sql_query("SELECT * FROM matches", conn)
        print("Loaded database.sqlite")
    except:
        print("ERROR: Dataset not found in data/ folder.")
        exit()

# -----------------------------
# Basic cleaning
# -----------------------------
df.columns = df.columns.str.lower()

if "tourney_date" in df.columns:
    df["year"] = df["tourney_date"].astype(str).str[:4]

# =================================================
# DECISION ARTIFACT 1
# Top 10 players by total wins
# =================================================
top_winners = (
    df.groupby("winner_name")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

top_winners.to_csv("out/evidence/top10_winners.csv")

# =================================================
# DECISION ARTIFACT 2
# Surface distribution (cohort comparison)
# =================================================
surface_distribution = df["surface"].value_counts(dropna=False)

surface_distribution.to_csv("out/evidence/surface_distribution.csv")

# =================================================
# DECISION ARTIFACT 3
# Trend slice: matches per year
# =================================================
if "year" in df.columns:
    matches_per_year = df.groupby("year").size()
else:
    matches_per_year = pd.Series(["year column missing"])

matches_per_year.to_csv("out/evidence/matches_per_year.csv")

# =================================================
# DECISION ARTIFACT 4
# Rule-based flags: long matches
# =================================================
if "minutes" in df.columns:
    long_matches = df[df["minutes"] > 180]

    long_matches[[
        "tourney_name",
        "winner_name",
        "loser_name",
        "minutes"
    ]].to_csv(
        "out/evidence/long_matches_flag.csv",
        index=False
    )
else:
    pd.DataFrame({"info":["minutes column missing"]}).to_csv(
        "out/evidence/long_matches_flag.csv",
        index=False
    )

# =================================================
# TRUST CHECK 1
# Missing values summary
# =================================================
missing_summary = df.isnull().sum()

missing_summary.to_csv("out/evidence/missing_summary.csv")

# =================================================
# TRUST CHECK 2
# Duplicate match check
# =================================================
if "tourney_id" in df.columns and "match_num" in df.columns:
    duplicates = df.duplicated(subset=["tourney_id","match_num"]).sum()
else:
    duplicates = "Columns not found"

duplicate_df = pd.DataFrame({
    "duplicate_match_count":[duplicates]
})

duplicate_df.to_csv("out/evidence/duplicate_match_check.csv", index=False)

# =================================================
# ASSUMPTION TEST
# Surface field cleanliness
# =================================================
surface_values = df["surface"].value_counts(dropna=False)

surface_values.to_csv("out/evidence/surface_values_check.csv")

# =================================================
# TEXT SUMMARY REPORT
# =================================================
summary_text = f"""
TENNIS DATASET EVIDENCE REPORT
==============================

Total Matches: {len(df)}

Unique Winners: {df['winner_name'].nunique() if 'winner_name' in df.columns else 'unknown'}

Surface Types: {df['surface'].nunique() if 'surface' in df.columns else 'unknown'}

Evidence Artifacts Generated:
--------------------------------
1. top10_winners.csv
2. surface_distribution.csv
3. matches_per_year.csv
4. long_matches_flag.csv
5. missing_summary.csv
6. duplicate_match_check.csv
7. surface_values_check.csv

Purpose:
--------------------------------
These artifacts support decision analysis, trust checks,
and assumption testing for the tennis dataset.

Generated automatically via scripts.
"""

with open("out/evidence/evidence_summary.txt", "w") as f:
    f.write(summary_text)

print("Evidence generation complete.")
print("Files saved to: out/evidence/")
