import pandas as pd
import sqlite3
import os

# --------------------------------------------------
# Create evidence folder
# --------------------------------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading dataset...")

# --------------------------------------------------
# Load dataset (CSV or SQLite)
# --------------------------------------------------
try:
    df = pd.read_csv("data/matches.csv")
    print("Loaded matches.csv")
except:
    try:
        conn = sqlite3.connect("data/database.sqlite")
        df = pd.read_sql_query("SELECT * FROM matches", conn)
        print("Loaded database.sqlite")
    except:
        print("ERROR: dataset not found in data/")
        exit()

# --------------------------------------------------
# Clean columns
# --------------------------------------------------
df.columns = df.columns.str.lower().str.strip()

# --------------------------------------------------
# Clean surface column
# --------------------------------------------------
df["surface"] = df["surface"].astype(str).str.strip().str.title()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]

df_clean = df[df["surface"].isin(valid_surfaces)]

# --------------------------------------------------
# Create year column
# --------------------------------------------------
df_clean["year"] = df_clean["tourney_date"].astype(str).str[:4]

# ==================================================
# 1️⃣ DECISION ARTIFACT
# Trend: Matches per Year
# ==================================================

matches_per_year = (
    df_clean.groupby("year")
    .size()
    .sort_index()
)

matches_per_year.to_csv(
    "out/evidence/matches_per_year_trend.txt",
    sep="\t",
    header=["match_count"]
)

# ==================================================
# 2️⃣ DECISION ARTIFACT
# Top 10 players by wins
# ==================================================

top_winners = df_clean["winner_name"].value_counts().head(10)

top_winners.to_csv(
    "out/evidence/top10_winners.txt",
    sep="\t",
    header=["wins"]
)

# ==================================================
# 3️⃣ DECISION ARTIFACT
# Surface distribution
# ==================================================

surface_distribution = df_clean["surface"].value_counts()

surface_distribution.to_csv(
    "out/evidence/surface_distribution.txt",
    sep="\t",
    header=["matches"]
)

# ==================================================
# 4️⃣ DECISION ARTIFACT
# Rule-based flag: Long matches
# ==================================================

df_clean["minutes"] = pd.to_numeric(df_clean["minutes"], errors="coerce")

long_matches = df_clean[df_clean["minutes"] > 180]

long_matches[
    ["tourney_name","winner_name","loser_name","minutes"]
].to_csv(
    "out/evidence/long_matches_flag.txt",
    sep="\t",
    index=False
)

# ==================================================
# 5️⃣ TRUST CHECK
# Missing values summary
# ==================================================

missing_summary = df_clean.isnull().sum()

missing_summary.to_csv(
    "out/evidence/missing_summary.txt",
    sep="\t"
)

# ==================================================
# 6️⃣ TRUST CHECK
# Duplicate match check
# ==================================================

duplicates = df_clean.duplicated(
    subset=["tourney_id","match_num"]
).sum()

duplicate_df = pd.DataFrame({
    "duplicate_matches":[duplicates]
})

duplicate_df.to_csv(
    "out/evidence/duplicate_match_check.txt",
    sep="\t",
    index=False
)

# ==================================================
# 7️⃣ ASSUMPTION TEST
# Surface wins summary
# ==================================================

matches_count = df_clean["surface"].value_counts().sort_index()

wins_count = df_clean.groupby("surface")["winner_name"].count().sort_index()

surface_summary = pd.DataFrame({
    "matches_played": matches_count,
    "wins_recorded": wins_count
})

surface_summary.to_csv(
    "out/evidence/surface_values_check.txt",
    sep="\t"
)

# ==================================================
# Evidence Summary
# ==================================================

summary = f"""
TENNIS DATASET EVIDENCE SUMMARY
================================

Dataset: Professional tennis match records

Total Matches Analyzed: {len(df_clean)}
Unique Players: {df_clean['winner_name'].nunique()}
Surface Types: {df_clean['surface'].nunique()}

-------------------------------------------------
Decision-Driving Artifacts
-------------------------------------------------

1. matches_per_year_trend.txt
   Shows yearly match volume to identify long-term
   participation and tournament trends.

2. top10_winners.txt
   Identifies players with the highest match wins,
   useful for impact and dominance analysis.

3. surface_distribution.txt
   Shows how matches are distributed across
   tennis surfaces (Hard, Clay, Grass, Carpet).

4. long_matches_flag.txt
   Flags matches longer than 180 minutes,
   highlighting high-intensity matches.

-------------------------------------------------
Trust Check Artifacts
-------------------------------------------------

5. missing_summary.txt
   Displays missing values for each column
   to evaluate dataset completeness.

6. duplicate_match_check.txt
   Verifies whether duplicate match records exist.

-------------------------------------------------
Assumption Test Artifact
-------------------------------------------------

7. surface_values_check.txt
   Validates surface values and counts how many
   matches and wins occur on each surface.

-------------------------------------------------
All evidence artifacts are generated automatically
by scripts and stored in the out/evidence directory.
"""

with open("out/evidence/evidence_summary.txt","w") as f:
    f.write(summary)

print("Evidence artifacts generated successfully.")
