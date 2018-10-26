import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fredperry.items import FredperryItem


class FredperryParser:
    visited_products = set()

    gender_map = {'women': 'women', 'men': 'men', 'kid': 'unisex-kids'}

    def parse(self, response):
        product_id = self.extract_retailer_sku(response)

        if self.id_exists(product_id):
            return

        item = FredperryItem()

        item['retailer_sku'] = product_id
        item['gender'] = self.extract_gender(response)
        item['brand'] = self.extract_brand(response)
        item['trail'] = self.extract_trail(response)
        item['name'] = self.extract_name(response)
        item['care'] = self.extract_care(response)
        item['skus'] = self.extract_skus(response)
        item['category'] = self.extract_category(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['description'] = self.extract_description(response)
        item['url'] = response.url

        item['meta'] = {'requests': self.generate_colour_requests(response)}

        return self.generate_request_or_item(item)

    def parse_colours(self, response):
        item = response.meta['item']
        item['skus'] += self.extract_skus(response)
        item['image_urls'] += self.extract_image_urls(response)

        return self.generate_request_or_item(item)

    def generate_request_or_item(self, item):

        if not item.get('meta'):
            return item

        if item['meta'].get('requests'):
            next_request = item['meta']['requests'].pop()
            next_request.meta['item'] = item
            return next_request

        del item['meta']
        return item

    def extract_skus(self, response):
        skus = []
        common_sku = {'price': self.extract_price(response),
                      'sku_id': self.extract_retailer_sku(response),
                      'currency': self.extract_currency(response)}
        previous_prices = self.extract_previous_prices(response)

        if previous_prices:
            common_sku['previous_prices'] = self.extract_previous_prices(response)

        colour = self.extract_colour(response)

        if colour:
            common_sku['colour'] = colour

        out_stock_sizes = self.extract_out_stock_sizes(response)

        for size in self.extract_sizes(response):
            sku = common_sku.copy()
            sku['size'] = size

            sku['sku_id'] = f"{colour}_{size}" if colour else f"{size}"

            if size in out_stock_sizes:
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def generate_colour_requests(self, response):
        requests = []

        for url in self.extract_colour_urls(response):
            requests.append(response.follow(
                url, callback=self.parse_colours, dont_filter=True))

        return requests

    def extract_colour_urls(self, response):
        css = '.colour-swatches :not(.active) > a::attr(href)'
        return response.css(css).extract()

    def extract_brand(self, response):
        css = 'head title::text'
        raw_brand = response.css(css).extract_first()

        if 'Fred Perry' in raw_brand:
            return 'Fred Perry'

    def extract_image_urls(self, response):
        css = '.product-image-gallery img::attr(src)'
        return response.css(css).extract()

    def extract_colour(self, response):
        css = "script[type='application/ld+json']::text"
        raw_colour = json.loads(response.css(css).extract_first())

        return raw_colour['color']

    def extract_retailer_sku(self, response):
        css = '.product-sku p::text'
        return response.css(css).extract_first()

    def extract_currency(self, response):
        css = '.price::text'
        raw_currency = response.css(css).extract_first()

        if '£' in raw_currency:
            return 'GBP'

    def extract_price(self, response):
        css = '.product-essential .special-price .price::text'
        raw_currency = response.css(css).extract_first()

        if raw_currency:
            return int(float(raw_currency.strip()[1:]) * 100)

        raw_currency = response.css('.price::text').extract_first()

        return int(float(raw_currency.strip()[1:]) * 100)

    def extract_previous_prices(self, response):
        css = '.product-essential .old-price .price::text'
        raw_prices = set(response.css(css).extract())

        return [int(float(price.strip()[1:]) * 100) for price in raw_prices]

    def extract_name(self, response):
        css = '.product-name h1 ::text'
        return response.css(css).extract_first()

    def extract_category(self, response):
        return [t for t, _ in response.meta['trail']]

    def extract_sizes(self, response):
        css = '#configurable_swatch_size a::attr(name)'
        return response.css(css).extract()

    def extract_out_stock_sizes(self, response):
        path = "//li[contains(@class, 'notify')]/a/@name"
        return response.selector.xpath(path).extract()

    def extract_care(self, response):
        css = '.further-reading li::text'
        return response.css(css).extract()

    def extract_description(self, response):
        return response.css('.std ::text').extract()

    def extract_gender(self, response):
        soup = ' '.join([t for t, _ in response.meta['trail']]).lower()

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

        return 'Unisex Adults'

    def extract_trail(self, response):
        return response.meta['trail']

    def id_exists(self, product_id):

        if product_id in self.visited_products:
            return True

        self.visited_products.add(product_id)


class FredperryCrawler(CrawlSpider):
    name = 'fredperry_spider'
    allowed_domains = ['fredperry.com']
    start_urls = ['https://www.fredperry.com/classic-oxford-shirt-m3551-644.html']

    listing_css = ['.skip-links-left', '.pages']
    product_css = ['.product-name']

    rules = [Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')]

    fredperry_parse = FredperryParser()

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first(), response.url)]

        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

    def parse_item(self, response):
        return self.fredperry_parse.parse(response)
