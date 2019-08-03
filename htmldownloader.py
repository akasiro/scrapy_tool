import requests
from proxypool import *
from headerpool import *

class htmldownloader():
    def __init__(self,baseurl, **proxypoolkwargs):
        '''

        :param baseurl:
        :param china: (optional) 使用国内代理还是国外代理
        :param qiyeurl: (optional) 获取七夜代理的地址
        :param xiciurl: (optional) 获取西刺代理的地址
        '''
        self.pp = proxypool(testurl=baseurl,**proxypoolkwargs)
        self.hp = headerpool()
        # 代理和header缓存器，每个downloadurl动作可以使用不同代理和header帮助实现多线程
        self.proxies = {}
        self.headers = {}

    def downloadurl(self,url, max_iter_time = 3, proxiesornot = True, proxies_code  = 0):
        iter_time = 0
        response = None
        if proxiesornot:
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
            # 使用代理和header下载网页
            while iter_time<max_iter_time:
                try:
                    response = requests.get(url,proxies = self.proxies[proxies_code], headers = self.headers[proxies_code])
                    if response.status_code == 200:
                        break
                except:
                    self.proxies[proxies_code] = self.pp.pickproxy()
                    self.headers[proxies_code] = self.hp.pickheaders()
                    iter_time +=1
                    time.sleep(0.1)
        else:
            while iter_time<max_iter_time:
                try:
                    temp_headers = self.hp.pickheaders()
                    response = requests.get(url,headers = temp_headers)
                    if response.status_code == 200:
                        break
                except:
                    iter_time += 1
                    time.sleep(5)
        return response

    def downloadurllist(self,urllist,  **kwargs):
        responselist = [self.downloadurl(url,**kwargs) for url in urllist]
        return responselist



if __name__ == "__main__":
    baseurl = 'https://www.indiegogo.com/'
    url = 'https://www.indiegogo.com/projects/mclassic-the-first-plug-play-graphics-processor/hmco'
    htmldownloader = htmldownloader(baseurl,qiyeurl= 'http://123.206.39.146:8000',china=False)
    res = htmldownloader.downloadurl(url,proxiesornot=False)
    print(res.status_code)
    print(res.text)


    







