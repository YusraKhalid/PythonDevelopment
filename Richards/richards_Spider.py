import json
import re
from scrapy import Request
from .base import BaseParseSpider, BaseCrawlSpider, clean, CurrencyParser
import urllib.parse


class Mixin:
    retailer = 'richards-br'
    allowed_domains = ['richards.com.br']
    lang = 'pt'
    market = 'BR'
    start_urls = ['http://www.richards.com.br']
    category_IDs = [560931917, 3056766704, 43564721, 1005777739]
    gender_map = [
        ('1005777739', 'men'),
        ('43564721', 'women'),
        ('3056766704', 'girls'),
        ('560931917', 'boys')]


class RichardsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):

        product = self.clean_json(response)
        sku_id = product['skuId']
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response)
        garment['gender'] = self.detect_gender_from_tokens(str(response.meta['id']), gender_map=Mixin.gender_map)
        garment['name'] = product['name']
        garment['brand'] = self.brand_name(garment['name'])
        garment['url'] = product['url']
        garment['description'] = self.product_description(product['details'])
        garment['care'] = self.product_care(product['details'])
        garment['skus'] = {}
        garment['image_urls'] = []

        return self.next_request(garment, product, response)

    def next_request(self, garment, product, response):

        all_color_sku = []
        for color in product['colorList']:
            all_color_sku.append(color['skuId'])

        params = {'imageProperties': 'thumb,large,zoom', 'productId': product['id'],
                  'selectedSkuId': all_color_sku.pop()}

        url_color = self.create_url(params)
        request = Request(url=url_color, callback=self.parse_color)
        request.meta['garment'] = garment
        request.meta['all_color_sku'] = all_color_sku
        request.meta['params'] = params
        request.meta['currency'] = self.get_currency(response)

        return request

    def get_currency(self, response):
        return CurrencyParser.currency(clean(response.css('meta[property="og:price:currency"]::attr(content)'))[0])

    def brand_name(self, name):
        name = name.split(' ')
        if "BIARRITZ" in name:
            return "BIARRITZ"
        elif "BIRKENSTOCK" in name:
            return "BIRKENSTOCK"
        return "RICHARDS"

    def parse_color(self, response):

        garment = response.meta['garment']
        all_color_sku = response.meta['all_color_sku']
        params = response.meta['params']
        json_data = json.loads(response.text)
        currency = response.meta['currency']

        garment['skus'] = self.skus(garment['skus'], json_data, currency)
        garment['image_urls'] = garment['image_urls'] + self.image_urls(json_data['mediaSets'])

        if len(all_color_sku) > 0:
            response.meta['all_color_sku'] = all_color_sku
            response.meta['garment'] = garment
            response.meta['params'] = params
            response.meta['currency'] = currency

            params["selectedSkuId"] = all_color_sku.pop()
            url_color = self.create_url(params)

            yield Request(url_color, callback=self.parse_color, meta=response.meta)

        else:
            yield garment

    def product_description(self, product):
        return [rd for rd in self.raw_description(product) if not self.care_criteria(rd)]

    def product_care(self, product):
        return [rd for rd in self.raw_description(product) if self.care_criteria(rd)]

    def raw_description(self, product):
        description_tab, details_tab = [], []
        if 'description' in product.keys():
            description_tab = [product['description']['value']]
        if 'details' in product.keys():
            details_tab = [product['details']['value']]
        return description_tab+details_tab

    def image_urls(self, json_data):
        img_url = []
        for image in json_data:
            img_url.append(image['zoom'])
        return img_url

    def skus(self, skus, json_data, currency):

        colors = json_data['colorList']
        sizes = []
        if 'sizeList' in json_data.keys():
            sizes = json_data['sizeList']
        color_sku = json_data['skuId']
        color_name = self.color_name(colors, color_sku)

        for size in sizes:
            skus[color_sku + "_" + size['skuId']] = {"size": size['name'], 'price': json_data['atualPrice'],
                                                     'currency': currency, 'out_of_stock': size['hasStock'],
                                                     'color': color_name}
        return skus

    def color_name(self, colors, color_sku):
        for color in colors:
            if color['skuId'] == color_sku:
                return color['name']

    def create_url(self, params):
        return 'http://www.richards.com.br/services/get-complete-product.jsp?' + urllib.parse.urlencode(params)

    def clean_json(self, response):
        json_string = self.get_json(response)
        return json.loads(json_string)

    def get_json(self, response):
        script = response.xpath('//script[contains(., "var globalProduct =")]/text()').extract()
        if script:
            raw_data = re.findall('var globalProduct = (.*);', script[0])[0]
            return raw_data


class RichardsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer+'-crawl'
    parse_spider = RichardsParseSpider()

    def parse(self, response):
        params = {'recsPerPage': 1000}
        for ids in Mixin.category_IDs:
            params.update({'N': int(ids)})
            url_params = urllib.parse.urlencode(params)
            url = Mixin.start_urls[0] + '/services/records.jsp?' + url_params
            request = Request(url=url, callback=self.parse_urls)
            request.meta["id"] = int(ids)
            yield request

    def parse_urls(self, response):
        json_dict = json.loads(response.text)
        ids = response.meta["id"]
        for record in json_dict['records']:
            request = Request(url=record['url'], callback=self.parse_item)
            request.meta["id"] = ids
            yield request


