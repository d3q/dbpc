import scrapy
from bs4 import BeautifulSoup


class FrontPageFetcher(scrapy.Spider):
    name = "douban_front_page"

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        urls = ["https://movie.douban.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
        print("asd")
        


#with open("movie.douban.com.html") as fp:
#    soup = BeautifulSoup(fp)

#soup = BeautifulSoup("<html>data</html>")

