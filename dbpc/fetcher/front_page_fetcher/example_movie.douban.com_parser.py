from bs4 import BeautifulSoup
import sys


with open("movie.douban.com.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

#soup = BeautifulSoup("<html>data</html>")

print(soup.title)


#print(soup.find_all('a'))

#sys.exit(0)
urls = {}

for link in soup.find_all('a'):
    if link.get('href'):
        link = link.get('href')
        if "movie.douban.com/subject" in link:
            url_int = link.split('/')[4]
            urls[url_int] = 0

print(f"total movies:{len(urls)}\n\n{urls}")
#print(links)





