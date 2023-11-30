import time
import datetime
import logging
from   internet_is_working import Is_internet_working
from   internet_whatis_my_ip import Whatis_my_ip
from   mailer import Mailer

class Internet_monitor:

    def __init__(self) -> None:
        self.what_is_my_ip = Whatis_my_ip()
        self.the_internet = Is_internet_working()
        self.last_ip=None
        self.ip=None
        self.ip_time=time.time()
        self.internet_error = False
        self.internet_error_time=time.time()
        self.ips_cache={}
        self.mailer = Mailer()

    def update_internet_state(self):
        if not self.the_internet.get_some_respone():
            if not self.internet_error:
                self.internet_error = True
                self.internet_error_time = time.time()
            return     
        
        self.internet_error = False
        self.last_ip = self.ip
        self.ip = self.what_is_my_ip.get_ip()
        if self.ip != self.last_ip:
            self.add_ip_to_cache(self.ip)

    def mail_new_ips(self):
        for ip, data in self.sorted_ips():
            if not data['mail']:
                logging.info(f'new ip: {self.ip}')    
                msg = self.get_ips_cache_str()
                success = self.mailer.send_mail(f'New IP: {ip}',msg)
                if success:
                    self.ips_cache[ip]['mail']=True
                    break

    def get_internet_error_time(self):
        if self.internet_error:
            return  time.time() - self.internet_error_time
        else:
            return 0

    def add_ip_to_cache(self,ip):
        if ip in self.ips_cache:
            self.ips_cache[ip]['time'] = time.time()  #time of new ip detected
            self.ips_cache[ip]['qty'] += 1            #quantity that ip has been assigned
            self.ips_cache[ip]['mail'] = False        #False = An email notifying about the new IP has not been successfully sent.
        else:
            self.ips_cache[ip]={'time':time.time(),'qty':1,'mail':False}    

    def get_ip_from_cache(self,ip):
        if ip in self.ips_cache:
            return self.ips_cache[ip]
        else:
            None

    def sorted_ips(self):
        # Sort the dictionary by the 'time' value in each subdictionary.
        return sorted(self.ips_cache.items(), key=lambda x: x[1]['time'],reverse=True)  
    
    def get_ips_cache_str(self):
        ret=''
        for ip, data in self.sorted_ips():
            huma_time = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')
            ret += f'IP: {ip}, Time: {huma_time}, qty: {data["qty"]}\n'
        return ret          


                



    