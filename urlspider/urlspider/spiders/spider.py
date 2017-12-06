import scrapy
from scrapy import Request
from urlparse import *
from urlspider.items import UrlspiderItem
import re

class UrlSpider(scrapy.Spider):
    name="Url"

    def __init__(self,category=None,*args,**kwargs):
        super(UrlSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["%s" % category]

    def parse(self, response):
        urls_list1 = re.findall(r'href="(https?://[^\[\]\<\>\"\']*?\.[^\[\]\<\>\"\']*?)"', response.body)
        urls_list2 = re.findall(r'href=\'(https?://[^\[\]\<\>\"\']*?\.[^\[\]\<\>\"\']*?)\'', response.body)
        urls_list1.extend(urls_list2)
        urls_list3 = []
        for url in urls_list1:
            netloc = urlparse(url)
            urls_list3.append(netloc.scheme + '://' + netloc.hostname)
        s1 = list(set(urls_list3))

        self.start_urls.extend(s1)
        s2 = s1[:]
        s3=','.join(s2)
        for url in s1:
            item = UrlspiderItem()
            item['url'] = url
            
            item['flag']=0
            item['fromWhere'] = response.url

            yield item

        for url in self.start_urls:
            yield Request(url, callback=self.parse)




