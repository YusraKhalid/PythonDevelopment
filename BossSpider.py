import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


def clean(raw_data):
    raw_info = []

    if isinstance(raw_data, list):
        for string in raw_data:
            if re.sub('\s+', '', string):
                raw_info.append(re.sub('\s+', '', string))

        return raw_info

    if re.sub('\s+', '', raw_data):
        return re.sub('\s+', '', raw_data)


class BossItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    stock = scrapy.Field()
    color = scrapy.Field()
    price = scrapy.Field()
    skus = scrapy.Field()
    color_queue = scrapy.Field()
    size_queue = scrapy.Field()


class BossSpider(CrawlSpider):
    name = 'boss'
    allowed_domains = ['hugoboss.com']
    start_urls = [
        'https://www.hugoboss.com/uk/home',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=('.main-header'))),
        Rule(LinkExtractor(restrict_css=('.product-tile__link')),callback='parse_item'),
    )

    def parse_item(self, response):
        item = BossItem()

        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(response)
        item['skus'] = {}
        color_urls = response.css('.swatch-list__image--is-large ::attr(href)').getall()

        for color_url,flag in zip(color_urls,range(len(color_urls),0,-1)):
            yield response.follow(url= color_url, callback=self.parse_size,
                                  meta={'item': item,'color_flag' : flag})

    def retailer_sku(self, response):
        return response.css('script[type="text/javascript"]').re("productSku\":\"(.+?)\"")[0]

    def product_gender(self, response):
        return response.css('script[type="text/javascript"]').re("productGender\":\"(.+?)\"")[0]

    def product_name(self, response):
        return response.css('.font__h2 ::text').get()

    def product_category(self, response):
        return response.css('.breadcrumb__title ::text').getall()[1:4]

    def product_url(self, response):
        return response.url

    def product_brand(self, response):
        return response.css('meta[itemprop= "brand"] ::attr(content)').get()

    def product_description(self, response):
        return clean(response.css('.description div ::text').get())

    def product_care(self, response):
        return response.css('.accordion__item__icon ::text').getall()

    def images_url(self, response):
        return response.css('.slider-item--thumbnail-image ::attr(src)').getall()

    def parse_size(self, response):
        item = response.meta['item']
        color_flag = response.meta['color_flag']


        size_urls = response.css('.product-stage__choose-size--container [disabled!="disabled"] '
                                 '::attr(href)').getall()

        for size_url , flag in zip(size_urls, range(len(size_urls), 0, -1)):
            yield response.follow(url=size_url, callback=self.parse_sku,
                                  meta={'item': item,'color_flag' : color_flag,'size_flag':flag})

    def parse_sku(self,response):
        item = response.meta['item']
        color_flag = response.meta['color_flag']
        size_flag = response.meta['size_flag']

        color = clean(response.css('.product-stage__control-item__label--variations ::text').getall()[2])
        price = clean(response.css('.product-price--price-sales ::text').get())
        previous_price = clean(response.css('.product-price--price-standard s ::text').getall())
        size = clean(response.css('.product-stage__control-item__selcted-size ::text').get())

        raw_sku = item['skus']
        raw_sku.update({f'{color}_{size}': {
            'color': color,
            'price': price,
            'previous_price': previous_price,
            'size': size
        }})
        item['skus'] = raw_sku

        if color_flag == 1 and size_flag == 1:
            yield item

