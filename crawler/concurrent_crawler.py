import requests
import asyncio

from parsel import Selector


BASE_URL = 'https://en.wikipedia.org/wiki/SOLRAD_2'
DOMAIN_URL = 'https://www.wikipedia.org'
bytes_downloaded = 0


def make_request(url):    
    response = requests.get(url)

    return response
    

def extract_urls(page_html, max_urls):    
    selector = Selector(text=page_html.text) 
    absolute_urls = selector.xpath('//a[contains(@href, "http")]/@href').getall()
    relative_urls = selector.xpath('//a[starts-with(@href, "/wiki")]/@href').getall()

    domain_urls = list(map(lambda url: DOMAIN_URL + url, relative_urls))
    absolute_urls.extend(domain_urls)

    return absolute_urls[:max_urls]


async def make_concurrent_request(url, download_delay):
    global bytes_downloaded   

    page_response = requests.get(url)
    bytes_downloaded += len(page_response.content)
    await asyncio.sleep(download_delay)


def print_report(bytes_downloaded, total_requests):
    print('Total Requests Made: ', total_requests)
    print(f'Total Bytes Downloaded: {bytes_downloaded} Bytes')
    print(f'Average Page Size: {(bytes_downloaded/total_requests)//1000} kb')        


async def main():
    max_urls = int(input('Please enter maximum number of urls to visit: '))
    download_delay = int(input('Please enter download delay (in sec): '))
    max_requests = int(input('Please enter number of concurrent requests: '))

    page_html = make_request(BASE_URL)
    urls = extract_urls(page_html, max_urls)    
    request_counter = 0

    for url in urls:
        if request_counter < max_requests:
            print('URL: ', url)
            await asyncio.gather(make_concurrent_request(url, download_delay))
        else:
            break               
        request_counter += 1 

    print_report(bytes_downloaded, request_counter)

if __name__ == "__main__":
    asyncio.run(main())
