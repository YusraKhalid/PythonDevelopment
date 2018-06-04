import datetime
import json
import re
import scrapy
import time

from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule, Request

from w3lib.url import add_or_replace_parameter as add_parameter


class PaginationExtractor():

    def extract_links(self, response):
        page_url = response.css('.search-result-content::attr(data-url)').extract_first()

        if not page_url:
            return []

        total_pages = int(response.css('.search-result-content::attr(data-maxpage)').extract_first())
        items_per_page = int(response.css('.search-result-content::attr(data-pagesize)').extract_first())
        return [Link(add_parameter(page_url, 'start', items_per_page * pl)) for pl in range(2, total_pages + 1)]   


class WoolrichSpider(CrawlSpider):
    name = 'woolrich_spider'
    allowed_url = r'.*/en/.*'
    allowed_domains = ['woolrich.eu']

    start_urls = ['http://www.woolrich.eu/en/gb/new-arrivals/new-men/men-summer-2018/WOCPS2666-PT40.html']

    rules = [Rule(LinkExtractor(allow=(allowed_url), restrict_css='.menu-category'), callback='parse', follow=True),
             Rule(PaginationExtractor(), callback='parse'),
             Rule(LinkExtractor(allow=(allowed_url), restrict_css='.product-name'), callback='parse_product')]

    care = ['polyster', 'cotton', 'silk', 'fabric', 'wash']

    def parse(self, response):
        page_title = response.css('title::text').extract_first()
        trail = response.meta.get('trail') or []
        trail.append([page_title, response.url])

        for request in super().parse(response):    
            request.meta['trail'] = trail.copy()
            yield request

    def parse_product(self, response):
        product = {}
        raw_product = self.raw_products(response)
        product['retailer_sku'] = self.retailer_sku(raw_product)
        product['uuid'] = "null"
        product['language'] = "en"
        product['trail'] = response.meta.get('trail')
        product['url'] = response.url
        product['url_original'] = response.url
        product['name'] = self.product_name(response)
        product['price'] = self.price(raw_product)
        product['brand'] = self.brand(raw_product)
        product['market'] = "GB"
        product['retailer'] = product['brand'] + '-' + product['language']
        product['category'] = self.category(raw_product)
        product['care'], product['description'] = self.raw_description(response)
        product['images'] = []
        product['date'] = int(time.time())
        product['skus'] = []
        product['currency'] = "POUND"
        product['spider_name'] = self.name
        product['crawl_start_time'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        product['request_queue'] = self.color_requests(response, product)

        return self.request_or_product(product)

    def parse_size(self, response):
        product = response.meta['product']
        product['skus'].append(self.skus(response))
        return self.request_or_product(product)

    def parse_color(self, response):
        product = response.meta['product']
        product['request_queue'] += self.size_requests(response, product)
        product['images'] += self.image_urls(response)
        return self.request_or_product(product)

    def request_or_product(self, product):
        if product['request_queue']:
            request = product['request_queue'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['request_queue']
            return product

    def color_requests(self, response, product):
        colors = response.css('.color>.selectable>a::attr(href)').extract()
        return [Request(color, callback=self.parse_color) for color in colors]

    def size_requests(self, response, product):
        sizes = response.css('.size>.selectable>a::attr(href)').extract()
        return [Request(size, callback=self.parse_size) for size in sizes]

    def brand(self, attributes):
        return attributes['brand']

    def retailer_sku(self, attributes):
        return attributes['id']

    def product_name(self, response):
        return response.css('.product-name::text').extract_first()

    def price(self, attributes):
        return attributes['price']

    def category(self, attributes):
        return attributes['category']

    def image_urls(self, response):
        css = '#pdp-mainimage>.carousel-container-inner>ul>li>a>picture>img::attr(src)'
        return response.css(css).extract()
    
    def raw_products(self, response):
        product_description = re.findall("dataLayer.push.apply(.+?);", response.text, re.S)[0][12:-1]
        product_description = json.loads(product_description)
        return product_description[0]['ecommerce']['detail']['products'][0]

    def raw_description(self, response):
        description = response.css('.description::text').extract_first()
        
        if not description:
            return [], []
        
        raw_descp = list(filter(str.strip, description.strip().split('.')))
        care = [descp for descp in raw_descp if any(care in descp for care in self.care)]
        descp = [descp for descp in raw_descp if not any(care in descp for care in self.care)]

        return care, descp

    def skus(self, response):
        size_info = response.css('.size .selected a::text').extract_first().strip()
        stock_info = response.css('.in-stock-msg::text').extract_first() or 'Out of Stock'
        color_name = response.css('.color .selected a div::text').extract_first().strip()
        skus_id = color_name.replace(" ", "-").lower() + '_' + size_info.replace(" ", "-").lower()

        return  {'size': size_info,
                 'color': color_name,
                 'price': response.meta.get('product')['price'],
                 'currency': response.meta.get('product')['currency'],
                 'stock_status': stock_info,
                 'skus_id': skus_id}
