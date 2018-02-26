# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RqcomItem(scrapy.Item):

    user_id = scrapy.Field()
    user_img = scrapy.Field()
    tittle = scrapy.Field()
    read_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()
    user_name = scrapy.Field()
    next_page_num = scrapy.Field()
    next_page_url = scrapy.Field()
    topic = scrapy.Field()

class UserInfoItem(scrapy.Item):
    user_id = scrapy.Field()
    followerCount = scrapy.Field()
    followingCount = scrapy.Field()
    user_title = scrapy.Field()

