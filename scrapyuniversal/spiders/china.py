# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.Loder import ChinaLoader
from scrapyuniversal.items import NewsItem
class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article\/.*\.html',restrict_xpaths=('//*[@id="left_side"]//div[@class="con_item"]')), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="pageStyle"]//a[contains(., "下一页")]')))
    )
    def parse_item(self, response):
        loader = ChinaLoader(item = NewsItem(), response=response)
        loader.add_xpath('title', '//*[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//*[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime', '//*[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('source', '//*[@id="chan_newsInfo"]/text()', re='来源: (.*)')
        loader.add_value('website', '中华网')
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield loader.load_item()
