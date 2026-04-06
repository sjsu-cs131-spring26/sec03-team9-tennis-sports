#!/bin/bash
set -euo pipefail

INPUT_FILE=$1

mkdir -p out logs
LOG_FILE="logs/pipeline.log"
echo "[$(date)] Pipeline started" > "$LOG_FILE"

# -------- PART 1: CLEANING (Waez) --------
sed -E 's/^[[:space:]]+|[[:space:]]+$//g; s/,/\t/g; s/\t{2,}/\tNA\t/g' "$INPUT_FILE" > out/data_cleaned.tsv
head -5 "$INPUT_FILE" > out/data_raw_sample.csv
head -5 out/data_cleaned.tsv > out/data_cleaned_sample.tsv

# -------- PART 2: FILTERING (Updesh) --------
awk -F'\t' 'BEGIN {OFS="\t"} 
NR==1 || ($6 != "" && $6 != "NA" && $11 != "" && $11 != "NA") 
' out/data_cleaned.tsv > out/data_filtered.tsv
head -n 11 out/data_filtered.tsv > out/data_filtered_sample.tsv

# -------- PART 3: SCOUTING REPORT (Tina) --------
awk -F'\t' '
NR>1 {
    if ($11 !~ /^[0-9]+$/ && $11 != "U" && $11 != "NA" && $11 != "") {
        p = $11
        first_in[p] += $31
        total_sv[p] += $30
        matches[p]++
    }
}
END {
    printf "%-25s\t%-10s\t%-15s\t%-15s\n", "PROSPECT", "MATCHES", "1ST_SRV_EFF", "SCOUT_RANK"
    for (p in matches) {
        if (total_sv[p] > 0) {
            eff = (first_in[p] / total_sv[p])
            if (eff > 0.70) rank="ELITE_CONSISTENT"
            else if (eff > 0.60) rank="PRO-READY"
            else rank="DEVELOPMENTAL"
            printf "%-25s\t%d\t%.2f%%\t%-15s\n", p, matches[p], eff*100, rank
        }
    }
}' out/data_filtered.tsv | sort -k3,3nr > out/entity_summary.tsv

{
    echo -e "\n--- SCOUTING DISTRIBUTION SUMMARY ---"
    printf "%-18s\t%-10s\n" "RANK" "COUNT"
    grep -c "ELITE_CONSISTENT" out/entity_summary.tsv | xargs printf "%-18s\t%d\n" "ELITE_CONSISTENT"
    grep -c "PRO-READY" out/entity_summary.tsv | xargs printf "%-18s\t%d\n" "PRO-READY"
    grep -c "DEVELOPMENTAL" out/entity_summary.tsv | xargs printf "%-18s\t%d\n" "DEVELOPMENTAL"
} >> out/entity_summary.tsv

# -------- PART 4: TEMPORAL (Updesh) --------
echo -e "month\tmatch_count\tavg_mins" > out/monthly_summary.tsv
awk -F'\t' '
NR > 1 {
    ym = substr($6, 1, 4) "-" substr($6, 5, 2)
    if (ym ~ /^[0-9]{4}-[0-9]{2}$/) { 
        count[ym]++; total_mins[ym] += $27
    }
} 
END { for (m in count) {
    avg = (count[m] > 0) ? (total_mins[m] / count[m]) : 0
    print m, count[m], sprintf("%.1f", avg)
}}' out/data_filtered.tsv | sort >> out/monthly_summary.tsv

# -------- PART 5: SIGNALS (Waez) --------
awk -F'\t' 'NR>1 { wins[$11]++ } 
END { for (p in wins) print p, wins[p] }' out/data_filtered.tsv | sort -k2,2nr -k1,1 | head -20 > out/signals.tsv

echo "Done! Results in out/ and logs in logs/"

