# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class RunningBareItem(scrapy.Item):
    brand = scrapy.Field(
        output_processor=TakeFirst()
    )
    care = scrapy.Field()
    currency = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field()
    gender = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    industry = scrapy.Field(
        output_processor=TakeFirst()
    )
    market = scrapy.Field(
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer_sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    skus = scrapy.Field(
        output_processor=TakeFirst()
    )
    spider_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    url_original = scrapy.Field(
        output_processor=TakeFirst()
    )
