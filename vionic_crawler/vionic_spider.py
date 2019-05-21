import json

from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:
    retailer = 'vionic-ca'
    market = 'CA'
    default_brand = 'Vionic'

    allowed_domains = ['vionicshoes.ca']
    start_urls = ['https://vionicshoes.ca/']


class VionicParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    description_x = '(//div[@class="product-accordion__content"])[1]//text()'
    care_x = '(//div[@class="product-accordion__content"])[2]//text()'

    def parse(self, response):
        raw_variants = self.variants(response)

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(raw_variants)
        garment['skus'] = self.skus(response, raw_variants)
        return garment

    def product_id(self, response):
        return clean(response.css('.product-form::attr(data-product-id)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-title.small--hide ::text'))[0]

    def product_category(self, response):
        return clean([t[0] for t in response.meta.get('trail', [])])

    def image_urls(self, response):
        urls = clean(response.css('.product__slides__item a::attr(href)'))
        return [response.urljoin(url) for url in urls]

    def variants(self, response):
        xpath = '//script[contains(., "window.products.")]/text()'
        script = response.xpath(xpath).re_first('({.*})')
        return json.loads(script)

    def product_gender(self, raw_variants):
        soup = raw_variants['type']
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def skus(self, response, raw_variants):
        skus = {}
        variants = raw_variants['variants']

        price = variants[0]['price']
        previous_price = variants[0]['compare_at_price']
        currency = clean(response.css('#in-context-paypal-metadata::attr(data-currency)'))

        common_sku = self.product_pricing_common(None, money_strs=[price, previous_price, currency])

        for variant in variants:
            sku = common_sku.copy()
            sku['colour'] = variant['option1']
            sku['size'] = variant['option2']

            skus[variant['sku']] = sku

        return skus


class VionicCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = VionicParseSpider()

    listings_css = [
        '.megamenu-list-border > ul',
        '.spinner'
    ]
    products_css = [
        '.name'
    ]

    listings_deny_r = [
        '/gift-card',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=listings_deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

