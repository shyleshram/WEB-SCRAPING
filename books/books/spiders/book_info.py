# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookInfoSpider(CrawlSpider):
    name = 'book_info'
    allowed_domains = ['books.toscrape.com']
    # start_urls = []

    user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request('http://books.toscrape.com', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'book_name': response.xpath("//div[@class = 'col-sm-6 product_main']/h1/text()").get(),
            'book_price': response.xpath("//p[@class = 'price_color']/text()").get(),
            'book_url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }
