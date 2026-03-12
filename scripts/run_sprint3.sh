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
