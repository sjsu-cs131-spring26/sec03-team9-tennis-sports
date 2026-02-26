# Dataset Path: /mnt/scratch/CS131_jelenag/projects/team09_sec3/data/raw/atp*.csv
# Delimiter: Comma (,)
# Assumptions: Data is already unzipped on the IBM server.



# path to data folder (will contain /raw and /samples)
DATA_DIR="/mnt/scratch/CS131_jelenag/projects/team09_sec3/data/"


# create samples folder
mkdir -p "$DATA_DIR/samples"


# create 1k sample for atp_matches.csv 
head -n 1 "$DATA_DIR/raw/atp_matches.csv" > "$DATA_DIR/samples/atp_matches_sample.csv"
tail -n +2 "$DATA_DIR/raw/atp_matches.csv" | shuf -n 1000 >> "$DATA_DIR/samples/atp_matches_sample.csv" 


# create 1k sample for atp_matches_qual_chall.csv
head -n 1 "$DATA_DIR/raw/atp_matches_qual_chall.csv" > "$DATA_DIR/samples/atp_matches_qual_chall_sample.csv"
tail -n +2 "$DATA_DIR/raw/atp_matches_qual_chall.csv" | shuf -n 1000 >> "$DATA_DIR/samples/atp_matches_qual_chall_sample.csv"



# create 1k sample for atp_players.csv
head -n 1 "$DATA_DIR/raw/atp_players.csv" > "$DATA_DIR/samples/atp_players_sample.csv"
tail -n +2 "$DATA_DIR/raw/atp_players.csv" | shuf -n 1000 >> "$DATA_DIR/samples/atp_players_sample.csv"


# create 1k sample for atp_rankings.csv
head -n 1 "$DATA_DIR/raw/atp_rankings.csv" > "$DATA_DIR/samples/atp_rankings_sample.csv"
tail -n +2 "$DATA_DIR/raw/atp_rankings.csv" | shuf -n 1000 >> "$DATA_DIR/samples/atp_rankings_sample.csv"

# frequency table #1, distribution of tournament surfaces
tail -n +2 "$DATA_DIR/raw/atp_matches.csv" | cut -d, -f3 | grep -v '^$' | sort | uniq -c | sort -nr > "$DATA_DIR/../out/freq_surface.txt"

# frequency table #2, distribution of winning country_ioc
tail -n +2 "$DATA_DIR/raw/atp_matches.csv" | cut -d, -f14 | grep -v '^$' | sort | uniq -c | sort -nr > "$DATA_DIR/../out/freq_winner_ioc.txt"

# top-N entity list: top 100 players with the most wins
tail -n+2 "$DATA_DIR/raw/atp_matches.csv" | cut -d, -f8 | grep -v '^$' | sort | uniq -c | sort -nr > "$DATA_DIR/../out/top100_winners.txt"

# skinny table: columns tourney_id, tourney_name, tourney_level
head -n 1 "$DATA_DIR/raw/atp_matches.csv" | cut -d, -f1,2,5 > "$DATA_DIR/../out/matches_skinny.csv"
tail -n+2 "$DATA_DIR/raw/atp_matches.csv" | cut -d, -f1,2,5| sort -u >> "$DATA_DIR/../out/matches_skinny.csv"
