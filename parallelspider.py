import requests
from parsel import Selector
import asyncio
import concurrent.futures

class ParallelSpider:

    def __init__(self, base_url, parallel_requests, download_delay, max_urls):
        self.base_url = base_url
        self.parallel_requests = parallel_requests
        self.download_delay = download_delay
        self.max_urls = max_urls
        self.extracted_urls = []
        self.total_bytes = 0

    def get_urls(self):

        response = requests.get(self.base_url)
        if response.status_code == requests.codes.ok:
            selector = Selector(text=response.text)
            urls = selector.xpath('//a/@href').getall()

            self.extracted_urls = [url for url in urls if url.startswith("http")]
            if len(self.extracted_urls) < self.max_urls:
                self.max_urls = len(self.extracted_urls)

            if self.max_urls < self.parallel_requests:
                self.parallel_requests = self.max_urls
        else:
            response.raise_for_status()

    def get_page_size(self, counter):

        response = requests.get(self.extracted_urls[counter], timeout=30)
        if response.status_code == requests.codes.ok:
            page_size = response.headers.get('content-length')
            if page_size:
                return int(page_size)
        return 0

    async def parallel_operation(self, loop, executor, counter = 0):

        if counter >= self.max_urls:
            return

        parallel_tasks = []
        for count in range(counter, counter + self.parallel_requests):
            parallel_tasks.append(loop.run_in_executor(executor, self.get_page_size, count))
        if parallel_tasks:
            completed, pending = await asyncio.wait(parallel_tasks, loop=loop)
            for t in completed:
                self.total_bytes += int(t.result())

        await asyncio.sleep(self.download_delay)
        await self.parallel_operation(loop, executor, counter + self.parallel_requests)

    def run_spider(self):

        executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=self.parallel_requests
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.parallel_operation(loop, executor))
        loop.close()

    def output_result(self):

        print("\nParallel spider results: ")
        print("Total requests made: {}".format(self.max_urls))
        print("Total bytes: {}".format(self.total_bytes))
        print("Average page size: {}".format(self.total_bytes / self.max_urls))

def main():

    concurrent_req = 5
    download_delay = 0.5
    max_urls = 10
    base_url = "https://rhettinger.wordpress.com/tag/wikipedia/"#"https://en.wikipedia.org/wiki/NumPy"

    parallel_spider = ParallelSpider(base_url, concurrent_req, download_delay, max_urls)
    parallel_spider.get_urls()
    parallel_spider.run_spider()
    parallel_spider.output_result()

if __name__ == "__main__":
    main()
