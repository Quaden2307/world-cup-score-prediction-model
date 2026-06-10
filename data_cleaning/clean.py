import pandas as pd

df = pd.read_csv("data/matches.csv")
df = df[df['tournament_name'].str.contains("Women's", na=False) == False]
df["total_goals"] = df["home_team_score"] + df["away_team_score"]
df["is_knockout_stage"] = df["knockout_stage"] == 1
df = df[["home_team_name", "away_team_name", "match_date", "home_team_score", 
         "away_team_score", "total_goals", "is_knockout_stage"]]

home_df = pd.DataFrame({"country": df["home_team_name"], "score": df["home_team_score"]})
away_df = pd.DataFrame({"country": df["away_team_name"], "score": df["away_team_score"]})

team_avg = pd.concat([away_df, home_df])
team_avg = team_avg.groupby("country")["score"].mean()

print(team_avg.tail(10))