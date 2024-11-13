# run_spider.py

import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from footballguys_scraper.spiders.footballguys_spider import FootballGuysSpider
from loguru import logger
import sys
import argparse

# Configure loguru to display info-level messages
logger.add("footballguys_spider.log", format="{time} {level} {message}", level="INFO", mode="w")  # "w" mode overwrites file

def main():
    # Parse command-line arguments for year
    parser = argparse.ArgumentParser(description="Run FootballGuys Spider")
    parser.add_argument("--year", type=int, default=2024, help="Year to scrape data for")
    args = parser.parse_args()
    
    # Notify user that the spider is starting
    logger.info("Starting the FootballGuys Spider...\n")

    # Set up Scrapy's CrawlerProcess with project settings
    process = CrawlerProcess(get_project_settings())

    # Add the spider to the process
    process.crawl(FootballGuysSpider, year=args.year)

    # Run the spider
    try:
        process.start()
        logger.info("\nSpider finished successfully.\n")
    except Exception as e:
        logger.error(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()
