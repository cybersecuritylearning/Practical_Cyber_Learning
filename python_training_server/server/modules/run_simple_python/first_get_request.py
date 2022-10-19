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
        now = datetime.now()
        flag = sha256(f"{str(now.microsecond)}{user.UserId}".encode()).hexdigest()
        return flag

    def process(self,user):
        if not len(self.request.GET):
            
            if self.TRAIN_ID not in user.Passed_modules:
                user.Passed_modules.append(self.TRAIN_ID)

            flag = self.make_flag(user)
            user.Hash_check = flag
            user.save()
            
            self.result["Data"] =f"""
                        
                            Great Job!
                        You can proceed!
                        Flag:{flag}
                        
                        """
            
        return self.result

