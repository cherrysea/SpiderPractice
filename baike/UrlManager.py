# coding:utf-8

class UrlManger(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    # 判断是否还有新的 url
    def has_new_url(self):
        return self.new_url_size() != 0

    # 获取一个未爬取的 url
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
    
    # 增加一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    # 增加一些新的url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 获取为爬取url集合的大小
    def new_url_size(self):
        return len(self.new_urls)
    
    # 获取未爬取url集合大小
    def old_urls_size(self):
        return len(self.old_urls)