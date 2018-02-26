from pyquery import PyQuery
from scrapy.http import Request
import json

def community_parse(response):
    result_list = list()
    jpy = PyQuery(response.text)
    list_li = jpy('#topics-container > li > div')
    for i in list_li.items():
        result = dict()
        try:
            result['user_id'] = i('a').attr('href').split('user/')[1]
            result['user_id'] = int(result['user_id'])
            result['user_img'] = i('a > img').attr('src')
            result['user_name'] = i('a > img').attr('title')
            result['tittle'] = i('h3 > a > span').text()
            result['comment_num'] = i('small > span.topic-nums > span:nth-child(1)').text()
            result['comment_num'] = int(result['comment_num'])
            result['read_num'] = i('small > span.topic-nums > span:nth-child(2)').text()
            result['read_num'] = int(result['read_num'])
            result['like_num'] = i('small > span.topic-nums > span:nth-child(3)').text()
            result['like_num'] = int(result['like_num'])
            result['topic'] = i('h3 > a').attr('href').split('topic/')[1]
            result['topic'] = int(result['topic'])
        except:
            pass
        result_list.append(result)

    return result_list


def user_page_parse(response):
    result = dict()
    user_following_data = json.loads(response.text)

    result['followingCount'] = user_following_data['followingCount']
    result['followingCount'] = int(result['followingCount'])

    result['followerCount'] = user_following_data['followerCount']
    result['followerCount'] = int(result['followerCount'])
    result['user_id'] = response.url.split('/')[6]
    # result['user_title'] = jpy('#page-profile > main > div.container > \
    #     section > div.user-info-content-wrap > div.user-info-grade > p').text()

    return result



def error_back(e):
    print('我报错啦👇：')
    print(e)

if __name__ == '__main__':
    import requests
    r = requests.get(r'https://www.ricequant.com/community/api/user/196300/following')
    print(user_page_parse(r))
