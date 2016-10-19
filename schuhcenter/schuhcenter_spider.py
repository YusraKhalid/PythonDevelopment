# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, tokenize
from scrapy import Request


class Mixin(object):
    market = 'DE'
    retailer = 'schuhcenter-de'
    lang = 'de'
    allowed_domains = ['www.schuhcenter.de']
    start_urls = [
        'http://www.schuhcenter.de/'
    ]
    GENDER_MAP = [('herren', 'boys'), ('damen', 'girls'), ('mädchen', 'girls')]


class SchuhcenterParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//span[contains(@itemprop, 'price')]//text()|//span[" \
              "@class='oldPrice']//text()"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response, response)
        garment['gender'] = self.product_gender(garment['category'], garment['description'])
        garment['image_urls'] = self.image_urls(response)
        response.meta['currency'] = self.currency(response)
        skus = self.skus(response, product_id)
        if skus:
            garment['skus'] = skus
        else:
            garment['out_of_stock'] = True
        return [garment] + self.color_requests(response)

    def product_care(self, response):
        return ''

    def product_brand(self, response):
        product_title = self.product_title(response)
        return product_title.split('-')[0]

    def currency(self, response):
        currency_css = '[itemprop=priceCurrency]::attr(content)'
        return response.css(currency_css).extract_first()

    def color_requests(self, response):
        request_urls = response.css('div.col_sel li>a::attr(href)').extract()
        return [Request(url, callback=self.parse) for url in request_urls]

    def product_id(self, response):
        return response.css('div.visible-lg>p::text').extract_first(
        ).split('.:')[1]

    def product_title(self, response):
        return response.css('h1[itemprop=name]::text').extract_first()

    def product_description(self, response):
        return response.css('div.visible-lg li>label::text').extract()

    def product_category(self, response):
        return response.css('[itemprop=title]::text').extract()

    def product_gender(self, categories, description):
        tokens = tokenize(categories)
        tokens |= tokenize(description)
        for token, gender in self.GENDER_MAP:
            if token in tokens:
                return gender
        return 'unisex-kids'

    def product_color(self, product_title):
        tokens = product_title.split(' ')
        title_components = tokens[len(tokens)-1].split('-')
        return title_components[len(title_components)-1]

    def skus(self, response, product_id):
        skus = {}
        common = {
            'colour': self.product_color(self.product_title(response)),
            'currency': response.meta['currency'],
        }
        for size_var in response.css('div.size_info li>a'):
            size_id = size_var.css('::attr(data-selection-id)').extract_first()
            skus[str(product_id+size_id)] = sku = common.copy()
            sku['size'] = size_var.css('span::text').extract_first().strip()
            previous_price, price, currency = self.product_pricing(response)
            sku['price'] = price
            if previous_price:
                sku['previous_prices'] = previous_price
            if size_var.css('.no_stock'):
                sku['out_of_stock'] = True
        return skus

    def image_urls(self, response):
        return [img.replace('87_87', '380_340') for img in response.css(
            'div.otherPictures img::attr(src)').extract()]

    def product_name(self, response):
        prod_title = self.product_title(response).split('-')
        return ''.join(prod_title[1:len(prod_title)-1])


class SchuhcenterCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SchuhcenterParseSpider()
    listings_c = ['div.flyoutholder article.main_categories ul a',
                  'a.next']
    products_c = 'div.over-links>a'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_c), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_c), callback='parse_item'),
    )
