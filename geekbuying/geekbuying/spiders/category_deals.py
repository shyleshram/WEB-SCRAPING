# -*- coding: utf-8 -*-
import scrapy


class CategoryDealsSpider(scrapy.Spider):
    name = 'category_deals'
    allowed_domains = ['www.geekbuying.com']
    # start_urls = ['https://www.geekbuying.com/deals/categorydeals']

    def start_requests(self):
        yield scrapy.Request(url='https://www.geekbuying.com/deals/categorydeals', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        })

    def parse(self, response):
        products = response.xpath("//div[@class='flash_li']")
        for product in products:
            product_name = product.xpath(
                ".//a[@class='flash_li_link']/text()").get()
            product_url = product.xpath(
                ".//a[@class='flash_li_link']/@href").get()
            product_discount_price = product.xpath(
                ".//div[@class='flash_li_price']/span/text()").get()
            product_original_price = product.xpath(
                ".//div[@class='flash_li_price']/del/text()").get()
            discount = product.xpath(
                ".//div[@class='category_li_off']/text()").get()

            yield {
                'name': product_name,
                'url': product_url,
                'discounted_price': product_discount_price,
                'original_price': product_original_price,
                'discount': discount,
                'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
            })
            # or yield scrapy.Request(url=next_page, callback=self.parse)
