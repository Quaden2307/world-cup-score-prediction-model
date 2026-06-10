import pandas as pd

df = pd.read_csv("data/matches.csv")
df = df[df['tournament_name'].str.contains("Women's", na=False) == False]
df["total_goals"] = df["home_team_score"] + df["away_team_score"]
df["is_knockout_stage"] = df["knockout_stage"] == 1
df = df[["home_team_name", "away_team_name", "match_date", "home_team_score", 
         "away_team_score", "total_goals", "is_knockout_stage"]]


home_df = pd.DataFrame({"country": df["home_team_name"], "score": df["home_team_score"], "conceded": df["away_team_score"]})
away_df = pd.DataFrame({"country": df["away_team_name"], "score": df["away_team_score"], "conceded": df["home_team_score"]})

score_avg = pd.concat([away_df, home_df])
score_avg = score_avg.groupby("country")[["score", "conceded"]].mean()

df["home_team_mean_goals"] = df["home_team_name"].map(score_avg["score"])
df["away_team_mean_goals"] = df["away_team_name"].map(score_avg["score"])

df["home_team_mean_conceded"] = df["home_team_name"].map(score_avg["conceded"])
df["away_team_mean_conceded"] = df["away_team_name"].map(score_avg["conceded"])


fx = pd.read_csv("data/archive/wc_2026_fixtures.csv")
fx["team1_mean_goals"] = fx["team1"].map(score_avg["score"])
fx["team2_mean_goals"] = fx["team2"].map(score_avg["score"])

fx = fx[fx["stage"].str.contains("Group") == True]
bad = fx[(fx["team1_mean_goals"].isna()) | (fx["team2_mean_goals"].isna())]
bad_team1 = fx[fx["team1_mean_goals"].isna()]["team1"].unique()
bad_team2 = fx[fx["team2_mean_goals"].isna()]["team2"].unique()
missing_teams = set(bad_team1) | set(bad_team2)


print(fx.isna().sum())
print()
print(len(bad), "of", len(fx), "fixtures involve a team with no history")
print(len(missing_teams), "distinct missing teams:")
print(sorted(missing_teams))