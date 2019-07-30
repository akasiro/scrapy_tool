import requests,json,time
from bs4 import BeautifulSoup

class proxypool():
    def __init__(self,qiyeurl = 'http://localhost:8000', xiciurl = 'http://www.xicidaili.com/wn/',china = True, testurl = 'http://www.baidu.com'):
        '''

        :param qiyeurl: the url  to get qiye proxiey
        :param xiciurl: t
        :param china: boolen, used china proxy or not
        :param testurl: 测试ip是否可用的网站
        '''
        self.Default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        self.qiyeurl = qiyeurl
        self.xiciurl = xiciurl
        self.china = china
        self.testurl = testurl

        self.pool = self.refreshpool(self.china)


    def refreshpool(self,china = True):
        '''
        build a proxy pool or refresh proxy pool
        :param china: china poxies or not
        :return:
        '''
        if china:
            iplist = self.get_ip_list1(china)+self.get_ip_list2()
        else:
            iplist = self.get_ip_list1(china)
        pool = [{'http': 'http://{}'.format(ip_temp),'https': 'https://{}'.format(ip_temp)} for ip_temp in iplist]
        return pool
    # 使用qiye的IProxy程序获取ip池
    def get_ip_list1(self,china):
        if china:
            country = '国内'
        else:
            country = '国外'
        try:
            r = requests.get('{}/?county={}'.format(self.qiyeurl,country))
            ip_list = ['{}:{}'.format(ipport[0], ipport[1]) for ipport in json.loads(r.text)]
        except:
            ip_list = []
        return ip_list

    #从西刺代理直接爬取获取ip池
    def get_ip_list2(self):
        try:
            web_data = requests.get(self.xiciurl, headers=self.Default_headers)
            soup = BeautifulSoup(web_data.text, 'html.parser')
            ips = soup.find_all('tr')
            ip_list = []
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_list.append(tds[1].get_text() + ":" + tds[2].get_text())
        except:
            ip_list = []
        return ip_list

    def pickproxy(self,**kwargs):
        '''
        :param
        :param url: (optional) baseurl used to test whether the proxies is useful

        :return:tempproxies, a useful proxies
        '''
        iter_time  =0
        tempproxies = {}
        while iter_time< 2:
            # 代理池里没有代理的话刷新
            if len(self.pool) == 0:
                self.pool = self.refreshpool(self.china)
                iter_time += 1
                continue
            # 从代理池中提取一个代理
            tempproxies = self.pool.pop()
            # 检验代理
            if kwargs.get('url') != None:
                testurl = kwargs.get('url')
            else:
                testurl = self.testurl
            try:
                res = requests.get(testurl, headers=self.Default_headers, proxies=tempproxies, timeout=1)
                if res.status_code == 200:
                    res.close()
                    break
            except:
                continue

        if tempproxies == {}:
            print("Warning: don't pick a proper proxies")
        return tempproxies

if __name__ == "__main__":
    ippool = proxypool()
    print(ippool.pickproxy())

