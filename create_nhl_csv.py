'''
The script takes the csvs that were downloaded from natural stat trick (naturalstattrick.com/games.php) and
converts them into a csv that is convenient for the modelling we want to do.
That is we need home/away goals, home/away id, regular season or playoffs, which season (i.e. year)
'''
import pandas as pd

def create_curated_df(df_season, df_playoffs, team2id, phoenix):
    # we build a df for the model with more conveniently labelled columns
    # we will parse away team names in the data as 'Canucks' instead of 'Vancouver Canucks'
    # we take the effort to convert because some are potentially confusing (e.g. 'Red' for 'Detroit Red Wings')
    # and because we want it to match the home team which we easily get from the Team column
    parse2team = {'Canucks': 'Vancouver Canucks',
                  'Oilers': 'Edmonton Oilers',
                  'Capitals': 'Washington Capitals',
                  'Blues': 'St Louis Blues',
                  'Senators': 'Ottawa Senators',
                  'Maple': 'Toronto Maple Leafs',
                  'Sharks': 'San Jose Sharks',
                  'Bruins': 'Boston Bruins',
                  'Stars': 'Dallas Stars',
                  'Canadiens': 'Montreal Canadiens',
                  'Hurricanes': 'Carolina Hurricanes',
                  'Ducks': 'Anaheim Ducks',
                  'Flames': 'Calgary Flames',
                  'Avalanche': 'Colorado Avalanche',
                  'Rangers': 'New York Rangers',
                  'Panthers': 'Florida Panthers',
                  'Lightning': 'Tampa Bay Lightning',
                  'Sabres': 'Buffalo Sabres',
                  'Penguins': 'Pittsburgh Penguins',
                  'Wild': 'Minnesota Wild',
                  'Predators': 'Nashville Predators',
                  'Blackhawks': 'Chicago Blackhawks',
                  'Flyers': 'Philadelphia Flyers',
                  'Islanders': 'New York Islanders',
                  'Devils': 'New Jersey Devils',
                  'Blue': 'Columbus Blue Jackets',
                  'Kings': 'Los Angeles Kings',
                  'Red': 'Detroit Red Wings',
                  'Jets': 'Winnipeg Jets',
                  'Coyotes': 'Arizona Coyotes',
                  'Golden': 'Vegas Golden Knights',
                  'Thrashers': 'Atlanta Thrashers'}
    if phoenix:
        parse2team['Coyotes'] = 'Phoenix Coyotes'

    # for now just iterating through games and appending data to lists which will be columns
    # of the curated list
    # initialize lists which will be columns of df
    home_team = []
    away_team = []
    home_team_id = []
    away_team_id = []
    home_goals = []
    away_goals = []
    regular_season = []
    # season games first
    for i in range(len(df_season)):
        curr_game = df_season.iloc[i]
        split_string = curr_game['Game'].split()
        away_team_parse = split_string[2]

        # check if we need to add the new team id when doing season
        if curr_game['Team'] not in list(team2id.keys()):  # home team check
            team2id[curr_game['Team']] = len(
                list(team2id.keys()))  # length of current list of teams in team2id gives next id
        if parse2team[away_team_parse] not in list(team2id.keys()):  # away team check
            team2id[parse2team[away_team_parse]] = len(list(team2id.keys()))

        home_team.append(curr_game['Team'])
        away_team.append(parse2team[away_team_parse])
        home_team_id.append(team2id[curr_game['Team']])
        away_team_id.append(team2id[parse2team[away_team_parse]])
        home_goals.append(curr_game['GF'])
        away_goals.append(curr_game['GA'])
        regular_season.append(1)
    # then playoffs games
    for i in range(len(df_playoffs)):
        curr_game = df_playoffs.iloc[i]
        split_string = curr_game['Game'].split()
        away_team_parse = split_string[2]

        home_team.append(curr_game['Team'])
        away_team.append(parse2team[away_team_parse])
        home_team_id.append(team2id[curr_game['Team']])
        away_team_id.append(team2id[parse2team[away_team_parse]])
        home_goals.append(curr_game['GF'])
        away_goals.append(curr_game['GA'])
        regular_season.append(0)

    df_curated = pd.DataFrame({'home_team': home_team,
                               'away_team': away_team,
                               'home_team_id': home_team_id,
                               'away_team_id': away_team_id,
                               'home_points': home_goals,
                               'away_points': away_goals,
                               'regular_season': regular_season})

    return df_curated, team2id

# need to iterate through strings of season and playoff csv's
base_dir = '/home/nico/hockey/data/home_only/'
# season_csvs = ['regular_season_2007_2008.csv',
#                'regular_season_2008_2009.csv',
#                'regular_season_2009_2010.csv',
#                'regular_season_2010_2011.csv',
#                'regular_season_2011_2012.csv',
#                'regular_season_2013.csv',
#                'regular_season_2013_2014.csv',
#                'regular_season_2014_2015.csv',
#                'regular_season_2015_2016.csv',
#                'regular_season_2016_2017.csv',
#                'regular_season_2017_2018.csv',
#                'regular_season_2018_2019.csv',
#                'regular_season_2019_2020.csv']
# playoff_csvs = ['playoffs_2007_2008.csv',
#                'playoffs_2008_2009.csv',
#                'playoffs_2009_2010.csv',
#                'playoffs_2010_2011.csv',
#                'playoffs_2011_2012.csv',
#                'playoffs_2013.csv',
#                'playoffs_2013_2014.csv',
#                'playoffs_2014_2015.csv',
#                'playoffs_2015_2016.csv',
#                'playoffs_2016_2017.csv',
#                'playoffs_2017_2018.csv',
#                'playoffs_2018_2019.csv',
#                'playoffs_2019_2020.csv']
# team2id = {  'Vancouver Canucks' : 0,
#              'Edmonton Oilers' : 1,
#              'Washington Capitals' : 2,
#              'St Louis Blues' : 3,
#              'Ottawa Senators' : 4,
#              'Toronto Maple Leafs' : 5,
#              'San Jose Sharks' : 6,
#              'Boston Bruins' : 7,
#              'Dallas Stars' : 8,
#              'Montreal Canadiens' : 9,
#               'Carolina Hurricanes' : 10,
#               'Anaheim Ducks' : 11,
#               'Calgary Flames' : 12,
#               'Colorado Avalanche' : 13,
#               'New York Rangers' : 14,
#               'Florida Panthers' : 15,
#               'Tampa Bay Lightning' : 16,
#               'Buffalo Sabres' : 17,
#               'Pittsburgh Penguins' : 18,
#               'Minnesota Wild' : 19,
#               'Nashville Predators' : 20,
#               'Chicago Blackhawks' : 21,
#               'Philadelphia Flyers' : 22,
#               'New York Islanders' : 23,
#               'New Jersey Devils' : 24,
#               'Columbus Blue Jackets' : 25,
#               'Los Angeles Kings' : 26,
#               'Detroit Red Wings' : 27,
#               'Winnipeg Jets' : 28,
#               'Arizona Coyotes' : 29,
#               'Vegas Golden Knights' : 30,
#               'Phoenix Coyotes' : 31,
#               'Atlanta Thrashers': 32  }
season_csvs = ['regular_season_2015_2016.csv',
               'regular_season_2016_2017.csv',
               'regular_season_2017_2018.csv',
               'regular_season_2018_2019.csv',
               'regular_season_2019_2020.csv']
playoff_csvs = ['playoffs_2015_2016.csv',
               'playoffs_2016_2017.csv',
               'playoffs_2017_2018.csv',
               'playoffs_2018_2019.csv',
               'playoffs_2019_2020.csv']
team2id = {  'Vancouver Canucks' : 0,
             'Edmonton Oilers' : 1,
             'Washington Capitals' : 2,
             'St Louis Blues' : 3,
             'Ottawa Senators' : 4,
             'Toronto Maple Leafs' : 5,
             'San Jose Sharks' : 6,
             'Boston Bruins' : 7,
             'Dallas Stars' : 8,
             'Montreal Canadiens' : 9,
              'Carolina Hurricanes' : 10,
              'Anaheim Ducks' : 11,
              'Calgary Flames' : 12,
              'Colorado Avalanche' : 13,
              'New York Rangers' : 14,
              'Florida Panthers' : 15,
              'Tampa Bay Lightning' : 16,
              'Buffalo Sabres' : 17,
              'Pittsburgh Penguins' : 18,
              'Minnesota Wild' : 19,
              'Nashville Predators' : 20,
              'Chicago Blackhawks' : 21,
              'Philadelphia Flyers' : 22,
              'New York Islanders' : 23,
              'New Jersey Devils' : 24,
              'Columbus Blue Jackets' : 25,
              'Los Angeles Kings' : 26,
              'Detroit Red Wings' : 27,
              'Winnipeg Jets' : 28,
              'Arizona Coyotes' : 29,
              'Vegas Golden Knights' : 30}
frames = []
phoenix = False # this is an artifact from when i was testing on data that used phoenix coyotes
for idx, csvs in enumerate(zip(season_csvs, playoff_csvs)):
    df_season = pd.read_csv(base_dir + csvs[0])
    df_playoffs = pd.read_csv(base_dir + csvs[1])
    if idx >= 7:
        phoenix = False
    df_curated, team2id = create_curated_df(df_season, df_playoffs, team2id, phoenix)
    df_curated['season'] = idx
    frames.append(df_curated)

df_curated = pd.concat(frames).reset_index(drop=True)

# write the final csv
df_curated.to_csv('./data/curated_csvs/nhl.csv')