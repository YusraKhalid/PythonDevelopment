# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from operator import attrgetter

class RequiredProductFields(object):
    required_fields = ['name', 'retailer_sku', 'lang', 'category', 'brand', 'url',
                       'description', 'care', 'image_urls', 'skus']

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem(f"Missing field: {field} in {item}")
        return item

class SetItemPrice(object):
    def process_item(self, item, spider):
        item['skus'] = [dict(sku, id=id) for (id, sku) in item['skus'].items()]
        item['price'] = min([x['price'] for x in item['skus']])
        item['currency'] = item['skus'][0]['currency']
        return item

