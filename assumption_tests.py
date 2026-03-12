import pandas as pd
import sqlite3
import os

# ------------------------------------------------
# Create output folder
# ------------------------------------------------
os.makedirs("out/evidence", exist_ok=True)

report = []

print("Loading dataset...")

# ------------------------------------------------
# Load dataset (supports CSV or SQLite)
# ------------------------------------------------
try:
    df = pd.read_csv("data/matches.csv")
    report.append("Loaded matches.csv")
except:
    conn = sqlite3.connect("data/database.sqlite")
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    report.append("Loaded database.sqlite")

# ------------------------------------------------
# Clean column names
# ------------------------------------------------
df.columns = df.columns.str.lower().str.strip()

report.append(f"Total rows before cleaning: {len(df)}")
report.append(f"Total columns: {len(df.columns)}")

# ------------------------------------------------
# Assumption Test 1 — Unique match id
# ------------------------------------------------
if "match_num" in df.columns:
    unique_ids = df["match_num"].nunique()
    report.append(f"Unique match_num values: {unique_ids}")
    report.append(f"Duplicate match_num rows: {len(df) - unique_ids}")

# ------------------------------------------------
# Assumption Test 2 — Surface field quality
# ------------------------------------------------
df["surface"] = df["surface"].astype(str).str.strip().str.title()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]

surface_counts = df["surface"].value_counts(dropna=False)

report.append("\nSurface value counts:")
report.append(surface_counts.to_string())

invalid_surfaces = df[~df["surface"].isin(valid_surfaces)]

report.append(f"\nInvalid surface rows: {len(invalid_surfaces)}")

# ------------------------------------------------
# Assumption Test 3 — Filtering rule impact
# ------------------------------------------------
rows_before = len(df)

df_filtered = df[df["surface"].isin(valid_surfaces)]

rows_after = len(df_filtered)

report.append("\nFiltering Test (valid surfaces)")
report.append(f"Rows before filter: {rows_before}")
report.append(f"Rows after filter: {rows_after}")
report.append(f"Rows removed: {rows_before - rows_after}")

# ------------------------------------------------
# Assumption Test 4 — Missing values
# ------------------------------------------------
missing = df.isnull().sum().sort_values(ascending=False)

report.append("\nTop missing columns:")
report.append(missing.head(10).to_string())

# ------------------------------------------------
# Assumption Test 5 — Match duration validity
# ------------------------------------------------
df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

invalid_minutes = df["minutes"].isna().sum()

report.append("\nMatch duration test:")
report.append(f"Invalid minutes values: {invalid_minutes}")

if "minutes" in df.columns:
    report.append("Minutes statistics:")
    report.append(df["minutes"].describe().to_string())

# ------------------------------------------------
# Assumption Test 6 — Rare values check
# ------------------------------------------------
rare_threshold = 10

rare_surfaces = surface_counts[surface_counts < rare_threshold]

report.append("\nRare surface values (<10 rows):")
report.append(rare_surfaces.to_string())

# ------------------------------------------------
# Create year column
# ------------------------------------------------
df["year"] = df["tourney_date"].astype(str).str[:4]

year_counts = df["year"].value_counts().sort_index()

report.append("\nMatches per year:")
report.append(year_counts.to_string())

# ------------------------------------------------
# Save report
# ------------------------------------------------
output_path = "out/evidence/assumption_tests.txt"

with open(output_path, "w") as f:
    f.write("\n".join(report))

print(f"Assumption tests saved to {output_path}")
