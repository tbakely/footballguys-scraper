import scrapy
from scrapy.utils.project import get_project_settings
from pathlib import Path
from footballguys_scraper.spider_config import *
from footballguys_scraper.items import SnapCountItem
from loguru import logger
import sys
import csv
import os
import re


class FootballGuysSpider(scrapy.Spider):
    name = "footballguys_spider"
    teams = NFL_ABBR.keys()  # Assuming NFL_ABBR is a dictionary of team abbreviations to full names

    def __init__(self, year=2024, output_file="output/football_snap_counts.csv", *args, **kwargs):
        super(FootballGuysSpider, self).__init__(*args, **kwargs)
        self.current_year = year  # Set the year based on the argument
        self.output_file = f"footballguys_scraper/output/nfl_snap_counts_{year}.csv"
        logger.info(f"Spider initialized for year {self.current_year}")

    def start_requests(self):
        for team in self.teams:
            url = f"https://www.footballguys.com/stats/snap-counts/teams?team={team}&year={self.current_year}"
            yield scrapy.Request(url, callback=self.parse, meta={'team': team})

    def parse(self, response):
        team = response.meta['team']
        
        # Parse each position's data
        for thead, tbody in zip(response.css(".table > thead"), response.css(".table > tbody")):
            headers = thead.css("th::text").getall()
            if len(headers) < 2:
                continue

            position = headers[0].strip()
            weeks = headers[1:-1]
            players = tbody.css("tr > td > a::text").getall()
            snap_counts = tbody.css("tr > td > div::text").getall()
            snap_percents = tbody.css("tr > td > b::text").getall()

            for i, player in enumerate(players):
                week_number = re.search(r'\d+', weeks[i]).group() if i < len(weeks) and re.search(r'\d+', weeks[i]) else "Unknown"
                
                item = SnapCountItem(
                    team=team,
                    year=self.current_year,
                    week=week_number,
                    position=position,
                    player=player.strip(),
                    snap_count=snap_counts[i].strip() if i < len(snap_counts) else '',
                    snap_percent=snap_percents[i].strip() if i < len(snap_percents) else ''
                )

                yield item
