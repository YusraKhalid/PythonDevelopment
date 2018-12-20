from scrapy import Field, Item


class ChildrensPlaceItem(Item):
    uuid = Field()
    brand = Field()
    care = Field()
    categories = Field()
    description = Field()
    gender = Field()
    image_urls = Field()
    name = Field()
    price = Field()
    retailer_sku = Field()
    skus = Field()
    url = Field()
    market = Field()
    retailer = Field()
    date = Field()
    crawl_id = Field()
    industry = Field()
    product_hash = Field()
    currency = Field()
    spider_name = Field()
    crawl_start_time = Field()