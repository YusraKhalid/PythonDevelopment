import re
import json
from urllib.parse import unquote

from scrapy import Selector
from scrapy.spiders import Spider
from scrapy.http import Request

from crawler_tasks.items import PhiluCourse


class PhiluSpider(Spider):
    name = 'philu'
    allowed_domains = [
        'novoed.com', 'cloudfront.net',
        'philanthropyuniversity.novoed.com'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler_tasks.pipelines.PhiluItemPipeline': 1,
            'crawler_tasks.pipelines.PhiluFilePipeline': 2,
        },
        'FILES_STORE': 'philu_files',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        'RETRY_TIMES': 1
    }

    def new_course_module(self):
        return {
            'units': [],
            'module_description': [],
            'toc_list': []
        }

    def new_module_unit(self):
        return {
            'unit_audio': [],
            'unit_video': [],
            'unit_content': []
        }

    def csrf_token(self, response):
        for cookie in response.headers.getlist('Set-Cookie'):
            match = re.match('XSRF-TOKEN=(.*);', cookie.decode())
            if match:
                return unquote(match.group(1))

    def strip_text_items(self, items):
        return [i.strip() for i in items if i.strip()]

    def __init__(self):
        super().__init__()
        self.email = 'muhammad.zeeshan@arbisoft.com'
        self.password = 'CfR-c9C-Jh8-B7o'

    def start_requests(self):
        url = 'https://app.novoed.com/my_account.json'
        meta = {
            'handle_httpstatus_list': [401],
            'dont_cache': True
        }
        return [Request(url, callback=self.sign_in_request, meta=meta)]

    def sign_in_request(self, response):
        payload = {
            'user': {
                'email': self.email,
                'password': self.password
            },
            'catalog_id': 'philanthropy-initiative'
        }
        url = 'https://app.novoed.com/users/sign_in.json'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-XSRF-TOKEN': self.csrf_token(response),
            'dont_cache': True
        }
        return Request(
            url, callback=self.request_home_page, method='POST',
            body=json.dumps(payload), headers=headers)

    def request_home_page(self, response):
        url = 'https://philanthropyuniversity.novoed.com/philanthropy-initiative/oe/#!/home'
        meta = {
            'sign_in_response': response
        }
        return Request(url, meta=meta, callback=self.courses_menu)

    def courses_menu(self, response):
        course_urls = response.css('.courses_menu ::attr(href)').extract()
        for url in course_urls:
            yield Request(url, meta=response.meta, callback=self.parse_course)

    def parse_course(self, response):
        course = PhiluCourse()
        course['lectures'] = []
        course['assignments'] = []
        course['url'] = response.url
        course['course_title'] = response.css(
            '.program-breadcrumbs a:not([href])::text'
        ).extract_first().strip()

        raw_text = response.css(
            '.onboarding-expandable ::attr("compile-once")'
        ).extract_first()
        selector = Selector(text=raw_text, type='html')

        course['course_welcome_text'] = self.strip_text_items(
            selector.css('::text').extract()
        )

        course_img_url = selector.css('::attr(src)').extract_first()
        request_queue = [
            Request(course_img_url, callback=self.redirected_course_img_url),
            self.request_lectures_section(response),
            self.request_assignments_section(response),
            self.request_course_announcements(response)
        ]
        course['meta'] = {
            'request_queue': request_queue
        }
        return self.next_request_or_course(course)

    def redirected_course_img_url(self, response):
        course = response.meta['course']
        course['course_image'] = response.url
        return self.next_request_or_course(course)

    def request_lectures_section(self, response):
        lectures_section_url =\
            response.css('.lectures ::attr(href)').extract_first()
        url = response.urljoin(lectures_section_url)
        return Request(url, callback=self.request_course_modules)

    def request_assignments_section(self, response):
        assignment_section_url =\
            response.css('.assignments ::attr(href)').extract_first()
        url = response.urljoin(assignment_section_url)
        return Request(url, callback=self.request_course_assignments)

    def request_course_announcements(self, response):
        url = response.urljoin('announcements')
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, callback=self.parse_instructor_message)

    def request_course_modules(self, response):
        module_urls = response.css('.lecture-page-navigation')[0]\
            .css('::attr(href)').extract()

        module_requests = []
        for module_url in module_urls:
            url = response.urljoin(module_url)
            module_requests.append(
                Request(url, callback=self.parse_course_module, dont_filter=True)
            )

        course = response.meta['course']
        course['meta']['request_queue'] += module_requests
        return self.next_request_or_course(course)

    def parse_course_module(self, response):
        selector = response.css('#lecture-components-list')
        nodes = selector.css(
            '[href^="#step"], a[href*="soundcloud"], img[src],'
            '[class=muted], [class="title-video-text"],'
            ':not(h2):not([class="muted"]):not([href^="#step"])::text'
        )
        module = self.parse_html_nodes(nodes, selector, response)

        course = response.meta['course']
        course['lectures'].append(module)

        module_index = course['lectures'].index(module)
        course['meta']['request_queue'] +=\
            self.module_transcript_requests(module, module_index)

        image_url = module.get('module_image')
        if image_url:
            meta = {
                'module_index': module_index
            }
            course['meta']['request_queue'] += [
                # a course will not be scrapped if its module
                # image gets filtered by duplicate request filter.
                Request(image_url, meta=meta, dont_filter=True,
                        callback=self.redirected_module_img_url)
            ]

        return self.next_request_or_course(course)

    def redirected_module_img_url(self, response):
        course = response.meta['course']
        module_index = response.meta['module_index']
        course['lectures'][module_index]['module_image'] = response.url
        return self.next_request_or_course(course)

    def module_transcript_requests(self, module, module_index):
        transcript_requests = []
        for unit_index, unit in enumerate(module['units']):
            for video_index, video in enumerate(unit['unit_video']):
                url = video['transcript']
                meta = {
                    'module_index': module_index,
                    'unit_index': unit_index,
                    'video_index': video_index,
                }
                transcript_requests.append(
                    Request(url, meta=meta, callback=self.redirected_module_transcript_url)
                )

        return transcript_requests

    def redirected_module_transcript_url(self, response):
        course = response.meta['course']
        module_index = response.meta['module_index']
        unit_index = response.meta['unit_index']
        video_index = response.meta['video_index']

        units = course['lectures'][module_index]['units']
        video = units[unit_index]['unit_video'][video_index]
        video['transcript'] = response.url

        return self.next_request_or_course(course)

    def module_title(self, response, selector):
        title = selector.css('h2::text').extract_first()
        if not title:
            return response.css('h2::text').extract_first()
        return title

    def parse_html_nodes(self, nodes, selector, response):
        module = self.new_course_module()
        module['module_title'] = self.module_title(response, selector)

        unit = None
        module_desc_complete = False
        for node in nodes:
            text = node.extract().strip()
            if not text or re.match('\$\(', text):
                continue

            if (self.node_is_toc_title(node, module)
                or self.node_is_audio_link(node, unit)
                or self.node_is_an_image(node, module, unit, module_desc_complete)
                or self.node_is_a_video(node, unit, selector)
            ):
                pass

            elif self.node_is_unit_title(node, module, unit):
                unit = self.new_module_unit()
                unit['unit_title'] = text

            elif self.node_is_toc_item(node, module):
                module_desc_complete = True

            elif not module_desc_complete:
                module['module_description'].append(text)

            else:
                unit['unit_content'].append(text)

        # append last unit to module, if any
        if unit:
            module['units'].append(unit)

        return module

    def node_is_toc_title(self, node, module):
        if node.css('[class="muted"]'):
            module['toc_title'] = node.css('::text').extract()
            return True

    def node_is_audio_link(self, node, unit):
        if node.css('a[href*="soundcloud"]'):
            unit['unit_audio'].append(
                node.css('::attr(href)').extract_first()
            )
            return True

    def node_is_an_image(self, node, module, unit, module_desc_complete):
        if node.css('img[src]'):
            image_url = node.css('::attr(src)').extract_first()
            if 'ajax-loader' in image_url:
                return True

            if not module_desc_complete:
                module['module_image'] = image_url
            elif not node.css('[class="lecture-video-thumb"]'):
                unit['unit_image'] = image_url
            return True

    def node_is_a_video(self, node, unit, selector):
        if node.css('[class="title-video-text"]'):
            video_name = node.css('::text').extract_first().strip()
            video_id = node.css('::attr(id)').re('\d+')[0]

            elem_css = '[id="video-download-link-{}"]::attr(href)'.format(video_id)
            video_url = selector.css(elem_css).extract_first()

            elem_css = '[id="transcript-link-{}"]::attr(href)'.format(video_id)
            transcript_url = selector.css(elem_css).extract_first()

            unit['unit_video'].append({
                'name': video_name,
                'url': video_url,
                'transcript': transcript_url
            })
            return True

    def node_is_unit_title(self, node, module, unit):
        if node.re('Step \d+:'):
            if unit:
                module['units'].append(unit)
            return True

    def node_is_toc_item(self, node, module):
        if node.css('[href^="#step"]'):
            module['toc_list'].append(
                node.css('::text').extract()
            )
            return True

    def request_course_assignments(self, response):
        assignment_urls = response.css('.exercise-table ::attr(href)').extract()

        assignment_requests = []
        for assignment_url in assignment_urls:
            url = response.urljoin(assignment_url)
            assignment_id = re.search('\d+$', assignment_url).group()
            elem_css = '[id="exercise-{}-title"]::text'.format(assignment_id)
            meta = {
                'assignment_title': response.css(elem_css).extract_first().strip()
            }
            assignment_requests.append(
                Request(url, meta=meta, callback=self.parse_course_assignment)
            )

        course = response.meta['course']
        course['meta']['request_queue'] += assignment_requests
        return self.next_request_or_course(course)

    def parse_course_assignment(self, response):
        raw_text = response.css('.expandable ::attr(compile-once)').extract_first()
        if not raw_text:
            raw_text = response.css('.expandable').extract_first()

        selector = Selector(text=raw_text, type='html')
        content = selector.css('::text').extract()
        content = self.strip_text_items(content)

        course = response.meta['course']
        course['assignments'].append({
            'url': response.url,
            'assignment_title': response.meta['assignment_title'],
            'assignment_content': content
        })
        return self.next_request_or_course(course)

    def parse_instructor_message(self, response):
        result = json.loads(response.text)['result'][0]
        sel = Selector(text=result['description'], type='html')
        texts = sel.css('::text').extract()

        course = response.meta['course']
        course['instructor_msg_title'] = result['title']
        course['instructor_msg_content'] = self.strip_text_items(texts)

        return self.next_request_or_course(course)

    def next_request_or_course(self, course):
        request_queue = course['meta']['request_queue']
        if request_queue:
            request = request_queue.pop()
            request.meta['course'] = course
            request.priority = 1
            return request

        del course['meta']
        return course
