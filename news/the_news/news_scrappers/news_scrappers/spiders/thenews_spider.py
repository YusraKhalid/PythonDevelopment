import scrapy
from scrapy.loader import ItemLoader
from news_scrappers.items import NewsScrappersItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class TheNewsSpider(CrawlSpider):
    news_paper = 'The News'
    source_url = 'https://www.thenews.com.pk/'
    name = "the-news"
    page = 0
    date_css = 'div.category-date::text'
    title_css = 'div.detail-heading h1::text'
    img_url_css = 'div.detail-heading div.news-pic img::attr(src)'
    detail_css = 'div.story-detail p::text'
    abstract_css = 'div.story-detail p:first-of-type ::text'
    link_extractor = LxmlLinkExtractor(
        restrict_css=['div.writter-list-item-story h2'],
    )
    rules = (

        Rule(
            link_extractor,
            callback='parse_news_detail',
            follow=True
        ),
    )

    start_urls = [
        'https://www.thenews.com.pk/latest-stories/0',
    ]

    def parse_news_detail(self, response):
        news_item = ItemLoader(item=NewsScrappersItem(), response=response)
        news_item.add_css('date', self.date_css)
        news_item.add_css('title', self.title_css)
        news_item.add_css('img_url', self.img_url_css)
        news_item.add_css('detail', self.detail_css)
        news_item.add_css('abstract', self.abstract_css)
        news_item.add_value('url', response.url)

        yield news_item.load_item()

        self.page += 1
        yield scrapy.Request('https://www.thenews.com.pk/latest-stories/' + str(self.page))
