# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import RqcomItem,UserInfoItem
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from ..utils.parse import community_parse,user_page_parse
from traceback import format_exc

class SpiderRqSpider(RedisSpider):
    name = 'spider_rq'
    allowed_domains = ['ricequant.com']
    start_urls = [r'https://www.ricequant.com/community/category/all?page=24']


    def parse(self,response):
        community_datas = community_parse(response)
        item = RqcomItem()
        page_num = int(response.url.split('?page=')[1])
        for data in community_datas:
            item.update(data)
            yield item

            user_page_url = 'https://www.ricequant.com/community/api/user/{}/following'.format(item['user_id'])
            yield scrapy.Request(user_page_url,
                                  callback = self.user_parse,
                                  errback = self.error_back,
                                  meta = {'id':item['user_id']},
                                  priority = 10,
                                )

        pn = response.meta.get('pn',page_num)
        if pn > 25:
            return

        pn += 1
        response.meta['pn'] = pn
        next_page_url = '?page={}'.format(pn)
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_url,
                              callback = self.parse,
                              errback = self.error_back,
                              priority = 20,
                              meta = {'pn':pn},
                             )



    def user_parse(self,response):
        item = UserInfoItem()
        user_data = user_page_parse(response)
        item.update(user_data)
        yield item


    def error_back(self,e):
        _ = e
        print('我报错啦👇：')
        self.logger.error(format_exc())



