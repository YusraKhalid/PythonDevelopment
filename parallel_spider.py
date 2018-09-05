"""This module runs the crawler in parallel threads
   with as many threads as specified by the user
"""

import re
import time
import concurrent.futures
from urllib.parse import urljoin
from parsel import Selector
import requests


BASE_URL = 'https://en.wikipedia.org/wiki/Quentin_Tarantino'


def get_anchor_tags(url, max_urls):
    """Gets all the anchor tags in a page"""
    hyperlinks_list = []
    html = requests.get(url)

    sel = Selector(html.text)
    hyperlinks = sel.xpath('//a/@href').getall()
    base_href = sel.xpath('/html/head/base/@href').get()

    for i in hyperlinks:
        """If there is a base href that appends before every href tag
           if there is a base href then that page must not be using href
           for anything other than pure hyperlinks
        """
        if base_href:
            hyperlinks_list.append(base_href+i)
        else:
            if re.match(r'^http', i):
                # To avoid matching up any page jumps
                hyperlinks_list.append(i)
            elif re.match(r'/', i):
                # Linking to other pages with same base url
                hyperlinks_list.append(urljoin(BASE_URL, i))
            else:
                continue
        if len(hyperlinks_list) == max_urls:
            break
    return hyperlinks_list


def download_page(url):
    """Downloads the page given and returns the bytes downloaded"""
    bytes_downloaded = 0

    print('Fetching url: ', url, sep='')
    downloaded_page = requests.get(url)
    bytes_downloaded += len(downloaded_page.content)

    return bytes_downloaded


def print_report(requests_made, bytes_downloaded):
    """Prints the report based on the arguments"""
    print('\n\n-----------Report-----------',
          '\n Requests made: ', requests_made,
          '\n Bytes downloaded: ', bytes_downloaded,
          '\n Average page size: ', (bytes_downloaded/requests_made)/1000,
          'kB')


def main():
    """The main driver function that drives the program"""
    max_workers = (int)(input("Specify maximum workers: "))
    max_urls = (int)(input("Specify maximum URLs : "))

    anchor_tags = get_anchor_tags(BASE_URL, max_urls)
    requests_made = len(anchor_tags)

    # bytes_downloaded = download_list(anchor_tags)           # Serial approach
    bytes_downloaded = 0

    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) \
            as executor:
        futures = {executor.submit(download_page, url) for url in anchor_tags}
        concurrent.futures.wait(futures)

        for byte in futures:
            bytes_downloaded += byte.result()
    end_time = time.time()

    print_report(requests_made, bytes_downloaded)

    print(' Time taken: ', round(end_time-start_time, 2), 'sec\n', sep='')


main()
