
class FIRST_REQUEST:
    REQUEST_METHOD_SUPPORTED = "GET"
    def __init__(self,request):
        self.request = request
    def print_req(self):
        print(self.request)
