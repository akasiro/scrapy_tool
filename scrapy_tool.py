# -*- coding: utf-8 -*-
import requests, time, json,os
import random
from bs4 import BeautifulSoup

class scrapy_tool():
    def __init__(self, test_url = 'http://www.baidu.com', china = True):
        self.Default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        path = os.path.dirname(__file__)
        with open(os.path.join(path,'user_agent'),'r') as f:
            self.list_user_agent = f.readlines()
        self.china = china
        self.test_url = test_url
        self.ip_list = list(set(self.get_ip_list1()+ self.get_ip_list2()))
        self.proxies = {}

    #获取随机header
    def random_headers(self):
        headers = {
            'User-Agent': random.choice(self.list_user_agent).replace('\n','')
        }
        return headers

    #获取随机代理ip
    def random_proxy(self):
        while True:
            if len(self.ip_list) == 0:
                break
            ip_temp = random.choice(self.ip_list)
            proxies_temp = {
                'http': 'http://{}'.format(ip_temp),
                'https': 'https://{}'.format(ip_temp)
            }
            try:
                res = requests.get(self.test_url,headers = self.Default_headers, proxies = proxies_temp, timeout = 1)
                if res.status_code == 200:
                    res.close()
                    self.proxies = proxies_temp
                    break
                else:
                    res.close()
                    self.ip_list.remove(ip_temp)
            except:
                self.ip_list.remove(ip_temp)
                time.sleep(0.1)
        return self.proxies

    #使用qiye的IProxy程序获取ip池
    def get_ip_list1(self):
        if self.china:
            country = '国内'
        else:
            country = '国外'
        ip_list = []
        try:
            r = requests.get('http://localhost:8000/?types=0&county={}'.format(country))
            ip_ports = json.loads(r.text)
            for ipport in ip_ports:
                ip_list.append('{}:{}'.format(ipport[0], ipport[1]))
        except:
            ip_list = []
        return ip_list

    #直接爬取获取ip池
    def get_ip_list2(self):
        url = 'http://www.xicidaili.com/wn/'

        ip_list = []
        try:
            web_data = requests.get(url, headers=self.Default_headers)
            soup = BeautifulSoup(web_data.text, 'html.parser')
            ips = soup.find_all('tr')
            ip_list = []
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_list.append(tds[1].get_text() + ":" + tds[2].get_text())
        except:
            pass
        return ip_list
    #刷新ip池
    def refresh_ip_pool(self):
        self.ip_list = list(set(self.get_ip_list1() + self.get_ip_list2()))
    #换代理ip
    def change_proxy(self):
        if self.proxies != {}:
            self.ip_list.remove(self.proxies['http'].replace('http://',''))
            self.proxies = {}
        return self.random_proxy()






if __name__ == '__main__':
    url = 'https://www.boundhub.com/'
    st = scrapy_tool(url,china= False)
    print(st.random_headers())
    print(st.random_proxy())
    print(st.change_proxy())
