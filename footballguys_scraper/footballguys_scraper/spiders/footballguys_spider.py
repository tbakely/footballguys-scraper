import scrapy
from pathlib import Path
from spider_config import *
from loguru import logger


class FootballGuysSpider(scrapy.Spider):
    pass


if __name__ == "__main__":
    logger.info(NFL_ABBR)