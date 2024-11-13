# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SnapCountItem(scrapy.Item):
    team = scrapy.Field()
    year = scrapy.Field()
    week = scrapy.Field()
    position = scrapy.Field()
    player = scrapy.Field()
    snap_count = scrapy.Field()
    snap_percent = scrapy.Field()
