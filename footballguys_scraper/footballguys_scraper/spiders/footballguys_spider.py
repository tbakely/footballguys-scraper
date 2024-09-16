import scrapy
from pathlib import Path
from footballguys_scraper.spider_config import *
from loguru import logger
import sys
import csv
import os
import re

output_type = "csv"
if output_type == "csv":
    class FootballGuysSpider(scrapy.Spider):
        name = "footballguys_spider"
        current_year = 2023
        teams = NFL_ABBR.keys()  # Assuming NFL_ABBR is a dictionary of team abbreviations to full names

        # Define the path to the CSV file
        output_file = 'football_snap_counts.csv'

        def start_requests(self):
            # Create CSV file if it doesn't exist and write the header row
            if not os.path.exists(self.output_file):
                with open(self.output_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Team', 'Year', 'Week', 'Position', 'Player', 'SnapCount', 'SnapPercent'])

            # Loop over each team and request the data
            for team in self.teams:
                url = f"https://www.footballguys.com/stats/snap-counts/teams?team={team}&year={self.current_year}"
                yield scrapy.Request(url, callback=self.parse, meta={'team': team})

        def parse(self, response):
            team = response.meta['team']
            rows_to_write = []

            # Loop through each position (thead, tbody pair)
            for thead, tbody in zip(response.css(".table > thead"), response.css(".table > tbody")):
                headers = thead.css("th::text").getall()
                if len(headers) < 2:
                    continue  # Skip if headers are not in the expected format

                position = headers[0].strip()  # Get the position (e.g., QB, RB)
                weeks = headers[1:-1]  # Extract the week headers (excluding extra columns)
                
                # Loop over each week in the season
                for week_index, week in enumerate(weeks):
                    # Flatten the week to just a number using regex, if it follows the format "Wk 1"
                    week_number = re.search(r'\d+', week).group() if re.search(r'\d+', week) else "Unknown"

                    # Prepare a dictionary for each position in the master dictionary
                    players = tbody.css("tr > td > a::text").getall()
                    snap_counts = tbody.css("tr > td > div::text").getall()
                    snap_percents = tbody.css("tr > td > b::text").getall()

                    for i, player in enumerate(players):
                        snap_count = snap_counts[i].strip() if i < len(snap_counts) else ''
                        snap_percent = snap_percents[i].strip() if i < len(snap_percents) else ''

                        # Append a flattened row to the list (Team, Year, Week, Position, Player, SnapCount, SnapPercent)
                        rows_to_write.append([team, self.current_year, week_number, position, player.strip(), snap_count, snap_percent])

            # Write the collected rows to the CSV file
            with open(self.output_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows_to_write)

else:
    class FootballGuysSpider(scrapy.Spider):
        name = "footballguys_spider"
        current_year = 2023
        teams = NFL_ABBR.keys()

        def start_requests(self):
            for team in self.teams:
                url = f"https://www.footballguys.com/stats/snap-counts/teams?team={team}&year={self.current_year}"
                yield scrapy.Request(url, callback=self.parse, meta={'team': team})

        def parse(self, response):
            # Grabbing team from meta
            team = response.meta['team']
            
            master_dict = {}
            master_dict[team] = {}

            # Loop through each position (thead, tbody pair)
            for thead, tbody in zip(response.css(".table > thead"), response.css(".table > tbody")):
                headers = thead.css("th::text").getall()
                if len(headers) < 2:
                    continue  # Skip if headers are not in the expected format
                
                position = headers[0].strip()
                weeks = [week for week in headers[1:-1]]
                for week in weeks:
                    if week not in master_dict[team]:
                        master_dict[team][week] = {}

                    master_dict[team][week][position] = {player.strip(): {} for player in tbody.css("tr > td > a::text").getall()}

                    snap_counts = tbody.css("tr > td > div::text").getall()
                    snap_percents = tbody.css("tr > td > b::text").getall()

                    for i, player in enumerate(master_dict[team][week][position]):
                        # Fill in the snap count and percentage for each player
                        if i < len(snap_counts):
                            master_dict[team][week][position][player]["snapCount"] = snap_counts[i].strip()
                        if i < len(snap_percents):
                            master_dict[team][week][position][player]["snapPercent"] = snap_percents[i].strip()

            # Yield the result for the current team
            yield master_dict


# class FootballGuysSpider(scrapy.Spider):
#     name = "footballguys_spider"
#     current_year = 2024
#     start_urls = ["https://www.footballguys.com/stats/snap-counts/teams?team=TEN&year=2024"]

#     def parse(self, response):
#         # This grabs position, weeks for that position, and total?

#         master_dict = {}
#         players = []
#         teams = ["ARI"]
#         for team in teams:
#             master_dict[team] = {}
#             for thead, tbody in zip(response.css(".table > thead"), response.css(".table > tbody")):
#                 position, week, _ = thead.css("th::text").getall()
#                 if not week in master_dict[team]:
#                     master_dict[team][week] = {}
#                 else:
#                     master_dict[team][week][position] = []
                
#                 master_dict[team][week][position] = {player.strip():{} for player in tbody.css("tr > td > a::text").getall()}
#                 for i, key in enumerate(master_dict[team][week][position].keys()):
#                     master_dict[team][week][position][key]["snapCount"] = tbody.css("tr > td > div::text").getall()[i]
#                     master_dict[team][week][position][key]["snapPercent"] = tbody.css("tr > td > b::text").getall()[i]
#         yield master_dict
#         logger.info([master_dict])
#         #     raw = tbody.css("tr > td > a::text").getall()
#         #     raw = [player.strip() for player in raw]
#         #     players.append(raw)  
#         # players = [player for player_list in players for player in player_list]
#         # logger.info(players) .table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1)

#         # logger.info(response.css(".table > tbody > tr::text").getall())
#             # logger.info(response.css("tr:nth-child(1) > td:nth-child(1) > a::text").get())
#         # logger.info(response.css(".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1) ::text").get())


if __name__ == "__main__":
    current_year = 2024
    current_team = "ARI"
    start_url = f"https://www.footballguys.com/stats/snap-counts/teams?team={current_team}&year={current_year}"
    logger.info()