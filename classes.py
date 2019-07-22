import asyncio
import aiohttp
import re
import parsel


class RecursiveCrawler:

    def __init__(self, url_list, concurrent_requests, url_limit, delay):

        self.urls = url_list
        self.concurrent_requests = concurrent_requests
        self.max_urls = url_limit
        self.download_delay = delay
        self.length = 0
        self.request_count = 0

    async def get_url_body(self, url):

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                length = len(html)
                self.length += length
                self.request_count += 1

        return html

    async def visited_urls(self, thread_id, work_queue):

        while not work_queue.empty():
            current_url = await work_queue.get()

            try:
                await self.get_results(current_url, thread_id)
                await asyncio.sleep(self.download_delay)

            except Exception as e:
                await asyncio.sleep(self.download_delay)

    async def get_results(self, url, thread_id):

        if self.request_count <= self.max_urls:
            html = await self.get_url_body(url)
            self.__get_urls_html(html)
            return 'Completed'

    def __get_urls_html(self, html):

        select = parsel.Selector(text=html)
        divs = select.xpath('//div')
        divs = divs.xpath('.//p')
        page_url_list = divs.css('a::attr(href)').extract()
        for urls in page_url_list:
            if re.match('http', str(urls)):
                self.urls.append(urls)

    def event_loop(self):

        while self.max_urls > self.request_count:
            queue = asyncio.Queue()
            [queue.put_nowait(url) for url in self.urls[self.request_count:self.max_urls]]
            loop = asyncio.get_event_loop()
            tasks = [self.visited_urls(thread_id, queue) for thread_id in range(self.concurrent_requests)]
            loop.run_until_complete(asyncio.wait(tasks))

