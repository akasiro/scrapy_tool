import requests
from proxypool import *
from headerpool import *
class htmldownloader():
    def __init__(self,baseurl):
        self.pp = proxypool(testurl=baseurl)
        self.hp = headerpool()
        self.proxies = {}
        self.headers = {}

    def downloadurl(self,url, max_iter_time = 2, sleeptime = 5, proxies_code  = 0):
        # 确认这个download使用的代理和headers的位置
        if self.proxies.get(proxies_code) == None:
            while True:
                temp_proxies = self.pp.pickproxy()
                if temp_proxies not in self.proxies.values():
                    self.proxies[proxies_code] = temp_proxies
                    break
        if self.headers.get(proxies_code) == None:
            while True:
                temp_headers = self.hp.pickheaders()
                if temp_headers not in self.headers.values():
                    self.headers[proxies_code] = temp_headers
                    break

        iter_time = 0
        while True:
            if iter_time == max_iter_time:
                response = None
                break
            try:
                response = requests.get(url,poxies = self.proxies[proxies_code], headers = self.headers[proxies_code])
                if response.status_code == 200:
                    break
            except:
                self.proxies[proxies_code] = self.pp.pickproxy()
                self.headers[proxies_code] = self.hp.pickheaders()
                iter_time +=1
                time.sleep(0.1)
        time.sleep(sleeptime)
        return response

    def downloadurllist(self,urllist,max_iter_time = 2, sleeptime = 5, proxies_code  = 0):
        responselist = [self.downloadurl(url,max_iter_time,sleeptime,proxies_code) for url in urllist]
        return responselist

    







