# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import urllib


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = 'dangdang'
    custom_settings = {
        'ITEM_PIPELINES': {'book.pipelines.DDMongoPipeline': 302}
    }



    def parse(self, response):
        # 大分类
        div_list = response.xpath("//div[@class='con flq_body']/div")[2:15]
        for div in div_list:
            item = {}
            item["b_cate"] = div.xpath("./dl/dt//text()").extract()
            item["b_cate"] = [i.strip() for i in item["b_cate"] if len(i.strip())>0]
            # 中间分类
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                item["m_cate"] = dl.xpath("./dt//text()").extract()
                item["m_cate"] = [i.strip() for i in item["m_cate"] if len(i.strip())>0][0]
                # 小分类分组
                dd_list = dl.xpath("./dd/a")
                for dd in dd_list:
                    item["s_cate"] = dd.xpath("./text()").extract_first()
                    item["s_href"] = dd.xpath("./@href").extract_first()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta={"item":deepcopy(item)}
                        )

    def parse_book_list(self,response):
        """列表页数据"""
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_name"] = li.xpath("./p[@class='name']/a/@title").extract_first()
            item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
            item["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/text()").extract()
            item["book_date"] = li.xpath("./p[@class='search_book_author']/span[2]/text()").extract_first()
            item["book_press"] = li.xpath("./p[@class='search_book_author']/span[3]/a/text()").extract_first()
            yield item


        # 下一页
        next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url is not None:
            next_url = urllib.parse.urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )



