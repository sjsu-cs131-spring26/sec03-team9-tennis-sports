import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, to_date, count, avg, broadcast, round, stddev, concat_ws


def build_parser():

    # gcloud command parser
    parser = argparse.ArgumentParser(description="CS131 Project 6 Tennis Analysis")
    parser.add_argument("--matches", required=True, help="Path to matches csv")
    parser.add_argument("--qual", required=True, help="Path to qualifying matches csv")
    parser.add_argument("--players", required=True, help="Path to players csv")
    parser.add_argument("--rankings", required=True, help="Path to rankings csv")
    parser.add_argument("--output", required=True, help="Path to output")
    return parser


def main():
    args = build_parser().parse_args()

    # spark session
    spark = (
        SparkSession.builder
        .appName("CS131-Sprint-6")
        .config("spark.sql.shuffle.partitions", "100")
        .getOrCreate()
    )

    # reading in cl args into df's
    matches_raw = (spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(args.matches))

    qual_raw = (spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(args.qual))

    players_raw = (spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(args.players))

    rankings_raw = (spark.read.option("header", True)
    .option("inferSchema", True)
    .csv(args.rankings))



    # A - cleaning tasks
    for name, df in [("Matches", matches_raw), ("Players", players_raw), ("Rankings", rankings_raw), ("Qual", qual_raw)]:
        print(f"----{name}----")
        df.printSchema()

    # Prepare player names for joining
    players_named = players_raw.withColumn(
        "full_name",
        concat_ws(" ", col("name_first"), col("name_last"))
    )

    # Use broadcast for player lookups (Small table optimization)
    p_w = broadcast(players_named).alias("p_w")
    p_l = broadcast(players_named).alias("p_l")

    # Column selection list to keep code DRY
    required_cols = [
        "w_bpSaved", "w_bpFaced", "l_bpSaved", "l_bpFaced", "tourney_date", 
        "tourney_level", "w_1stWon", "w_2ndWon", "w_svpt", "l_svpt", 
        "winner_id", "loser_id", "surface", "winner_rank", "loser_rank", 
        "w_1stIn", "l_1stIn", "l_ace", "w_ace", "w_df", "l_df", "l_2ndWon"
    ]

    # Clean Main Matches
    matches = (matches_raw.select(*required_cols)
        .filter(
            (col("winner_id").isNotNull()) & (col("loser_id").isNotNull()) &
            (col("w_svpt") > 0) & (col("l_svpt") > 0) &
            (col("winner_rank").isNotNull()) & (col("loser_rank").isNotNull())
        )
        .alias("m")
        .join(p_w, col("m.winner_id") == col("p_w.player_id"), "left")
        .join(p_l, col("m.loser_id") == col("p_l.player_id"), "left")
        .select("m.*", col("p_w.full_name").alias("winner"), col("p_l.full_name").alias("loser"))
    )

    # Clean Qual Matches
    qual = (qual_raw.select(*required_cols)
        .filter(
            (col("winner_id").isNotNull()) & (col("loser_id").isNotNull()) &
            (col("w_svpt") > 0) & (col("l_svpt") > 0) &
            (col("winner_rank").isNotNull()) & (col("loser_rank").isNotNull())
        )
        .alias("q")
        .join(p_w, col("q.winner_id") == col("p_w.player_id"), "left")
        .join(p_l, col("q.loser_id") == col("p_l.player_id"), "left")
        .select("q.*", col("p_w.full_name").alias("winner"), col("p_l.full_name").alias("loser"))
    )


    # B - additional analysis tasks (Part 1)

    # filter last 10 years, remove matches with 0 break points
    # calculate winners bp_save_pct as bpSaved/bpFaced
    recent_winners = (matches
    .filter(col("tourney_date") >= 20160101)
    .filter(col("w_bpFaced") > 0)
    .withColumn("bp_save_pct", col("w_bpSaved") / col("w_bpFaced")))

    recent_winners_qual = (qual
    .filter(col("tourney_date") >= 20160101)
    .filter(col("w_bpFaced") > 0)
    .withColumn("bp_save_pct", col("w_bpSaved") / col("w_bpFaced")))

    # calculate avg bp save % by tourney level
    summary = (recent_winners
            .groupBy("tourney_level")
            .agg(round(avg(col("bp_save_pct")) * 100, 2).alias("winner_avg_bp_saved"))
            .orderBy("winner_avg_bp_saved", ascending=False))

    summary_qual = (recent_winners_qual
                    .groupBy("tourney_level")
                    .agg(round(avg("bp_save_pct") * 100, 2).alias("winner_avg_bp_saved"))
                    .orderBy("winner_avg_bp_saved", ascending=False))

    print("Average break point saved % of winners in main draw (2016-2026):")
    summary.show()

    print("Average break point saved % of winners in qual draw (2016-2026):")
    summary_qual.show()

    # writing results back to cloud storage
    summary.write.mode("overwrite").partitionBy("tourney_level").parquet(f"{args.output}/main_draw_BPS")
    summary_qual.write.mode("overwrite").partitionBy("tourney_level").parquet(f"{args.output}/qual_BPS")



    # B - additional analysis tasks (Part 2)

    # main draw

    # filtering last 10 years and svpt > 0
    # calculating serving dominance metric
    recent_matches = (matches
        .filter("tourney_date >= 20160101 AND w_svpt > 0")
        .withColumn("dom", (col("w_1stWon") + col("w_2ndWon")) / col("w_svpt")))

    # average the serving dominance by surface
    surface_summary = (recent_matches
        .groupBy("surface")
        .agg(round(avg("dom") * 100, 2).alias("avgSD"))
        .orderBy("avgSD", ascending=False))

    # calculate volatility value
    # group by winner and surface to get each player's average serving dominance per surface
    # group by winner to find the standard deviation of those averages (v)
    # filter out nulls (players who only played on one surface) 
    # average all individual volatility scores to get a single threshold
    volatility = (recent_matches
        .groupBy("winner_id", "surface").agg(avg("dom").alias("p_avg"))
        .groupBy("winner_id").agg(stddev("p_avg").alias("v"))
        .filter(col("v").isNotNull())
        .agg(round(avg("v") * 100, 2).alias("avg_volatility_threshold")))


    # qual draw
    recent_matches_qual = (qual
        .filter("tourney_date >= 20160101 AND w_svpt > 0")
        .withColumn("dom", (col("w_1stWon") + col("w_2ndWon")) / col("w_svpt")))

    surface_summary_qual = (recent_matches_qual
        .groupBy("surface")
        .agg(round(avg("dom") * 100, 2).alias("avgSD"))
        .orderBy("avgSD", ascending=False))

    volatility_qual = (recent_matches_qual
        .groupBy("winner_id", "surface").agg(avg("dom").alias("p_avg"))
        .groupBy("winner_id").agg(stddev("p_avg").alias("v"))
        .filter(col("v").isNotNull())
        .agg(round(avg("v") * 100, 2).alias("avg_volatility_threshold")))

    print("Surface Dominance (Main Draw):")
    surface_summary.show()
    print("Volatility (Main Draw):")
    volatility.show()


    print("Surface Dominance (Qual):")
    surface_summary_qual.show()
    print("Volatility (Qual):")
    volatility_qual.show()

    surface_summary.write.mode("overwrite").partitionBy("surface").parquet(f"{args.output}/main_surface_dom")
    surface_summary_qual.write.mode("overwrite").parquet(f"{args.output}/qual_surface_dom")

    # B - additional analysis tasks (Part 3)

    # filter by last 10 years, loser rank exceeded winner rank by 20 (as per your code logic)
    upset_matches = matches.filter(col("tourney_date") >= 20160101) \
                        .filter(col("winner_rank") > col("loser_rank") + 20) \
                        .filter((col("w_bpFaced") > 0) & (col("l_bpFaced") > 0)) \
                        .filter((col("w_svpt") > col("w_1stIn")) & (col("l_svpt") > col("l_1stIn")))

    # calculating performance gap of winner vs loser
    upset_stats = upset_matches.withColumn(
        "ace_gap", col("w_ace") - col("l_ace")
    ).withColumn(
        "bp_save_gap", (col("w_bpSaved") / col("w_bpFaced")) - (col("l_bpSaved") / col("l_bpFaced"))
    ).withColumn(
        "first_serve_gap", (col("w_1stIn") / col("w_svpt")) - (col("l_1stIn") / col("l_svpt"))
    ).withColumn(
        "second_serve_win_gap",
        (col("w_2ndWon") / (col("w_svpt") - col("w_1stIn"))) -
        (col("l_2ndWon") / (col("l_svpt") - col("l_1stIn")))
    ).withColumn(
        "df_gap", col("w_df") - col("l_df")
    )

    underdog_report = upset_stats.agg(
        round(avg("ace_gap"), 2).alias("avg_extra_aces"),
        round(avg("bp_save_gap") * 100, 2).alias("avg_extra_bp_save_pct"),
        round(avg("first_serve_gap") * 100, 2).alias("avg_extra_1st_serve_pct"),
        round(avg("second_serve_win_gap") * 100, 2).alias("avg_extra_2nd_serve_win_pct"),
        round(avg("df_gap"), 2).alias("avg_df_diff")
    )

    underdog_report.show()

    underdog_report.write.mode("overwrite").parquet(f"{args.output}/upset_performance_gaps")


    # additional analysis for quick use of broadcasted players table
    country = broadcast(players_raw
        .select("player_id", col("ioc").alias("winner_country")))

    ioc_wins = (matches
        .join(country, col("winner_id") == col("player_id"))
        .groupBy("winner_country")
        .agg(count("*").alias("total_wins"))
        .orderBy("total_wins", ascending=False))

    print("Total Wins by Country (IOC)")
    ioc_wins.show(10)

    # writing back to cloud storage
    (ioc_wins
    .coalesce(1) 
    .write
    .mode("overwrite")
    .parquet(f"{args.output}/country_win_stats"))

    spark.stop()

if __name__ == "__main__":
    main()
