import re
import json
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'tesco-uk'
    market = 'UK'
    currency = '£'
    allowed_domains = ['tesco.com']
    start_urls = ['https://www.tesco.com/direct/clothing/']
    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-kids')
    ]


class TescoParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'

    def parse(self, response):

        product_json, product_sku_json = self.product_json(response)
        if product_json['prices'].get('error'):
            return
        product_id = self.product_id(product_json)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)

        requests = []
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(product_sku_json)
        if self.homeware(garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        product_sku_ids = self.product_sku_ids(product_json, product_sku_json['id'])
        garment['skus'].update(self.sku(response, product_json, product_sku_json))

        for sku_id in product_sku_ids:
            product_sku_url = add_or_replace_parameter(response.url, 'skuId', sku_id)
            requests.append(Request(product_sku_url, self.parse_color, dont_filter=True))

        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        product_json, product_sku_json = self.product_json(response)

        if not product_sku_json.get('prices'):
            return self.next_request_or_garment(garment)

        garment['skus'].update(self.sku(response, product_json, product_sku_json))
        garment['image_urls'] += self.image_urls(product_sku_json)

        return self.next_request_or_garment(garment)

    def product_id(self, product_json):
        return product_json.get('id')

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        return clean(response.css('[itemprop="description"]::text, [itemprop="description"] p::text'))

    def product_category(self, response):
        return clean(response.css('#breadcrumb-v2 [itemprop="title"]::text'))[1:]

    def product_care(self, response):
        return clean(response.css('.product-spec-label::text, .product-spec-value::text'))

    def product_gender(self, garment):
        soup = garment['category']
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, product_sku_json):
        image_urls = []
        for media in product_sku_json['mediaAssets']['skuMedia']:
            if media["mediaType"] == "Large":
                image_urls.append(media['src'])
        return image_urls

    def homeware(self, garment):
        return garment.get('industry') or 'Homeware' in garment['category']

    def product_json(self, response):
        product_script = clean(response.css('#ssb_block_10 > script:first-child::text'))
        product_json = re.findall('product = ({.*}), sku = ({.*}), assetData', product_script[0], flags=re.DOTALL)[0]
        return json.loads(product_json[0]), json.loads(product_json[1])

    def sku(self, response, product_json, product_sku_json):
        sku = {}
        sku_prices, product_prices = product_sku_json['prices'], product_json['prices']
        price_string = self.currency + sku_prices.get('price', sku_prices.get('fromPrice'))
        pprice_string = self.currency + sku_prices.get('was', product_prices.get('price', product_prices.get('toPrice')))

        prices = self.product_pricing_common_new(response, [price_string, pprice_string])

        sku_id = product_sku_json['id']
        sku[sku_id] = {
            "merch_info": "Earn " + str(product_sku_json['prices']["clubcardPoints"]) + " Clubcard points"
        }
        sku[sku_id].update(prices)
        if product_sku_json['attributes'].get('colour'):
            sku[sku_id].update({'colour': product_sku_json['attributes']['colour']})
        if product_sku_json['attributes'].get('size'):
            sku[sku_id].update({'size': product_sku_json['attributes']['size']})

        return sku

    def product_sku_ids(self, product_json, current_product_sku_id):
        remaining_product_sku_ids = []
        for link in product_json['links']:
            if link['type'] == "sku" and link['rel'] == "childSku":
                if link['id'] != current_product_sku_id:
                    remaining_product_sku_ids.append(link['id'])

        return remaining_product_sku_ids



class TescoCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = TescoParseSpider()
    product_category_css = '.product'

    STANDARD_PRODUCT_RANGE = 20

    pagination_url = "https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?catId={0}&offset={1}"

    rules = (
        Rule(LinkExtractor(restrict_css=product_category_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        product_count_css = '#listing::attr(data-maxcount)'
        category_id_css = '.products-wrapper::attr(data-endecaid)'
        total_products = clean(response.css(product_count_css))

        if not total_products:
            return
        requests = []
        total_products = int(total_products[0])

        for offset in range(0, total_products, self.STANDARD_PRODUCT_RANGE):
            category_id = clean(response.css(category_id_css))[0]
            pagination_url = self.pagination_url.format(category_id, offset)
            requests.append(Request(pagination_url, self.parse_products, dont_filter=True))
        return requests

    def parse_products(self, response):
        requests = []
        product_card_css = '.image-container .thumbnail::attr(href)'
        products_json = json.loads(response.text)['products']
        products_html = Selector(text=products_json)

        for product_url in clean(products_html.css(product_card_css)):
            requests.append(Request(response.urljoin(product_url), self.parse_spider.parse, dont_filter=True))
        return requests
