#!/bin/bash
set -euo pipefail

INPUT_FILE=$1

mkdir -p out logs

# -------- PART 1: CLEANING (Waez) --------
head -5 "$INPUT_FILE" > out/data_raw_sample.csv

sed -E '
s/^[[:space:]]+|[[:space:]]+$//g;
s/,/\t/g;
s/\t{2,}/\tNA\t/g
' "$INPUT_FILE" > out/data_cleaned.tsv

head -5 out/data_cleaned.tsv > out/data_cleaned_sample.tsv

# -------- PART 2: FILTERING (Updesh) --------
# to be added

# -------- PART 3: RATIOS (Tina) --------
# to be added

# -------- PART 4: TEMPORAL (Updesh) --------
# to be added

# -------- PART 5: SIGNALS (Waez) --------
awk -F'\t' '
NR>1 {
  player = $11
  wins[player]++
}
END {
  for (p in wins) {
    print p, wins[p]
  }
}' out/data_filtered.tsv | sort -k2 -nr | head -20 > out/signals.tsv
