import scrapy
import sys
import os.path
import json
from bs4 import BeautifulSoup


class GrandPageFetcher(scrapy.Spider):
    name = "douban_grand_pages"

    def start_requests(self):
        urls = ["https://movie.douban.com/subject/3750104/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('\n' * 5, "response.url:\n", response.url, '\n' * 5)
        
        if "imdb" in response.url.split("."):
            return response.body
        
        page_type_match = {"subject": "movie", "celebrity": "celebrity", "title": "movie", "name": "celebrity"}
        
        storage_path = (os.path.abspath(os.pardir)) + "/local_storage/html_queue/"
        print('\n' * 5, "storage_path:\n", storage_path, '\n' * 5)
        
        page = response.url.split("/")
        page_type = page_type_match[page[3]]
        page_id = page[-2]
        print('\n' * 5, "page_type:\n", page_type, '\n' * 5)
        print('\n' * 5, "page_id:\n", page_id, '\n' * 5)
        filename_douban = page_type + '_' + page_id + "_douban.html"
        filename_imdb = page_type + '_' + page_id + "_imdb.html"
        data = scrapy.Request(url = "https://www.imdb.com/name/nm1169562", callback=self.parse)
        
        
        
        
        print('\n' * 5, "data.response.body:\n", data.body, '\n' * 5)
        
        sys.exit(0)
        
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

