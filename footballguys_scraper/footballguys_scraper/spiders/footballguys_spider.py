import scrapy
from pathlib import Path
from footballguys_scraper.spider_config import *
from loguru import logger
import sys


class FootballGuysSpider(scrapy.Spider):
    name = "footballguys_spider"
    current_year = 2024
    start_urls = ["https://www.footballguys.com/stats/snap-counts/teams?team=TEN&year=2024"]

    def parse(self, response):
        # This grabs position, weeks for that position, and total?
        # logger.info(response.css(".table > thead > th::text").getall())
        players = []
        for tbody in response.css(".table > tbody"):
            raw = tbody.css("tr > td > a::text").getall()
            raw = [player.strip() for player in raw]
            players.append(raw)
        logger.info(players)
        # logger.info(response.css(".table > tbody > tr::text").getall())
            # logger.info(response.css("tr:nth-child(1) > td:nth-child(1) > a::text").get())
        # logger.info(response.css(".table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1) ::text").get())


if __name__ == "__main__":
    current_year = 2024
    current_team = "ARI"
    start_url = f"https://www.footballguys.com/stats/snap-counts/teams?team={current_team}&year={current_year}"
    logger.info()

# .table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1)
# .table > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)
# .table > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(1)