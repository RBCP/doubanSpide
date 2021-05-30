# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

header = {'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Connection': 'keep-alive',
      'Host': 'www.jjwxc.net',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
     }

def init(name):
    csvinfo = open(name+'.csv','ab')
    begcsv = csv.writer(csvinfo)
    begcsv.writerow(['作者', '标题', '类型', '积分','发表时间'])
    csvinfo.close()

def getContent(url,name):
    #url='http://www.jjwxc.net/bookbase.php?fw3=3&fbsj=2010&ycx0=0&xx1=1&mainview0=0&sd0=0&lx0=0&fg0=0&collectiontypes=ors&null=0&searchkeywords='
    db_data = requests.get(url, headers=header)
    db_data.encoding = 'gbk'
    soup = BeautifulSoup(db_data.text, 'lxml')
    authors = list()
    titles = list()
    types = list()
    counts = list()
    times = list()
    for idx,tr in enumerate(soup.find_all('tr')):
        if idx !=0:
            tds =tr.find_all('td')
            authors.append(tds[0].contents[1].string)
            titles.append(tds[1].contents[1].string)
            types.append(tds[2].contents[0].string.strip())
            counts.append(tds[6].contents[0].string.strip())
            times.append(tds[7].contents[0].string.strip())
    for author,title,type,count,time in zip(authors,titles,types,counts,times):
        data = [
            (author,title,type,count,time)
        ]
       # print(data)
        csvfile = open(name + '.csv', 'ab')
        writer = csv.writer(csvfile)
        #print(data)
        writer.writerows(data)
        csvfile.close()

def setCsv(name):
    init(name)
    url='http://www.jjwxc.net/bookbase.php?fw3=3&fbsj='+name+'&ycx0=0&xx1=1&mainview0=0&sd0=0&lx0=0&fg0=0&collectiontypes=ors&null=0&searchkeywords='
    getContent(url,name)
    urls =[('http://www.jjwxc.net/bookbase.php?fw3=3&fbsj='+name+'&ycx0=0&xx1=1&mainview0=0&sd0=0&lx0=0&fg0=0&collectiontypes=ors&null=0&searchkeywords=&page={}').format(str(i)) for i in range(2,11)]
    for single_url in urls:
        print(single_url)
        getContent(single_url,name)

if __name__ == '__main__':
    #写入你想爬取小说的年份列表
    years =['2017','2018','2019','2020']
    for year in years:
        setCsv(year)

