"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class FIRST_GET_REQUEST:
    REQUEST_METHOD_SUPPORTED = "GET"
    TRAIN_ID = "TRAIN-01-01"
    def __init__(self,request):
        self.request = request
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
        if self.request.method != self.REQUEST_METHOD_SUPPORTED:
            self.result["Data"] ="You've made a POST request, not a GET request!"
            return self.result

        if not "python" in self.request.META['HTTP_USER_AGENT']:
            self.result["Data"] ="You have to use python!!"
            return self.result

        if not len(self.request.GET):
            # Updates user database
            flag = self.make_flag(user)
            user.Hash_check = flag
            user.save()
            
            self.result["Data"] =f"""
                        
                            Great Job!
                        You can proceed!
                        Flag:{flag}
                        
                        """
            
        return self.result

