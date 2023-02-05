from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from importlib import import_module
import glob,os,sys
from django.views.decorators.csrf import csrf_exempt

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class User:
    id = "7989b708b5320d57108631ff9f151c2fdabbc481208fd713e545475283b8df44"

@csrf_exempt
def runner(request):
    simple_modules_path = PARENT_DIR + "/scripts/"
    modules_to_load = []
   
    sys.path.append(simple_modules_path)

    for module_file in glob.glob(simple_modules_path + "*.py"):
        modules_to_load.append(os.path.basename(module_file)[:-3])

    modules_instances = []

    for module in modules_to_load:
        _mod = import_module(module)
        _cls = getattr(_mod,module.upper())
        try:
            data = _cls(request).process(User)
        except Exception as e:
            print(str(e))
    
    return HttpResponse(data['Data'])
    
