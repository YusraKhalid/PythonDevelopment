import argparse
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool, Manager
import time
import logging

import requests
from lxml import html

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')


class FetchResponse:
    def __init__(self, start_url):
        self.start_url = start_url

    def parse_url_response(self, url):
        raw_response = requests.get(url)
        return raw_response.status_code, raw_response.text

    def parse_urls(self, raw_response_text):
        response = html.fromstring(raw_response_text)
        return response.xpath('//a[contains(@href, "/")]/@href')[0]

    def fetch_absolute_urls(self, relative_urls):
        return [urljoin(self.start_url, url) for url in relative_urls]

    def filter_urls(self, absolute_urls):
        return [url for url in absolute_urls if self.start_url in url]


class Scheduler:
    def __init__(self, start_url, delay, threads, max_urls_limit):
        self.start_url = start_url
        self.delay = delay
        self.threads = threads
        self.max_urls_limit = max_urls_limit
        self.extracted_urls = Manager().list([start_url])
        self.visited_urls = Manager().list()
        self.total_bytes_downloaded = Manager().Value('value', 0)
        self.total_pages_crawled = Manager().Value('value', 0)
        self.total_errors = Manager().Value('value', 0)

    def crawl_parallel(self):
        while len(self.visited_urls) < self.max_urls_limit:
            pool = Pool(self.threads)
            pool.apply(self.get_next_urls)
            pool.terminate()
            pool.join()

        return self.total_bytes_downloaded.value, self.total_pages_crawled.value, self.total_errors.value

    def get_next_urls(self):
        url = self.extracted_urls.pop()
        self.visited_urls.append(url)

        fetch = FetchResponse(self.start_url)
        raw_response_status_code, raw_response_text = fetch.parse_url_response(url)
        time.sleep(self.delay)

        if raw_response_status_code == 200:
            self.total_bytes_downloaded.value += len(raw_response_text)
            self.total_pages_crawled.value += 1

            relative_urls = fetch.parse_urls(raw_response_text)
            absolute_urls = fetch.fetch_absolute_urls(relative_urls)
            domain_urls = fetch.filter_urls(absolute_urls)

            domain_urls = set(domain_urls)
            domain_urls = domain_urls - set(self.visited_urls)

            self.add_next_urls(domain_urls)

        else:
            self.total_errors.value += 1

    def add_next_urls(self, domain_urls):
        for url in domain_urls:
            if url not in self.extracted_urls:
                self.extracted_urls.append(url)


class CrawlerReport:
    def __init__(self, total_bytes_downloaded, total_pages_crawled, total_errors):
        self.total_bytes_downloaded = total_bytes_downloaded
        self.total_pages_crawled = total_pages_crawled
        self.total_errors = total_errors

    def print_crawler_report(self, start_time):
        total_crawl_time = time.time() - start_time
        print("Total bytes downloaded: {}".format(self.total_bytes_downloaded))
        print("Total pages crawled: {}".format(self.total_pages_crawled))
        print("Average page size: {}".format(self.total_bytes_downloaded / self.total_pages_crawled))
        print("Total crawel time: {}".format(total_crawl_time))
        print("Total Errors: {}".format(self.total_errors))


def main():
    try:
        args = parse_configuration()
        start_time = time.time()

        scheduler = Scheduler(args.url, args.delay, args.threads, args.limit)
        scheduler.get_next_urls()
        total_bytes_downloaded, total_pages_crawled, total_errors = scheduler.crawl_parallel()

        report = CrawlerReport(total_bytes_downloaded, total_pages_crawled, total_errors)
        report.print_crawler_report(start_time)

    except argparse.ArgumentTypeError:
        args.print_help()


def validate_url(url):
    if urlparse(url).netloc and urlparse(url).scheme:
        return url


def parse_configuration():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-u', '--url', type=validate_url,
                            help='Enter site url --Input format: https://website.com/ ')
    arg_parser.add_argument('-d', '--delay', type=int, help='Enter delay time ')
    arg_parser.add_argument('-t', '--threads', type=int, help='Enter concurrent call requests')
    arg_parser.add_argument('-l', '--limit', type=int, help='Total urls to visit limit')

    return arg_parser.parse_args()


if __name__ == '__main__':
    main()

