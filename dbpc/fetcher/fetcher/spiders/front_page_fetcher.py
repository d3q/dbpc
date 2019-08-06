import scrapy
import sys
import os.path
import json
from bs4 import BeautifulSoup


class FrontPageFetcher(scrapy.Spider):
    name = "douban_front_page"

    def start_requests(self):
        
        #print('\n' * 10)
        #print((os.path.abspath(os.pardir)) + "/local_storage/url_queue.json")
        #print(os.path.abspath(os.path.join("../../../local_storage/url_queue.json", os.pardir)))
        #print('\n' * 10)

        #sys.exit(0)
        
        
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

        print(f"total movies:{len(urls)}\n")   
        
        to_url_queue = {}
        
        for url in urls:
            to_url_queue["movie" + url] = {
                "min_depth": 0,
                "status_code": 555
            }

        print(to_url_queue)
        
        #y = json.dumps(to_url_queue, indent=4)
        #print('\n')
        #print(y)
        
        self.log(f"Opening URL queue...")
        url_queue_file = (os.path.abspath(os.pardir)) + "/local_storage/url_queue.json"
        
        #print(os.stat(url_queue_file).st_size)
        
        if os.stat(url_queue_file).st_size == 0:
            in_url_queue = {}
        else:
            with open(url_queue_file, 'r') as f:
                in_url_queue = json.load(f)
        self.log(f"URL queue opened: {len(in_url_queue)} items.")        
        
        in_url_queue.update(to_url_queue)
        self.log(f"URL queue updating... Now there're {len(in_url_queue)} items. Saving file...")
        with open(url_queue_file, 'w') as f:
            json.dump(in_url_queue, f, indent=4)
        self.log(f"Saved to {url_queue_file}.")

