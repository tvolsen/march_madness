from bs4 import BeautifulSoup
import requests
import os
import csv

if not os.path.isdir("stats"):
    os.system(f"mkdir stats")

for year in range(2003, 2025):
    # skip the two years most heavily impacted by COVID-19 for stat reliability
    if year == 2020 or year == 2021:
        continue
    
    # save the data from the entire season, and from just the tournament. These two will later be subtracted to have pre-tournament stats (to prevent data leakage)
    for season in ["total", "tournament"]:

        # access the correct page depending on if we are scraping the entire season, or just the NCAA tournament
        url_dict = {
            "total" : 0,
            "tournament" : 6
        }
        # HTML and CSV file names and paths
        url = f"https://basketball.realgm.com/ncaa/team-stats/{year}/Totals/Team_Totals/{url_dict[season]}"
        html_name = f"{year}-{season}-stats.html"
        html_file_path = f"stats/{html_name}"
        csv_name = f"{year}-{season}-stats.csv"
        csv_file_path = f"stats/{csv_name}"



        # only request if the file doesn't exist locally to prevent flooding the site
        if not os.path.exists(html_file_path):
            with open(html_file_path, "w") as f:
                response = requests.get(url)
                f.write(response.text)
            
        with open(html_file_path) as f:
            soup = BeautifulSoup(f, "html.parser")

        # find all of the relevant information from the HTML source
        all_stats = soup.find_all(name="td", class_="")

        # save all of the information to a csv file
        with open(csv_file_path, "w") as f:
            write = csv.writer(f)
            # here are the column headers
            categories = ["year", "team", "pts", "fgm", "fga", "3pm", "3pa", "ftm", "fta", "orb", "drb", "reb", "ast", "stl", "blk", "tov", "pf"]
            write.writerow(categories)
            while all_stats:
                team = []
                # add the year and school columns
                team.append(year)
                team.append(all_stats.pop(0).text)
                for i in range(20):
                    # ignore a few irrelevant or incompatible columns
                    if i in [0, 1, 5, 8, 11]:
                        all_stats.pop(0)
                    else:
                        # format the numbers as integers
                        s = str(all_stats.pop(0).text)
                        s = s.replace(",", "")
                        team.append(int(s))
                write.writerow(team)