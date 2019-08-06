import scrapy
import sys
import os.path
import json
import urllib.parse
from bs4 import BeautifulSoup


class FrontPageFetcher(scrapy.Spider):
    name = "douban_front_page_dynamic"
    
    def __init__(self):
        pass

    def start_requests(self):
        
        urls = [
            "https://movie.douban.com/j/search_tags?type=movie&tag=%E7%83%AD%E9%97%A8&source=index",
            "https://movie.douban.com/j/search_tags?type=tv&tag=%E7%83%AD%E9%97%A8&source=index"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #print('\n' * 10)
        self.log(f"This page is: {response.url.split('/')[-1].split('?')[0]}")
        
        if response.url.split("/")[-1].split("?")[0] == "search_tags":
            tags_to_query_type = response.url.split("/")[-1].split("=")[1].split("&")[0]
            #print(tags_to_query_type)
            tags_to_query = response.body.decode("utf-8")
            #print(tags_to_query)
            tags_to_query = json.loads(tags_to_query)
            tags_to_query[tags_to_query_type] = tags_to_query.pop("tags")
            #print(tags_to_query)
            self.log(f"Found tags: {tags_to_query}")
            
            
            for tag in tags_to_query[tags_to_query_type]:
                #print(tag)
                url = "https://movie.douban.com/j/search_subjects?type=" + tags_to_query_type + "&tag="
                url = url + tag + "&page_limit=50&page_start=0"
                #print(url)
                #url = urllib.parse.quote(url)
                #print(url)
                #%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&page_limit=50&page_start=0"
                #urllib.parse.quote(query)
                yield scrapy.Request(url=url, callback=self.parse)
            
        elif response.url.split("/")[-1].split("?")[0] == "search_subjects":
            #print(response.body.decode("utf-8"))
            #print(response.url.split("/")[-1].split('=')[2].split('&')[0])
            tag_decode = urllib.parse.unquote(response.url.split("/")[-1].split('=')[2].split('&')[0])
            self.log(f"Found movie lists under: {tag_decode}")
            movie_list = response.body.decode("utf-8")
            movie_list = json.loads(movie_list)
            to_json = []
            #print(movie_list)
            for item in movie_list["subjects"]:
                #print(item["url"].split('/')[-2])
                to_json.append(item["url"].split('/')[-2])
            
            self.log(f"Found movie ids: {to_json}")
            
            to_url_queue = {}
        
            for url in to_json:
                to_url_queue["movie" + url] = {
                    "min_depth": 0,
                    "status_code": 555
                }
                
            #print('\n' * 5, "to_url_queue:\n", to_url_queue, '\n' * 5)
            
            
            url_queue_file = (os.path.abspath(os.pardir)) + "/local_storage/url_queue.json"
        
            #print(os.stat(url_queue_file).st_size)
            self.log(f"Opening URL queue...")
        
            if os.stat(url_queue_file).st_size == 0:
                in_url_queue = {}
            else:
                with open(url_queue_file, 'r') as f:
                    in_url_queue = json.load(f)
            
            self.log(f"URL queue opened: {len(in_url_queue)} items.")
            
            in_url_queue.update(to_url_queue)
            #print('\n' * 5, "in_url_queue:\n", in_url_queue, '\n' * 5)
            
            self.log(f"URL queue updating... Now there're {len(in_url_queue)} items. Saving file...")

            with open(url_queue_file, 'w') as f:
                json.dump(in_url_queue, f, indent=4)
            
            self.log(f"Saved to {url_queue_file}.")
            