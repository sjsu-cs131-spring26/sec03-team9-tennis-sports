import pandas as pd
import sqlite3
import os

# ------------------------------------------------
# Create output folder
# ------------------------------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading dataset...")

# ------------------------------------------------
# Load dataset (supports CSV or SQLite)
# ------------------------------------------------
try:
    df = pd.read_csv("data/matches.csv")
    print("Loaded matches.csv")
except:
    conn = sqlite3.connect("data/database.sqlite")
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    print("Loaded database.sqlite")

# ------------------------------------------------
# Clean column names
# ------------------------------------------------
df.columns = df.columns.str.lower().str.strip()

# ------------------------------------------------
# Clean surface values
# ------------------------------------------------
df["surface"] = df["surface"].astype(str).str.strip().str.title()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]
df = df[df["surface"].isin(valid_surfaces)]

# ------------------------------------------------
# Clean match duration
# ------------------------------------------------
df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

# ------------------------------------------------
# Create year column
# ------------------------------------------------
df["year"] = df["tourney_date"].astype(str).str[:4]

# ------------------------------------------------
# Remove rows missing key information
# ------------------------------------------------
df = df.dropna(subset=["winner_name","loser_name"])

# =====================================================
# ️⃣Top-N by Impact
# Top 10 players with most wins
# =====================================================

top_winners = (
    df["winner_name"]
    .value_counts()
    .head(10)
)

top_winners.to_csv(
    "out/evidence/top10_players_by_wins.txt",
    sep="\t",
    header=["total_wins"]
)

# =====================================================
#  Cohort Comparison
# Surface performance comparison
# =====================================================

surface_stats = (
    df.groupby("surface")
    .agg(
        matches=("surface","count"),
        avg_match_duration=("minutes","mean")
    )
)

surface_stats.to_csv(
    "out/evidence/surface_cohort_comparison.txt",
    sep="\t"
)

# =====================================================
# 3️⃣ Trend Slice
# Matches played per year
# =====================================================

matches_per_year = (
    df.groupby("year")
    .size()
    .sort_index()
)

matches_per_year.to_csv(
    "out/evidence/matches_per_year_trend.txt",
    sep="\t",
    header=["match_count"]
)

# =====================================================
# ⃣ Rule-Based Flags
# Flag long matches >180 minutes
# =====================================================

long_matches = df[df["minutes"] > 180]

long_matches[
    ["tourney_name","winner_name","loser_name","minutes"]
].to_csv(
    "out/evidence/long_matches_flag.txt",
    sep="\t",
    index=False
)

# =====================================================
#  Optional Join-Enriched Summary
# Ranking difference analysis
# =====================================================

df["winner_rank"] = pd.to_numeric(df["winner_rank"], errors="coerce")
df["loser_rank"] = pd.to_numeric(df["loser_rank"], errors="coerce")

df["rank_difference"] = df["loser_rank"] - df["winner_rank"]

rank_summary = df["rank_difference"].describe()

rank_summary.to_csv(
    "out/evidence/ranking_difference_summary.txt",
    sep="\t"
)

# =====================================================
# Evidence Summary
# =====================================================

summary = f"""
Tennis Dataset Evidence Report
--------------------------------

Total Matches Analyzed: {len(df)}
Unique Winners: {df['winner_name'].nunique()}
Surface Types: {df['surface'].nunique()}

Artifacts Generated:

1. top10_players_by_wins.txt
   Shows the players with the most match wins.

2. surface_cohort_comparison.txt
   Compares match counts and average match
   duration across different surfaces.

3. matches_per_year_trend.txt
   Shows how match volume changes over time.

4. long_matches_flag.txt
   Flags matches longer than 180 minutes.

5. ranking_difference_summary.txt
   Analyzes ranking differences between
   winners and losers.

All artifacts were generated automatically
from cleaned dataset values.
"""

with open("out/evidence/evidence_summary.txt","w") as f:
    f.write(summary)

print("Evidence artifacts generated successfully.")
