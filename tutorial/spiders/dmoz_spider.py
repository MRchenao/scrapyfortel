# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import DmozItem


class DmozSpider(scrapy.spiders.Spider):
    host = 'https://segmentfault.com'
    name = "dmoz"
    allowed_domains = ["segmentfault.com"]
    start_urls = [
        "https://segmentfault.com/t/php/blogs",
        "https://segmentfault.com/t/python/blogs"
    ]

    def parse_content(self, response):
        item = response.meta['key']
        item['content'] = response.xpath('/html/body/div[3]/div[2]/div/div[1]/div[1]').extract_first()
        return item

    def parse(self, response):
        selector = response.xpath('//*[@id="blog"]')
        for sel in selector.xpath('//section[@class="stream-list__item"]'):
            item = DmozItem()
            item['title'] = sel.xpath('div[@class="summary"]/h2/a/text()').extract_first()
            item['link'] = self.host + sel.xpath('div[@class="summary"]/h2/a[@href]/@href').extract_first()
            item['desc'] = sel.xpath('div[@class="summary"]/p/text()').extract_first()
            item['article_id'] = self.name+sel.xpath('div/div/@data-id').extract_first()
            yield self.make_requests_from_url(item['link']).replace(callback=self.parse_content, meta={'key': item})
