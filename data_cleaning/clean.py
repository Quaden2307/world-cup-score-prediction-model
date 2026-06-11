import os
import pandas as pd

df = pd.read_csv("data/matches.csv")
df = df[df['tournament_name'].str.contains("Women's", na=False) == False]
df["total_goals"] = df["home_team_score"] + df["away_team_score"]
df["is_knockout_stage"] = df["knockout_stage"] == 1
df = df[["home_team_name", "away_team_name", "match_date", "home_team_score",
         "away_team_score", "total_goals", "is_knockout_stage"]]

#due to certain country name changes, need to rename before the groupby
#so old histories pool under the 2026 names (incl. Czechoslovakia + Czech Republic -> Czechia):
renamed = {"United States": "USA", "Turkey": "Türkiye", "Czech Republic":
           "Czechia", "Czechoslovakia": "Czechia", "Zaire": "DR Congo"}
df["home_team_name"] = df["home_team_name"].replace(renamed)
df["away_team_name"] = df["away_team_name"].replace(renamed)

home_df = pd.DataFrame({"country": df["home_team_name"], "score": df["home_team_score"], "conceded": df["away_team_score"]})
away_df = pd.DataFrame({"country": df["away_team_name"], "score": df["away_team_score"], "conceded": df["home_team_score"]})

score_avg = pd.concat([away_df, home_df])
score_avg = score_avg.groupby("country")[["score", "conceded"]].mean()

df["home_team_mean_goals"] = df["home_team_name"].map(score_avg["score"])
df["away_team_mean_goals"] = df["away_team_name"].map(score_avg["score"])

df["home_team_mean_conceded"] = df["home_team_name"].map(score_avg["conceded"])
df["away_team_mean_conceded"] = df["away_team_name"].map(score_avg["conceded"])

fx = pd.read_csv("data/archive/wc_2026_fixtures.csv")
fx["team1_mean_goals_scored"] = fx["team1"].map(score_avg["score"])
fx["team2_mean_goals_scored"] = fx["team2"].map(score_avg["score"])
fx["team1_mean_goals_conceded"] = fx["team1"].map(score_avg["conceded"])
fx["team2_mean_goals_conceded"] = fx["team2"].map(score_avg["conceded"])


fx = fx[fx["stage"].str.contains("Group") == True]
bad = fx[(fx["team1_mean_goals_scored"].isna()) | (fx["team2_mean_goals_scored"].isna()) 
         | (fx["team1_mean_goals_conceded"].isna()) | (fx["team2_mean_goals_conceded"].isna())]

bad_team1 = fx[fx["team1_mean_goals_scored"].isna()]["team1"].unique()
bad_team2 = fx[fx["team2_mean_goals_scored"].isna()]["team2"].unique()
missing_teams = set(bad_team1) | set(bad_team2)


mean_scored = score_avg["score"].mean()
mean_conceded = score_avg["conceded"].mean()
fx["team1_mean_goals_scored"] = fx["team1_mean_goals_scored"].fillna(mean_scored)
fx["team2_mean_goals_scored"] = fx["team2_mean_goals_scored"].fillna(mean_scored)
fx["team1_mean_goals_conceded"] = fx["team1_mean_goals_conceded"].fillna(mean_conceded)
fx["team2_mean_goals_conceded"] = fx["team2_mean_goals_conceded"].fillna(mean_conceded)



print(df.head(10))
print(fx.head(10))

print(len(bad), "of", len(fx), "fixtures involved a team with no history, filled with", round(mean_scored, 3), "/", round(mean_conceded, 3))
print("NaNs left in feature columns:")
print(fx[["team1_mean_goals_scored", "team2_mean_goals_scored",
          "team1_mean_goals_conceded", "team2_mean_goals_conceded"]].isna().sum())

#hand off the clean tables to the model stage (index=False: no phantom index column)
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/train.csv", index=False)
fx.to_csv("data/processed/fixtures_2026.csv", index=False)
print("saved", len(df), "training rows and", len(fx), "fixture rows to data/processed/")