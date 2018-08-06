import json

from scrapy import Spider, Request
from w3lib import url

from Task4.items import ProductItem


class CeaSpider(Spider):
    name = 'cea'
    custom_settings = {'DOWNLOAD_DELAY': 0.25}
    allowed_domains = ['cea.com.br']
    start_urls = ['https://www.cea.com.br']

    item_base_url_t = "https://www.cea.com.br/api/catalog_system/pub/products/search?fq=productId:{}"
    image_url_t = "https://cea.vteximg.com.br/arquivos/ids/{}"
    gender_map = {
        'unissex': 'Unisex',
        'masculina': 'Men',
        'masculino': 'Men',
        'feminino': 'Women',
        'feminina': 'Women',
        'menina': 'Girl',
        'menino': 'Boy',
        'neutro': 'Kids'
    }

    def parse(self, response):
        category_links = response.css('script[id^="submenu-data-"]::text').re(r'"url":"([\w+/-]+)[\?|"]')
        yield from [response.follow(category_link, callback=self.parse_category_link)
                    for category_link in category_links]

    def parse_category_link(self, response):
        base_category_link = response.urljoin(response.css('script::text').re_first(r'(/buscapagina?.+)&PageNumber'))
        base_category_link = url.add_or_replace_parameter(base_category_link, "PageNumber", 1)
        return Request(base_category_link, callback=self.parse_pagination)

    def parse_pagination(self, response):
        item_links = response.css('.product-actions_details a::attr(href)').extract()

        if item_links:
            yield from [Request(item_link, callback=self.parse_item) for item_link in item_links]

            page_number = url.url_query_parameter(response.url, "PageNumber")
            next_page_url = url.add_or_replace_parameter(response.url, "PageNumber", int(page_number) + 1)
            return Request(next_page_url, callback=self.parse_pagination)

    def parse_item(self, response):
        item = ProductItem()
        item['name'] = self.extract_item_name(response)
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['price'] = self.extract_price(response)
        item['brand'] = self.extract_brand(response)
        item['skus'] = self.extract_skus(response)
        item['url'] = response.url

        return Request(self.item_base_url_t.format(item['retailer_sku']),
                       callback=self.parse_json_request, meta={'item': item})

    def parse_json_request(self, response):
        item_detail = json.loads(response.text)[0]
        item = response.meta["item"]

        item['category'] = self.extract_category(item_detail)
        item['gender'] = self.extract_gender(response.url, item['name'], item['category'])
        item['image_urls'] = self.extract_image_urls(item_detail)
        item['description'] = self.extract_description(item_detail)

        return item

    def extract_item_name(self, response):
        return response.css('.productName::text').extract_first()

    def extract_retailer_sku(self, response):
        return response.css('#___rc-p-id::attr(value)').extract_first()

    def extract_brand(self, response):
        return response.css('td.Marca::text').extract_first()

    def extract_gender(self, url, item_name, item_categories):
        lookup_text = (item_name + url + ' '.join(item_categories)).lower()

        for gender_term in self.gender_map.keys():
            if gender_term in lookup_text:
                return self.gender_map[gender_term]

        return 'Unisex'

    def extract_price(self, response):
        raw_price = response.css('#___rc-p-dv-id::attr(value)').extract_first()
        return float(raw_price.replace(',', '')) * 100

    def extract_image_urls(self, item_detail):
        return [self.image_url_t.format(image_id['imageId']) for image_id in item_detail['items'][0]['images']]

    def extract_category(self, item_detail):
        return item_detail['categories']

    def extract_description(self, item_detail):
        return item_detail['description'].split("\n")

    def extract_skus(self, response):
        raw_skus = json.loads(response.css('script::text').re_first(r'var skuJson_0 = (.+]});'))
        skus = []

        for sku_json in raw_skus['skus']:
            sku = {
                "colour": sku_json.get("dimensions").get("Cor"),
                "price": sku_json.get("bestPrice"),
                "currency": "BRL",
                "size": sku_json.get("dimensions").get("Tamanho"),
                "sku_id": sku_json.get("sku")
            }

            if not sku_json.get("available"):
                sku["out_of_stock"] = True

            if sku_json.get("listPrice") > 0:
                sku["previous_prices"] = [sku_json.get("listPrice")]

            skus.append(sku)

        return skus
