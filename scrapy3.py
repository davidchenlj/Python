# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

reload(sys)
sys.setdefaultencoding('utf-8')


class HaoduofuliItem(scrapy.Item):
    title  = scrapy.Field()

class myspider(CrawlSpider):
    name = 'soga'
    allowed_domains = ['arthl.com']
    start_urls = ['http://blog.arthl.com']

    rules = (
       Rule(SgmlLinkExtractor(allow=('page=(\d+)', )), callback='parse_item', follow=True),
    )

    def parse_content(self, response):
        tt=response.xpath('/html/body/div[2]/div[2]/div/div[1]/h2/a/text()').extract()
        file_obj = open("log.txt", "a")
        print >> file_obj,tt[0]

    def parse_item(self, response):
        urls = response.xpath("//h2[@class='blog-post-title']/a/@href").extract()
        for url in urls:
            f_url = 'http://blog.arthl.com{url}'.format(url=url)
            yield Request(f_url, callback=self.parse_content)
