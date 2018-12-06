# coding: utf-8
"""
Scrapy spider for stylerunner.
@author: Adeel Ehsan
"""
import copy
import json

from scrapy.http.request import Request
from scrapy.selector import Selector

from scrapyproduct.items import ProductItem, SizeItem
from scrapyproduct.spiderlib import SSBaseSpider
from scrapyproduct.toolbox import selective_copy


class StyleRunnerSpider(SSBaseSpider):
    """ Scrapy spider for stylerunner """

    name = 'stylerunner'
    long_name = 'stylerunner'
    base_url = 'http://www.stylerunner.com/'
    max_stock_level = 5000
    country_code = 'au'
    language_code = 'en'
    currency = 'AUD'
    auto_register = True
    version = '1.0.1'
    gst = 10
    seen_basesku = []

    item_details_url = "https://www.stylerunner.com/api/items?country=AU&currency=AUD&fieldset=details&include" \
                       "=facets&language=en&url={}"

    def start_requests(self):
        yield Request(
            url=self.base_url,
            callback=self.parse_homepage
        )

    def make_request(self, selectors, response):
        """
        make requests for category levels

        """
        category_level_label = [sel.xpath("./a/text()").extract_first('').strip() for sel in selectors]
        url = selectors[-1].xpath("./a/@href").extract_first()
        meta = copy.deepcopy(response.meta)
        meta['categories'] = category_level_label
        url = response.urljoin(url) + "?page=1"
        return Request(
            url=url,
            callback=self.extract_products,
            meta=meta,
        )

    def parse_homepage(self, response):
        """
        Parse categories level
        @url http://www.stylerunner.com/
        @returns requests 0 1000
        """

        for level1 in response.xpath("//ul[@class='header-menu-level1']/li")[1:]:
            yield self.make_request([level1], response)

            for level2 in level1.xpath("./ul/li/ul/li"):
                yield self.make_request([level1, level2], response)

                for level3 in level2.xpath(".//ul/li"):
                    yield self.make_request([level1, level2, level3], response)

    def extract_products(self, response):
        """
        Parse products
        @url http://www.stylerunner.com/shop/just-in/?limit=All%2C
        @returns requests 0 100
        """

        categories = response.meta.get('categories')
        for sel_product in response.xpath("//div[@class='facets-item-cell-grid']"):
            item = ProductItem()
            item_url = sel_product.xpath('.//meta/@content').extract_first()
            if "Gift" in item_url:
                continue

            item['title'] = sel_product.xpath("./div[2]/a[2]/span/text()").extract()[0].strip()
            item['url'] = response.urljoin(item_url)
            item['identifier'] = sel_product.css('::attr(data-sku)').extract_first('')
            item['referer_url'] = response.url
            item['category_names'] = categories
            item['country_code'] = self.country_code
            item['language_code'] = self.language_code
            item['currency'] = self.currency
            item['brand'] = sel_product.xpath("./div[2]/a[1]/span/text()").extract()[0].strip()

            mini_item = ProductItem()
            selective_copy(item, mini_item, [
                'language_code', 'identifier', 'category_names', 'language_code'])

            yield mini_item
            if item['identifier'] not in self.seen_basesku:
                self.seen_basesku.append(item['identifier'])
                yield Request(
                    url=self.item_details_url.format(item_url[1:]),
                    meta={'item': item},
                    callback=self.parse_detail
                )
        for req in self.parse_pagination(response):
            yield req

    def parse_pagination(self, response):
        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page:
            yield Request(
                url=next_page,
                callback=self.extract_products,
                meta=response.meta,
            )

    def parse_detail(self, response):
        """
        Parse detail product
        @url https://www.stylerunner.com/api/items?country=AU&currency=AUD&fieldset=details&language=en&url=producturl
        @returns items 0 1
        """
        item = response.meta.get('item', ProductItem())

        product = self.extract_json_details(response.text)
        if not product:
            return

        colors = self.extract_siblingcolors(product)

        item['base_sku'] = self.extract_base_sku(colors)
        item['description_text'] = self.extract_description(product)
        item['identifier'] = product.get('itemid', item['identifier'])

        final_item = copy.deepcopy(item)
        final_item['image_urls'] = [image.get('url', '') for image in product['itemimages_detail'].get('urls', [])]
        final_item['color_name'] = product.get('custitem_color_label', product.get('custitem_item_colour', ''))
        final_item['sku'] = final_item['identifier']
        final_item['use_size_level_prices'] = True
        self.extract_sizes(product, final_item)

        yield final_item

        for color_code in colors:
            temp_item = copy.deepcopy(item)
            temp_item['url'] = temp_item['url'].replace(final_item['identifier'], color_code)
            url = response.url.replace(final_item['identifier'], color_code)
            temp_item['identifier'] = color_code
            if temp_item['identifier'] not in self.seen_basesku:
                self.seen_basesku.append(temp_item['identifier'])
                yield Request(
                    url=url,
                    meta={'item': temp_item},
                    callback=self.parse_detail
                )

    def extract_siblingcolors(self, product):
        colors = [clr for clr in product['custitem_related_items'].split(', ') if clr != '&nbsp;']
        if colors:
            colors = [color.split(' : ')[1].split(' ')[0] for color in colors]
        colors = colors + [product.get('itemid')]

        return colors

    def extract_json_details(self, json_text):
        details = json.loads(json_text)
        product = details.get('items', [])
        if product:
            return product[0]
        return []

    def extract_description(self, product):
        description_details = product.get("storedetaileddescription")
        description_details = Selector(text=description_details).xpath("//li/text()").extract()
        description_details.append(product.get("storedescription"))
        return description_details

    def extract_base_sku(self, color_codes):
        if len(color_codes) == 1:
            code = color_codes[0]
            index = code.rfind('-')
            if index:
                code = code[:index + 1]
            return code

        i = 0
        match = True
        while i < len(color_codes[0]):
            base_sku = color_codes[0][i]
            for color in color_codes:
                if color[i] != base_sku:
                    match = False
                    break
            if not match:
                return color_codes[0][:i]
            i += 1
        return color_codes[0]

    def extract_sizes(self, product, item):
        item_price = self.add_gst(product['pricelevel7'])
        sizes = product['matrixchilditems_detail']

        for size in sizes:
            is_discounted, item_price, dis_price = self.extract_prices(item_price, size)
            size_item = SizeItem(
                size_name=size['custitem1'],
                size_identifier=size.get("itemid"),
                stock=size.get('quantityavailable', 0),
                size_original_price_text=item_price,
                size_current_price_text=dis_price if is_discounted else item_price,
            )
            item['size_infos'].append(size_item)

    def extract_prices(self, item_price, size):
        dis_price = self.add_gst(size['onlinecustomerprice_detail']['onlinecustomerprice'])
        is_discounted = True if dis_price < item_price else False
        item_price = "{0:.2f}".format(float(item_price))
        dis_price = "{0:.2f}".format(float(dis_price))

        return is_discounted, item_price, dis_price

    def add_gst(self, price):
        return price + (self.gst * (price / 100))
