import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst


class DoctorItem(scrapy.Item):
    crawled_date = scrapy.Field()
    speciality = scrapy.Field()
    source_url = scrapy.Field()
    affiliation = scrapy.Field()
    medical_school = scrapy.Field()
    image_url = scrapy.Field()
    full_name = scrapy.Field()
    address = scrapy.Field()
    graduate_education = scrapy.Field()


class DoctorItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
