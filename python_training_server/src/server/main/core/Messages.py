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
            <button class="btn waves-effect waves-light" type="submit" name="action" id="Instance-btn">PLACEHOLDER</button>
            <input type="hidden" value="PLACEHOLDER"/ id="Instance-input">
            </div>
        </div>
        </div>
    </div>
    <script type="text/javascript" src='/static/main/js/start_docker_inst.js' ></script>
    """
    CONTACT = """
        We'd love to hear your feedback! Please reach out to us at <b>cyber.contact.learning@gmail.com.</b><br>
        If you'd like to support our work, feel free to send some ETH to the following wallet address:<br><b>
        0xB0153C4e2D091714d1F771754aCd09Ac4F742bE6.</b><br>
        Also, If you want to join our team, just tell us by sending also an <b>email to the above address.</b>
        <br><b>Thank you for your support!</b>

    """