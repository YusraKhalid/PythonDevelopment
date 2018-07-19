import requests
from parsel import Selector
import asyncio
from urllib.parse import urljoin, urlparse


class Crawler:
    def __init__(self, url, workers=1, download_delay=0, max_urls=0):
        self._total_data = 0
        self._url = f'{urlparse(url).scheme}://{urlparse(url).netloc}'
        self._pending_urls = {self._url}
        self._download_delay = download_delay
        self._max_urls = max_urls
        self._seen_urls = set()
        self._in_progress = 0
        self._loop = asyncio.get_event_loop()

    def _find_urls(self, html):
        found_urls = set()
        selector = Selector(html)
        for anchor in selector.css('a::attr(href)').extract():
            url = urljoin(self._url, anchor)
            if url not in self._seen_urls and url.startswith(self._url):
                found_urls.add(url)
        return found_urls

    async def _request(self, url):
        print(self._in_progress)
        future = self._loop.run_in_executor(None, requests.get, url)
        response = await future
        html = response.text
        print(url)
        self._total_data = self._total_data + len(str(html))
        self._pending_urls |= self._find_urls(str(html))
        self._in_progress -= 1

    async def crawl(self):
        while self._pending_urls or self._in_progress:
            if self._pending_urls:
                url = self._pending_urls.pop()
                if len(self._seen_urls) < self._max_urls or self._max_urls == 0:
                    asyncio.sleep(self._download_delay)
                    self._seen_urls.add(url)
                    self._in_progress += 1
                    await self._request(url)
                    print(url)
        return self._total_data, len(self._seen_urls)
