"""Simple request module"""
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class FIRST_GET_REQUEST:
    REQUEST_METHOD_SUPPORTED = "GET"
    TRAIN_ID = "TRAIN-01-01"
    def __init__(self,request):
        self.request = request
        self.result = {"Data":"Try Harder"}
    def process(self,user):

        print(PARENT_DIR)
        if not len(self.request.GET):
            self.result["Data"] = "Great Job!"
            
        return self.result

