"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime
import json

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class POST_REQUEST_JSON_DATA:
    REQUEST_METHOD_SUPPORTED = "POST"
    TRAIN_ID = "TRAIN-01-05"
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
        if self.request.method !=self.REQUEST_METHOD_SUPPORTED:
            self.result["Data"] ="You've made a GET request, not a POST request!"
            return self.result

        if not "python" in self.request.META['HTTP_USER_AGENT']:
            self.result["Data"] ="You have to use python!!"
            return self.result

        if not len(self.request.POST):
            self.request["Data"] = "You didn't provide any data!"
            return self.result

        if "code" in self.request.POST:
            # Pass user and add the module to the passed one's list 
            if len(self.request.POST['code']) > 5:
                    if self.TRAIN_ID not in user.Passed_modules:
                        user.Passed_modules.append(self.TRAIN_ID)

                # Updates user database
                    flag = self.make_flag(user)
                    user.Hash_check = flag
                    user.save()

                    self.result["Data"] = f"""
                            
                                Great Job!
                            You can proceed!
                            Flag:{flag}
                            
                            """
            else:
                self.result["Data"] = f"You need to give a paramater longer than {len(self.request.POST['code'])}"
        else:
            self.result["Data"] = f"You didn't provide code data key!"
        
        return self.result

