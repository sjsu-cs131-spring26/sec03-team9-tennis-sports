import pandas as pd
import sqlite3
import os

# ------------------------------------------------
# Create output folder
# ------------------------------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading database...")

# ------------------------------------------------
# Load SQLite database
# ------------------------------------------------
conn = sqlite3.connect("data/database.sqlite")

df = pd.read_sql_query("SELECT * FROM matches", conn)

print("Loaded matches table")

# Clean column names
df.columns = df.columns.str.lower().str.strip()

# ------------------------------------------------
# TEST 1: Country representation
# ------------------------------------------------

winner_counts = df["winner_ioc"].value_counts()
loser_counts = df["loser_ioc"].value_counts()

country_games = winner_counts.add(loser_counts, fill_value=0)

rare_countries = country_games[country_games < 200]

# ------------------------------------------------
# TEST 2: Surface values check
# ------------------------------------------------

df["surface"] = df["surface"].astype(str).str.strip().str.title()

surface_distribution = df["surface"].value_counts()

valid_surfaces = ["Hard", "Clay", "Grass", "Carpet"]

unknown_surfaces = df[~df["surface"].isin(valid_surfaces)]

# ------------------------------------------------
# TEST 3: Match duration sanity check
# ------------------------------------------------

df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

long_matches = df[df["minutes"] > 300]
short_matches = df[df["minutes"] < 20]

# ------------------------------------------------
# Write combined artifact
# ------------------------------------------------

with open("out/evidence/assumption_tests.txt", "w") as f:

    f.write("ASSUMPTION TEST ARTIFACTS\n")
    f.write("=========================\n\n")

    # ------------------------------
    # Country representation
    # ------------------------------

    f.write("TEST 1: Country Representation\n")
    f.write("--------------------------------\n")

    f.write(f"Total countries: {len(country_games)}\n")
    f.write(f"Countries with <200 games: {len(rare_countries)}\n\n")

    for country, count in rare_countries.sort_values().items():
        f.write(f"{country}: {int(count)} games\n")

    f.write("\n\n")

    # ------------------------------
    # Surface validation
    # ------------------------------

    f.write("TEST 2: Surface Value Distribution\n")
    f.write("----------------------------------\n")

    f.write(surface_distribution.to_string())

    f.write("\n\nUnknown surface values:\n")
    f.write(str(len(unknown_surfaces)))

    f.write("\n\n")

    # ------------------------------
    # Match duration sanity
    # ------------------------------

    f.write("TEST 3: Match Duration Check\n")
    f.write("----------------------------\n")

    f.write(f"Matches longer than 300 minutes: {len(long_matches)}\n")
    f.write(f"Matches shorter than 20 minutes: {len(short_matches)}\n")

print("Assumption tests completed.")
print("Output saved to out/evidence/assumption_tests.txt")
