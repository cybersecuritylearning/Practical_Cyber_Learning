import paramiko
from main.core.connections import Connection

"""Simple request module"""
import os
from hashlib import sha256
from datetime import datetime
import uuid

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class CVE_2021_41773:
    REQUEST_METHOD_SUPPORTED = ["GET","POST"]
    TRAIN_ID = "TRAIN-01-08"
    DOCKER_NAME = "cve-2021-41773C"
    SSH_KEY = "/run/secrets/host_ssh_key"
    
    def __init__(self,request):
        self.request = request
        self.result = {"Data":"Try Harder"}
        self.__conn = Connection(self.SSH_KEY,"192.168.0.104","root",22)
        self.__conn.make_connection()
  
    def __sets_user_flag(self):
        """
        It gets the flag from the docker and sets to user for checks
        params:
            flag(str):represents a flag which will be written to the vuln docker
        return:
            True/False(Boolean):it says if it's up or not
        """
        output = self.__conn.exec_command(f"docker exec {self.DOCKER_NAME} cat /tmp/flag.txt")
        read_flag = output[1].read().decode().strip()

        return read_flag                
 
    def process(self,user):
        """
        params:
            user(object):represents the object of a user (from sql)
        return:
            result(dict):represents a dictionary with the result
        """
        
        
        __docker_flag = self.__sets_user_flag()
        if __docker_flag:
            user.Hash_check = __docker_flag
            user.save()
            return {"Status":"Up"}
        
        return self.result

