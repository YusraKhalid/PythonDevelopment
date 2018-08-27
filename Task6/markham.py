import json
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode
from w3lib.url import add_or_replace_parameter

from Task6.items import Product


class MarkhamSpider(CrawlSpider):
    name = 'markham'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['markham.co.za']
    start_urls = ['https://www.markham.co.za']

    allowed_r = ('plp/clothing/', 'plp/shoes/', '/plp/accessories/')
    rules = (Rule(LinkExtractor(allow=allowed_r, restrict_css=".nav__item-title"),
                  callback='parse_pagination'),)

    skus_request_t = 'https://www.markham.co.za/product/generateProductJSON.jsp?productId={}'
    category_request_t = 'https://www.markham.co.za/search/ajaxResultsList.jsp?N={0}&baseState={0}'

    def parse_pagination(self, response):
        products_details = json.loads(response.css('#product-listing-static-data::text')
                                      .extract_first())["data"]
        total_pages = products_details["totalPages"]

        category_id = re.findall('N-([\w+]+);', response.url)[0]
        category_request = self.category_request_t.format(category_id)

        requests = []
        for page in range(1, total_pages + 1):
            url = add_or_replace_parameter(category_request, 'page', page)
            url = add_or_replace_parameter(url, 'No', page * 15)

            requests.append(Request(url, callback=self.parse_item_links))

        return requests

    def parse_item_links(self, response):
        products = json.loads(response.text)["data"]["products"]
        item_urls = [product["pdpLinkUrl"] for product in products]

        return [response.follow(item_url, callback=self.parse_item) for item_url in item_urls]

    def parse_item(self, response):
        item = Product()
        raw_product = self.extract_raw_product(response)

        item["retailer_sku"] = self.extract_retailer_sku(raw_product)
        item["name"] = self.extract_name(raw_product)
        item["price"] = self.extract_price(raw_product)
        item["brand"] = self.extract_brand(raw_product)
        item["url"] = response.url
        item["category"] = self.extract_categories(response)
        item["gender"] = "Men"
        item["description"] = self.extract_description(response)
        item["image_urls"] = self.extract_image_urls(raw_product)
        item["care"] = self.extract_care(response)
        item["skus"] = []
        item["requests_queue"] = self.get_skus_requests(raw_product, item)

        return item["requests_queue"].pop()

    def get_skus_requests(self, item_detail, item):
        colors = item_detail["colors"]
        sku_request = self.skus_request_t.format(item_detail["id"])

        skus_requests = [add_or_replace_parameter(sku_request, "selectedColor", color["id"])
                         for color in colors]

        return [Request(url, callback=self.parse_skus, meta={"item": item}) for url in skus_requests]

    def parse_skus(self, response):
        item = response.meta["item"]
        sku_detail = json.loads(response.text)

        item["skus"].extend(self.extract_sku(sku_detail))

        return self.process_skus_requests(item)

    def process_skus_requests(self, item):

        if item["requests_queue"]:
            return item["requests_queue"].pop()

        del item["requests_queue"]
        return item

    def extract_raw_product(self, response):
        return json.loads(response.css('textarea#product-static-data::text').extract_first())

    def extract_sku(self, sku_detail):
        skus = []

        if not sku_detail.get("sizes"):
            sku_detail["sizes"] = [{"name": "One Size", "available": True}]

        for size in sku_detail["sizes"]:
            sku = {"color": sku_detail["colors"][0]["name"],
                   "size": size["name"],
                   "price": sku_detail["price"],
                   "currency": 'PHP',
                   "sku_id": f'{sku_detail["colors"][0]["name"]}_{size["name"]}'}

            if not size["available"]:
                sku["out_of_stock"] = True

            if sku_detail.get("oldPrice"):
                sku["previous_prices"] = [sku_detail["oldPrice"]]

            skus.append(sku)

        return skus

    def extract_retailer_sku(self, item_detail):
        return item_detail["id"]

    def extract_name(self, item_detail):
        return item_detail["name"]

    def extract_price(self, item_detail):
        return float(re.findall('([\d+,]+)', item_detail["price"])[0].replace(",", "")) * 100

    def extract_brand(self, item_detail):
        return item_detail["brand"]

    def extract_categories(self, response):
        return response.css('.breadcrumbs__item a::text').extract()[1:-1]

    def extract_description(self, response):
        return response.css('meta[itemprop="description"]::attr(content)').extract_first()

    def extract_image_urls(self, item_detail):
        return [img["large"] for img in item_detail["images"]]

    def extract_care(self, response):
        return response.css('script#product-detail-template::text').re('<td>(.+)</td>')
