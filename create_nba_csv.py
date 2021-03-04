'''
The script takes the csvs  from basketball reference (https://www.basketball-reference.com/leagues/NBA_2020_games.html) and
converts them into a csv that is convenient for the modelling we want to do.
That is we need home/away goals, home/away id, regular season or playoffs, which season (i.e. year)
'''
import pandas as pd
import datetime

season_month = {2016: {'months': ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may',
                                  'june'],
                       'playoff_cutoff' : datetime.datetime(year=2016, month=4, day=13)},
                2017: {'months': ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may',
                                  'june'],
                       'playoff_cutoff' : datetime.datetime(year=2017, month=4, day=14)},
                2018: {'months': ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may',
                                  'june'],
                       'playoff_cutoff': datetime.datetime(year=2018, month=4, day=12)},
                2019: {'months': ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may',
                                  'june'],
                       'playoff_cutoff': datetime.datetime(year=2019, month=4, day=11)},
                2020: {'months': ['october', 'november', 'december', 'january', 'february', 'march', 'july', 'august',
                                  'september'],
                       'playoff_cutoff': datetime.datetime(year=2020, month=5, day=1)}
                }
month2int = {'Oct': 10,
             'Nov': 11,
             'Dec': 12,
             'Jan': 1,
             'Feb': 2,
             'Mar': 3,
             'Apr': 4,
             'May': 5,
             'Jun': 6,
             'Jul': 7,
             'Aug': 8,
             'Sep': 9}
team2id = {'Toronto Raptors': 0,
           'Los Angeles Clippers': 1,
           'Charlotte Hornets': 2,
           'Indiana Pacers': 3,
           'Orlando Magic': 4,
           'Brooklyn Nets': 5,
           'Miami Heat': 6,
           'Philadelphia 76ers': 7,
           'Dallas Mavericks': 8,
           'San Antonio Spurs': 9,
           'Utah Jazz': 10,
           'Portland Trail Blazers': 11,
           'Phoenix Suns': 12,
           'Detroit Pistons': 13,
           'Houston Rockets': 14,
           'Golden State Warriors': 15,
           'Memphis Grizzlies': 16,
           'New Orleans Pelicans': 17,
           'Oklahoma City Thunder': 18,
           'Denver Nuggets': 19,
           'Sacramento Kings': 20,
           'Los Angeles Lakers': 21,
           'Milwaukee Bucks': 22,
           'Atlanta Hawks': 23,
           'New York Knicks': 24,
           'Chicago Bulls': 25,
           'Cleveland Cavaliers': 26,
           'Minnesota Timberwolves': 27,
           'Washington Wizards': 28,
           'Boston Celtics': 29}

curr_season = -1
frames = []
for season in season_month.keys():
    curr_season += 1
    date_time = []
    away_team = []
    away_team_id = []
    away_points = []
    home_team = []
    home_team_id = []
    home_points = []
    regular_season = []
    seasons = []
    for month in season_month[season]['months']:
        csv_string = './data/nba/months/{}/{}_{}.csv'.format(season, season, month)
        df = pd.read_csv(csv_string)
        for row in df.iterrows():
            row_series = row[1]  # row is a tuple of (index, series), we want the series
            date = row_series['Date']
            time = row_series['Start (ET)']
            away_team.append(row_series['Visitor/Neutral'])
            away_team_id.append(team2id[row_series['Visitor/Neutral']])
            away_points.append(row_series['PTS'])
            home_team.append(row_series['Home/Neutral'])
            home_team_id.append(team2id[row_series['Home/Neutral']])
            home_points.append(row_series['PTS.1'])
            # parse datetime
            date_split = date.split(' ')
            year = int(date_split[3])
            month = date_split[1]
            day = int(date_split[2])
            month = month2int[month]
            if len(time) == 6:  # 10/11/12 e.g. 10:30
                hour = int(time[:2])
                minute = int(time[3:5])
            else:  # single digit hour e.g. 1:30
                hour = int(time[0])
                minute = int(time[2:4])
            if time[-1] == 'p':  # pm, so we add 12 since datetime works with 24-hr clock
                if hour != 12:
                    hour += 12
            date_time.append(datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute))
            if datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute) > season_month[season]['playoff_cutoff']:
                regular_season.append(0)
            else:
                regular_season.append(1)
            seasons.append(curr_season)

    nba_df = pd.DataFrame({"date": date_time,
                           "away_team": away_team,
                           "away_team_id": away_team_id,
                           "away_points": away_points,
                           "home_team": home_team,
                           "home_team_id": home_team_id,
                           "home_points": home_points,
                           "regular_season": regular_season,
                           "season": seasons})

    nba_df = nba_df.sort_values(by='date')
    frames.append(nba_df)

df_curated = pd.concat(frames).reset_index(drop=True)

# write the final csv
df_curated.to_csv('./data/curated_csvs/nba.csv')
