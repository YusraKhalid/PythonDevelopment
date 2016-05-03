import json
from runningbare.items import RunningbareItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request


class RunningbareSpiderSpider(CrawlSpider):
    name = "runningbare_spider"
    allowed_domains = ["runningbare.com.au"]
    start_urls = [
        'http://www.runningbare.com.au/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//div[contains(@class,"col-md")]//ul/li']),
             callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_xpaths=['//div[contains(@class,"productName")]']),
             callback='parse_product_contents')
    )

    def parse_pagination(self, response):
        page = response.xpath('//li[@class="active"]/a/@data-page').extract()
        if page:
            category_id = response.xpath('//article/@data-categoryid')[0].extract()

            url = 'http://www.runningbare.com.au/product/list?categoryId={category_id}&page={page}&' \
                  'viewName=ProductListItems&ts=1462180932717'.format(category_id=category_id, page=page)
            request = Request(url, method="GET", callback=self.sku_details)
            yield request

    def parse_product_contents(self, response):
        item = RunningbareItem()
        item['spider_name'] = self.name
        item['retailer'] = 'runningbare-au'
        item['currency'] = 'AUD'
        item['market'] = 'AU'
        item['category'] = []
        item['retailer_sku'] = self.product_retailer_sku(response)
        item['price'] = self.product_price(response)
        item['description'] = self.product_description(response)
        item['url_original'] = response.url
        item['brand'] = 'Running Bare'
        item['image_urls'] = self.product_image_urls(response)
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(response)
        item['url'] = response.url
        item['gender'] = 'women'
        item['industry'] = None
        item['skus'] = {}
        item['requests'] = self.product_sku(response, item)

        if item['requests']:
            req = item['requests'].pop()
            req.meta['item'] = item
            yield req
        else:
            item.pop('requests')
            yield item

    def product_name(self, response):
        return response.xpath('//h1[@class="hidden-xs productTitle"]/text()').extract()

    def product_price(self, response):
        return response.xpath('//span[@class="is"]//text()').extract()[0][1:]

    def product_retailer_sku(self, response):
        return response.xpath('//p[@class="productCode"]/text()').extract()[0].split()[-1]

    def product_description(self, response):
        return [response.xpath('//div[contains(@id,"collapseOne")]/div/text()').extract()[0].strip()]

    def product_image_urls(self, response):
        return response.xpath('//li[@class="fullscreen-thumbnails"]/a/img/@src').extract()

    def product_sku(self, response, item):
        requests = []
        colours = response.xpath('//div[contains(@class,"selectcolour")]/@title').extract()
        size_chart = response.xpath('//div[contains(@class,"selectsize")]/@title').extract()

        for colour in colours:
            request_data = self.get_product_details(response, colour)
            url = 'http://www.runningbare.com.au/product/getskudata'
            header = {"Content-Type": "application/json; charset=UTF-8",
                      "X-Requested-With": "XMLHttpRequest"}
            requests += [Request(url, method="POST", body=request_data, callback=self.sku_details, headers=header,
                                 meta={'size_chart': size_chart, 'colour': colour})]
        return requests

    def product_care(self, response):
        return response.xpath('//em/descendant::text()').extract()

    def product_previous_price(self, response):
        if response.xpath('//span[contains(@class,"hidden")]/text()').extract():
            return ''
        else:
            return [response.xpath('//span[contains(@class,"was")]/text()').extract()[0][1:]]

    def get_product_details(self, response, colour):
        id = response.xpath('//input[@id="ProductId"]/@value').extract()[0]
        size = response.xpath('//div[contains(@class,"selectsize")]/@data-value').extract()[0]
        return json.dumps({"productId": id, "colour": colour, "size": "",
                           "skuSelections": [{"name": "Colour", "selectedValues": [colour]},
                                             {"name": "Size", "selectedValues": [size]}]})

    def sku_details(self, response):
        try:
            item = response.meta['item']
            size_chart = response.meta['size_chart']
            colour = response.meta['colour']
            sku_common = {}
            body = json.loads(response.body)
            price = round(body['data']['price'], 2)
            sku_common['colour'] = colour
            sku_common['currency'] = 'AUD'
            sku_common['price'] = price
            prev_price = round(body['data']['rrp'], 2)
            if price != prev_price:
                sku_common['previous_prices'] = [prev_price]

            product_data = body['data']['skuSelectorData'][0]['availableOptions']
            for size in size_chart:
                sku = {'size': size, 'colour': colour}
                sku.update(sku_common)
                if not any(oos['value'] == size.lower() for oos in product_data):
                    sku['out_of_stock'] = True
                item['skus'][colour + '_' + size] = sku

            if item['requests']:
                req = item['requests'].pop()
                req.meta['item'] = item
                yield req
            else:
                item.pop('requests')
                yield item
        except:
            yield
