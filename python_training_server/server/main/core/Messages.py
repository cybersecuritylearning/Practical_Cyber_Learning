"""This is a module just for messages"""

class MESSAGES:
    NOT_REGISTERED = """
        You are not registered. Please make a request
        to /home/get_token and obtain your token. Be 
        advised that you have to save your token if you
        want to resume your levels
    """
    TOKEN_NOT_PRESENT = """
        Your identification token is not present in the
        headers request. Please include it
        by the following form "usert:<token>"
    """
    REGISTER_ERROR = """
        An error occured at user registration.
        Please try again!
    """
    SOLVED = """
            <div class="center-align">
        <div class="col s12 m6 ">
        <div class="card green darken-1">
            <div class="card-content white-text">
            <span class="card-title">Solved!</span>
            
            </div>
            
        </div>
        </div>
    </div>
    """
    INSTANCE ="""
            <div class="center-align">
        <div class="col s12 m6 ">
        <div class="card blue-grey darken-1">
            
            <div class="card-content white-text card-action">
            <a href="#"> <<PLACEHOLDER>></a>
            </div>
            
        </div>
        </div>
    </div>
    """