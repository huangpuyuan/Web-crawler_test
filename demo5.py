# -*- coding: utf-8 -*-

import urllib2
import re

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

#下载函数
def download(url,user_agent='wswp',num_retries=5):#下载,设置用户代理wswp,打开页面失败重试次数 num_retries

    print 'Downloading: '+url#显示下载的文件
    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)#自定义访问
    
    try:
        html=urllib2.urlopen(request).read()#打开链接并读取内容
    except urllib2.URLError as e:
        print 'Download error | '+e.reason
        html=None
        if num_retries>0:
            #if hasattr(e,'code') and 500<=code<600:
            return download(url,headers,num_retries-1)
    return html

import lxml.html
#import csv
import os
import codecs
import HTMLParser
#回调类
class ScrapeCallback:
    def __init__(self,name):
        self.name=unicode(name,'utf-8')#对中文名进行编码
        #print self.name+'.txt'
        self.fp=codecs.open(self.name+'.txt', 'a', 'utf-8')#使用codecs打开文件防止文中编码问题
        #fp = codecs.open(‘output.txt’, ‘a+’, ‘utf-8’);;

    def __call__(self,url,html):
        #if re.search('/view/',url):
        tree=lxml.html.fromstring(html)
        #print tree.cssselect('div#content')
        if tree.cssselect('div#content'):
            #取得页面内容
            title=tree.cssselect('div.box_con > div.bookname > h1')[0].text_content()
            self.fp.write( title )
            self.fp.write('\n\r')
            #text=tree.cssselect('div.box_con > div#content')[0].text_content()
            text=lxml.html.tostring(tree.cssselect('div.box_con > div#content')[0])

            html_parser = HTMLParser.HTMLParser()
            text = html_parser.unescape(text)
            text = re.sub('<br><br>', '\n\r', text)
            text = re.sub('<div id=\"content\"><script>readx\(\);', '', text)
            text = re.sub('</script>', '', text)
            text = re.sub('</div>', '', text)
  
            self.fp.write( text )
            self.fp.write('\n\r\n\r\n\r ')


import urlparse
def link_crawler(seed_url,scrape_callback=None,delay=-1):#delay打开页面间隔时间
    crawl_queue=[seed_url]#设置需要下载的链接
    seen=set(crawl_queue)#存放已下载链接
    #print seed_url,scrape_callback
    throttle = Throttle(delay)#下载限速
    
    while crawl_queue:
        url=crawl_queue.pop()#取出要下载的链接
        throttle.wait(url)#设置间隔时间
        html=download(url)
        links = []
        if scrape_callback:
            links.extend(scrape_callback(url,html) or [])
        for link in get_links(html):
            link=urlparse.urljoin(seed_url,link)#将链接转换为绝对链接
            if link not in seen:
                seen.add(link)#添加已经下载的链接
                crawl_queue.append(link)#添加需要下载的链接
    

def get_links(html):
    tree=lxml.html.fromstring(html)
    arr=[]
    #分析并组成下载链接组
    for e in tree.cssselect('div.box_con > div#list > dl > dd > a'):
        #print e.get('href')
        arr.append( e.get('href') )
    arr.reverse()
    return arr

 #下载限速
import time
from datetime import datetime
class Throttle:
    def __init__(self,delay):
        self.delay=delay
        self.domains={}
    def wait(self,url):
        domain=urlparse.urlparse(url).netloc
        last_accessed=self.domains.get(domain)

        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay-(datetime.now()-last_accessed).seconds
            if sleep_secs>0:
                time.sleep(sleep_secs)
        self.domains[domain]=datetime.now()
   


link_crawler('http://www.qu.la/book/401/',scrape_callback=ScrapeCallback('凡人修仙传'))