import asyncio
import requests

from parsel import Selector
from urllib.parse import urljoin

BASE_URL = 'https://en.wikipedia.org/wiki/SOLRAD_2'
DOMAIN_URL = 'https://www.wikipedia.org'
bytes_downloaded = 0


def extract_urls(base_url, max_urls):
    response = requests.get(base_url)
    selector = Selector(text=response.text)
    absolute_urls = selector.xpath('//a[contains(@href, "http")]/@href').getall()
    relative_urls = selector.xpath('//a[starts-with(@href, "/wiki")]/@href').getall()

    domain_urls = list(map(lambda url: urljoin(DOMAIN_URL, url), relative_urls))
    absolute_urls.extend(domain_urls)

    return absolute_urls[:max_urls]


async def make_request(download_delay, queue):
    global bytes_downloaded

    while True:
        url = await queue.get()
        print('URL: ', url)
        response = requests.get(url)
        bytes_downloaded += len(response.content)
        
        await asyncio.sleep(download_delay)
        queue.task_done()


async def process_queue(urls, concurrent_requests, download_delay):
    queue = asyncio.Queue()

    for url in urls:
        queue.put_nowait(url)

    tasks = [asyncio.create_task(make_request(download_delay, queue)) for _ in range(concurrent_requests)]
    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


def print_report(bytes_downloaded, total_requests):
    print('Total Requests Made: ', total_requests)
    print(f'Total Bytes Downloaded: {bytes_downloaded} Bytes')
    print(f'Average Page Size: {(bytes_downloaded / total_requests) // 1000} kb')


def main():
    max_urls = int(input('Please enter maximum number of urls to visit: '))
    download_delay = int(input('Please enter download delay (in sec): '))
    concurrent_requests = int(input('Please enter number of concurrent requests: '))

    urls = extract_urls(BASE_URL, max_urls)
    asyncio.run(process_queue(urls, concurrent_requests, download_delay))
    print_report(bytes_downloaded, max_urls)

if __name__ == '__main__':
    main()
