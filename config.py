import os
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.mail_user        = os.getenv('MAIL_USER', '?')
        self.mail_pass        = os.getenv('MAIL_PASS', '?')
        self.mail_to          = os.getenv('MAIL_TO', '?')
        self.send_mails       = 'YES' ==  os.getenv('BOT_SEND_MAILS', '?').upper()
        
