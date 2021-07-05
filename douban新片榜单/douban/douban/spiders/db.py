import scrapy

# 豆瓣新片榜 · · · · · ·

headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

class DouBanSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/chart/']

    def start_requests(self):
        links = response.xpath('//*[@id="content"]/div/div[1]/div/div/table/tbody/tr/td[2]/div/a/@href').extract()
        yield [scrapy.Request(url=link, headers=headers, callback=self.parse) for link in links]
    def parse(self, response):
        url = response.url
        yield scrapy.Request(url, headers=headers, callback = self.parse_movie)
    def parse_movie(self, response):
        yield {
            # //*[@id="content"]/h1/span[1]
            'title' : response.xpath('//*[@id="content"]/h1/span[1]/text()').extract_first(),
            # 'cover' : response.xpath('//*[@id="mainpic"]/a/img/@src').extract_first(),
            'intro' : response.xpath('//*[@id="link-report"]/span/text()').extract()
        }


