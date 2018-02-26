# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
#from .init_utils import init_add_request
from pymongo.errors import DuplicateKeyError
from .items import RqcomItem,UserInfoItem
from traceback import format_exc
from pymongo import MongoClient
import pymysql
from scrapy.conf import settings


class RqcomPipeline(object):

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MongoDB_uri'),
            mongo_db = crawler.settings.get('MongoDB_database','items')
            )

    def open_spider(self,spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['rqcomitem'].ensure_index('topic',unique = True)
        self.db['userinfoitem'].ensure_index('user_id',unique = True)

    def process_item(self, item, spider):
        try:
            if isinstance(item,RqcomItem):
                self.db.rqcomitem.update({'topic':item['topic']},
                    {'$set':item},upsert = True)
            elif isinstance(item,UserInfoItem):
                self.db.userinfoitem.update({'user_id':item['user_id']},
                    {'$set':item},upsert = True)

        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')
        
        # 如果要入库MySQL，将下文添加进来即可
        # try:
        #     db_mysql = pymysql.connect(host = "localhost",
        #                          port = ***,
        #                          user = "***",
        #                          password = "***",
        #                          db = "test",
        #                          charset = "utf8")

        #     if isinstance(item,RqcomItem):
        #         cursor = db_mysql.cursor()
        #         # cursor.execute("\                                                       # 创建字段
        #         #                 CREATE TABLE rice_quant_community_4(topic INT,\
        #         #                                                     user_id INT,\
        #         #                                                     user_img varchar(20),\
        #         #                                                     tittle varchar(50),\
        #         #                                                     comment_num int,\
        #         #                                                     read_num int,\
        #         #                                                     like_num int,\
        #         #                                                     primary key(topic)\
        #         #                                                     );\
        #         #               ")

        #         cursor.execute("USE test")
        #         sql = "INSERT INTO `rice_quant_community_4`(`topic`,`user_id`,`user_img`,`tittle`,`read_num`,`comment_num`,`like_num`) \
        #                VALUES ({0},{1},'{2}','{3}',{4},{5},{6})"\
        #                .format(item['topic'],item['user_id'],item['user_img'],item['tittle'],item['read_num'],item['comment_num'],item['like_num'])
        #         cursor.execute(sql)
        #         db_mysql.commit()
        #         cursor.close()

        #     elif isinstance(item,UserInfoItem):
        #         cursor = db_mysql.cursor()
        #         # cursor.execute("\
        #         #                 CREATE TABLE rice_quant_user_info(user_id INT,\
        #         #                                                   follower_count INT,\
        #         #                                                   following_count INT,\
        #         #                                                   primary key(user_id)\
        #         #                                                   );\
        #         #               ")
        #         cursor.execute('USE test')
        #         sql ="INSERT INTO `rice_quant_user_info`(`user_id`,`follower_count`,`following_count`) \
        #                    VALUES ({0},{1},{2})"\
        #                    .format(item['user_id'],item['followerCount'],item['followingCount'])
        #         cursor.execute(sql)
        #         db_mysql.commit()
        #         cursor.close()
        #     db_mysql.close()
        # except Exception as e:
        #     _ = e
        #     spider.logger.error(format_exc())
        # except DuplicateKeyError:
        #     spider.logger.debug('duplicate key error collection')

        return item

    def close_spider(self,spider):
        _ = spider
        self.client.close()
        print('数据库关闭啦！')
