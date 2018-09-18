# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor

class LnkextSpider(scrapy.Spider):
    name = 'lnkext'
    allowed_domains = ['www.orsay.com/de-de']
    start_urls = ['http://www.orsay.com/de-de/']

    def parse(self, response):
        lx = LinkExtractor(allow=(r'/produkte/'),tags=('a', 'area'), attrs=('href', )).extract_links(response)
        for i in lx:
            self.log(i.url)
            
