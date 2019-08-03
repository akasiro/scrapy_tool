from requests.api import request
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

    def downloadurl(self,url, method = 'get',
                    data=None, headers=None, cookies=None, files=None,
                    auth=None, timeout=None, allow_redirects=True, proxies=None,
                    hooks=None, stream=None, verify=None, cert=None, json=None,
                    max_iter_time = 3, proxiesornot = True, proxies_code  = 0, sleeptime_forerror = 5):
        iter_time = 0
        response = None
        sleeptime = sleeptime_forerror
        send_kwargs = {
            'url' : url,
            'method' : method,
            'data':data,
            'headers':headers,
            'cookies':cookies,
            'files':files,
            'auth':auth,
            'timeout':timeout,
            'allow_redirects':allow_redirects,
            'proxies':proxies,
            'hooks':hooks,
            'stream':stream,
            'verify':verify,
            'cert':cert,
            'json':json}
        if proxiesornot:
            # 确认这个download使用的代理的位置
            if self.proxies.get(proxies_code) == None:
                while True:
                    temp_proxies = self.pp.pickproxy()
                    if temp_proxies not in self.proxies.values():
                        self.proxies[proxies_code] = temp_proxies
                        break
            send_kwargs['proxies'] = self.proxies[proxies_code]
            sleeptime = 0.1
        #确认header的位置
        if self.headers.get(proxies_code) == None:
            while True:
                temp_headers = self.hp.pickheaders()
                if temp_headers not in self.headers.values():
                    self.headers[proxies_code] = temp_headers
                    break
        send_kwargs['headers'] = self.headers[proxies_code]
        # 使用代理和header下载网页
        while iter_time<max_iter_time:
            try:
                response = request(**send_kwargs)
                if response.status_code == 200:
                    break
            except:
                if proxiesornot:
                    self.proxies[proxies_code] = self.pp.pickproxy()
                    send_kwargs['proxies'] = self.proxies[proxies_code]
                self.headers[proxies_code] = self.hp.pickheaders()
                send_kwargs['headers'] = self.headers[proxies_code]
                iter_time +=1
                time.sleep(sleeptime)
        return response

    def downloadurllist(self,urllist,  **kwargs):
        responselist = [self.downloadurl(url=url,**kwargs) for url in urllist]
        return responselist



if __name__ == "__main__":
    baseurl = 'https://www.indiegogo.com'
    url = 'https://www.indiegogo.com/projects/mclassic-the-first-plug-play-graphics-processor#/'
    htmldownloader = htmldownloader(baseurl,qiyeurl= 'http://123.206.39.146:8000',china=False)
    res = htmldownloader.downloadurl(url,proxiesornot=False)
    print(res.status_code)
    print(res.text)


    







