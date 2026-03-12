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

# =================================================
# ASSUMPTION TEST 1
# Key field cleanliness
# =================================================

print("Running assumption test: key field cleanliness")

unique_tourney_ids = df["tourney_id"].nunique()
total_rows = len(df)
missing_tourney_ids = df["tourney_id"].isna().sum()

report1 = f"""
ASSUMPTION TEST 1: TOURNEY_ID CLEANLINESS

Total rows: {total_rows}
Unique tourney_id: {unique_tourney_ids}
Missing tourney_id: {missing_tourney_ids}

Duplicate rows based on tourney_id:
{total_rows - unique_tourney_ids}
"""

with open("out/evidence/assumption_test_key_field.txt", "w") as f:
    f.write(report1)

print("Saved: out/evidence/assumption_test_key_field.txt")

# =================================================
# ASSUMPTION TEST 2
# Unknown / rare surface values
# =================================================

print("Running assumption test: surface values")

surface_counts = df["surface"].value_counts()

report2 = "ASSUMPTION TEST 2: SURFACE VALUE DISTRIBUTION\n\n"
report2 += surface_counts.to_string()

with open("out/evidence/assumption_test_surface_distribution.txt", "w") as f:
    f.write(report2)

print("Saved: out/evidence/assumption_test_surface_distribution.txt")

# =================================================
# ASSUMPTION TEST 3
# Filtering rule check
# =================================================

print("Running assumption test: filtering rule")

long_matches = df[df["minutes"] > 180]
short_matches = df[df["minutes"] < 20]

report3 = f"""
ASSUMPTION TEST 3: MATCH LENGTH FILTER

Matches longer than 180 minutes:
{len(long_matches)}

Matches shorter than 20 minutes:
{len(short_matches)}

Total matches checked:
{len(df)}
"""

with open("out/evidence/assumption_test_match_length.txt", "w") as f:
    f.write(report3)

print("Saved: out/evidence/assumption_test_match_length.txt")

print("All assumption tests completed.")
