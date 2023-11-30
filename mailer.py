import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class Mailer:
    def __init__(self):
        cfg=Config()
        self.fromaddr = cfg.mail_user
        self.toaddrs  = cfg.mail_to
        self.username = cfg.mail_user
        self.password = cfg.mail_pass
        self.send_mails =  cfg.send_mails

    def send_mail(self,title,body):
        success = False
        if not self.send_mails:
            return
    
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddrs
        msg['Subject'] = title
        msg.attach(MIMEText(body, 'plain'))
        logging.info(f'Sending mail...')

        try:
            # sending mail
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.ehlo()
            server.login(self.username,self.password)
            text=msg.as_string()
            problems = server.sendmail(self.fromaddr, self.toaddrs, text)
            server.quit()
            if problems:
                logging.error(problems)
            else:
                logging.info('Sent.')
                success = True

        except Exception as e:
                err_msg = "Error sending email"
                logging.error( err_msg,str(e) )
        return success        