import re
import json

import scrapy


class APCUSSpider(scrapy.Spider):
    name = "apc_us"
    start_urls = [
        'https://www.apc-us.com'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'apc-us.com'
    ]

    def parse(self, response):
        listing_css = '#main-nav a::attr(href)'

        for url in response.css(listing_css).extract():
            yield response.follow(url, self.parse_listing)

    def parse_listing(self, response):
        product_css = 'a.product-image::attr(href)'

        for url in response.css(product_css).extract():
            yield response.follow(url, self.parse_product)

    def parse_product(self, response):
        return {
            'retailer_sku': self.get_product_retailer_sku(response),
            'name': self.get_product_name(response),
            'category': self.get_product_categories(response),
            'description': self.get_product_description(response),
            'image_urls': self.get_product_images(response),
            'url': response.url,
            'gender': self.get_product_gender(response),
            'brand': 'A.P.C.',
            'care': self.get_product_care(response),
            'skus': self.get_product_skus(response)
        }

    @staticmethod
    def get_product_categories(response):
        categories = response.css('div.breadcrumbs a::text').extract()
        return categories[1:]

    @staticmethod
    def get_product_name(response):
        return response.css('div.product-name h1::text').extract_first()

    @staticmethod
    def get_product_description(response):
        description = response.css('section#description div > div::text').extract_first()
        return [d.strip() for d in description.split('. ') if '%' not in d]

    @staticmethod
    def get_product_care(response):
        care = response.css('section#description div > div::text').extract_first()
        return [c.strip() for c in care.split('. ') if '%' in c]

    def get_product_images(self, response):
        retailer_sku = self.get_product_retailer_sku(response)
        product_gallery = response.css('div.product-image-gallery img::attr(src)').extract()
        retailer_sku_lowercase = retailer_sku.lower()
        return [i.replace('600x', '1800x') for i in product_gallery
                if retailer_sku_lowercase in i.lower()]

    @staticmethod
    def get_product_retailer_sku(response):
        return response.url.split('-')[-1]

    @staticmethod
    def get_product_gender(response):
        gender_map = {'women_apparel_size_label': 'female', 'men_apparel_size_label': 'male'}
        size_label = response.xpath('//dt/label[contains(@id, "size")]/@id').extract_first()
        return gender_map.get(size_label)

    def get_product_skus(self, response):
        skus = []
        colors = response.css('#configurable_swatch_color li')
        sizes = response.css('ul.configurable-swatch-list.configurable-block-list.clearfix li')
        prices = self.get_product_prices(response)
        raw_product = self.get_raw_product(response)

        sku_price = {}

        if len(prices) > 1:
            sku_price['previous_price'] = prices[0]
            sku_price['price'] = prices[1]
        else:
            sku_price['price'] = prices[0]

        for color in colors:
            color_code, color_name = self.get_product_color(color)
            for size in sizes:
                sku = {}
                sku.update(sku_price)
                size_code, size_name = self.get_product_size(size)
                key = f"{color_code},{size_code}"
                raw_sku = raw_product.get(key)
                if not raw_sku:
                    continue

                sku['sku_id'] = raw_sku.get('product_id')
                sku['color'] = color_name
                sku['currency'] = 'USD'
                sku['size'] = size_name
                sku['out_of_stock'] = not raw_sku.get('is_in_stock')

                skus.append(sku)
        return skus

    @staticmethod
    def get_product_size(response):
        size_code = response.css('li::attr(id)').extract_first()
        size_code = re.findall(r'\d+', size_code)[0]
        size_text = response.css('a::attr(name)').extract_first()
        return size_code, size_text

    @staticmethod
    def get_product_color(response):
        color_code = response.css('li::attr(id)').extract_first()
        color_code = re.findall(r'\d+', color_code)[0]
        color_text = response.css('a::attr(name)').extract_first()
        return color_code, color_text

    @staticmethod
    def get_raw_product(response):
        script = response.xpath(
            '//div[@id="product-options-wrapper"]//script[contains(text(), "StockStatus")]/text()'
        ).extract_first()
        stock_status_json = script.split('new StockStatus(')[1].split(')')[0]
        return json.loads(stock_status_json)

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d*.?\d*$', string)[0]
        return int(float(price.replace(',', '')) * 100)

    def get_product_prices(self, response):
        prices = response.css('div.product-shop div.price-info span.price::text').extract()
        return [self.get_price_from_string(price.strip()) for price in prices]
