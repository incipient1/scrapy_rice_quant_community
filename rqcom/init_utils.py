from scrapy.http import Request
def init_add_request(spider,url):
    '''
    scarpy在启动的时候添加一些已经跑过的url，让爬虫不再重复跑
    '''
    rf = spider.crawler.engine.slot.scheduler.df
    request = Request(url)
    rf.request_seen(request)