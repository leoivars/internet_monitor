
import ipaddress
import json
import random
import logging
from requests import get

class Whatis_my_ip:

    def __init__(self):
        # https://wtfismyip.com/json ésta me paració simpatica..
        self.urls=["https://api.ipify.org",
                   "https://api.myip.com",
                   "https://api.my-ip.io/ip",
                   "https://ipinfo.io/json",
                   "https://ipapi.co/json/",
                   "http://ip-api.com/json/",
                   "http://ip-api.org/json",
                   "https://ip.seeip.org/",
                   "https://ip.42.pl/raw",
                   "https://ip.tyk.nu/",
                   "https://l2.io/ip",
                   "https://myexternalip.com/raw",
                   "https://wtfismyip.com/json",
                   "https://jsonip.com/",
                   "https://www.trackip.net/ip",
                  ]
        self.headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Expires': '0'}

        self.nexurl = random.randint(0, len(self.urls)-1)

    def get_next_url(self):
        url = self.urls[self.nexurl]
        self.nexurl += 1
        if self.nexurl == len(self.urls):
            self.nexurl = 0
        return url

    def get_ip(self):
        ip=None
        for i in range(5):
            url = self.get_next_url()
            logging.info(f'Testing from {url}')
            ip=self.ip_from_url(url)
            if ip:
                logging.info(f'{ip}')
                break
            logging.error(f'fail {i}')
        return ip

    def ip_from_url(self,url):
        try: 
            respose = get(url,headers=self.headers).content.decode('utf8')
            if "{" in respose:
                ip = self.parse_ip_from_json(json.loads(respose.lower()))
            else:
                ip = self.parse_ip(respose)
        except:
            ip = None        
        
        return ip        

    def parse_ip_from_json(self,json:dict):
        ip=None
        if 'ip' in json.keys():
            ip = self.parse_ip(json['ip'])
        for key in json.keys():
            if ip:
                break
            ip = self.parse_ip(json[key])
        return ip    

    def parse_ip(self,ip):
        ip = str(ip)
        if 7 > len(ip) <15:
            return None
        try:
            ipaddress.ip_address(ip)
            return ip
        except:
            return None    

if __name__=="__main__":
    import time
    wmyip = Whatis_my_ip()
    for _ in range(len(wmyip.urls)):
        ip = wmyip.get_ip()
        if ip:
            logging.info(f'{ip} OK')
        
        
