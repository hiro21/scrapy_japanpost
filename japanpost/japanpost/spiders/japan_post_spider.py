import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
class JapanPostSpider(CrawlSpider):
    name = 'japanpost'
    start_urls = [
            'http://www.post.japanpost.jp/zipcode/download.html',
    ]

    rules = [
            Rule(LinkExtractor(allow=("a href")), follow=True)
    ]

    def parse(self, response):
        print("out response")
        print(response)
        print(self)

        for url in response.css('a::attr(href)'):
            #print(url)
            #print(url.extract())

            if url.extract() == "/zipcode/dl/oogaki-zip.html":
                print("target")
                # 対象の場合、処理を実行
                print(response.urljoin(url.extract() ))
                nextUrl = response.urljoin(url.extract() )
                yield scrapy.Request(nextUrl, self.parse_nextUrl)

    def parse_nextUrl(self, response):
        #pattern = r'*zip$'
        #repatter = re.compile(pattern)
        #re.search(r'*zip$', )

        for url in response.css('a::attr(href)'):
            #matchObj = repatter.search(url.extract())
            #print(matchObj)
            m = re.search(re.escape(r'*.zip$'), url.extract())
            print(m)
            #if "zip" in url.extract():
            #    print(url.extract())
