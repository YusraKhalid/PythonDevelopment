"""To scrape all the products from the website Orsay"""
# -*- coding: utf-8 -*-
import scrapy


class ProductsBasicSpider(scrapy.Spider):
    """Basic class inheriting from scrapy.spider"""
    name = 'products_basic'
    allowed_domains = ['orsay.com']
    BASE_URL = 'http://orsay.com/de-de/'
    start_urls = [BASE_URL]
    PAGE_SIZE = 72
    total_products_count = 0

    def parse(self, response):
        """The main method that is called on the start_urls"""
        products_link = self.BASE_URL + 'produkte/'
        yield scrapy.Request(url=products_link, callback=self.parse_products)

    def parse_products(self, response):
        """This method parses the products one by one on the products page"""
        if self.total_products_count == 0:
            total_products = response.xpath('//div[contains(@class, \
                "pagination-product-count")]/b/ \
                text()').extract_first()
            total_products = total_products.replace('.', '')
            self.total_products_count = int(total_products)
            self.items_viewed = 72

        products_list = response.xpath('//div[contains(@class, \
                                        "product-name")]/a/@href'
                                      ).extract()

        for product_link in products_list:
            product_link = response.urljoin(product_link)
            yield scrapy.Request(url=product_link, callback=self.parse_details)

        if self.items_viewed < self.total_products_count:
            self.items_viewed = self.items_viewed + self.PAGE_SIZE
            products_url = self.BASE_URL + 'produkte/?sz=' + str(self.items_viewed)
            self.log('Items viewed: ' + str(self.items_viewed))
            yield scrapy.Request(url=products_url, callback=self.parse_products)

    def parse_details(self, response):
        """This parses the product details from the individual product page"""

        yield{
            'brand': 'Orsay',
            'care': self.get_care(response),
            'category': self.get_category(response),
            'description': self.get_description(response),
            'gender': 'female',
            'img_url': self.get_img_urls(response),
            'name': self.get_name(response),
            'retailer_sku': self.get_retailer_sku(response),
            'skus': self.get_skus(response),
            'url': response.url
        }

    def get_availability(self, response):
        """To see if the item is in stock"""
        availability = response.xpath('//p[contains(@class, \
                                       "in-stock-msg")]/text()'
                                     ).extract_first()
        #response.css("p.in-stock-msg :: text").extract()
        if not availability == 'Auf Lager':
            return 'True'
        else:
            return None

    def get_care(self, response):
        """Xpath getter for care"""
        care_list = response.xpath('//div[contains(@class, \
                                    "product-material product-info-block" \
                                    )]/p/text()').extract()
        #response.css("div.product-material.product-info-block > p :: text").extract()
        care = ''
        for i in care_list:
            care = care + i
        return care

    def get_category(self, response):
        """Xpath getter for category"""
        return response.xpath('//a[contains(@class, \
                               "breadcrumb-element-link")] \
                               /span/text()')[-1].extract()
        #response.css("a.breadcrumb-element-link > span :: text")[-1].extract()

    def get_description(self, response):
        """Xpath getter for description"""
        return response.xpath('//div[contains(@class, \
                               "js-collapsible collapsible-block") \
                               ]/text()')[-4].extract()
        #response.css("div.collapsible-block > span :: text")[-4].extract()

    def get_img_urls(self, response):
        """Xpath getter for image urls"""
        return response.xpath('//img[contains(@class, \
                               "productthumbnail")]/@src').extract()
        #response.css("img.productthumbnail :: attr(src)").extract()

    def get_name(self, response):
        """Xpath getter for name"""
        return response.xpath('//span[contains(@class, \
                               "breadcrumb-element")]/text()'
                             ).extract_first()
        #response.css("span.breadcrumb-element :: text").extract_first()

    def get_retailer_sku(self, response):
        """Xpath getter for reatiler sku"""
        sku_str = response.xpath('//div[contains(@class, \
                                  "product-sku")]/text()')[1].extract()
        #response.css("div.product-sku :: text")[1].extract()
        retailer_sku = sku_str.split(' ')[-1]
        return retailer_sku

    def get_price(self, response):
        """Xpath getter for price"""
        price_span = response.xpath('//span[contains(@class, \
                                     "price-sales")]/text()'
                                   ).extract_first()
        #response.css("span.price-sales :: text").extract_first()
        price = price_span.split(' ')[0][1:]
        return price

    def get_currency(self, response):
        """Xpath getter for currency"""
        return response.xpath('//div[contains(@class, \
                               "locale-item current")]//span[contains \
                               (@class, "country-currency")]/text()'
                             ).extract_first()
        #response.css('div.locale-item.current span.country-currency :: text').extract_first()

    def get_color_and_size(self, response):
        """Xpath getter for color and size"""
        return response.xpath('//span[contains(@class, \
                               "selected-value")]/text()').extract()
        #response.css('span.selected-value :: text').extract()

    def get_skus(self, response):
        """Creates and returns the sku for a product"""
        color_and_size = self.get_color_and_size(response)
        size = ''
        color = color_and_size[0]
        if len(color_and_size) == 2:
            size = color_and_size[1]
        sku_name = color + '_' + size

        sku_selected = {
            'colour': color,
            'currency': self.get_currency(response),
            'price': self.get_price(response),
            'out_of_stock': self.get_availability(response),
            'size': size,
        }

        skus = {
            sku_name: sku_selected
        }
        return skus
