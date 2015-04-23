# -*- coding: utf-8 -*-

# Scrapy settings for newegg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from scrapy.settings.default_settings import DOWNLOAD_DELAY

BOT_NAME = 'newegg'
DOWNLOAD_DELAY = 5


HTTPCACHE_ENABLED = True
SPIDER_MODULES = ['newegg.spiders']
NEWSPIDER_MODULE = 'newegg.spiders'

FEED_FORMAT = 'jsonlines'
FEED_URI = "jsons/%(name)s-%(time)s.json"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newegg (+http://www.yourdomain.com)'
