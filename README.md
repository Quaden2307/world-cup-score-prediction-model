# World Cup Match Goal Predictor

A small machine learning project I built for fun while the 2026 World Cup was
getting underway. LETS GOOOOOOO CANADA!!! 🇨🇦 🍁  I wanted hands-on practice taking a model from raw data all the
way to predictions, including writing the algorithm myself instead of just calling
a library.

The model predicts the total number of goals in a World Cup match from the two
teams' historical scoring and defensive records.

## What I built

- Cleaned and prepared the raw data: combined two Kaggle datasets, filtered to
  men's matches, reconciled team names that differed across sources (for example
  older country names like Zaire and Czechoslovakia), and handled missing values
  for teams with no match history.
- Engineered two features per team from past matches: average goals scored and
  average goals conceded.
- Implemented linear regression two ways in the same file
  (`models/linear_regression.py`): one written from scratch in NumPy, working out
  the gradient descent and its math by hand, and one using
  [scikit-learn](https://scikit-learn.org/). The scikit-learn version is there to
  check the hand-written one against a known-correct implementation.

## How it works

Each match is one row: four features (both teams' average goals scored and
conceded) and the target, total goals. The data is split by time so the model is
tested on tournaments it never trained on, and team averages are computed from the
training matches only to avoid leaking future information into the features.

## What I found

Total goals in a single match is close to random, so the model only slightly beats
guessing the average. The time-based split also surfaced something I didn't expect:
scoring has declined across World Cup eras, so a model trained on older tournaments
over-predicts modern matches. The main takeaway was how much the way you split your
data affects what you can trust about the results.

## Data

Two public Kaggle datasets, found by searching for FIFA World Cup match data:

- Match history, 1930 to 2026:
  https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup
- 2026 fixtures, teams, and tournament records:
  https://www.kaggle.com/datasets/kulkarniparth09/fifa-world-cup-complete-dataset-19302026

## Project layout

```
data_cleaning/clean.py        raw data -> cleaned tables in data/processed/
models/linear_regression.py   split, feature engineering, training, evaluation
data/                         raw csvs plus the generated processed/ tables
```

## Running it

```
pip install -r requirements.txt
python data_cleaning/clean.py
python models/linear_regression.py
```
