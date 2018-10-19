# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class Product(scrapy.Item):
    pid = scrapy.Field(output_processor=TakeFirst())
    gender = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    skus = scrapy.Field()
    image_urls = scrapy.Field()
    crawl_start_time = scrapy.Field() 
