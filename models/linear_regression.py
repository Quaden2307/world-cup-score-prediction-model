import numpy as np
import pandas as pd

#split

df = pd.read_csv("data/processed/train.csv")

df["match_date"] = pd.to_datetime(df["match_date"])
df = df.sort_values("match_date")

train_threshold = df["match_date"].quantile(0.7)
val_threshold = df["match_date"].quantile(0.85)

train = df[df["match_date"] <= train_threshold] 
val = df[(df["match_date"] > train_threshold) & (df["match_date"] <= val_threshold)]
train = df[df["match_date"] > val_threshold]

print(train.head())