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
    SSH_KEY = "/run/secrets/host_ssh_key"
    
    def __init__(self,request):
        self.request = request
        self.result = {"Data":"Try Harder"}
        self.data = request.POST["con_data"]
        self.ip = self.data.split(":")[0]
        self.port = self.data.split(":")[1]
        self.__conn = Connection(self.SSH_KEY,self.ip,"root")
        self.__conn.make_connection()
        
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


    def __restart_docker(self,flag,user):
        """
        It restarts the vulnerable docker instance
        params:
            flag(str):represents a flag which will be written to the vuln docker
        return:
            True/False(Boolean):it says if it's up or not
        """
        flag_file = f"/tmp/{uuid.uuid4()}"
        self.__conn.exec_command(f"docker run --name {self.TRAIN_ID}_{user.UserId} -p {self.port}:80 --rm -d vulnerable-apache")
        self.__conn.exec_command(f'docker exec {self.TRAIN_ID}_{user.UserId} sh -c "echo {flag} > /tmp/flag.txt"')
        output = self.__conn.exec_command(f"docker exec {self.TRAIN_ID}_{user.UserId} cat /tmp/flag.txt")
        read_flag = output[1].read().decode().strip()
                
        if flag == read_flag:
            return True
        return False        
 
    def process(self,user):
        """
        params:
            user(object):represents the object of a user (from sql)
        return:
            result(dict):represents a dictionary with the result
        """
        flag = self.make_flag(user)
        
        __docker_run = self.__restart_docker(flag,user)
        if __docker_run:
            user.Hash_check = flag
            user.save()
            return {"Status":"Up"}
        
        return self.result

