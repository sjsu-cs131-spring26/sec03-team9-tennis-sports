#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-data/samples/atp_matches_sample.csv}"

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR] Input file not found: $INPUT"
  exit 1
fi

chmod -R g+rX "$INPUT"

mkdir -p out logs

echo "[INFO] Starting pipeline..."

# Step 1: Clean
sed -E -f scripts/clean.sed "$INPUT" > out/clean.tsv

# Save sample (requirement)
head -5 "$INPUT" > out/sample_before.txt
head -5 out/clean.tsv > out/sample_after.txt

# Step 2: Filter
awk -f scripts/filter.awk out/clean.tsv > out/filtered.tsv

# Step 3: Metrics
awk -f scripts/metrics.awk out/filtered.tsv > out/metrics.tsv

# Step 4: Player summary
awk -f scripts/summary.awk out/metrics.tsv | sort > out/player_summary.tsv

# Step 5: Time summary
awk -f scripts/time.awk out/metrics.tsv | sort > out/time_summary.tsv

# Step 6: Signals
awk -f scripts/signals.awk out/metrics.tsv | sort -k2,2nr > out/signals.tsv

echo "[INFO] Pipeline completed."
