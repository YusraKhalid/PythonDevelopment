# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class StoresLocationItem(Item):
    city = Field()
    address = Field()
    country = Field()
    hours = Field()
    phone_number = Field()
    services = Field()
    state = Field()
    store_email = Field()
    store_floor_plan_url = Field()
    store_id = Field()
    store_image_url = Field()
    store_name = Field()
    store_url = Field()
    weekly_ad_url = Field()
    zipcode = Field()
