import requests,json,time
from bs4 import BeautifulSoup
from config import *
class proxypool():
    def __init__(self,
                 qiyeurl = QIYE_URL,
                 xiciurl = XICI_URL,
                 china = True,
                 testurl = TEST_URL):
        '''

        :param qiyeurl: the url  to get qiye proxies
        :param xiciurl: the url to get xici proxies
        :param china: boolen, used china proxy or not
        :param testurl: 测试ip是否可用的网站
        '''

        self.qiyeurl = qiyeurl
        self.xiciurl = xiciurl
        self.china = china
        self.testurl = testurl

        self.pool = self.refreshpool()


    def refreshpool(self):
        '''
        build a proxy pool or refresh proxy pool
        :param china: china poxies or not
        :return:
        '''
        if self.china:
            iplist = list(set(self.get_ip_list1()+self.get_ip_list2()))
        else:
            iplist = self.get_ip_list1()
        pool = [{'http': 'http://{}'.format(ip_temp),'https': 'https://{}'.format(ip_temp)} for ip_temp in iplist]
        return pool
    # 使用qiye的IProxy程序获取ip池
    def get_ip_list1(self):
        if self.china:
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
            web_data = requests.get(self.xiciurl, headers=DEFAULT_HEADER)
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

    def pickproxy(self,testurl = None):
        '''
        :param
        :param testurl: (optional) baseurl used to test whether the proxies is useful

        :return:tempproxies, a useful proxies
        '''
        iter_time  =0
        tempproxies = {}
        while iter_time< 2:
            # 代理池里没有代理的话刷新
            if len(self.pool) == 0:
                self.pool = self.refreshpool()
                iter_time += 1
                continue
            # 从代理池中提取一个代理
            tempproxies = self.pool.pop()
            # 检验代理
            if testurl == None:
                testurl = self.testurl
            try:
                res = requests.get(testurl, headers=DEFAULT_HEADER, proxies=tempproxies)
                if res.status_code == 200:
                    res.close()
                    break
            except:
                continue

        if tempproxies == {}:
            print("Warning: don't pick a proper proxies")
        return tempproxies

if __name__ == "__main__":
    url = 'https://www.indiegogo.com/'
    ippool = proxypool(china=False, qiyeurl= 'http://123.206.39.146:8000',testurl=url)
    print(ippool.pickproxy())

