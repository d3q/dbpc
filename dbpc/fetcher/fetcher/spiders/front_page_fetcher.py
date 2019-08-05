import scrapy
import sys
import json
from bs4 import BeautifulSoup


class FrontPageFetcher(scrapy.Spider):
    name = "douban_front_page"

    def start_requests(self):
        urls = ["https://movie.douban.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        self.log('Start parsing %s' % filename)
        
        with open(filename, 'rt') as f:
            soup = BeautifulSoup(f, "html.parser")
            
        self.log(soup.title)
        urls = {}

        for link in soup.find_all('a'):
            if link.get('href'):
                link = link.get('href')
                if "movie.douban.com/subject" in link:
                    url_int = link.split('/')[4]
                    urls[url_int] = 0

        print(f"total movies:{len(urls)}\n\n{urls}")   
        
        to_url_queue = {}
        
        for url in urls:
            to_url_queue["movie" + url] = {
                "min_depth": 0,
                "status_code": 0
            }

        print(to_url_queue)
        
        y = json.dumps(to_url_queue)
        print('\n')
        print(y)

        


