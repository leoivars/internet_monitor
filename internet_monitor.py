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
            ip_stat = self.get_ip_from_cache(self.ip)
            if ip_stat['cant'] < 3:
                
                msg = self.get_ips_cache_str()
                self.mailer.send_mail(f'New IP: {self.ip}',msg)
            logging.info(f'{self.ip}')    

    def get_internet_error_time(self):
        if self.internet_error:
            return  time.time() - self.internet_error_time
        else:
            return 0

    def add_ip_to_cache(self,ip):
        if ip in self.ips_cache:
            self.ips_cache[ip]['time'] = time.time()
            self.ips_cache[ip]['cant'] += 1 
        else:
            self.ips_cache[ip]={'time':time.time(),'cant':1}    

    def get_ip_from_cache(self,ip):
        if ip in self.ips_cache:
            return self.ips_cache[ip]
        else:
            None

    def get_ips_cache_str(self):
        # Ordena el diccionario por el valor de 'time' en cada subdiccionario
        ips_ordenados = sorted(self.ips_cache.items(), key=lambda x: x[1]['time'],reverse=True)  
        # Ahora ips_ordenados es una lista de tuplas ordenadas por 'time'
        # Cada tupla contiene (clave, valor) del diccionario original
        ret=''
        for ip, data in ips_ordenados:
            tiempo_legible = datetime.datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')
            ret += f'IP: {ip}, Tiempo: {tiempo_legible}, Cantidad: {data["cant"]}\n'
        return ret          


                









    