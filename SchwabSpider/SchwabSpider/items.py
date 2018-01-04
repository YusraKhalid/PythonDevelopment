import scrapy


class SchwabProduct(scrapy.Item):
    brand = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    retailer = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
    remaining_request = scrapy.Field()
    information = scrapy.Field()
