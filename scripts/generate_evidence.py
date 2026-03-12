import pandas as pd
import sqlite3
import os

conn = sqlite3.connect("data/database.sqlite")

df = pd.read_sql_query("SELECT * FROM matches", conn)

os.makedirs("out/evidence", exist_ok=True)
# -----------------------------
# Decision Artifact 1
# Top 10 players by wins
# -----------------------------
top_winners = (
    df.groupby("winner_name")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

top_winners.to_csv("out/evidence/top10_winners.csv")


# -----------------------------
# Decision Artifact 2
# Cohort comparison (surface)
# -----------------------------
surface_counts = df["surface"].value_counts()

surface_counts.to_csv("out/evidence/surface_distribution.csv")


# -----------------------------
# Decision Artifact 3
# Trend slice (matches by year)
# -----------------------------
df["year"] = df["tourney_date"].astype(str).str[:4]

matches_per_year = df.groupby("year").size()

matches_per_year.to_csv("out/evidence/matches_per_year.csv")


# -----------------------------
# Decision Artifact 4
# Rule-based flag
# matches longer than 3 hours
# -----------------------------
long_matches = df[df["minutes"] > 180]

long_matches[["tourney_name","winner_name","loser_name","minutes"]].to_csv(
    "out/evidence/long_matches_flag.csv",
    index=False
)


# -----------------------------
# Trust Check 1
# Missingness summary
# -----------------------------
missing = df.isnull().sum()

missing.to_csv("out/evidence/missing_summary.csv")


# -----------------------------
# Trust Check 2
# Duplicate match numbers
# -----------------------------
duplicates = df.duplicated(subset=["tourney_id","match_num"]).sum()

pd.DataFrame({
    "duplicate_matches":[duplicates]
}).to_csv("out/evidence/duplicate_match_check.csv", index=False)


# -----------------------------
# Assumption Test
# surface field cleanliness
# -----------------------------
surface_check = df["surface"].value_counts(dropna=False)

surface_check.to_csv("out/evidence/surface_values_check.csv")

print("Evidence files generated in out/evidence/")
