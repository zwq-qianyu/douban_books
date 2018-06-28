# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import quote
from master.items import MasterItem
import time,redis

class BookdetailUrlsSpider(scrapy.Spider):
    name = 'bookdetail_urls'
    allowed_domains = ['book.douban.com']
    base_url = 'http://book.douban.com/'

    def start_requests(self):
    	# 连接Redis数据库
    	r = redis.Redis(host=self.settings.get('REDIS_HOST'),port=self.settings.get('REDIS_PORT'),decode_responses=True)
    	# 遍历数据库中的books:tag_urls，爬取数据
    	while r.llen('books:tag_urls'):
    		tag = r.lpop('books:tag_urls')
    		url = self.base_url + quote(tag)
    		yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        '''解析图书页面的每本图书的详情页url地址'''
        print(response.url)
        # 获取每一页中20本书的url
        lists = response.css('li.subject-item div.pic a::attr(href)').extract()
        #print(lists)
        if lists:
        	for i in lists:
        		item = MasterItem()
        		item['url'] = i
        		yield item
        # 下一页url地址
        next_url = response.css('span.next link::attr(href)').extract_first()
        # 如果不是最后一页，继续解析下一页
        if next_url:
        	# 拼接下页地址
        	nexturl = response.urljoin(next_url)
        	# 解析下一页数据
        	yield scrapy.Request(url=nexturl, callback=self.parse)

