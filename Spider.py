from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem

class FilaSpider(CrawlSpider):

    name = "Fila"
    currency = "Brazilian real"
    start_urls = ["https://www.fila.com.br/"]
    listings_css = [".nav-primary", ".carrossel-thumb"]
    products_css = [".category-products"]

    rules = (
        Rule(LinkExtractor(restrict_css = listings_css)),
        Rule(LinkExtractor(restrict_css = products_css), callback = "product_items"),
    )

    care_list = [
        "malha de poliamida","poliéster","algodão","pele","Cuidado","resistência","sentindo-me",
        "casual","confortável","couro","tecido","protecção","material","conforto","confortável"
    ]
    gender_list = ["Masculina","Masculino","mulheres","infantial","Infantil","Feminino","Feminina","FEMININO"]

    def product_items(self, response):

        product = StartItem()

        product["retailer_sku"] = self.extract_retailer_sku(response)
        product["brand"] = self.name
        product["url"] = response.url
        product["name"] = self.extract_name(response)
        product["gender"] = self.extract_gender(product["name"])
        product["image_urls"] = self.extract_image_url(response)
        product["skus"] = self.extract_skus(response)

        if product["skus"]:
            product["out_of_stock"] = False
        else:
            product["out_of_stock"] = True

        raw_description = self.extract_raw_description(response)
        product["care"] = self.extract_care(raw_description)
        product["description"] = self.extract_description(raw_description)

        yield product

    def extract_retailer_sku(self,response):
        return response.css(".wrap-sku small::text").extract_first()

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_gender(self,product_name):

        if product_name is None:
            return "unisex"

        for gender in self.gender_list:
            if gender in product_name:
                return gender
        return "unisex"

    def extract_image_url(self, response):
        return  response.css(".product-image-gallery img::attr(src)").extract()

    def extract_skus(self, response):

        skus = {}
    
        price = response.css(".price::text").extract_first()
        currency = self.currency
        sku_id = response.css(".no-display input[id = 'product-id']::attr(value)").extract_first()

        common_sku = {
            "price": price,
            "currency": currency,
            "sku_id" : sku_id
        }

        if response.css(".product-shop.unlogged div[class = 'unavailable-product-block']"):
            return None

        size_label =  response.css(".configurable-swatch-list.clearfix li::attr(data-size)").extract()

    
        if size_label is None:
            return common_sku
    
        if sku_id is None:
            common_sku["sku_id"] = size_label

        for index,size in enumerate(size_label): 

            sku = {
                "size": size
            }
            sku.update(common_sku)              
            skus[str(index)] = sku

        return skus

    def extract_raw_description(self, response):
        return response.css(".wrap-long-description p::text").extract()

    def extract_care(self,raw_description):
        
        if raw_description is  None:
            return None

        care = []

        for index, line in enumerate(raw_description):
            for care_words in self.care_list:

                if care_words in line:
                    care.append(line)
                    raw_description.pop(index)
                break

        return care

    def extract_description(self,description):

        if description :
            return description  

