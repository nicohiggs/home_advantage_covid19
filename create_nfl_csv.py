'''
The script takes the csvs  from football reference (https://www.pro-football-reference.com/years/2020/games.htm) and
converts them into a csv that is convenient for the modelling we want to do.
That is we need home/away goals, home/away id, regular season or playoffs, which season (i.e. year)
'''
import pandas as pd
import datetime

seasons = [2016, 2017, 2018, 2019, 2020]
nfl_team2id = {'Denver Broncos' : 0,
               'Green Bay Packers' : 1,
               'Baltimore Ravens' : 2,
               'Kansas City Chiefs' : 3,
               'Tampa Bay Buccaneers' : 4,
               'Minnesota Vikings' : 5,
               'Oakland Raiders' : 6,
               'Las Vegas Raiders' : 6,
               'Cincinnati Bengals' : 7,
               'Philadelphia Eagles' : 8,
               'Houston Texans' : 9,
               'Seattle Seahawks' : 10,
               'New York Giants' : 11,
               'Detroit Lions' : 12,
               'New England Patriots' : 13,
               'Pittsburgh Steelers' : 14,
               'San Francisco 49ers' : 15,
               'New York Jets' : 16,
               'Tennessee Titans' : 17,
               'Carolina Panthers' : 18,
               'Dallas Cowboys' : 19,
               'Arizona Cardinals' : 20,
               'Los Angeles Rams' : 21,
               'San Diego Chargers' : 22,
               'Los Angeles Chargers' : 22,
               'Atlanta Falcons' : 23,
               'Buffalo Bills' : 24,
               'Miami Dolphins' : 25,
               'Washington Redskins' : 26,
               'Washington Football Team' : 26,
               'Indianapolis Colts' : 27,
               'Jacksonville Jaguars' : 28,
               'Chicago Bears' : 29,
               'New Orleans Saints' : 30,
               'Cleveland Browns' : 31}
nfl_month2int = { 'October' : 10,
              'November' : 11,
              'December' : 12,
              'January' : 1,
              'February' : 2,
              'March' : 3,
              'April' : 4,
              'May' : 5,
              'June' : 6,
              'July' : 7,
              'August' : 8,
              'September' : 9 }

frames = []
curr_season = -1
for season in seasons:
    curr_season += 1
    date = []
    away_team = []
    home_team = []
    away_team_pts = []
    home_team_pts = []
    away_team_id = []
    home_team_id = []
    which_season = []
    regular_season = []
    df = pd.read_csv('./data/nfl/seasons/{}_season.csv'.format(season))
    df.columns = ['week', 'day', 'date', 'time', 'winner', 'home_or_away', 'loser', 'boxscore',
                  'winner_pts', 'loser_pts', 'winner_yds', 'tow', 'loser_yds', 'tol']
    df = df.iloc[:, [2,3,4,5,6,8,9]]
    for idx, row in df.iterrows():
        if row.home_or_away == 'N':
            continue
        elif row.home_or_away == '@':
            home_team.append(row.loser)
            home_team_pts.append(row.loser_pts)
            home_team_id.append(nfl_team2id[row.loser])
            away_team.append(row.winner)
            away_team_pts.append(row.winner_pts)
            away_team_id.append(nfl_team2id[row.winner])
        else:
            away_team.append(row.loser)
            away_team_pts.append(row.loser_pts)
            away_team_id.append(nfl_team2id[row.loser])
            home_team.append(row.winner)
            home_team_pts.append(row.winner_pts)
            home_team_id.append(nfl_team2id[row.winner])
        split_string = row.date.split(' ')
        date.append(datetime.datetime(year=2019, month=nfl_month2int[split_string[0]], day=int(split_string[1])))
        which_season.append(curr_season)
        regular_season.append(1)

    df = pd.read_csv('./data/nfl/seasons/{}_playoffs.csv'.format(season))
    df.columns = ['week', 'day', 'date', 'time', 'winner', 'home_or_away', 'loser', 'boxscore',
                  'winner_pts', 'loser_pts', 'winner_yds', 'tow', 'loser_yds', 'tol']
    df = df.iloc[:, [2, 3, 4, 5, 6, 8, 9]]
    for idx, row in df.iterrows():
        if row.home_or_away == 'N':
            continue
        elif row.home_or_away == '@':
            home_team.append(row.loser)
            home_team_pts.append(row.loser_pts)
            home_team_id.append(nfl_team2id[row.loser])
            away_team.append(row.winner)
            away_team_pts.append(row.winner_pts)
            away_team_id.append(nfl_team2id[row.winner])
        else:
            away_team.append(row.loser)
            away_team_pts.append(row.loser_pts)
            away_team_id.append(nfl_team2id[row.loser])
            home_team.append(row.winner)
            home_team_pts.append(row.winner_pts)
            home_team_id.append(nfl_team2id[row.winner])
        split_string = row.date.split(' ')
        date.append(datetime.datetime(year=2019, month=nfl_month2int[split_string[0]], day=int(split_string[1])))
        which_season.append(curr_season)
        regular_season.append(0)
    nfl_df = pd.DataFrame({'date': date,
                           'away_team': away_team,
                           'home_team': home_team,
                           'away_team_id': away_team_id,
                           'home_team_id': home_team_id,
                           'home_points': home_team_pts,
                           'away_points': away_team_pts,
                           'season': which_season,
                           'regular_season': regular_season})
    frames.append(nfl_df)

df_curated = pd.concat(frames).reset_index(drop=True)
# write the final csv
df_curated.to_csv('./data/curated_csvs/nfl.csv')
