# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']
    custom_settings = {
        'ITEM_PIPELINES':{'book.pipelines.JDMongoPipeline': 300}
    }

    def parse(self, response):
        """获取大小分类，返回列表页url"""
        # 大分类列表
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            # 小分类列表
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:
                item["s_href"] = em.xpath("./a/@href").extract_first()
                item["s_cate"] = em.xpath("./a/text()").extract_first()
                if item["s_href"] is not None:
                    item["s_href"] = "https:" + item["s_href"]
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item":deepcopy(item)}
                    )


    def parse_book_list(self,response):
        """获取每本书信息"""
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item["book_author"] = li.xpath(".//span[@class='author_type_1']/a/text()").extract()
            item["book_store"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item["book_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
            item["book_sku"] = li.xpath("./div/@data-sku").extract_first()
            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["book_sku"]),
                callback=self.parse_book_price,
                meta={"item": deepcopy(item)}
            )
        # 列表页翻页
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = "https://list.jd.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )


    def parse_book_price(self,response):
        """获取价格"""
        item = response.meta["item"]
        item["book_price"] = json.loads(response.body.decode())[0]["op"]
        # print(item)
        return item
