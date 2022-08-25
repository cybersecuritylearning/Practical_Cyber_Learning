
class FIRST_GET_REQUEST_WITH_PARAMS:
    REQUEST_METHOD_SUPPORTED = "GET"
    def __init__(self,request):
        self.request = request
        self.result = {}
    def process(self):
        if "code" in self.request.GET:
            if len(self.request.GET['code']) > 5:
                self.result["Data"] = f"Great job! Your parameter was: {self.request.GET['code']}"
            else:
                self.result["Data"] = f"You need to give a paramater larger than {len(self.request.GET['code'])}"
        return self.result
               
        
