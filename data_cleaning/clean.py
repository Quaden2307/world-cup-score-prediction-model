import pandas as pd

df = pd.read_csv("data/matches.csv")
df = df[df['tournament_name'].str.contains("Women's", na=False) == False]
df["total_goals"] = df["home_team_score"] + df["away_team_score"]
df["is_knockout_stage"]
df = df[["home_team_name", "away_team_name", "match_date", "home_team_score", 
         "away_team_score", "total_goals", "is_knockout_stage"]]