import json
import re
from datetime import datetime

from lindex.items import LindexItem
from lindex.utils import LindexItemLoader
from scrapy import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LindexSpider(CrawlSpider):
    name = "lindex"
    allowed_domains = ["www.lindex.com"]
    start_urls = ["http://www.lindex.com/uk/"]
    listing_css = [".mega_menu_box"]
    products_css = [".gridPage .img_wrapper"]
    deny_re = [
        "/sale/", "/new-in/", "guide", "giftcard",
        "/children-wear/", "/campaign/", "/Assets/"
        ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_re),callback="parse_pagination"),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny_re), callback="parse_product")
    ]

    def parse_pagination(self, response):
        node_id = self.product_node_id(response)
        total_pages = self.total_page_count(response)
        curr_page = 0
        url = "https://www.lindex.com/uk/SiteV3/Category/GetProductGridPage"
        headers = {"X-Requested-With": "XMLHttpRequest"}

        for curr_page in range(total_pages):
            yield FormRequest(
                url=url, headers=headers,
                formdata={"nodeId": node_id, "pageIndex": str(curr_page)},
                callback=self.parse)

    def skus(self, details):
        sizes = details["SizeInfo"]
        color_name = details["Color"]
        skus = []

        for size in sizes[1:]:
                size = re.findall(".+?(?=\s|-|\()", size["Text"])[0]
                skus.append({
                    "color": color_name, "price": details["Price"],
                    "is_sold_out": details["IsSoldOut"], "size": size,
                    "sku_id": "{}_{}".format(size, color_name)
                })
        return skus

    def parse_colors(self, response):
        details = json.loads(response.body)["d"]
        item_loader = response.meta["item-loader"]
        item_loader.add_value("skus", self.skus(details))
        item_loader.add_value("image_urls", self.image_urls(details))
        return self.next_request_or_item(item_loader)

    def color_requests(self, response, item_loader):
        colors = self.product_colors_id(response)
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json; charset=UTF-8"}
        url = "https://www.lindex.com/WebServices/ProductService.asmx/GetProductData"

        colors_request = []
        for color in colors:
            colors_request.append(Request(
                url=url, method="POST", callback=self.parse_colors,
                headers=headers, priority=10,
                body=json.dumps({
                    "productIdentifier": self.product_id(response),
                    "colorId": color,
                    "primaryImageType": "1"}),
                meta={"item-loader": item_loader}
                ))
        return colors_request

    def next_request_or_item(self, item_loader):
        colors_request = item_loader.get_collected_values("meta")
        if not colors_request:
            yield item_loader.load_item()
        else:
            yield colors_request.pop(0)

    def parse_product(self, response):
        item_loader = LindexItemLoader(item=LindexItem(), response=response)
        item_loader.add_value("uuid", self.product_uuid(response))
        item_loader.add_value("retailer_sku", self.product_id(response))
        item_loader.add_value("industry", self.product_industry(response))
        item_loader.add_value("name", self.product_name(response))
        item_loader.add_value("brand", self.product_brand(response))
        item_loader.add_value("pricing_details", self.get_pricing_details(response))
        item_loader.add_value("gender", "Women")
        item_loader.add_value("categories", self.product_categories(response))
        item_loader.add_value("description", self.product_description(response))
        item_loader.add_value("care", self.product_care(response))
        item_loader.add_value("url_orignal", response.url)
        item_loader.add_value("url", self.product_url(response))
        item_loader.add_value("date", datetime.now().strftime("%Y-%m-%d"))
        item_loader.add_value("market", self.get_market(response))
        item_loader.add_value("retailer", "lindex-uk")
        item_loader.add_value("spider_name", "lindex-uk-crawl")
        item_loader.add_value("crawl_id", f"lindex-uk-{datetime.now().strftime('%Y%m%d-%H%M%s')}-axuj")
        item_loader.add_value("crawl_start_time", datetime.now().isoformat())
        item_loader.add_value("meta", self.color_requests(response, item_loader))
        return self.next_request_or_item(item_loader)

    def image_urls(self, details):
        return [image["Standard"] for image in details["Images"]]

    def get_market(self, response):
        css = ".selectedCountry[type='hidden']::attr(value)"
        return response.css(css).extract()

    def currency_type(self, response):
        css = ".totalPrice::text"
        currency = response.css(css).extract()
        return "".join(re.findall(r"[^\d. ]", currency[0]))

    def total_page_count(self, response):
        css = ".gridPages::attr(data-page-count)"
        return int(response.css(css).extract_first())

    def product_node_id(self, response):
        css = "body::attr(data-page-id)"
        return response.css(css).extract_first()

    def product_colors_id(self, response):
        css = ".info_wrapper .colors a::attr(data-colorid)"
        return response.css(css).extract()

    def product_uuid(self, response):
        css = ".main_content::attr(data-productid)"
        return response.css(css).extract()

    def product_name(self, response):
        css = ".name::text"
        return response.css(css).extract()

    def product_id(self, response):
        css = ".main_content .product_placeholder::attr(data-product-identifier)"
        return response.css(css).extract_first()

    def product_brand(self, response):
        css = ".main_content .product_placeholder::attr(data-product-brand)"
        return response.css(css).extract()

    def product_price(self, response):
        css = ".main_content .product_placeholder::attr(data-product-price)"
        return response.css(css).extract_first()

    def get_pricing_details(self, response):
        return {
            "price": self.product_price(response),
            "currency": self.currency_type(response),
            "symbol": re.findall(r"[^\d.]", self.product_price(response))[0]
        }

    def product_categories(self, response):
        css = ".main_content .product_placeholder::attr(data-product-category)"
        return response.css(css).extract()

    def product_description(self, response):
        css = ".description ::text"
        return response.css(css).extract()

    def product_care(self, response):
        css = ".more_info ::text"
        return response.css(css).extract()

    def product_url(self, response):
        css = "link[rel='canonical']::attr(href)"
        return response.css(css).extract()

    def product_industry(self, response):
        css = ".main_content .product_placeholder::attr(data-style)"
        return response.css(css).extract()
