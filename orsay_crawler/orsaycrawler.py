import json

from w3lib.url import add_or_replace_parameter
from scrapy.spiders import Rule, CrawlSpider, Request
from scrapy.linkextractors import LinkExtractor
from orsay_crawler.items import OrsayCrawlerItem


class OrsaySpider(CrawlSpider):

    name = 'orsaycrawler'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']

    listings_css = ['.navigation .level-1']
    products_css = ['.js-product-grid-portion']

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_pagination(self, response):
        page_size = 72
        css = '.load-more-progress::attr(data-max)'
        pages = response.css(css).extract_first()
        pages = int(pages) if pages else 0

        for page in range(0, pages+1, page_size):
            next_url = add_or_replace_parameter(response.url, 'sz', page)
            yield Request(url=next_url, callback=self.parse)

    def parse_product(self, response):
        item = OrsayCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'de'
        item['market'] = 'DE'
        item['gender'] = 'women'
        item['url'] = self.product_url(response)
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(raw_product)
        item['meta'] = self.colours_requests(response)
        item['brand'] = self.product_brand(raw_product)
        item['category'] = self.product_category(raw_product)
        item['image_urls'] = self.product_images_urls(response)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)
        item['skus'] = {}

        return self.next_request(item)

    def parse_colour(self, response):
        item = response.meta['item']
        item['skus'].update(self.skus(response))
        return self.next_request(item)

    def next_request(self, item):
        requests = item['meta']
        if requests:
            request = requests.pop()
            request.meta['item'] = item
            return request
        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['name']

    def product_brand(self, raw_product):
        return raw_product['brand']

    def product_category(self, raw_product):
        return raw_product['categoryName']

    def product_retailer_sku(self, raw_product):
        return raw_product['idListRef6']

    def raw_product(self, response):
        css = '.js-product-content-gtm::attr(data-product-details)'
        return json.loads(response.css(css).extract_first())

    def product_images_urls(self, response):
        return response.css('.thumb.js-thumb img::attr(src)').extract()

    def product_description(self, response):
        css = '.product-info-block.product-details div.with-gutter::text'
        return response.css(css).extract()

    def product_care(self, response):
        css = '.product-material.product-info-block.js-material-container p::text'
        return response.css(css).extract()

    def colours_requests(self, response):
        css = 'ul.swatches.color li a::attr(href)'
        colours = response.css(css).extract()
        return [Request(url=response.urljoin(c),
                callback=self.parse_colour, dont_filter=True) for c in colours]

    def skus(self, response):
        skus = {}
        raw_sku = self.raw_product(response)
        sizes_css = '.swatches.size > li'

        for size_s in response.css(sizes_css):
            size = size_s.css('a::text').extract_first().strip('\n')
            sku = {'colour': raw_sku['color']}

            if not size_s.css('.selectable'):
                sku['out_of_stock'] = True

            sku['currency'] = raw_sku['currency_code']
            sku['price'] = raw_sku['grossPrice']
            sku['size'] = raw_sku['size']
            skus[f'{raw_sku["idListRef6"]}_{raw_sku["color"]}_{size}'] = sku
        return skus
