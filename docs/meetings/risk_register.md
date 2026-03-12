# Risks & Mitigations

Risk 1:

- Inconsistency in data: Player statistics may be missing or incomplete. For example, detailed match stats like aces (w_ace), double faults (w_df), and match duration are sparse because precise tracking only began in the late 1990s, which can skew results.

Mitigation 1:

- Check for missing values in key columns and include the results in the evidence files. If a field has too much missing data, we will avoid using it heavily in the analysis and mention the limitation in the Decision Brief.


Risk 2:

- Factors like injuries, fatigue, and weather conditions are often unrecorded in the dataset but may have a larger impact on performance than measurable statistics.
 
Mitigation 2:

- Use a variety of matches and players from different tournaments and years so the analysis is based on a larger and more diverse sample. This helps reduce bias from unusual conditions in any single match.


Risk 3:

- Some player groups (such as certain age ranges, regions, or skill levels) may have smaller sample sizes, which could introduce bias in comparisons.

Mitigation 3:

- Check the number of observations for each group when generating evidence artifacts. Avoid making strong conclusions for groups with very few samples, and clearly note these limitations.


