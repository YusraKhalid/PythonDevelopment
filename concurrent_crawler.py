import argparse
import asyncio
from urllib import parse

import requests
import parsel


class AsyncSpider:

    def __init__(self, url, concurrent_req, delay, url_visit_limit):
        self.visited_urls = dict()
        self.pending_urls = set([url])
        self.concurrent_req = concurrent_req
        self.delay = delay
        self.url_visit_limit = url_visit_limit
        self.num_request_made = 0
        self.total_bytes_downloaded = 0

    async def extract_urls(self, semaphore):
        await semaphore.acquire()
        self.num_request_made += 1
        url = self.pending_urls.pop()
        response = requests.get(url)
        if response.status_code == 200 \
                and response.headers.get('content-length'):
            print(f'URL = {url}')
            self.visited_urls[url] = True
            self.total_bytes_downloaded += int(response.headers.get(
                'content-length'))
            selector = parsel.Selector(text=response.text)
            extracted_urls = selector.css("a::attr(href)").extract()
            for link in extracted_urls:
                link = parse.urljoin(url, link)
                if not self.visited_urls.get(link):
                    self.pending_urls.add(link)

        await asyncio.sleep(self.delay)
        semaphore.release()

    def crawl(self):

        semaphore = asyncio.BoundedSemaphore(self.concurrent_req)
        futures = []
        for i in range(self.url_visit_limit):
            futures.append(
                asyncio.ensure_future(
                    self.extract_urls(semaphore)))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))

    def spider_report(self):
        print(f"Total Bytes downloaded: {self.total_bytes_downloaded//1024}KB")
        print(f"Number of requests: {self.num_request_made}")
        print(f"Average page size :"
              f"{(self.total_bytes_downloaded//self.num_request_made)//1024}"
              f"KB")


def main():
    arg_parser = argparse.ArgumentParser(description='Process some date')
    arg_parser.add_argument('url', type=str,
                            help='Domain to crawl')
    arg_parser.add_argument('concurrent_request', type=int,
                            help='Number of Concurrent Request in one go')
    arg_parser.add_argument('delay', type=float,
                            help='Delay time each user gets')
    arg_parser.add_argument('total_urls', type=int,
                            help='Maximum number of urls to visit)')
    args = arg_parser.parse_args()
    sp = AsyncSpider(args.url, args.concurrent_request, args.delay,
                     args.total_urls)
    sp.crawl()
    sp.spider_report()


if __name__ == "__main__":
    main()
