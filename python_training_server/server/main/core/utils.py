from main.models import UserToken
from datetime import datetime
from hashlib import sha256


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
  

def super_user_upgrade(request):
    User_data = UserToken()

    now = datetime.now()
    user_token = sha256(str(now.microsecond).encode()).hexdigest()
    
    User_data.User = request.user
    User_data.Score = 0 
    User_data.UserId = user_token
    User_data.save()

    return User_data
