# -*- coding: utf-8 -*-

import urllib2
import re

def download(url,user_agent='wswp',num_retries=2):#下载,设置用户代理wswp

    print 'Downloading:',url
    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)#自定义访问
    try:
        html=urllib2.urlopen(request).read()#打开链接并读取内容
    except urllib2.URLError as e:
        print 'Download error',e.reason
        html=None
        if num_retries>0:#重试下载
            if hasattr(e,'code') and 500<=e.code<600:
                return download(url,user_agent,num_retries-1)
    return html

#download('http://httpstat.us/500')

'''
#网站地图爬虫
def crawl_sitmap(url):
    sitemap=download(url)
    links=re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html=download(link)

crawl_sitmap('http://example.webscraping.com/sitemap.xml')
'''

'''
#ID遍历爬虫
import itertools
max_errors=5
num_errors=0
for page in itertools.count(1):
    url='http://example.webscraping.com/view/-%d' % page
    html=download(url)
    if html is None:
        num_errors+=1#累计错误次数
        if num_errors==max_errors:
            break
    else:
        num_errors=0
'''

#链接爬虫
import urlparse
def link_crawler(seed_url,link_regex):
    crawl_queue=[seed_url]
    seen=set(crawl_queue)#设定元组
    while crawl_queue:
        url=crawl_queue.pop()#移除列表最后元素并取得该元素
        html=download(url)
        for link in get_links(html):
            if re.match(link_regex,link):
                link=urlparse.urljoin(seed_url,link)#将相对链接转换为绝对链接
                seen.add(link)
                crawl_queue.append(link)#将访问过的链接加入列表

def get_links(html):
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)#将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果,re.IGNORECASE忽略大小写
    return webpage_regex.findall(html)


link_crawler('http://example.webscraping.com/','/(index|view)')