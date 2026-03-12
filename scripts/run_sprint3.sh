#!/usr/bin/env bash

# --- 1. DEFINE PATHS (The computer needs these first!) ---
OUT_DIR="out"
EVID_DIR="${OUT_DIR}/evidence"
LOG_FILE="${OUT_DIR}/run_sprint3.log"

# Create the folder so the "Permission Denied" error goes away
mkdir -p "${EVID_DIR}"

# Start logging everything to the log file
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "Sprint 3 Run Started: $(date)"

# --- 2. YOUR DATA LOGIC ---

# Artifact 1: Top-N by Impact (Top 20 Countries by Win Rate)
echo "Generating top20_ioc_by_winrate.txt..."
awk -F',' '
NR > 1 {
    wins[$14]++
    losses[$22]++
}
END {
    for (c in wins) {
        total = wins[c] + losses[c]
        if (total > 200)
            printf "%.6f %s\n", wins[c]/total, c
    }
}' "$1" \
| sort -nr \
| head -20 \
| tee "${EVID_DIR}/top20_ioc_by_winrate.txt"

# Artifact 2: Cohort Comparison (Winner vs Loser Ace Rate)
echo "Generating ace_rates_comparison.txt..."
awk -F',' '
NR > 1 {
    if ($30 > 0) { w_aces += $28; w_svpt += $30 }
    if ($39 > 0) { l_aces += $37; l_svpt += $39 }
}
END {
    if (w_svpt > 0 && l_svpt > 0) {
        printf "Winner ace rate: %.6f\n", w_aces / w_svpt
        printf "Loser  ace rate: %.6f\n", l_aces / l_svpt
    }
}' "$1" \
> "${EVID_DIR}/ace_rates_comparison.txt" \
2> "${OUT_DIR}/errors.log"


# Artifact 3: Trend Slice (Height by Decade)
echo "Generating height_trend_by_decade.txt..."
awk -F',' 'NR > 1 { 
    decade = substr($6, 1, 3) "0s"; 
    if($13 > 0) { sum[decade] += $13; count[decade]++ } 
} END { 
    for (d in sum) printf "%s, %.2f cm\n", d, (sum[d]/count[d]) 
}' "$1" | sort | tee "${EVID_DIR}/height_trend_by_decade.txt"

# Trust Check: Missing Physical Data (Col 13)
echo "Generating trust_check_height.txt..."
awk -F',' 'NR > 1 { if($13 == "" || $13 == 0) missing++; total++ } END { print "Total_Matches:" total ", Missing_Height_Data:" missing }' "$1" \
| tee "${EVID_DIR}/trust_check_height.txt"

echo "Run Complete: $(date)"
