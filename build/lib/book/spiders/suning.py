# -*- coding: utf-8 -*-
import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 大分类
        b_list = response.xpath("//div[@class='submenu-left']/p")
        for b in b_list:
            item = {}
            item["b_cate"] = b.xpath("./a/text()").extract_first()
            # 小分类
            s_list = b.xpath("../ul/li/a")
            for s in s_list:
                item["s_cate"] = s.xpath("./text()").extract_first()
                item["s_href"] = s.xpath("./@href").extract_first()
                if item["s_href"] is not None:
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item":item}
                    )

    def parse_book_list(self,response):
        # 获取列表页
        item = response.meta["item"]
        # 详情页数据是动态的
        # 1.获取页面规律
        # https://list.suning.com/emall/showProductList.do?ci=503096&pg=03&cc=010&paging=0
        # ci值和paging值通过列表页response获取
        # 2.构造真正的url列表
        # 3.返回详情页请求

    def parse_real_list(self,response):
        # 真正列表页数据
        pass


    def parse_book_info(self,response):
        pass