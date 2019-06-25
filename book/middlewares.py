# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import requests


class BookSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BookDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # cookiedict = {}
        # cookies = 'session-id=458-3677303-0276763; ubid-acbcn=461-0308207-3543623; i18n-prefs=CNY; amznacsleftnav-750c67d9-2c54-30fc-ba99-5372627cac13=1; amznacsleftnav-cff38b65-0f11-3902-aeb9-ddc681100d65=1; p2dPopoverID_all_1=1560315370.073; p2dPopoverID_default_1=1560315370.074; a-ogbcbff=1; session-token="zcP/bdGw3HMXN4XUcjASGJVMfWvNZ76rZCQX4/JqO0Fbsw0zm/J+IoDKpxO2+Lq2PhEdctO0/ndxbDyZCH0nTNKbux1lnhAtgkSC/djTGHxmDPxt27n0mQ5zuDS1w/9qR74yPHzni2cnIoZqQq59qcewFRhAQTLlkSbOqPex+NY+mk562k/deHQKWQct2ddfHPZCZaimql67iv0zZBDeHckjNf44hNs81WJvGSnTFNc="; x-acbcn="1@Ptr5rDVKu1qTbFIohWgCDvIC0?HSSdESihcmBAK3CH@oEW6Bi64APO3Gir01PK"; at-main=Atza|IwEBINvwQeYFbiB_ACrWql2-JwwsMotbh8VVejs_NT10X_9uTYy6Xzyv6SRgxbjsqr8AcbhlqdTmFnCOKn9Kx6LIM5i6SPX3-CbcKx18j8wXWs7t3KW_K0ez1SoQJBzQvLR4apkFyZPyWiW4tikR5zJW3-HYToze2HsK80dzRuOvn0_IHQ0sJQIlWGh6zLvmVPq8cO9zgFmGm2PUvAAlNjpkrmPGKECRcWkNh_Df3YTluUYN0GY9e5Ljz8d1L3ywnayvT4IgfrEQfZGe8K3reOe9LIb7QpPZPINIuLDfbauMG6To48g8DgxXny2tOru5qIjkxarE96XwzOOEeKKBy3C_U7uNaGG1-DJOxd8HP3qhE-97gP9sNi1ppIPbDrvaywszLt6kzF3lNSOTYghKx6ChtnPE; sess-at-main="fTIRXorKi7TlgeJzjj0p3fQ3dtBTNNKsgIsCSkGtpS8="; sst-main=Sst1|PQERJZ15GPnEq89vo-sXn4a0CvKnRjqeCkFwlSOIoO0cMnJpSEpD9zh_Zifkqdq_HiWLTibCc6Ne09XrccAbh5tvH83CLDgsBvVfzaPi4-8XJYyimE_6wP2O-bhneIPsinzp5jNOkWO8rzcuQvp57De2W4-iigmdB4nT9_CjStaDuHzTztNXFZjSkLf82U80QOQ6H-HCk91Qbakt-aKk08Z4YrCczaJGMpPuZ8v1nErnuy0rjYNE05vJV6cCvLNYUVkfz18zmbVistLy44sC7IluFUIxjPKKp82qtOnUnV4HgDY5iv5QCR4gSRWa6RYP7bmh; x-wl-uid=1XEMm3jdi35mdizdUELv/ZaWmqpsdiHHm6xcrDGrsHL4/s1tLoCh0wRUBazg+xT1S3f/DLfNPwCltex7WWJXu2R62FVAzGdibCKG2Wi5SDU/6NvILs0hNKjWQqrql6ddEfgt5EHH4tto=; csm-hit=tb:s-AZFE4H9PMWJ36S3A0Z64|1560756928388&t:1560756930390&adb:adblk_no; session-id-time=2082729601l'
        # for i in cookies.split(';'):
        #     cookiedict[i.split('=')[0]] = i.split('=')[1]
        #     request.cookie = cookiedict
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUserAgentMiddleware(object):
    '''随机更换User-Agent'''
    def __init__(self,crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):

        def get_ua():
            return getattr(self.ua,self.ua_type)
        request.headers.setdefault('User-Agent',get_ua())


class HttpbinProxyMiddleware(object):
    """代理IP"""
    def process_request(self, request, spider):
        pro_addr = requests.get('http://127.0.0.1:5555/random').text
        request.meta['proxy'] = 'http://' + pro_addr
        print('http://' + pro_addr)
        return  None

