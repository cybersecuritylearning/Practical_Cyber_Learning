import paramiko
from main.core.connections import Connection

"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class CVE_2021_41773:
    REQUEST_METHOD_SUPPORTED = ["GET","POST"]
    TRAIN_ID = "TRAIN-01-08"
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
        

        
        return self.result

