
class FIRST_GET_REQUEST_WITH_PARAMS:
    REQUEST_METHOD_SUPPORTED = "GET"
    TRAIN_ID = "TRAIN-01-02"
    def __init__(self,request):
        self.request = request
        self.result = {"Data":"Not allowed yet"}
    def process(self,user):
        if "code" in self.request.GET:
            if len(self.request.GET['code']) > 5:
                self.result["Data"] = f"Great job! Your parameter was: {self.request.GET['code']}"
            else:
                self.result["Data"] = f"You need to give a paramater larger than {len(self.request.GET['code'])}"
        return self.result
               
        
