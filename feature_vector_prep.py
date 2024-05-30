# basic imports
import pandas as pd
import numpy as np

def matchup_generator(all_stats, year, team0_name, team1_name, winner=None):
    '''
    Input all_stats df, year, team0 and team1 name and the winner (0 for the first team input, 1 for the second)
    if one exists to return the two mirrored games team0-team1 and team1-team0
    '''
    year_stats = all_stats[all_stats["year"] == year]
    teams_df = year_stats[year_stats["team"].isin([team0_name, team1_name])]
    if len(teams_df) < 2:
        return None

    team0 = teams_df[teams_df["team"] == team0_name].drop(["year", "team"], axis=1).squeeze()
    team1 = teams_df[teams_df["team"] == team1_name].drop(["year", "team"], axis=1).squeeze()
    team0_team1 = team0 - team1
    team0_team1["year"] = year
    team0_team1["team0"] = team0_name
    team0_team1["team1"] = team1_name
    
    team1_team0 = team1 - team0
    team1_team0["year"] = year
    team1_team0["team0"] = team1_name
    team1_team0["team1"] = team0_name

    team0_team1["result"] = winner
    team1_team0["result"] = 1 - winner

    return [team0_team1, team1_team0]


all_stats = pd.read_csv("stats/all_stats.csv")

# create a dataframe of each tournament game
df_games = pd.DataFrame({})
for year in range(2003, 2023):
    if year == 2020 or year == 2021:
        continue
    df_bracket = pd.read_csv(f"brackets/{year}-bracket.csv")
    df_bracket = df_bracket[df_bracket["round"] > 0]
    for i, game in df_bracket.iterrows():
        games = matchup_generator(all_stats, game.year, game.team0, game.team1, game.winner)
        if games:
            team0_team1, team1_team0 = games
            df_games = df_games._append(team0_team1, ignore_index=True)
            df_games = df_games._append(team1_team0, ignore_index=True)

df_games = df_games.round(3)
df_games.to_csv("feature_vectors.csv", index=False)