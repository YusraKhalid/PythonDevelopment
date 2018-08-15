from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
import js2py

from Task7.items import Product


class StoriesSpider(CrawlSpider):
    name = 'stories'
    custom_settings = {'DOWNLOAD_DELAY': 1.25}
    allowed_domains = ['stories.com']
    start_urls = ['https://www.stories.com/en_eur/index.html']

    allowed_r = ('/clothing', '/shoes', '/bags', '/jewellery', '/accessories',
                 '/swimwear', '/lingerie', '/stationery', '/beauty', )
    rules = (Rule(LinkExtractor(allow=allowed_r, restrict_css=".categories"), callback='parse_pagination'),)

    def parse_pagination(self, response):
        total_items = response.css("#productCount::attr(class)").extract_first()
        page_url = response.urljoin(response.css("#productPath::attr(class)").extract_first())

        return [Request(f"{page_url}?start={start}", callback=self.parse_items_links)
               for start in range(0, int(total_items)+1, 32)]

    def parse_items_links(self, response):
        items_links = response.css("a::attr(href)").extract()
        items_urls = [response.urljoin(url) for url in items_links]

        return [Request(items_url, callback=self.parse_item) for items_url in items_urls]

    def parse_item(self, response):
        item_details = response.css("[class*='o-page-content '] script::text").extract_first()
        item_details = js2py.eval_js(item_details)
        current_item = item_details[item_details["articleCode"]]
        item = Product()

        item["retailer_sku"] = self.extract_retailer_sku(item_details)
        item["name"] = self.extract_name(item_details)
        item["url"] = self.extract_url(current_item)
        item["brand"] = self.extract_brand(current_item)
        item["price"] = self.extract_price(current_item)
        item["gender"] = "Women"
        item["description"] = self.extract_description(current_item)
        item["image_urls"] = self.extract_image_urls(current_item)
        item["category"] = self.extract_categories(item_details)
        item["skus"] = self.extract_skus(item_details)

        return item

    def extract_retailer_sku(self, item_detail):
        return item_detail["articleCode"]

    def extract_name(self, item_detail):
        return item_detail["name"]

    def extract_url(self, current_item):
        return current_item["pdpLink"]

    def extract_brand(self, current_item):
        return current_item["brandName"]

    def extract_price(self, current_item):
        return float(current_item["priceValue"])*100

    def extract_description(self, current_item):
        return current_item["description"]

    def extract_image_urls(self, current_item):
        return [f'https:{image_url["fullscreen"]}' for image_url in current_item["images"]]

    def extract_categories(self, item_details):
        return item_details["mainCategorySummary"]

    def extract_skus(self, item_details):
        color_variants = [item_details[key] for key in item_details if key.isdigit()]

        skus = []
        for color_variant in color_variants:
            for sku_variant in color_variant["variants"]:
                sku = {"size": sku_variant["sizeName"], "color": color_variant["name"]}
                sku["price"] = color_variant["price"]
                sku["currency"] = "EUR"

                if color_variant["priceOriginal"]:
                    sku["previous_prices"] = [color_variant["priceOriginal"]]

                skus.append(sku)

        return skus
