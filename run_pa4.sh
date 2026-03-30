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
awk -F'\t' 'BEGIN {OFS="\t"} 
NR==1 || ($6 != "" && $6 != "NA" && $11 != "" && $11 != "NA" && $21 != "" && $21 != "NA") 
' out/data_cleaned.tsv > out/data_filtered.tsv
head -n 11 out/data_filtered.tsv > out/data_filtered_sample.tsv
# -------- PART 3: RATIOS (Tina) --------
# to be added

# -------- PART 4: TEMPORAL (Updesh) --------
awk -F'\t' 'BEGIN {OFS="\t"; print "month\tmatch_count"} 
NR > 1 {
    ym = substr($6, 1, 4) "-" substr($6, 5, 2)
    if (ym ~ /^[0-9]{4}-[0-9]{2}$/) { count[ym]++ }
} 
END {
    for (m in count) print m, count[m]
}' out/data_filtered.tsv | sort > out/monthly_summary.tsv

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
