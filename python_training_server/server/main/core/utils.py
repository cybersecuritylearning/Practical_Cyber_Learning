


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

    number = number.split('-')
    
    number_f = int(number[-1])
    number_f += 1
    number_f = str(number_f)
    
    if len(number_f) < 2:
        number_f = '0'+number_f
    number = number[0]+'-'+number[1]+'-'+ number_f
    
    return number
  

