import logging
from requests import get

class Is_internet_working:

    def __init__(self):
        # https://wtfismyip.com/json ésta me paració simpatica..
        self.urls=["https://www.google.com/",
                   "https://www.facebook.com/",
                   "https://github.com/",
                   "https://www.uptrends.com/tools/uptime",
                   "https://www.pingdom.com/",
                   "https://www.statuscake.com/",
                   "https://www.site24x7.com/",
                   "https://www.clarin.com/",
                   "https://digital.elmercurio.com/",
                   "https://espanol.yahoo.com/",
                   "https://edition.cnn.com/",
                   "https://www.alertra.com/",
                   "https://www.siteuptime.com/",
                   "https://www.host-tracker.com/",
                   "https://www.mdzol.com/",
                   "https://web.whatsapp.com/",
                   "https://www.tradingview.com/",
                   "https://www.binance.com/",
                   "https://www.binance.com/",
                   "https://www.w3schools.com/",
                   "https://wikipedia.org/",
                   "https://stackoverflow.com/"

                  ]
        self.nexurl = 0

    def get_next_url(self):
        url = self.urls[self.nexurl]
        self.nexurl += 1
        if self.nexurl == len(self.urls):
            self.nexurl = 0
        return url

    def get_some_respone(self):
        response = None
        for _ in range(5):
            url = self.get_next_url()
            response=self.response_from_url(url)
            if response:
                break
        return response

    def get_respone(self):
        response = None
        url = self.get_next_url()
        response=self.response_from_url(url)
        return response    

    def response_from_url(self,url):
        try:
            response = get(url)
        except Exception as e:
            response = None
            logging.error(str(e)[:10])

        return response    
               

if __name__=="__main__":
    import time
    theinternet = Is_internet_working()
    for _ in range(len(theinternet.urls)):
        i = theinternet.nexurl
        t = time.time()
        if theinternet.get_respone():
            logging.info(f'{theinternet.urls[i]} OK {round(time.time() -t,2)}')
        else:
            logging.error(f'{theinternet.urls[i]}        ERROR')    

    for _ in range(8):
        t = time.time()
        if theinternet.get_respone():
            logging.info(f'OK {round(time.time() -t,2)}')
        else:
            logging.error(f'ERROR')  
