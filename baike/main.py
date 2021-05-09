# coding:utf-8
from DataOutput import DataOutput
from HTMLDownloader import HtmlDownload
from HtmlParser import HtmlParser
from UrlManager import UrlManger

class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManger()
        self.downloader = HtmlDownload()
        self.parser = HtmlParser()
        self.output = DataOutput()
    def crawl(self, root_url):
        self.manager.add_new_url(root_url)
        # print(self.manager.new_url_size())
        # print(self.manager.old_urls_size())
        while(self.manager.has_new_url() and self.manager.old_urls_size() < 100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                # print(html)
                # print('新的url：', new_url)
                new_urls, data = self.parser.parser(new_url, html)
                # print("new_urls长度：", len(new_urls))
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print('已经抓取了%s个链接' % self.manager.old_urls_size())
            except Exception as e:
                print(e,'Crawl failed')
        self.output.output_html()
        print("已保存至 baike.html")

if __name__=='__main__':
    spider_man = SpiderMan()
    spider_man.crawl("https://baike.baidu.com/item/%E5%8D%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6")