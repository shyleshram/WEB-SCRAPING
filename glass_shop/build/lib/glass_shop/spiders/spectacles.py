# -*- coding: utf-8 -*-
import scrapy


class SpectaclesSpider(scrapy.Spider):
    name = 'spectacles'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def get_price(self, selector):
        original_price = selector.xpath(".//del/text()").get()
        if original_price is not None:
            return original_price
        else:
            return selector.xpath(".//div[@class='row']/div[contains(@class, 'pprice')]/span/text()").get()

    def parse(self, response):
        glassess = response.xpath(
            "//div[@class='col-sm-6 col-md-4 m-p-product']")
        for glass in glassess:
            product_url = glass.xpath(".//a/@href").get()
            product_image_url = glass.xpath(".//img/@src").get()
            product_name = glass.xpath(
                ".//p[@class='pname col-sm-12']/a/text()").get()
            product_price = self.get_price(glass)
            # product_price = glass.xpath(".//span/text()").get()

            yield {
                'url': product_url,
                'image_url': product_image_url,
                'name': product_name,
                'price': product_price
            }

        next_page = response.xpath("//a[@class='page-link']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
