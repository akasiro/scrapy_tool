from dataoutput import dataoutput
from htmldownloader import htmldownloader
from htmlparser import htmlpaser
from urlmanager import urlmanager
from config import *
class spiderman():
    def __init__(self,baseurl):
        self.urlmanager = urlmanager()
        self.htmldownloader = htmldownloader(baseurl = baseurl)
        self.htmlparser = htmlpaser()
        self.dataoutput = dataoutput()

        self.max_iter_time = max_iter_time
        self.sleeptime = sleeptime

    def crawl(self,proxies_code = 0):
        while self.urlmanager.has_new_url():
            # 提取一个未爬取的url
            url = self.urlmanager.get_new_url()
            #  下载html
            res = self.htmldownloader.downloadurl(url,max_iter_time=self.max_iter_time,sleeptime=self.sleeptime, proxies_code=proxies_code)
            # 下载失败的话记录一下
            if res == None:
                self.urlmanager.add_error_url(url)
                print("error: {}".format(url))
            # 下载成功保存
            else:
                data = self.htmlparser.paser(res)
                urls = self.htmlparser.get_new_url(res)
                self.urlmanager.add_new_urls(urls)
                self.dataoutput.savedata(data)
                self.urlmanager.add_used_url(url)
                print('success: {}'.format(url))

