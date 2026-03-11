#!/usr/bin/env bash
set -euo pipefail

# Sprint 3 Evidence Pack generator for SQLite tennis dataset
#
# Usage:
#   ./scripts/run_sprint3.sh data/tennis_raw/database.sqlite
#
# Outputs:
#   out/evidence/
#   out/run_sprint3.log
#   out/errors.log

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <SQLITE_DB_PATH>" >&2
  exit 1
fi

DB_PATH="$1"
OUT_DIR="out"
EVID_DIR="${OUT_DIR}/evidence"
LOG="${OUT_DIR}/run_sprint3.log"
ERR="${OUT_DIR}/errors.log"

mkdir -p "${EVID_DIR}"
: > "${LOG}"
: > "${ERR}"

exec > >(tee -a "${LOG}") 2> >(tee -a "${ERR}" >&2)

echo "Sprint 3 evidence pack run"
date
echo "Database: ${DB_PATH}"
echo

if [[ ! -f "${DB_PATH}" ]]; then
  echo "ERROR: database not found at ${DB_PATH}" >&2
  exit 2
fi

echo "Listing tables"
sqlite3 "${DB_PATH}" ".tables" | tee "${EVID_DIR}/table_list.txt"
echo

echo "Saving matches schema"
sqlite3 "${DB_PATH}" "PRAGMA table_info(matches);" | tee "${EVID_DIR}/matches_schema.txt"
echo

echo "Decision artifact 1: top surfaces"
sqlite3 "${DB_PATH}" "
SELECT COALESCE(surface, 'UNKNOWN') AS surface, COUNT(*) AS match_count
FROM matches
GROUP BY COALESCE(surface, 'UNKNOWN')
ORDER BY match_count DESC;
" | tee "${EVID_DIR}/top_surfaces.txt"
echo

echo "Decision artifact 2: top tournaments"
sqlite3 "${DB_PATH}" "
SELECT COALESCE(tourney_name, 'UNKNOWN') AS tourney_name, COUNT(*) AS match_count
FROM matches
GROUP BY COALESCE(tourney_name, 'UNKNOWN')
ORDER BY match_count DESC
LIMIT 20;
" | tee "${EVID_DIR}/top_tournaments.txt"
echo

echo "Decision artifact 3: matches by year"
sqlite3 "${DB_PATH}" "
SELECT SUBSTR(CAST(tourney_date AS TEXT), 1, 4) AS year, COUNT(*) AS match_count
FROM matches
GROUP BY SUBSTR(CAST(tourney_date AS TEXT), 1, 4)
ORDER BY year;
" | tee "${EVID_DIR}/matches_by_year.txt"
echo

echo "Trust check: missing surface values"
sqlite3 "${DB_PATH}" "
SELECT
  SUM(CASE WHEN surface IS NULL OR TRIM(surface) = '' THEN 1 ELSE 0 END) AS missing_surface_rows,
  COUNT(*) AS total_rows
FROM matches;
" | tee "${EVID_DIR}/trust_check_missing_surface.txt"
echo

echo "Assumption test: duplicate match IDs"
sqlite3 "${DB_PATH}" "
SELECT match_id, COUNT(*) AS repeats
FROM matches
GROUP BY match_id
HAVING COUNT(*) > 1
ORDER BY repeats DESC
LIMIT 20;
" | tee "${EVID_DIR}/assumption_test_duplicate_match_ids.txt"
echo

echo "Done"
date
e

