# Meeting 1: Stakeholder Alignment
Team: Team 9 Sec 3 - Racketrics
Date/Time: 2026-03-10 10:10
Duration: 60 minutes
Facilitator (PM): Md Waez Islam
Notetaker: Shakshi Sharma


Goal of the meeting: 
Align on one stakeholder persona, one decision question, sprint scope, and assigned action items.

1) Quick round (5 min)
- Each person: one sentence on what the stakeholder needs from this dataset.

Tennis scouts need standardized metrics for player traits to assess talent across different players

Tennis scouts need data on match outcomes and win rates to identify players who consistently perform well in competition

Tennis scouts need data that shows the relationship between measurable player traits and match wins to identify characteristics most predictive of tournament success.


2) Stakeholder persona (10 min)
- Who are they (role and context)?

Our stakeholder is a tennis scout or recruiter working for a professional or collegiate tennis program. They are responsible for identifying talent and evaluating players’ potential to win matches and succeed in tournaments.


- What do they care about (top 3 priorities)?

Our stakeholders top 3 priorities include:

1. Recruit players with the highest likelihood of success in matches and tournaments
2. Prioritize measurable, actionable traits (e.g., height, age, hand dominance, serving efficiency)when evaluating players.
3. Make recruitment decisions quickly and efficiently based on past evidence.



- What constraints do they have (time, budget, risk tolerance)?

Constrained by time (few days/weeks) to evaluate players. 

Limited in-person access to matches, and limited scouting resources/budget (5k-20k).

Generally low-to-moderate risk tolerance (single poor decision can be financially costly and fail to meet an organization’s expectations).


Decision:
Stakeholder persona = Tennis scout/recruiter evaluating players for recruitment at the collegiate or professional level.


3) Decision question (10 to 15 min)
Draft 2 to 3 candidate decision questions and select one.

Draft Q1: What patterns in ATP match data reveal which players dominate the most matches over time?

Draft Q2: Which player performance metrics should coaches prioritize to improve match win rates in ATP tournaments?

Draft Q3: Which measurable player traits (e.g., height, age, hand dominance, serving efficiency) should recruiters prioritize when identifying tennis players with the highest likelihood of match success?

Checklist:
- Answerable with our data
- Relevant to a real decision
- Supportable with 3 to 5 evidence artifacts within 2 weeks

Final decision question (one sentence):

> Which measurable player traits (e.g., height, age, hand dominance, serving efficiency) should recruiters prioritize when identifying tennis players with the highest likelihood of match success?


4) Success criteria (5 min)

- SC1: Tennis scouts/recruiters provided with evidence pack of >= 5 artifacts that can support recruitment decisions.
- SC2: All claims in decision brief are readable by non-technical stakeholder.
- SC3: Recommendations are actionable and reproducible, with scripts for verifying outputs. 


5) Scope exclusions (5 min)
What we will not do this sprint:

- Not doing: Providing exact match outcomes for an individual player.
- Not doing: Offering recommendations on which specific player to recruit.
- Not doing: Making decisions based on live match observations


6) Evidence brainstorm (10 min)
Candidate evidence artifacts:

- Artifact 1: Cohort Comparison - Winner / Loser Ace Rates
- Artifact 2: Top-N by Impact – Top 20 Countries by Win Rate
- Artifact 3: Trend Slice – Player Height by Decade
- Trust check: Height Column Missingness Summary
- Assumption test: 

7) Risks and limitations (5 to 10 min)
Finalize 3 to 5 bullets. Make them specific.

- Inconsistency in data: Player statistics may be missing. For example, detailed match stats like aces (w_ace), double faults (w_df), and match duration are sparse because precise tracking only began in the late 1990s, which can skew results.
- Variable player conditions: Factors like injuries and weather are often unrecorded, but may have a bigger impact on performance than the measurable traits.
- Limited sample size: Smaller data samples for players of certain age groups, regions, or skill levels may introduce bias.


8) Action items (10 min)
List tasks with owners and due dates (these become sprint board tickets).

Format: Task | Owner | Deliverable | Due date | Definition of Done (DoD)

1. Sprint Board & Ticketing | Md Waez Islam | Discuss/assign clear tickets for sprint 3 and guide team during meetings | 3/11 | Sprint board filled out with tickets & all tasks completed.

2. Document Meeting Artifacts | Shakshi Sharma | Meeting 1 and 2 agenda/notes/action items file, and mitigation file filled out | 3/11 | All meeting files under docs/meetings. Pushed to git. 

3. Decision Driving Artifact (1) | Pratheek | 3/11 | Decision Driving Artifact 1 reproducible from run_sprint3.sh and in the evidence pack folder (out/evidence/). Pushed to git. 

4. Decision Driving Artifact (2) | Pratheek | 3/11 | Decision Driving Artifact 2 reproducible from run_sprint3.sh and in the evidence pack folder (out/evidence/). Pushed to git.

5. Decision Driving Artifact (3) | Updesh | 3/11 | Decision Driving Artifact 3 reproducible from run_sprint3.sh and in the evidence pack folder (out/evidence/). Pushed to git.

6. 1 Trust Check Artifact | Updesh | 3/11 | One trust check artifact reproducible from run_sprint3.sh and in the evidence pack folder(out/evidence/). Pushed to git. 

7. 1 Assumption Test Artifact | Tina | 3/11 | One assumption test artifact reproducible from run_sprint3.sh and in the evidence pack folder (out/evidence/). Pushed to git. 

8. Script Reproducibility | Data Engineer ALL | Script meets all assignment requirements and is reproducible, generating 5+ evidence artifacts in (out/evidence/) | 3/11 | Finalized script pushed to git.

9. Ops Proof Txt File | Pratheek | Ops Proof txt file in (out/ops_proof.txt) and includes all requirements listed in assignment | 3/11 | Ops proof txt file pushed to git. 

10. Decision Brief | Md Waez Islam | Decision brief filled out with required sections (stakeholder, question, recommendation, etc) | 3/11 | Finalized decision brief & reviewed with the whole team.


9) Wrap (2 min)
Confirm stakeholder persona, decision question, and next steps.

Stakeholder persona confirmed as: Tennis scout/recruiter evaluating players for recruitment at the collegiate or professional level.

Decision question confirmed as: Which measurable player traits (e.g., height, age, hand dominance, serving efficiency) should recruiters prioritize when identifying tennis players with the highest likelihood of match success?

Next Steps: Complete assigned tickets and be prepared to discuss evidence artifact outputs, as well as how we can provide stakeholders with recommendations based on them.
