'''
The script takes the csvs  from retrosheet (https://www.retrosheet.org/) and
converts them into a csv that is convenient for the modelling we want to do.
That is we need home/away goals, home/away id, regular season or playoffs, which season (i.e. year)
'''
import pandas as pd

mlb_team2id = {'SFN' : 0,
               'NYA' : 1,
               'MIL' : 2,
               'DET' : 3,
               'ATL' : 4,
               'MIA' : 5,
               'ARI' : 6,
               'PIT' : 7,
               'BAL' : 8,
               'MIN' : 9,
               'KCA' : 10,
               'SEA' : 11,
               'ANA' : 12,
               'TOR' : 13,
               'COL' : 14,
               'CHN' : 15,
               'NYN' : 16,
               'SDN' : 17,
               'CHA' : 18,
               'LAN' : 19,
               'SLN' : 20,
               'TBA' : 21,
               'BOS' : 22,
               'WAS' : 23,
               'CLE' : 24,
               'TEX' : 25,
               'HOU' : 26,
               'CIN' : 27,
               'OAK' : 28,
               'PHI' : 29}

seasons = [2016, 2017, 2018, 2019, 2020]
frames = []
curr_season = -1
for season in seasons:
    curr_season += 1
    which_season = []
    regular_season = []
    df = pd.read_csv('./data/mlb/GL{}.TXT'.format(season), header=None)
    # columns per the retrosheet description: https://www.retrosheet.org/gamelogs/glfields.txt
    mlb_df = df.iloc[:, [0, 3, 6, 9, 10]]
    mlb_df.columns = ['date', 'away_team', 'home_team', 'away_points', 'home_points']
    # add team ids
    away_team_id = []
    home_team_id = []
    for idx, row in mlb_df.iterrows():
        away_team_id.append(mlb_team2id[row.away_team])
        home_team_id.append(mlb_team2id[row.home_team])
        which_season.append(curr_season)
        regular_season.append(1)
    mlb_df = mlb_df.assign(season=pd.Series(which_season).values)
    mlb_df = mlb_df.assign(regular_season=pd.Series(regular_season).values)
    mlb_df = mlb_df.assign(away_team_id=pd.Series(away_team_id).values)
    mlb_df = mlb_df.assign(home_team_id=pd.Series(home_team_id).values)
    frames.append(mlb_df)

# retrosheet stores playoffs in separate files... ugh
df_lcs = pd.read_csv('./data/mlb/GLLC.TXT')
df_lcs = df_lcs.iloc[:, [0, 3, 6, 9, 10]]
df_lcs.columns = ['date', 'away_team', 'home_team', 'away_points', 'home_points']
df_div = pd.read_csv('./data/mlb/GLDV.TXT')
df_div = df_div.iloc[:, [0, 3, 6, 9, 10]]
df_div.columns = ['date', 'away_team', 'home_team', 'away_points', 'home_points']
df_wild = pd.read_csv('./data/mlb/GLWC.TXT')
df_wild = df_wild.iloc[:, [0, 3, 6, 9, 10]]
df_wild.columns = ['date', 'away_team', 'home_team', 'away_points', 'home_points']
df_world = pd.read_csv('./data/mlb/GLWS.TXT')
df_world = df_world.iloc[:, [0, 3, 6, 9, 10]]
df_world.columns = ['date', 'away_team', 'home_team', 'away_points', 'home_points']

['date', 'away_team', 'home_team', 'away_points', 'home_points']
date = []
away_team = []
home_team = []
away_points = []
home_points = []
away_team_id = []
home_team_id = []
which_season = []
regular_season = []
for idx, row in df_lcs.iterrows():
    # so date is an int like 20200101, so we cast to string to grab first 4 chars (year)
    # and then cast back to int to see if it is the current season
    curr_season = int(str(row.date)[:4])
    if curr_season in seasons:
        date.append(row.date)
        away_team.append(row.away_team)
        home_team.append(row.home_team)
        away_points.append(row.away_points)
        home_points.append(row.home_points)
        away_team_id.append(mlb_team2id[row.away_team])
        home_team_id.append(mlb_team2id[row.home_team])
        which_season.append(seasons.index(curr_season))
        regular_season.append(0)
for idx, row in df_div.iterrows():
    # so date is an int like 20200101, so we cast to string to grab first 4 chars (year)
    # and then cast back to int to see if it is the current season
    curr_season = int(str(row.date)[:4])
    if curr_season in seasons:
        date.append(row.date)
        away_team.append(row.away_team)
        home_team.append(row.home_team)
        away_points.append(row.away_points)
        home_points.append(row.home_points)
        away_team_id.append(mlb_team2id[row.away_team])
        home_team_id.append(mlb_team2id[row.home_team])
        which_season.append(seasons.index(curr_season))
        regular_season.append(0)
for idx, row in df_wild.iterrows():
    # so date is an int like 20200101, so we cast to string to grab first 4 chars (year)
    # and then cast back to int to see if it is the current season
    curr_season = int(str(row.date)[:4])
    if curr_season in seasons:
        date.append(row.date)
        away_team.append(row.away_team)
        home_team.append(row.home_team)
        away_points.append(row.away_points)
        home_points.append(row.home_points)
        away_team_id.append(mlb_team2id[row.away_team])
        home_team_id.append(mlb_team2id[row.home_team])
        which_season.append(seasons.index(curr_season))
        regular_season.append(0)
for idx, row in df_world.iterrows():
    # so date is an int like 20200101, so we cast to string to grab first 4 chars (year)
    # and then cast back to int to see if it is the current season
    curr_season = int(str(row.date)[:4])
    if curr_season in seasons:
        date.append(row.date)
        away_team.append(row.away_team)
        home_team.append(row.home_team)
        away_points.append(row.away_points)
        home_points.append(row.home_points)
        away_team_id.append(mlb_team2id[row.away_team])
        home_team_id.append(mlb_team2id[row.home_team])
        which_season.append(seasons.index(curr_season))
        regular_season.append(0)

frames.append(pd.DataFrame({'date': date,
                            'away_team': away_team,
                            'home_team': home_team,
                            'away_team_id': away_team_id,
                            'home_team_id': home_team_id,
                            'away_points': away_points,
                            'home_points': home_points,
                            'season': which_season,
                            'regular_season': regular_season}))

df_curated = pd.concat(frames).reset_index(drop=True)
# might want to consider during dates into datetime datatypes
# df_curated = df_curated.sort_values(by='date')

# write the final csv
df_curated.to_csv('./data/curated_csvs/mlb.csv')