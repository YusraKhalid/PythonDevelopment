import itertools
import ast
from datetime import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import ccy


class JackLemkusCrawler(CrawlSpider):
    name = 'jacklemkus'

    allowed_domains = ['jacklemkus.com']
    start_urls = ['https://www.jacklemkus.com/']

    listings_css = ['#nav > li > a', 'a.next']
    products_css = ['.products-grid > li > .product-image']

    retailer = 'jacklemkus-za'
    currency = 'ZAR'

    rules = (
        Rule(LinkExtractor(deny='how-to-order', restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    def parse(self, response):
        trail = response.meta.get('trail', [["", response.url]])
        for request in super().parse(response):
            request.meta['trail'] = trail + [[request.meta['link_text'].strip(), request.url]]
            yield request

    def parse_product(self, response):
        product = {}

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['trail'] = response.meta['trail'][:-1]
        product['description'] = self.extract_description(response)
        product['gender'] = self.extract_gender(response)
        product['category'] = self.extract_category(product['trail'])
        product['brand'] = self.extract_brand(response)
        product['url'] = self.extract_url(response)
        product['date'] = self.extract_date(response)
        product['price'] = self.extract_price(response)
        product['currency'] = JackLemkusCrawler.currency
        product['market'] = self.extract_market(product['currency'])
        product['retailer'] = JackLemkusCrawler.retailer
        product['url_original'] = response.url
        product['name'] = self.extract_name(response)
        product['care'] = self.extract_care(product['description'])
        product['image_urls'] = self.extract_image_urls(response)
        product['skus'] = self.extract_skus(response, product['price'])
        product['spider_name'] = JackLemkusCrawler.name
        product['crawl_start_time'] = self.extract_crawl_start_time()

        yield product

    def extract_retailer_sku(self, response):
        return response.css('span.sku::text').get().strip()

    def extract_gender(self, response):
        gender_x = ('//*[@id="product-attribute-specs-table"]/tbody/tr/th[contains(text(),"Gender")]/'
                    'following-sibling::td/text()')
        gender = response.xpath(gender_x).get()
        if gender is None:
            return 'unisex'
        gender = gender.lower()

        genders = {
            'men': {'men'},
            'women': {'women'},
            'kid': {'kid', 'boy', 'girl', 'toddler', 'gradeschool', 'preschool', 'infant'},
            'unisex': {'unisex', 'neutral'}
        }

        for g in genders:
            if check_words_existence(genders[g], gender):
                return g
        return ''

    def extract_brand(self, response):
        brands_x = ('//*[@id="product-attribute-specs-table"]/tbody/tr/th[contains(text(),"Item Brand")]/'
                    'following-sibling::td/text()')
        return response.xpath().get()

    def extract_category(self, trail):
        return [t[0] for t in itertools.islice(trail, 1, None)]

    def extract_url(self, response):
        return response.css('head link[rel="canonical"]::attr("href")').get()

    def extract_date(self, response):
        date = response.headers["Date"].decode('utf-8')
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

    def extract_market(self, currency):
        return ccy.currency(currency).default_country

    def extract_name(self, response):
        return response.css('div.product-name h1::text').get().strip()

    def extract_description(self, response):
        description_tab_data = (data.strip() for data in response.css('#description-tab .std *::text').getall())
        return [data for data in description_tab_data if data != '']

    def extract_care(self, description):
        care_words = {'synthetic', 'composition'}

        return [d for d in description if check_words_existence(care_words, d.lower())]

    def extract_image_urls(self, response):
        image_urls = response.css('.product-image-wrapper a::attr("href")').getall()
        return image_urls

    def extract_skus(self, response, price):
        product_data = ast.literal_eval(response.css('div.product-data-mine::attr("data-lookup")').get())

        common_sku = {'price': price, 'currency': JackLemkusCrawler.currency}
        skus = []
        for data in product_data.values():
            sku = common_sku.copy()
            sku['size'] = data.get('size')
            sku['out_of_stock'] = not data['stock_status']
            sku['sku_id'] = data.get('id')
            skus.append(sku)

        return skus

    def extract_price(self, response):
        return response.css('.regular-price .price::text').get()

    def extract_crawl_start_time(self):
        return self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')


def check_words_existence(words, text):
    return any(word in text for word in words)
