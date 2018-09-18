import scrapy
import logging
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class ProductsBasicSpider(CrawlSpider):
    """Basic class inheriting from CrawlSpider"""
    name = 'products_all_colors'
    allowed_domains = ['orsay.com']
    BASE_URL = 'http://www.orsay.com/de-de/'
    start_urls = [BASE_URL]
    rules = (
        Rule(
            LinkExtractor(allow=(r'/produkte/[a-z\-]*/$'), 
                tags=('a','area'), 
                attrs=('href',)),
            callback='parse_products',
            follow=False
            ),
    )
    PAGE_SIZE = 72
    total_products_count = 0
    retailer_sku_set = set()

    def parse_products(self, response):
        """This method parses the products one by one on the products page"""
        products_list = LinkExtractor(allow=(r'/de-de/.*[0-9-]{12}\.html$'),
                           tags=('a','area'),
                           attrs=('href')
                          ).extract_links(response)
        # products_list = response.xpath('//a[contains(@class, "thumb-link")]/@href').extract()

        products_list_final = response.meta.get('products_list')
        if not products_list_final:
            products_list_final = list()
        for i in products_list:
            if not i.url[-17:-11] in self.retailer_sku_set:
                products_list_final.append(i.url)
                self.retailer_sku_set.add(i.url[-17:-11])
            # products_list_final.extend(products_list)
        self.log(len(products_list_final))

        if response.xpath('//div[contains(@class, "load-more-wrapper")]\
                           /button[contains(@class,"js-next-load")]').extract():
            url_split = response.url.split('?sz=')
            if len(url_split) == 1:
                next_products = url_split[0] + '?sz=144'
            else:
                count = int(url_split[-1]) + 72
                next_products = url_split[0] + '?sz=' + str(count)
            req = scrapy.Request(url=next_products, callback=self.parse_products, dont_filter=True)
            req.meta['products_list'] = products_list_final
            yield req
        else:
            for link in products_list_final:
                link = response.urljoin(link)
                # self.total_products_count += 1
                self.log(str(self.total_products_count) + " " + link)
                details_request = scrapy.Request(url=link, callback=self.parse_details, dont_filter=True)
                details_request.meta['origin_link'] = link
                yield details_request


    def parse_details(self, response):
        """This parses the product details from the individual product page"""

        product_attributes = self.json_get_attributes(response)     # Only color and size details
        product_details = self.json_get_details(response)           # Major other details

        color_links_list = response.xpath('//ul[contains(@class, \
                                        "swatches color")]//a/@href').extract()
        
        if response.meta.get('origin_link') == response.url:
            if response.url in color_links_list:
                color_links_list.remove(response.url)
            item = {
                'retailer_sku': product_details['idListRef6'],
                'brand': 'Orsay',
                'care': self.get_care(response),
                'category': product_details['categoryName'],
                'description': self.get_description(response),
                'gender': 'female',
                'name': product_details['name'],
                'img_urls': self.get_img_urls(response),
                'skus': self.get_skus(response, product_details, product_attributes),
                'url': response.url
            }
            if len(color_links_list):
                color_url = color_links_list.pop()
                req = scrapy.Request(url=color_url, callback=self.get_colors, dont_filter=True)
                req.meta['item'] = item
                req.meta['color_links'] = color_links_list
                yield req
            else:
                yield item
        else:
            self.log('ERRRORRRRRRR: \n' + response.meta['origin_link'])

    def get_colors(self, response):
        #self.log('\n' + 'in getting other colors')

        item = response.meta['item']
        color_links_list = response.meta['color_links']
        
        product_attributes = self.json_get_attributes(response)
        if product_attributes is None:                # Broken color link
            self.log('broken link')
            if len(color_links_list):
                color_url = color_links_list.pop()
                req = scrapy.Request(url=color_url, callback=self.get_colors, dont_filter=True)
                req.meta['item'] = item
                req.meta['color_links'] = color_links_list
                yield req
        else:
            self.log('correct link')
            product_details = self.json_get_details(response)
            img_url = self.get_img_urls(response)
            item['img_urls'].append(img_url)
            item['skus'].update(self.get_skus(response, product_details, product_attributes))
            # updates the skus dictionary with the skus from this color page

            if len(color_links_list):
                color_url = color_links_list.pop()
                req = scrapy.Request(url=color_url, callback=self.get_colors, dont_filter=True)
                req.meta['item'] = item
                req.meta['color_links'] = color_links_list
                yield req
            else:
                yield item
            

    def json_get_attributes(self, response):
        data_attributes = response.xpath('//div[contains(@class, \
                                          "product-variations")]/@data-attributes').extract_first()
        if data_attributes:
            return json.loads(data_attributes)
        else:
            return None

    def json_get_details(self, response):
        product_details = response.xpath('//form[contains(@class, \
                                          "pdpForm")]/@data-product-details').extract_first()
        if product_details:
            return json.loads(product_details)
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

    def get_available_sizes(self, response):
        size_list = response.xpath('//ul[contains(@class, "swatches size")]/li[contains(concat(" ", @class), " selectable")]/a/text()').extract()
        if not size_list:
            size_list = response.xpath('//ul[contains(@class, "swatches shoeSize")]/li[contains(concat(" ", @class), " selectable")]/a/text()').extract()
        return size_list

    def get_unavailable_sizes(self, response):
        size_list = response.xpath('//ul[contains(@class, "swatches size")] \
                                    /li[contains(concat(" ", @class), " unselectable")] \
                                    /a/text()'
                                  ).extract()
        if not size_list:
            size_list = response.xpath('//ul[contains(@class, "swatches size")]/li[contains(concat(" ", @class), " unselectable")]/a/text()').extract()
        return size_list

    def get_skus(self, response, product_details, product_attributes):
        """Creates and returns the sku for a product"""
        skus = dict()
        if not product_attributes:            # Broken color link first in links
            return skus
        color_id = product_attributes['color']['value']
        color = product_details['color']
        size_list = self.get_available_sizes(response)
        currency = product_details['currency_code']
        price = product_details['grossPrice']
        unavailable_sizes = self.get_unavailable_sizes(response)

        if not size_list:
            sku_name = color_id
            sku = {
                'colour': color,
                'currency': currency,
                'price': price,
            }
            skus[sku_name] = sku
        else:
            for size in size_list:                     # Create an sku for every size and color
                size = size.replace('\n','')
                sku_name = color_id + '_' + size
                sku = {
                    'colour': color,
                    'currency': currency,
                    'price': price,
                    'size': size,
                }
                skus[sku_name] = sku
        if unavailable_sizes:
            for size in unavailable_sizes:                     # Create an sku for every size and color
                size = size.replace('\n','')
                sku_name = color_id + '_' + size
                sku = {
                    'colour': color,
                    'currency': currency,
                    'price': price,
                    'size': size,
                    'out_of_stock': True,
                }
                skus[sku_name] = sku
        return skus
