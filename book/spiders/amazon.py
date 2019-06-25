# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
from scrapy.http import Request,FormRequest


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/s/ref=lp_658409051_ex_n_1?rh=n%3A658390051&bbn=658390051&ie=UTF8&qid=1560152543']

    custom_settings = {
        'ITEM_PIPELINES': {'book.pipelines.AMAZONMongoPipeline': 304}
    }


    rules = (
        # 匹配大分类  部分小分类
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='leftNav']/ul[1]/ul/div/li",)),follow=True),
        # 少儿
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='leftNav']/ul[2]/ul/div/li",)),follow=True),
        # 图书的url地址
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='mainResults']/ul/li//h2/..",)),callback='parse_book'),
        Rule(LinkExtractor(restrict_xpaths=("//*[@class='s-result-list s-search-results sg-row']/div//h2",)),callback='parse_book'),
        # 匹配翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)),follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='a-pagination']/li[@class='a-last']",)),follow=True),
    )




    def parse_book(self,response):
        response = etree.HTML(response.text)

        item = {}
        item["book_name"] = response.xpath("//span[@id='productTitle']/text()")
        if len(item["book_name"]) == 0:
            item["book_name"] = response.xpath("//span[@id='ebooksProductTitle']/text()")
            item["book_name"] = [i.strip() for i in item["book_name"]]


        item["book_date"] = response.xpath("//*[@id='title']/span[3]/text()")


        item["book_author"] = response.xpath("//*[@id='bylineInfo']/span/a/text()")
        item["book_author"] = [i.strip() for i in item["book_author"]]


        item["book_price"] = response.xpath("//div[@id='soldByThirdParty']/span[2]/text()")
        if len(item["book_price"]) == 0:
            item["book_price"] = response.xpath("//tr[@class='kindle-price']/td[2]/text()")
            item["book_price"] = [i.strip() for i in item["book_price"]]
            if len(item["book_price"]) == 0:
                item["book_price"] = "Kindle Unlimited"


        item["book_cate"] = response.xpath("//a[@class='a-link-normal a-color-tertiary']/text()")
        item["book_cate"] = [i.strip() for i in item["book_cate"]]


        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()")
        if len(item["book_press"])>0:
            item["book_press"] = item["book_press"][0]


        yield item

