# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherCrawlerItem(scrapy.Item):
    plate_codes = scrapy.Field()
    date = scrapy.Field()
    up = scrapy.Field()
    low = scrapy.Field()

    pass
