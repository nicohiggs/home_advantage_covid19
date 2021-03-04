import pandas as pd
from scipy.stats import chisquare

# num_teams * 2 (home and away strengths) plus home advantage gives number params

# NHL
df = pd.read_csv('./data/curated_csvs/nhl.csv')
# variance mean ratio
print(df.home_points.mean(), df.home_points.var(), df.home_points.var() / df.home_points.mean())
print(df.away_points.mean(), df.away_points.var(), df.away_points.var() / df.away_points.mean())
# dispersion parameter
print(chisquare(df.home_points)[0] / (len(df.home_points) - 63))
print(chisquare(df.away_points)[0] / (len(df.away_points) - 62))

# NBA
df = pd.read_csv('./data/curated_csvs/nba.csv')
print(df.home_points.mean(), df.home_points.var(), df.home_points.var() / df.home_points.mean())
print(df.away_points.mean(), df.away_points.var(), df.away_points.var() / df.away_points.mean())
print(chisquare(df.home_points)[0] / (len(df.home_points) - 61))
print(chisquare(df.away_points)[0] / (len(df.away_points) - 60))

# MLB
df = pd.read_csv('./data/curated_csvs/mlb.csv')
print(df.home_points.mean(), df.home_points.var(), df.home_points.var() / df.home_points.mean())
print(df.away_points.mean(), df.away_points.var(), df.away_points.var() / df.away_points.mean())
print(chisquare(df.home_points)[0] / (len(df.home_points) - 61))
print(chisquare(df.away_points)[0] / (len(df.away_points) - 60))

# NFL
df = pd.read_csv('./data/curated_csvs/nfl.csv')
print(df.home_points.mean(), df.home_points.var(), df.home_points.var() / df.home_points.mean())
print(df.away_points.mean(), df.away_points.var(), df.away_points.var() / df.away_points.mean())
print(chisquare(df.home_points)[0] / (len(df.home_points) - 65))
print(chisquare(df.away_points)[0] / (len(df.away_points) - 64))