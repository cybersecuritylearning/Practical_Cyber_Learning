"""Simple request module"""

class FIRST_GET_REQUEST:
    REQUEST_METHOD_SUPPORTED = "GET"
    def __init__(self,request):
        self.request = request
        self.result = {"Data":"Try Harder"}
    def process(self):
        if not len(self.request.GET):
            self.result["Data"] = "Great Job!"
            
        return self.result

