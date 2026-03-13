import pandas as pd
import sqlite3
import os

# ------------------------------------------------
# Create output folders
# ------------------------------------------------
os.makedirs("out/clean", exist_ok=True)

print("Loading dataset...")

# ------------------------------------------------
# Load dataset
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
# Remove duplicate rows
# ------------------------------------------------
before = len(df)
df = df.drop_duplicates()
after = len(df)

print(f"Removed {before-after} duplicate rows")

# ------------------------------------------------
# Clean surface column
# ------------------------------------------------
df["surface"] = df["surface"].astype(str).str.strip().str.title()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]

df = df[df["surface"].isin(valid_surfaces)]

# ------------------------------------------------
# Convert match duration
# ------------------------------------------------
df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

# Remove impossible durations
df = df[(df["minutes"] > 0) | (df["minutes"].isna())]

# ------------------------------------------------
# Clean player names
# ------------------------------------------------
df["winner_name"] = df["winner_name"].astype(str).str.strip()
df["loser_name"] = df["loser_name"].astype(str).str.strip()

# ------------------------------------------------
# Create year column
# ------------------------------------------------
df["year"] = df["tourney_date"].astype(str).str[:4]

# ------------------------------------------------
# Remove rows missing key values
# ------------------------------------------------
df = df.dropna(subset=["winner_name", "loser_name"])

# ------------------------------------------------
# Save cleaned dataset
# ------------------------------------------------
output_path = "out/clean/matches_cleaned.csv"

df.to_csv(output_path, index=False)

print("Clean dataset saved to:", output_path)
print("Final rows:", len(df))

