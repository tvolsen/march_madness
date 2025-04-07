# basic imports
import pandas as pd

all_stats = pd.DataFrame({})

for year in range(2003, 2023):
    if year in [2020, 2021]:
        continue
    # load the previously generated csv files

    df_tour_stats = pd.read_csv(f"stats/{year}-tournament-stats.csv")
    df_stats = pd.read_csv(f"stats/{year}-total-stats.csv")
    df_records = pd.read_csv(f"records/{year}-records.csv")
    
    # which cols do we want to substract the tour from the total stats
    cols = ['pts', 'fgm', 'fga', '3pm',
            '3pa', 'ftm', 'fta', 'orb',
            'drb', 'reb', 'ast', 'stl',
            'blk', 'tov', 'pf']
    
    # merge the total and tour stats, then substract the stat columns
    df_stats = pd.merge(df_stats, df_tour_stats, on=["year", "team"], how="left", suffixes=["_total", "_tour"])
    for col in cols:
        total = f"{col}_total"
        tour = f"{col}_tour"
        df_stats[col] = df_stats[total] - df_stats[tour]
        df_stats = df_stats.drop([total, tour], axis=1)
    
    # merge in the records and drop na
    df_stats = pd.merge(df_stats, df_records, on=["year", "team"], how="left")
    df_stats = df_stats.dropna()
    
    # total number of games played
    num_games = df_stats["wins"] + df_stats["losses"]
    
    # columns to be averaged per game
    total_cols = ['pts', 'orb', 'drb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf']
    
    # append pg to the column names above
    per_game_cols = [col + "pg" for col in total_cols]
    for stat, stat_per_game in zip(total_cols, per_game_cols):
        # add the per game columns to the dataframe
        df_stats.insert(df_stats.columns.get_loc(stat)+1, stat_per_game, df_stats[stat]/num_games)
    df_stats.insert(df_stats.columns.get_loc("losses")+1, "winp", df_stats["wins"]/num_games)
    
    # insert the conference win percentage column
    num_cgames = df_stats["cwins"] + df_stats["closses"]
    df_stats.insert(df_stats.columns.get_loc("closses")+1, "cwinp", df_stats["cwins"]/num_cgames)
    
    # insert the field goal percentage column
    df_stats.insert(df_stats.columns.get_loc("fga")+1, "fgp", df_stats["fgm"]/df_stats["fga"])
    
    # insert the 3 point percentage column
    df_stats.insert(df_stats.columns.get_loc("3pa")+1, "3pp", df_stats["3pm"]/df_stats["3pa"])
    
    # insert the free throw percentage column
    df_stats.insert(df_stats.columns.get_loc("fta")+1, "ftp", df_stats["ftm"]/df_stats["fta"])
    
    # round everything in the dataframe to 3 decimal places
    df_stats = df_stats.round(3)
    
    # append the current year to the list of all years
    all_stats = pd.concat([all_stats, df_stats], ignore_index=True) 
    
all_stats.to_csv("stats/all_stats.csv", index=False)
