import scrapy


class Product(scrapy.Item):
    retailer_sku = scrapy.Field()
    trail = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    market = scrapy.Field()
    retailer = scrapy.Field()
    url_original = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
