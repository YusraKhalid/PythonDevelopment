import scrapy


class NwhSpider(scrapy.Spider):
    name = 'NwhSpider'
    base_url = 'https://www.nwh.org/find-a-doctor/find-a-doctor-home'
    start_urls = [base_url]
    allowed_domains = ['www.nwh.org']

    def get_parameters(self, response):
        specialty = response.css('#ctl00_cphContent_ctl01_ddlResultsSpecialties > option::attr(value)').extract_first()
        generator = response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').extract_first()
        state = response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()
        results_per_page = response.css('style::text').re_first("\d{5}")
        target = response.css('#ctl00_cphContent_ctl01_lnkSeachResults::attr(href)').extract()
        target_param = target[0][25:-5]
        data = {
            'ctl00$cphContent$ctl01$ddlResultsSpecialties': specialty,
            '__VIEWSTATE': state,
            '__VIEWSTATEGENERATOR': generator,
            '__EVENTTARGET': target_param,
            'ctl00$cphContent$ctl01$ddlResultsPerPage': results_per_page,
        }
        return data

    def parse(self, response):
        _params = self.get_parameters(response)
        yield scrapy.FormRequest(url=u'https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847',
                                 formdata=_params, method='POST', callback=self.parse_doctors)

    def parse_doctors(self, response):
        doc_params = self.get_parameters(response)
        for doctors in response.css('a.link-name-profile'):
            target_doc = doctors.css('a.link-name-profile::attr(href)').extract()
            target_doc_param = target_doc[0][25:-5]
            doc_params.update({
                '__EVENTTARGET': target_doc_param,
            })
            yield scrapy.FormRequest(url=u'https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847',
                                     formdata=doc_params, method='POST', callback=self.parse_profile)

    def parse_profile(self, response):
        for information in response.css('div.light'):
            item = {
                'full-name': information.xpath(
                    '//*[@class="header-doctor-name"]/text()').extract_first(),
                'specialty': information.xpath(
                    '//*[@class="pnl-doctor-specialty"]//h2/text()').extract_first().strip().split(','),
                'year-joined': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlYearJoined"]//h2/text()').re_first("\d{4}"),
                'med-school': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlMedicalSchool"]//ul//li/text()').extract_first(),
                'affiliation': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlBoardOfCertifications"]//ul//li/text()').extract_first(),
                'fellowship': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlFellowship"]//ul//li/text()').extract_first(),
                'internship': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlInternship"]//ul//li/text()').extract_first(),
                'residency': information.xpath(
                    '//*[@id="ctl00_cphContent_ctl01_pnlResidency"]//ul//li/text()').extract_first(),
                'address': information.css('.doctor-contact-location-address>a::text').extract(),
                'img-url': response.urljoin(information.css('.pnl-doctor-image>img::attr(src)').extract_first()),
                'source-url': response.request.url,
                'contact': {
                    'phone': information.css('.pnl-doctor-contact-phone>a>span::text').extract_first(),
                    'fax': information.xpath('//*[@id="ctl00_cphContent_ctl01_lblDocContactFax"]/text()').extract_first(),
                }
            }
            yield item
