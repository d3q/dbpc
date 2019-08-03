import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')
# 不发出警告


#数据的采集

u="https://movie.douban.com/subject/26100958/comments?start=0&limit=20&sort=new_score&status=P"
r=requests.get(url=u)
r.encoding='utf-8'
#print(r,type(r))

soup=BeautifulSoup(r.text)   #在访问网页
#print(soup)

infor_lst=soup.find('div',id='comments').find_all('div',class_='comment-item') #定位到相应的短评
#print(infor_lst)

dic = {}  #定义一个字典

for infor in infor_lst[:1]:
    dic['viewer']=infor.find('span',class_='comment-info').find('a').text
    dic['score']=infor.find('span',class_='comment-info').find_all('span')[1]['class'][0][-2:]
    dic['time']=infor.find('span',class_='comment-time').text.replace(' ','').replace('\n','')
    dic['number']=int(infor.find('span',class_='votes').text)
    dic['content']=infor.find('p').text.replace('\n','')
#print(dic)

#以上为整个数据采集测试部分

#以下为网页数据获取函数
def get_data(url):
    try:
        r1 = requests.get(url=u1)
        r1.encoding = 'utf-8'
        soup1 = BeautifulSoup(r1.text)  # 在访问网页
        infor_lst1 = soup1.find('div', id='comments').find_all('div', class_='comment-item')  # 获取所有标签
        datalist = [] # 定义一个数组
        for infor in infor_lst1[:]:
            dic = {}  # 定义一个字典
            dic['viewer'] = infor.find('span', class_='comment-info').find('a').text
            dic['score'] = int(infor.find('span', class_='comment-info').find_all('span')[1]['class'][0][-2:])
            dic['time'] = infor.find('span', class_='comment-time').text.replace(' ', '').replace('\n', '')
            dic['number'] = int(infor.find('span', class_='votes').text)
            dic['content'] = infor.find('p').text.replace('\n', '')
            datalist.append(dic)
        return datalist
    except:
        return []

u1='https://movie.douban.com/subject/26100958/comments?start=0&limit=20&sort=new_score&status=P'
#print(get_data(u1)[:2])

#以下为构建页面URL函数
def get_urls(n):
    urllst = []  #定义一个数组
    for i in range(n):
        urllst.append('https://movie.douban.com/subject/26100958/comments?start=%i&limit=20&sort=new_score&status=P'%(i*20))
    return urllst

urllsts=get_urls(50)
#print(urllsts[:3])

#获取批量数据

datalst1=[]
n=1
for u1 in urllsts:
    datalst1.extend(get_data(u1))
    print('get%inumbers of data'%(n*20))
    n += 1
print(datalst1[:2])

df=pd.DataFrame(datalst1)
print(df.iloc[:10])
