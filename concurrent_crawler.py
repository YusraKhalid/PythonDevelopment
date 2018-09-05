"""This module runs a crawler in concurrent manner
   with the help of asyncio module
   """

import re
import time
import asyncio
from urllib.parse import urljoin
import requests
from parsel import Selector

BASE_URL = 'https://en.wikipedia.org/wiki/Quentin_Tarantino'
bytes_download_list = []


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


async def concurrent_download_page(url, download_delay):
    """Downloads the page given and returns the bytes downloaded"""
    print('Fetching url: ', url, sep='')
    downloaded_page = requests.get(url)
    await asyncio.sleep(download_delay)

    bytes_download_list.append(len(downloaded_page.content))


def print_report(requests_made):
    """Prints the report based on the arguments"""
    bytes_downloaded = sum(bytes_download_list)
    print('\n\n-----------Report-----------',
          '\n Requests made: ', requests_made,
          '\n Bytes downloaded: ', bytes_downloaded,
          '\n Average page size: ', (bytes_downloaded/requests_made)/1000,
          'kB')


async def wrapper_for_async():
    """A wrapper method for creating and calling the async functions"""
    max_urls = (int)(input("Specify maximum URLs : "))
    download_delay = (int)(input("Specify minimum download delay : "))
    anchor_tags = get_anchor_tags(BASE_URL, max_urls)
    requests_made = len(anchor_tags)

    start_time = time.time()
    tasks = [concurrent_download_page(url, download_delay)
             for url in anchor_tags]

    await asyncio.gather(*tasks)
    end_time = time.time()

    print_report(requests_made)
    print(' Time taken: ', round(end_time-start_time, 2), 'sec\n', sep='')


def main():
    """The main driver function"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wrapper_for_async())
    loop.close()


main()
