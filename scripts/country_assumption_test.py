import pandas as pd
import sqlite3
import os

# ---------------------------------------
# Create output folder
# ---------------------------------------
os.makedirs("out/evidence", exist_ok=True)

print("Loading SQLite database...")

# ---------------------------------------
# Connect to database
# ---------------------------------------
conn = sqlite3.connect("data/database.sqlite")

# Load matches table
df = pd.read_sql_query("SELECT winner_ioc, loser_ioc FROM matches", conn)

print("Loaded matches table")

# ---------------------------------------
# Count matches per country
# ---------------------------------------

winner_counts = df["winner_ioc"].value_counts()
loser_counts = df["loser_ioc"].value_counts()

country_games = winner_counts.add(loser_counts, fill_value=0)

# Countries with fewer than 200 games
rare_countries = country_games[country_games < 200]

# ---------------------------------------
# Write artifact file
# ---------------------------------------

with open("out/evidence/assumption_tests.txt", "w") as f:

    f.write("ASSUMPTION TEST ARTIFACT\n")
    f.write("-----------------------\n\n")

    f.write("Assumption:\n")
    f.write("Countries should have enough match representation.\n\n")

    f.write("Method:\n")
    f.write("Count games per country using winner_ioc + loser_ioc.\n\n")

    f.write(f"Total countries: {len(country_games)}\n")
    f.write(f"Countries with <200 games: {len(rare_countries)}\n\n")

    f.write("Countries with fewer than 200 games:\n\n")

    for country, count in rare_countries.sort_values().items():
        f.write(f"{country}: {int(count)} games\n")

print("Assumption test completed.")
print("Saved to out/evidence/assumption_tests.txt")
