# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FashionPakistna(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    product_sku = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    attributes = scrapy.Field()
    out_of_stock = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
