from bs4 import BeautifulSoup
import requests
import os
import csv
from math import floor

if not os.path.isdir("records"):
    os.system(f"mkdir records")

# each bracket url has a different number at the end, since there is such a small number of brackets, I found manually copying them was the easiest option
url_year = {
    2003 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2003/312",
    2004 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2004/311",
    2005 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2005/310",
    2006 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2006/309",
    2007 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2007/230",
    2008 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2008/229",
    2009 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2009/227",
    2010 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2010/226",
    2011 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2011/433", 
    2012 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2012/489", 
    2013 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2013/546",
    2014 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2014/610",
    2015 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2015/677",
    2016 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2016/708",
    2017 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2017/803",
    2018 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2018/872",
    2019 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2019/936",
    2022 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2022/1128"
}

for year in range(2003, 2023):
    # skip the two years most heavily impacted by COVID-19 for stat reliability
    if year == 2020 or year == 2021:
        continue

    # HTML and CSV file names and paths
    url = url_year[year]
    html_name = f"{year}-records.html"
    html_file_path = f"records/{html_name}"
    csv_name = f"{year}-records.csv"
    csv_file_path = f"records/{csv_name}"

    # only request if the file doesn't exist locally to prevent flooding the site
    # these HTML files already exist, but they are small so I am copying them for simplicity
    if not os.path.exists(html_file_path):
        with open(html_file_path, "w") as f:
            response = requests.get(url)
            f.write(response.text)
        
    with open(html_file_path) as f:
        soup = BeautifulSoup(f, "html.parser")

    # find all of the relevant information from the HTML source
    all_records = soup.find_all(name="td")
    all_records = [x.get("rel") for x in all_records] # if x.get("rel")]
    all_records = [x for x in all_records if x != None]
    
    records = []
    teams = []
    while all_records:
        # year and team name
        team = [year, all_records.pop(2)]
        for i in range(9):
            if i in [1, 4, 7, 8]:
                # columns to ignore
                all_records.pop(0)
            else:
                # seed, season total wins and losses, conference win and loss totals
                seed = float(all_records.pop(0))
                seed = floor(seed)
                team.append(int(seed))
        teams.append(team[:])
    
    
    tournament_record = {}

    # tally the tournament wins and losses in order to remove them to prevent data leakage
    games_path = f"brackets/{year}-bracket.csv"
    with open(games_path) as f:
        reader = csv.reader(f)
        games = [x for x in reader]
        # the championship game is not recorded in the team's records for some reason
        games.pop()

    # count the wins and losses of each team in the tournament
    for game in games:
        winner = game[1]
        loser = game[2]
        if winner not in tournament_record:
            tournament_record[winner] = [1, 0]
        else:
            tournament_record[winner][0] += 1
        if loser not in tournament_record:
            tournament_record[loser] = [0, 1]
        else:
            tournament_record[loser][1] += 1

    # remove the tournament wins and losses from the season totals to have accurate pre-tournament values
    for team in teams:
        name = team[1]
        tournament_wins = tournament_record[name][0]
        tournament_losses = tournament_record[name][1]
        team[3] -= tournament_wins
        team[4] -= tournament_losses

# save all of the information to a csv file
with open(csv_file_path, "w") as f:
    write = csv.writer(f)
    # here are the column headers
    categories = ["year", "team", "seed", "wins", "losses", "cwins", "closses"]
    write.writerow(categories)
    while teams:
        team = teams.pop(0)
        write.writerow(team)