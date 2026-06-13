import numpy as np
import pandas as pd



df = pd.read_csv("data/processed/train.csv")

df["match_date"] = pd.to_datetime(df["match_date"])
df = df.sort_values("match_date")

train_threshold = df["match_date"].quantile(0.7)
val_threshold = df["match_date"].quantile(0.85)

#split
train = df[df["match_date"] <= train_threshold] 
val = df[(df["match_date"] > train_threshold) & (df["match_date"] <= val_threshold)]
test = df[df["match_date"] > val_threshold]

#map train score_avg to train, val, and test
home_df = pd.DataFrame({"country": train["home_team_name"], "score": train["home_team_score"], "conceded": train["away_team_score"]})
away_df = pd.DataFrame({"country": train["away_team_name"], "score": train["away_team_score"], "conceded": train["home_team_score"]})

score_avg = pd.concat([away_df, home_df])
score_avg = score_avg.groupby("country")[["score", "conceded"]].mean()

def map_score_avg(old_df, score_avg):
    old_df = old_df.copy()

    old_df["home_team_mean_goals"]  = old_df["home_team_name"].map(score_avg["score"])
    old_df["away_team_mean_goals"] = old_df["away_team_name"].map(score_avg["score"])

    old_df["home_team_mean_conceded"] = old_df["home_team_name"].map(score_avg["conceded"])
    old_df["away_team_mean_conceded"] = old_df["away_team_name"].map(score_avg["conceded"])

    # teams unseen in the train era -> NaN. Fill with train-derived means.
    mean_scored = score_avg["score"].mean()
    mean_conceded = score_avg["conceded"].mean()
    old_df["home_team_mean_goals"] = old_df["home_team_mean_goals"].fillna(mean_scored)
    old_df["away_team_mean_goals"] = old_df["away_team_mean_goals"].fillna(mean_scored)
    old_df["home_team_mean_conceded"] = old_df["home_team_mean_conceded"].fillna(mean_conceded)
    old_df["away_team_mean_conceded"] = old_df["away_team_mean_conceded"].fillna(mean_conceded)

    return old_df

train = map_score_avg(train, score_avg)
val = map_score_avg(val, score_avg)
test = map_score_avg(test, score_avg)



feature_cols = ["home_team_mean_goals", "away_team_mean_goals",
                "home_team_mean_conceded", "away_team_mean_conceded"]
for name, frame in [("train", train), ("val", val), ("test", test)]:
    print(name, "rows:", len(frame), " feature NaNs:", int(frame[feature_cols].isna().sum().sum()))

