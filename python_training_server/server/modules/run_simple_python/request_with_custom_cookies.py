"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime
from main.core.utils import log_data

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class REQUEST_WITH_CUSTOM_COOKIES:
    REQUEST_METHOD_SUPPORTED = ["GET","POST"]
    TRAIN_ID = "TRAIN-01-07"
    def __init__(self,request):
        self.request = request
        self.cookies = request.COOKIES
        self.result = {"Data":"Try Harder"}
    
    def make_flag(self,user):
        """
        params:
            user(object):represents the object of a user (from sql)
        return:
            flag(str):represents a unique flag crafted
        """
        now = datetime.now()
        flag = sha256(f"{str(now.microsecond)}{user.UserId}".encode()).hexdigest()
        return flag

    def process(self,user):
        """
        params:
            user(object):represents the object of a user (from sql)
        return:
            result(dict):represents a dictionary with the result
        """
        if not self.request.method in self.REQUEST_METHOD_SUPPORTED:
            self.result["Data"] = "Method not allowed!"
            return self.result

        if not "python" in self.request.META['HTTP_USER_AGENT']:
            self.result["Data"] = "You have to use python!!"
            return self.result

        try:  

            if self.cookies['session'] != user.UserId:
                self.result["Data"] = "Please make sure you passed the right session token and try again :)"
            else:
                # Updates user database
                flag = self.make_flag(user)
                self.result["Data"] = f"Good job! Here's your flag: \nFlag: {flag}"
                user.Hash_check = flag

                if self.TRAIN_ID not in user.Passed_modules:
                    user.Passed_modules.append(self.TRAIN_ID)
                    
                user.save()
        
        except Exception as e:
            log_data.log_debug(e)
            self.result['Data'] = "You can't access this resource. Missing cookie: session"
    
        return self.result