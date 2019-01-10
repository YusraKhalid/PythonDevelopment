import scrapy


class IntersportCrawlerItem(scrapy.Item):
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    lang = scrapy.Field()
    market = scrapy.Field()
    name = scrapy.Field()
    retailer_sku = scrapy.Field()
    skus = scrapy.Field()
    url = scrapy.Field()
