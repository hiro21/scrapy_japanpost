import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import shutil
import requests

class JapanPostSpider(CrawlSpider):
    name = 'japanpost'
    start_urls = [
            'http://www.post.japanpost.jp/zipcode/download.html',
    ]

    rules = [
            Rule(LinkExtractor(allow=("a href")), follow=True)
    ]

    def parse(self, response):

        for url in response.css('a::attr(href)'):

            if url.extract() == "/zipcode/dl/oogaki-zip.html":
                nextUrl = response.urljoin(url.extract() )
                yield scrapy.Request(nextUrl, self.parse_nextUrl)

    def parse_nextUrl(self, response):

        for url in response.css('a::attr(href)'):

            if url.extract() == "oogaki/zip/ken_all.zip":
                downloadUrl = response.urljoin(url.extract())

                file_name = downloadUrl.split("/")[-1]

                r = requests.get(downloadUrl)
                if r.status_code == 200:
                    f = open(file_name, 'wb')
                    f.write(r.content)
                    f.close()

