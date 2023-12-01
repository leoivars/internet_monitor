import time
import logging
from internet_monitor import Internet_monitor
from functions import lnow

logging.basicConfig(level=logging.INFO)
wait_interval = 300

i = Internet_monitor()

while True:
    
    i.update_internet_state()
    time_error = i.get_internet_error_time()
  
    if time_error ==0:
        logging.info(f'{lnow()} Internet is working')
        i.mail_new_ips()
    else:
        logging.error(f'{lnow()} Interneet in NO working since {time_error}') 

    logging.info(f'{lnow()} Waiting {wait_interval}')
    time.sleep(wait_interval)