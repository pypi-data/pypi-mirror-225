import string
import random
import hashlib
import os
from datetime import datetime

__version__ = '1.0.0'


class CustomLib(object):
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def randomString(size):
        return hashlib.md5(os.urandom(128)).hexdigest()[:int(size)]
    
    def get_random_name(self, email_length):
        letters = string.ascii_lowercase[:12]
        return ''.join(random.choice(letters) for i in range(email_length))
    
    def getvalidEmail():
        email = ['pallav.kumar@capillarytech.com']
        return random.choice(email)
    
    def generate_random_emails(self, length):

        domains = ["hotmail.com", "gmail.com", "aol.com",
                   "mail.com", "mail.kz", "yahoo.com"]

        return [self.get_random_name(length)
                + '@'
                + random.choice(domains)]
    
    def generate_random_mobile(self,countryCode='91'):
        if countryCode == '91':
            return countryCode + str(random.randint(7000000000, 8999999999))
    
    def generate_random_name(self,size=7):
        return self.get_random_name(size)
    
    def get_today_datetime(self,format="%Y-%m-%d %H:%M:%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string
    
    def get_time(self,format="%Y-%m-%d %H:%M:%S"):
        now = datetime.now()
        dt_string = now.strftime(format)
        return dt_string
    
    def update_result_to_apitester(self,testStatus,testMessage):
        print("Result updated",testStatus, testMessage)