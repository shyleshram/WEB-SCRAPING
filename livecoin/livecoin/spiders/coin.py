# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    # as we use splash we have to override the start_requests()

    script = '''
        function main(splash ,args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            
            input_box = assert(splash:select(".searchText___3mLvd"))
            input_box:focus()
            input_box:send_text("RUR")
            assert(splash:wait(1))
            
            input_box:send_keys("<Enter>")
            assert(splash:wait(1))
            
            splash:set_viewport_full()
            --[[
            other = assert(splash:select_all(".filterPanelItem___2z5Gb active___1otJu"))
            other:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            ]]
            return splash:html()  
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='https://www.livecoin.net/en', callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }
