import os

from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint


class ColorFilter(RFPDupeFilter):
    def __getid(self, url):
        return url

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if '.html' in fp:
            fp = fp.split('?')[0]
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
