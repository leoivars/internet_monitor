import time
import logging
from internet_monitor import Internet_monitor

logging.basicConfig(level=logging.INFO)
wait_interval = 600

i = Internet_monitor()

while True:
    i.update_internet_state()
    time_error = i.get_internet_error_time()
  
    if time_error ==0:
        logging.info('Internet is working')
        i.mail_new_ips()
    else:
        logging.error(f'Interneet in NO working since {time_error}') 

    logging.info(f'Waiting {wait_interval}')
    time.sleep(wait_interval)