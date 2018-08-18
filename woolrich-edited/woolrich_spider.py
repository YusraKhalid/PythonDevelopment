# -*- coding: utf-8 -*-
import json
import re
from urllib.parse import parse_qsl

from scrapy.http import FormRequest
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['https://www.woolrich.com']


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'


class WoolrichParseSpider(BaseParseSpider, MixinUS):
    request_url = 'https://www.woolrich.com/remote/v1/product-attributes/{}'
    raw_description_css = '#features-content li::text, #details-content::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = {}

        garment['meta'] = {'requests_queue': self.color_requests(response, product_id)}

        return self.next_request_or_garment(garment)

    def color_requests(self, response, product_id):
        attributes_map = self.get_product_attrs(response)

        color_map = attributes_map.pop('color')
        attr_value = color_map.get('value')

        formdata = {'action': 'add', 'product_id': product_id}
        color_reqs = []
        for color, color_id in color_map['varients']:
            formdata[attr_value] = color_id
            
            raw_sku = {'colour': color, 'currency': attributes_map.get('currency')}
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            url = self.request_url.format(product_id)

            request = FormRequest(url=url, meta=meta, formdata=formdata, 
                            callback=self.parse_color)
            color_reqs += [request]
        
        return color_reqs

    def parse_color(self, response):
        garment = response.meta.get('garment')

        size_reqs = self.size_requests(response)
        if not size_reqs:
            garment['skus'].update(self.make_sku(response))
            
        garment['meta']['requests_queue'] += size_reqs
        return self.next_request_or_garment(garment)
    
    def size_requests(self, response):
        attributes_map = response.meta.get('attributes_map')
        sku_common = response.meta.get('raw_sku')

        sku_details = json.loads(response.text)['data']
        in_stock_attributes = sku_details['in_stock_attributes']

        size_map = attributes_map.get('size', {})
        attr_value = size_map.get('value')
        size_reqs = []
        for size, size_id in size_map.get('varients', []):
            if int(size_id) not in in_stock_attributes:
                continue

            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata[attr_value] = size_id

            raw_sku = sku_common.copy()
            raw_sku['size'] = size
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            request = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_size)
            size_reqs += [request]
        
        return size_reqs

    def parse_size(self, response):
        garment = response.meta.get('garment')

        fit_requests = self.fitting_requests(response)
        if not fit_requests:
            garment['skus'].update(self.make_sku(response))
            
        garment['meta']['requests_queue'] += fit_requests
        return self.next_request_or_garment(garment)
    
    def fitting_requests(self, response):
        attributes_map = response.meta.get('attributes_map')
        sku_common = response.meta.get('raw_sku')

        sku_details = json.loads(response.text)['data']
        in_stock_attributes = sku_details['in_stock_attributes']

        fit_map = attributes_map.get('fit', {})
        attr_value = fit_map.get('value')
        fitting_reqs = []
        for fit, fit_id in fit_map.get('varients', []):
            if int(fit_id) not in in_stock_attributes:
                continue

            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata[attr_value] = fit_id

            raw_sku = sku_common.copy()
            raw_sku['size'] = f'{raw_sku["size"]}/{fit}'
            meta = {'raw_sku': raw_sku, 'attributes_map': attributes_map}
            request = FormRequest(url=response.url, meta=meta,
                              formdata=formdata, callback=self.parse_fitting)
            fitting_reqs += [request]
        
        return fitting_reqs
    
    def parse_fitting(self, response):
        garment = response.meta.get('garment')

        garment['skus'].update(self.make_sku(response))
        return self.next_request_or_garment(garment)
    
    def make_sku(self, response):
        sku = response.meta.get('raw_sku')
        sku_details = json.loads(response.text)['data']
        pprice, price = self.sku_pricing(sku_details)

        money_strs = [price, pprice, sku['currency']]
        raw_sku = self.product_pricing_common(None, money_strs=money_strs)
        sku.update(raw_sku)

        sku['size'] = sku.get('size', self.one_size)
        return {sku_details['sku']: sku}

    def sku_pricing(self, raw_sku):
        price = raw_sku['price']['without_tax']['value']
        pprice = raw_sku['price'].get('non_sale_price_without_tax', {}).get('value')

        return pprice, price

    def get_product_attrs(self, response):
        product_attrs_sel = response.css('.productView-options [data-product-attribute]')
        attr_name_r = re.compile('color|size|fit', flags=re.I)

        attributes_map = {}
        for attr_sel in product_attrs_sel:
            attr_name = attr_sel.css('.form-label span::text').re_first(attr_name_r).lower()

            attributes_map[attr_name] = {}
            attributes_map[attr_name]['value'] = attr_sel.css('.form-radio::attr(name)').extract_first()

            attr_titles_css = '.form-option-variant::attr(title), .form-option-variant::text'
            attr_titles = clean(attr_sel.css(attr_titles_css))
            attr_titles_ids = clean(attr_sel.css('.form-radio::attr(value)'))

            attributes_map[attr_name]['varients'] = list(zip(attr_titles, attr_titles_ids))

        currency_css = '[itemprop="priceCurrency"]::attr(content)'
        attributes_map['currency'] = response.css(currency_css).extract_first()
        return attributes_map

    def product_id(self, response):
        return response.css('[name="product_id"]::attr(value)').extract_first()
    
    def raw_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()

    def product_name(self, response):
        brand = self.product_brand(response)
        raw_name = self.raw_name(response)

        return re.sub(brand, '', raw_name)

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text'))[1:]
    
    def product_brand(self, response):
    	raw_name = self.raw_name(response)

    	brand = 'John Rich & Bros'
    	return brand if brand in raw_name else 'Woolrich'
    
    def product_gender(self, response):
        soup = [self.raw_name(response)] + self.product_category(response)
        return self.gender_lookup(' '.join(soup)) or Gender.ADULTS.value        
    
    def image_urls(self, response):
        image_urls = response.css('[data-sku]::attr(data-images)').extract_first()
        image_urls = json.loads(image_urls)
        
        return [u['data'].replace('{:size}', '1200x1318') for u in image_urls if not "thumbnail" in u['alt']]


class WoolrichCrawlSpider(BaseCrawlSpider):
    listing_css = ['#primary', '.pagination-item--next']
    product_css = '.card-title'
    rules = (
                Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
                Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
            )


class WoolrichParseSpiderUS(WoolrichParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class WoolrichCrawlSpiderUS(WoolrichCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = WoolrichParseSpiderUS()
