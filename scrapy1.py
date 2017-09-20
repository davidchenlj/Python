# -*- coding: utf-8 -*-
import sys, re
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest

reload(sys)
sys.setdefaultencoding('utf-8')


class HaoduofuliItem(scrapy.Item):
    title  = scrapy.Field()

class myspider(CrawlSpider):
    name = 'soga'
    allowed_domains = ['arthl.com']
    start_urls = ['http://www.arthl.com']

    rules = (
       Rule(LinkExtractor(allow=('pn=(\d+)', )), follow=True),
       Rule(LinkExtractor(allow=('show\-\d+\-\d+\.html', )),callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        url=response.url
        title = response.xpath("//div[@class='showArea box']/h1/text()").extract()[0]
        file_obj = open("log.txt", "a")
        print >> file_obj,'%s %s' % (url, title)
