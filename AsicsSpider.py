import re

from scrapy import Item, Field, Spider


class AsicsItem(Item):
    retailer_sku = Field()
    gender = Field()
    name = Field()
    category = Field()
    url = Field()
    brand = Field()
    description = Field()
    care = Field()
    image_urls = Field()
    skus = Field()
    requests = Field()


def clean(raw_strs):
    if isinstance(raw_strs, list):
        cleaned_strs = [re.sub('\s+', ' ', st).strip() for st in raw_strs]
        return [st for st in cleaned_strs if st]
    elif isinstance(raw_strs, str):
        return re.sub('\s+', ' ', raw_strs).strip()


class AsicsSpider(Spider):
    name = 'asics'
    allowed_domains = ['asics.com']
    start_urls = [
        'https://www.asics.com/us/en-us/',
    ]

    def parse(self, response):
        listing_urls = response.css('.childlink-wrapper ::attr(href)').getall()
        return [response.follow(url=url, callback=self.parse_category)
                for url in listing_urls]

    def parse_category(self, response):
        product_urls = response.css('.prod-wrap ::attr(href)').getall()
        return [response.follow(url=url, callback=self.parse_item)
                for url in product_urls]

        next_page_url = response.css('rightArrow ::attr(href)').get()
        if next_page_url:
            return response.follow(url=next_page_url, callback=self.parse_category)

    def parse_item(self, response):
        item = AsicsItem()
        item['retailer_sku'] = self.retailer_sku(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['description'] = self.product_description(response)
        item['brand'] = self.product_brand(response)
        item['care'] = []
        item['image_urls'] = self.product_image_urls(response)
        item['skus'] = self.product_skus(response)

        item['requests'] = self.colour_requests(response)
        return self.next_request_or_item(item)

    def colour_requests(self, response):
        color_urls = response.css('.colorVariant ::attr(href)').getall()
        return [response.follow(color_url, callback=self.parse_color)
                for color_url in color_urls]

    def parse_color(self, response):
        item = response.meta['item']
        item['image_urls'].extend(self.product_image_urls(response))
        item['skus'].update(self.product_skus(response))
        return self.next_request_or_item(item)

    def product_skus(self, response):
        skus = {}
        common_sku = {
            'color': response.css('[itemprop="color"] ::text').get(),
            'previous_price': response.css('del ::text').getall()
        }

        size_sels = response.css('.tab:not(.hide-tab) > .size-box-select-container '
                                 '#sizes-options > .SizeOption')
        for sku_sel in size_sels:
            key = sku_sel.css('::attr(data-value)').get()
            sku = {
                'out_of_stock': bool(sku_sel.css('.disabled')),
                'currency': sku_sel.css('[itemprop="priceCurrency"]::attr(content)').get(),
                'price': sku_sel.css('[itemprop="price"]::attr(content)').get(),
                'size': clean(sku_sel.css('a.SizeOption ::text').get()),
            }

            sku.update(common_sku)
            skus[key] = sku

        return skus

    def next_request_or_item(self, item):
        if item['requests']:
            request = item['requests'].pop()
            request.meta['item'] = item
            return request

        item.pop('requests', None)
        return item

    def retailer_sku(self, response):
        return response.css('[itemprop="productID"] ::attr(content)').get()

    def product_name(self, response):
        return response.css('.single-prod-title ::text').get()

    def product_gender(self, response):
        return response.css('script:contains("gender")').re_first('\"gender\":\"(.+?)\"')

    def product_category(self, response):
        return response.css('.breadcrumb ::text').getall()[1].split(' ')

    def product_url(self, response):
        return response.url

    def product_description(self, response):
        raw_descriptions = response.css('.tabInfoChildContent ::text').getall()
        return clean(raw_descriptions)[1:]

    def product_image_urls(self, response):
        return response.css('.owl-carousel ::attr(data-big)').getall()

    def product_brand(self, response):
        return response.css('::attr(data-brand)').get()
