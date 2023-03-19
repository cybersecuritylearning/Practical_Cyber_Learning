from main.models import UserToken
from datetime import datetime
from hashlib import sha256
import json


import logging
import os 

LOG_PATH = os.path.join("main/core/","logging/")
PATH_CVES_SERVERS = "main/code/"

if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)
    LOG_PATH =os.path.join(LOG_PATH,"modules.log")
    f=open(LOG_PATH,"w")
    f.close()
else:
    LOG_PATH =os.path.join(LOG_PATH,"modules.log")

logging.basicConfig(filename=LOG_PATH,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class log_data:
    @staticmethod
    def log_info(value):
        logging.info(f"Value is: {value}")
    
    @staticmethod
    def log_debug(value):
        logging.info(f"Error is{str(value)}")


def dec_number_from_name(number):
    """Module which decrements by 1
        the module number
    """

    number = number.split('-')
    
    number_f = int(number[-1])
    number_f -= 1
    number_f = str(number_f)
    
    if len(number_f) < 2:
        number_f = '0'+number_f
    number = number[0]+'-'+number[1]+'-'+ number_f
    
    return number
  
def inc_number_from_name(number):
    """Module which increments by 1
        the module number
    """
    try:
        number = number.split('-')
        
        number_f = int(number[-1])
        number_f += 1
        number_f = str(number_f)
        
        if len(number_f) < 2:
            number_f = '0'+number_f
        number = number[0]+'-'+number[1]+'-'+ number_f
    except IndexError:
        return -1    
    return number
  

def init_userToken(request):
    User_data = UserToken()

    now = datetime.now()
    user_token = sha256(str(now.microsecond).encode()).hexdigest()
    
    User_data.User = request.user
    User_data.Score = 0 
    User_data.UserId = user_token
    User_data.save()

    return User_data

class CVEsAndServers:
    @staticmethod
    def get_server(CVE):
       servers_and_cves = os.path.join(PATH_CVES_SERVERS,"servers_cves")
        
       with open(servers_and_cves,"r") as file:
           servers = file.readlines()[3:]
        
       for server in servers:
           server = json.loads(server)
           if server['CVE_NUMBER'] == CVE:
               return server["SERVER"]
    
    
