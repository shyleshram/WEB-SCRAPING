# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class BooksToScrapePipeline(object):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'bookname': item.get('book_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        return 'full/%s.jpg' % (request.meta['bookname'])
