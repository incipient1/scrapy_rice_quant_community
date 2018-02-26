# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

class UAMiddleware(object):

    def process_request(self,request,spider):
        pass

    def process_response(self,request,response,spider):
        return response

    def process_exception(self,request,exception,spider):
        pass

class ProxyMiddleware(object):
    def process_request(self,request,spider):
        proxy_ip = '165.227.104.78:3128'
        request.meta['proxy'] = 'http://{}'.format(proxy_ip)

    def process_response(self,request,response,spider):
        return response

    def process_exception(self,request,exception,spider):
        pass