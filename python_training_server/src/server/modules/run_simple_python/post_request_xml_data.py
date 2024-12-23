"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime
import xml.etree.ElementTree as ET
from main.core.utils import log_data

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class POST_REQUEST_XML_DATA:
    REQUEST_METHOD_SUPPORTED = "POST"
    TRAIN_ID = "TRAIN-01-06"
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

        if not len(self.request.body.decode()):
            self.request["Data"] = "You didn't provide any data!"
            return self.result

        try:
            root = ET.fromstring(self.request.body.decode())

            for item in root.findall("item"):
                name = item.find("name").text
                username = item.find("username").text
    

            if username != user.User.username:
                self.result["Data"] = "Please make sure you passed the right username and try again :)"
            else:
                # Updates user database
                flag = self.make_flag(user)
                self.result["Data"] = f"Good job, {name}! Here's your flag: \nFlag: {flag}"

                user.Hash_check = flag
                user.save()
        
        except Exception as e:
            log_data.log_debug(e)
            self.result["Data"] = f"Please make sure you passed a valid XML as the request data and try again :)"

        return self.result