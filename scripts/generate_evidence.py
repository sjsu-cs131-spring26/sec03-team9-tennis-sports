import pandas as pd
import sqlite3
import os

# --------------------------------
# Create evidence folder
# --------------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading dataset...")

# --------------------------------
# Load dataset (CSV or SQLite)
# --------------------------------
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

# --------------------------------
# Clean column names
# --------------------------------
df.columns = df.columns.str.lower().str.strip()

# --------------------------------
# Clean surface column
# --------------------------------
df["surface"] = df["surface"].astype(str).str.strip().str.title()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]

df_clean = df[df["surface"].isin(valid_surfaces)]

# --------------------------------
# Create year column
# --------------------------------
if "tourney_date" in df_clean.columns:
    df_clean["year"] = df_clean["tourney_date"].astype(str).str[:4]

# =====================================================
# 1️⃣ Decision Artifact
# Top 10 winners
# =====================================================
top_winners = (
    df_clean["winner_name"]
    .value_counts()
    .head(10)
)

top_winners.to_csv(
    "out/evidence/top10_winners.txt",
    sep="\t"
)

# =====================================================
# 2️⃣ Decision Artifact
# Surface distribution
# =====================================================
surface_distribution = df_clean["surface"].value_counts()

surface_distribution.to_csv(
    "out/evidence/surface_distribution.txt",
    sep="\t"
)

# =====================================================
# 3️⃣ Decision Artifact
# Matches per year trend
# =====================================================
if "year" in df_clean.columns:
    matches_per_year = df_clean.groupby("year").size()

    matches_per_year.to_csv(
        "out/evidence/matches_per_year.txt",
        sep="\t"
    )

# =====================================================
# 4️⃣ Decision Artifact
# Rule based flag (long matches)
# =====================================================
if "minutes" in df_clean.columns:

    df_clean["minutes"] = pd.to_numeric(
        df_clean["minutes"], errors="coerce"
    )

    long_matches = df_clean[df_clean["minutes"] > 180]

    long_matches[
        ["tourney_name", "winner_name", "loser_name", "minutes"]
    ].to_csv(
        "out/evidence/long_matches_flag.txt",
        sep="\t",
        index=False
    )

# =====================================================
# 5️⃣ Trust Check
# Missing value summary
# =====================================================
missing_summary = df_clean.isnull().sum()

missing_summary.to_csv(
    "out/evidence/missing_summary.txt",
    sep="\t"
)

# =====================================================
# 6️⃣ Trust Check
# Duplicate match check
# =====================================================
if "tourney_id" in df_clean.columns and "match_num" in df_clean.columns:

    duplicates = df_clean.duplicated(
        subset=["tourney_id", "match_num"]
    ).sum()

    duplicate_df = pd.DataFrame({
        "duplicate_match_count": [duplicates]
    })

    duplicate_df.to_csv(
        "out/evidence/duplicate_match_check.txt",
        sep="\t",
        index=False
    )

# =====================================================
# 7️⃣ Assumption Test
# Surface wins summary (clean)
# =====================================================
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

print("Evidence pack generated successfully.")
print("Files saved in: out/evidence/")
