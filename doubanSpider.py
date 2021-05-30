# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

hds =[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
# 请求头设置
header = {
    'Accept': '*/*;',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}


# 初始化csv文件
def info(name):
    csvinfo = open(name + '.csv', 'ab')
    begcsv = csv.writer(csvinfo)
    begcsv.writerow(['titles', 'authors', 'nums', 'peoples'])
    csvinfo.close()


# 爬取指定name模块的url,并存储至name.csv文件
def web(url, name):
    db_data = requests.get(url, headers=header)
    db_data.encoding ='utf-8'
    soup = BeautifulSoup(db_data.text, 'lxml')
    titles = soup.select('#subject_list > ul > li > div.info > h2 > a')
    authors = soup.select('#subject_list > ul > li > div.info > div.pub')
    nums = soup.select('#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums')
    peoples = soup.select('#subject_list > ul > li > div.info > div.star.clearfix > span.pl')
    for title, author, num, people in zip(titles, authors, nums, peoples):
        data = [
            (
                title.get('title'),
                author.get_text().replace(' ', '').replace("\n", ""),
                num.get_text().replace(' ', '').replace("\n", ""),
                people.get_text().replace(' ', '').replace("\n", "")
            )
        ]
        csvfile = open(name + '.csv', 'ab')
        writer = csv.writer(csvfile)
        print(data)
        writer.writerows(data)
        csvfile.close()


# name模块标签分页  指定为前50页
def setCsv(name):
    url = 'https://book.douban.com/tag/' + name
    urls = [('https://book.douban.com/tag/' + name + '?start={}&type=T').format(str(i)) for i in range(20, 980, 20)]
    info(name=name)
    web(url, name)
    for single_url in urls:
        print(single_url)
        web(single_url, name=name)

if __name__ == '__main__':
    setCsv('晋江')  #str为标签名