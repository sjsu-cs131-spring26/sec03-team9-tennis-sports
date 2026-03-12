#!/usr/bin/env bash
set -euo pipefail

# CS 131 Project, Sprint 3
# Entry script to generate the Evidence Pack used in the Decision Brief.
#
# Usage:
#   ./scripts/run_sprint3.sh <DATASET_PATH> <DELIM>
#
# Example:
#   ./scripts/run_sprint3.sh /path/to/data.tsv $'\\t'
#
# Outputs:
#   out/evidence/ (evidence artifacts referenced by the Decision Brief)
#   out/run_sprint3.log
#   out/errors.log

# Usage check
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <DATASET_PATH> <DELIM>" >&2
  exit 1
fi

DATASET_PATH="$1"
DELIM="$2"

OUT_DIR="out"
EVID_DIR="${OUT_DIR}/evidence"
LOG="${OUT_DIR}/run_sprint3.log"
ERR="${OUT_DIR}/errors.log"

mkdir -p "${EVID_DIR}"
: > "${LOG}"
: > "${ERR}"

# Separate stdout and stderr globally
exec > >(tee -a "${LOG}") 2> >(tee -a "${ERR}" >&2)

echo "Sprint 3 evidence pack run"
date
echo "Dataset: ${DATASET_PATH}"
echo "Delimiter: '${DELIM}'"
echo

if [[ ! -f "${DATASET_PATH}" ]]; then
  echo "ERROR: dataset not found at: ${DATASET_PATH}" >&2
  exit 2
fi

# Basic Diagnostics

echo "File size"
ls -lh "${DATASET_PATH}" | tee "${EVID_DIR}/file_size.txt"
echo

echo "Header preview"
head -n 3 "${DATASET_PATH}" | tee "${EVID_DIR}/header_preview.txt"
echo

echo "Row count"
wc -l "${DATASET_PATH}" | tee "${EVID_DIR}/row_count.txt"
echo



# Artifact 1: Top 20 Countries by Win Rate
echo "Generating top20_ioc_by_winrate.txt..."

awk -F"${DELIM}" '
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
}' "${DATASET_PATH}" \
| sort -nr \
| head -20 \
| tee "${EVID_DIR}/top20_ioc_by_winrate.txt"

echo


# Artifact 2: Cohort Comparison (Winner vs Loser Ace Rate)
echo "Generating ace_rates_comparison.txt..."

awk -F"${DELIM}" '
NR > 1 {
    if ($30 > 0) { w_aces += $28; w_svpt += $30 }
    if ($39 > 0) { l_aces += $37; l_svpt += $39 }
}
END {
    w_rate = w_aces / w_svpt
    l_rate = l_aces / l_svpt
    print w_rate, ", winner ace rate"
    print l_rate, ", loser ace rate"
}' "${DATASET_PATH}" \
| tee "${EVID_DIR}/ace_rates_comparison.txt"

echo


# Artifact 3: Trend Slice (Height by Decade)
echo "Generating height_trend_by_decade.txt..."

awk -F"${DELIM}" '
NR > 1 {
    decade = substr($6, 1, 3) "0s"
    if ($13 > 0) { sum[decade] += $13; count[decade]++ }
}
END {
    for (d in sum)
        printf "%s, %.2f cm\n", d, (sum[d]/count[d])
}' "${DATASET_PATH}" \
| sort \
| tee "${EVID_DIR}/height_trend_by_decade.txt"

echo


# Trust Check: Missing Height Data
echo "Generating trust_check_height.txt..."

awk -F"${DELIM}" '
NR > 1 {
    if ($13 == "" || $13 == 0) missing++
    total++
}
END {
    print "Total_Matches:" total ", Missing_Height_Data:" missing
}' "${DATASET_PATH}" \
| tee "${EVID_DIR}/trust_check_height.txt"

echo


# Assumption Check: Countries with <200 Matches
echo "Generating assumption_check_ioc.txt..."
{
  echo "Countries with fewer than 200 total matches:"
  echo

  tail -n +2 "${DATASET_PATH}" \
  | cut -d"${DELIM}" -f14,22 \
  | tr "${DELIM}" '\n' \
  | grep -v '^$' \
  | sort \
  | uniq -c \
  | awk '$1 < 200' \
  | sort -n

  echo
  echo "Number of countries with less than 200 matches:"

  tail -n +2 "${DATASET_PATH}" \
  | cut -d"${DELIM}" -f14,22 \
  | tr "${DELIM}" '\n' \
  | grep -v '^$' \
  | sort \
  | uniq -c \
  | awk '$1 < 200' \
  | wc -l

  echo
} | tee "${EVID_DIR}/assumption_check_ioc.txt"



echo

echo "Sprint 3 run complete"
date