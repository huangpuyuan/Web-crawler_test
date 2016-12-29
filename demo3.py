# -*- coding: utf-8 -*-

import urllib2
import re

#下载函数
def download(url,user_agent='wswp',num_retries=2):#下载,设置用户代理wswp

    print 'Downloading: '+url
    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)#自定义访问
    
    try:
        html=urllib2.urlopen(request).read()#打开链接并读取内容
    except urllib2.URLError as e:
        print 'Download error',e.reason
        html=None
        if num_retries>0:
            if hasattr(e,'code') and 500<=code<600:
                return download(url,headers,proxy,num_retries-1,data)
    return html

import lxml.html
import csv
#回调类
class ScrapeCallback:
    def __init__(self):
        self.writer=csv.writer( open('countris.csv','wb') )
        self.fields=('area','population','iso','country','capital','continent','tld','currency_code','currency_name','phone','postal_code_format','postal_code_regex','languages','neighbours')
        self.writer.writerow(self.fields)

    def __call__(self,url,html):
        if re.search('/view/',url):
            tree=lxml.html.fromstring(html)
            row=[]
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)
            print row,'  |内容'


import urlparse
def link_crawler(seed_url,link_regex,scrape_callback=None):
    crawl_queue=[seed_url]
    seen=set(crawl_queue)
    while crawl_queue:
        url=crawl_queue.pop()
        html=download(url)
        links = []
        if scrape_callback:
            links.extend(scrape_callback(url,html) or [])
        for link in get_links(html):
            #print 'link:',link
            #'''
            if re.match(link_regex,link):#正则比较link是否符合要求
                link=urlparse.urljoin(seed_url,link)#将链接转换为绝对链接
                if link not in seen:
                    seen.add(link)    
                    crawl_queue.append(link)
                    #print url,html
            #'''

def get_links(html):
    #webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)#将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果,re.IGNORECASE忽略大小写
    #print webpage_regex.findall(html)
    #return webpage_regex.findall(html)
    tree=lxml.html.fromstring(html)
    arr=[]
    for e in tree.cssselect('a'):
        #print e.get('href')
        arr.append( e.get('href') )
    #print 'get_links:',tree.cssselect('a')
    return arr

    


link_crawler('http://example.webscraping.com/','/(index|view)',scrape_callback=ScrapeCallback())