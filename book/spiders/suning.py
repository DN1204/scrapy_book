# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
import json
from copy import deepcopy

class SuningSpider(RedisSpider):
    name = 'suning'
    allowed_domains = ['suning.com']
    # start_urls = ['https://book.suning.com/']
    redis_key = "suning"

    def parse(self,response):
        li_list = response.xpath("//ul[@class='book-name-list clearfix']/li")
        for li in li_list:
            name = li.xpath("./a/text()").extract_first()
            listurl = li.xpath("./a/@href").extract_first()
            # print(name)
            yield scrapy.Request(
                url=listurl,
                callback=self.parse_list
            )

    def parse_list(self,response):
        """重新构造列表页数据的url"""
        # 详情页数据是动态的
        # 1.获取页面规律
        # https://list.suning.com/emall/showProductList.do?ci=503096&pg=03&cc=010&paging=0
        # ci值和paging值通过列表页response获取
        ci = re.findall('"categoryId": "(.*?)"',response.body.decode())[0]
        # page_num = 200
        print(ci)
        # 2.构造真正的url列表
        for i in range(0,2):
            base_url = "https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cc=010&paging={}".format(ci,i)
            # 3.返回详情页请求
            yield scrapy.Request(
                url=base_url,
                callback=self.parse_real_list
            )

    def parse_real_list(self,response):
        # 真正列表页数据
        url_list = response.xpath("//div[@class='img-block']")
        for url in url_list:
            url = response.xpath("//div[@class='img-block']/a/@href").extract_first()
            url = "https:" + url
            yield scrapy.Request(
                url=url,
                callback=self.parse_book_info
            )


    def parse_book_info(self,response):
        item = {}
        item["book"] = response.xpath("//h1[@id='itemDisplayName']/text()").extract_first().strip()
        item["author"] = response.xpath("//span[text()='作者： ']/../text()").extract_first()
        item["press"] = response.xpath("//span[text()='出版社：']/../text()").extract_first().strip()
        item["date"] = response.xpath("//span[text()='出版时间：']/../span[2]/text()").extract_first()
        print(item)
        # 提取价格 json数据
        # https://pas.suning.com/nspcsale_0_000000010966067125_000000010966067125_0070726642_10_010.html
        # flagshipid
        # passPartNumber
        fla_id = re.findall("'flagshipid':'(\d+)'",response.body.decode())
        passpnum = re.findall("'passPartNumber':'(\d+)'",response.body.decode())
        price_url = "https://pas.suning.com/nspcsale_0_{}_{}_{}_10_010.html".format(passpnum,passpnum,fla_id)

        yield scrapy.Request(
            url=price_url,
            callback=self.parse_price,
            meta={"item":deepcopy(item)}
        )

    def parse_price(self,response):
        item = response.meta["item"]
        data = json.loads(response.text)
        item["price"] = data.get('promotionPrice')
        print(item)