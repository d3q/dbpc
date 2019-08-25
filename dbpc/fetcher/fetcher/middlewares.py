# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import time
import hashlib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from faker import Faker
from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.httpcache import HttpCacheMiddleware
from .script.scripts_request_with_xdaili import scripts_request_with_xdaili
from scrapy.http import Response,HtmlResponse,TextResponse
import faker
import random
from .settings import USER_AGENT


class FetcherSpiderMiddleware(object):
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


class FetcherDownloaderMiddleware(object):
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



class FetcherDownloaderMiddlewareProxyIP(object):

    def __init__(self):
        self.fake = faker.Faker()
        #self.user_agent=random.choice(USER_AGENT)

        # orderno = "ZF20198180632BK2FZP"
        # secret = "e6d04e020e714f97a441afcbda48a2b5"
        # ip_port = "forward.xdaili.cn:80"
        # timestamp = str(int(time.time()))
        # string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        # string = string.encode()
        # md5_string = hashlib.md5(string).hexdigest()
        # sign = md5_string.upper()
        # self.auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        # self.proxy = ip_port


    def process_request(self, request, spider):
        if request.meta.get('usescript',False):
            statu_code, response_text = scripts_request_with_xdaili(request.url,self.fake.user_agent())
            print(statu_code)
            print(self.fake.user_agent())
            return HtmlResponse(url=request.url, body=response_text, encoding='utf-8',request=request,status=statu_code)

        # request.headers.setdefault('Proxy-Authorization',self.auth)
        # request.headers.setdefault('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')

class FetcherDownloaderMiddlewareUserAgent(object):
    def __init__(self):
       self.fake = Faker()


    def process_request(self,request,spider):
        print(self.fake.user_agent())
        request.headers.setdefault('User-Agent',self.fake.user_agent())


