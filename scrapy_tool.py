# -*- coding: utf-8 -*-
import requests, time
import random, json
from bs4 import BeautifulSoup

class scrapy_tool():
    def __init__(self):
        self.Default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

        with open('user_agent','r') as f:
            self.list_user_agent = f.readlines()

        self.ip_list = list(set(self.get_ip_list1()+ self.get_ip_list2()))

    def random_headers(self):
        headers = {
            'User-Agent': random.choice(self.list_user_agent).replace('\n','')
        }
        return headers

    def random_proxy(self, test_url = 'http://www.baidu.com'):
        proxies = None
        while True:
            if len(self.ip_list) == 0:
                break
            ip_temp = random.choice(self.ip_list)
            proxies_temp = {
                'http': 'http://{}'.format(ip_temp),
                'https': 'https://{}'.format(ip_temp)
            }
            try:
                res = requests.get(test_url,headers = self.Default_headers, proxies = proxies, timeout = 2)
                if res.status_code == 200:
                    res.close()
                    proxies = proxies_temp
                    break
                else:
                    res.close()
                    self.ip_list.remove(proxies_temp)
            except:
                self.ip_list.remove(proxies_temp)
                time.sleep(0.5)
        return proxies

    #使用qiye的IProxy程序获取ip
    def get_ip_list1(self):
        ip_list = []
        try:
            r = requests.get('http://127.0.0.1:8000/?types=0&county=国内')
            ip_ports = json.loads(r.text)
            for ipport in ip_ports:
                ip_list.append('{}:{}'.format(ipport[0], ipport[1]))
        except:
            ip_list = []
        return ip_list

    #直接爬取获取ip
    def get_ip_list2(self):
        url = 'http://www.xicidaili.com/wn/'

        ip_list = []
        try:
            web_data = requests.get(url, headers=self.Default_headers)
            soup = BeautifulSoup(web_data.text, 'lxml')
            ips = soup.find_all('tr')
            ip_list = []
            for i in range(1, len(ips)):
                ip_info = ips[i]
                tds = ip_info.find_all('td')
                ip_list.append(tds[1].get_text() + ":" + tds[2].get_text())
        except:
            pass
        return ip_list





if __name__ == '__main__':
    url = 'http://aso.niaogebiji.com'
    st = scrapy_tool()
    print(st.random_headers())
    print(st.random_proxy())
