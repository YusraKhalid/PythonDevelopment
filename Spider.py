from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem

class LemkusSpider(CrawlSpider):

    name = "Lemkus"
    start_urls = ['https://www.jacklemkus.com/']
    pagging = [".clearfix.menu-simple-dropdown.menu-columns", ".next.i-next"]
    product_page = [".row.products-grid"]
    
    rules = (
        Rule(LinkExtractor(restrict_css = pagging)),
        Rule(LinkExtractor(restrict_css = product_page), callback = 'product_items'),
    )

    def product_items(self, response):

        product = StartItem()

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['gender'] = self.extract_gender(response)
        product['brand'] = self.extract_brand(response)
        product['url'] = response.url
        product['name'] = self.extract_name(response)
        product['description'] = self.extract_description(response)
        product['image_urls'] = self.extract_image_url(response)
        product['skus'] = self.extract_skus(response)

        yield product

    def extract_retailer_sku(self,response):        
        return response.css(".sku::text").extract_first()
        
    def extract_gender(self,response):
        return response.xpath('//th[contains(text(),"Gender")]/following-sibling::td/text()').extract_first()

    def extract_brand(self,response):
        return response.xpath('//th[contains(text(),"Item Brand")]/following-sibling::td/text()').extract_first()

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_description(self, response):
        return response.css(".std::text").extract_first("").strip()

    def extract_image_url(self, response):
        return  response.css(".hidden-xs img::attr(src)").extract()

    def extract_skus(self, response):

        skus = []

        price = response.css(".price::text").extract_first()
        currency = 'R'
        product_id = response.css(".product-data-mine::attr(data-confproductid)").extract_first()  
        size_label = response.css(".product-data-mine::attr(data-lookup)").extract()

        if size_label is not None:
            size_label =  eval(size_label[0])   

            for p_id, p_info in size_label.items():

                if p_info["stock_status"] is not 0:
                    sku = {
                        "price": price,
                        "currency": currency,
                        "sku-id": product_id,
                        "size": p_info["size"],
                        "quantity": p_info["qty"],
                        "id": p_info["id"]
                    }
                    skus.append(sku)
        
            return skus
        else:

            sku = {
                    "price": price,
                    "currency": currency,
                    "sku-id": product_id,
                    "size": None,
                    "quantity": None,
                    "id": None
                }

            return sku

