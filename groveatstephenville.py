import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveStephenville(BaseMixinPPE):
    name = property_slug = 'grove-at-stephenville'
    allowed_domains = [
        'groveatstephenville.prospectportal.com',
        'groveatstephenville.com'
    ]

    login_domain = 'https://groveatstephenville.prospectportal.com/'
    site_domain = 'http://groveatstephenville.com/'

    property_name = 'Grove at Stephenville'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveStephenville(PPBaseParseSpiderE, MixinGroveStephenville):
    name = MixinGroveStephenville.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveStephenville(MixinGroveStephenville, PPBaseCrawlSpiderE):
    name = MixinGroveStephenville.name + '-crawl'
    parse_spider = ParseSpiderGroveStephenville()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
