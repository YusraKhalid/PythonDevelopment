import re
import json

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ullapopken.spiders.ullapopken_parser import UllapopkenParser


class UllapopkenCrawler(CrawlSpider, UllapopkenParser):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    name = 'ullapopken'
    start_urls = ["https://www.ullapopken.de/"]

    top_navigation = '.top_level_nav'
    category_navigation = '.toplevel > .nav_content'
    denied_top_nav = '.*sale.*'

    rules = (Rule(LinkExtractor(restrict_css=top_navigation, deny=denied_top_nav),
                  follow=True),
             Rule(LinkExtractor(restrict_css=category_navigation),
                  callback='parse_category_parameters'))

    article_url_t = 'https://www.ullapopken.de/api/res/article/{}'
    category_url_t = 'https://www.ullapopken.de/api/res/category/articles/language/de/' \
                     'size/60/page/{}/category/{}/grouping/{}/filter/_/sort/normal/fs/_'

    def parse_category_parameters(self, response):
        category = response.css('#paging::attr(data-category)').extract_first()
        grouping = response.css('#paging::attr(data-grouping)').extract_first()

        category_request = self.category_request(category, grouping)
        category_request.meta['categories'] = self.categories(response)

        return category_request

    def parse_category(self, response):
        categories = response.meta.get('categories')
        response_json = json.loads(response.text)

        items = response_json['results']
        yield from self.item_requests(items, categories)

        return self.pagination_requests(response_json['pagination'], response.url, categories)

    def category_request(self, category, grouping, page=1):
        url = self.category_url_t.format(page, category, grouping)
        return Request(url=url, callback=self.parse_category)

    def pagination_requests(self, pagination, url, categories):
        if pagination['currentPage'] != 0:
            return

        category = re.findall('category.*category/(.+)/grouping', url)[0]
        grouping = re.findall('grouping/(.+)/filter', url)[0]

        for page_number in range(2, pagination['numberOfPages'] + 1):
            category_request = self.category_request(category, grouping, page_number)
            category_request.meta['categories'] = categories
            yield category_request

    def item_requests(self, items, categories):
        item_requests = []

        for item in items:
            item_request = Request(url=self.article_url_t.format(item['code']), callback=self.parse_item)
            item_request.meta['categories'] = categories
            item_request.meta['variants'] = self.variants_codes(item)
            item_requests.append(item_request)

        return item_requests

    @staticmethod
    def variants_codes(item):
        variants = item['variantsArticlenumbers']
        variants.remove(item['code'])

        return variants

    @staticmethod
    def categories(response):
        return response.css('.active > .nav_content a::text').extract()