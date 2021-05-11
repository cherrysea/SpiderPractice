import scrapy
from chuanzhi.items import ChuanzhiItem

class ItcastSpider(scrapy.Spider):
    # 爬虫名字， 必须，启动爬虫时需要的参数
    name = 'itcast'
    # 爬取域范围，可选的，允许爬虫在这个域爬取
    allowed_domains = ['itcast.cn']
    # 起始url 爬虫执行的第一批请求，是一个列表
    start_urls = ['https://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        node_list = response.xpath("//div[@class='maincon']//div[2]")
        # 用来存储所有字段
        items = []
        for node in node_list:
            item = ChuanzhiItem()
            # extract() 将xpath对象转化为 Unicode 字符串返回的是一个列表，  extract_first() 取第一个
            name = node.xpath("./h2/text()").extract_first()
            title = node.xpath("./h2/span/text()").extract_first()
            info = node.xpath("./p/span/text()").extract()

            item['name'] = name
            item['title'] = title
            item['info'] = info

            items.append(item)
        return items