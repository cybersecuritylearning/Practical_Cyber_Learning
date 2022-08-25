from django.shortcuts import render
from importlib import import_module
from django.http import HttpResponse
import glob,os,sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# Create your views here.
def hello(request):
    return render(request = request,
                  template_name='main/home.html')
    
def run_simple_python(request):
    
    simple_modules_path = PARENT_DIR + "/modules/run_simple_python/"
    modules_to_load = []
    
    sys.path.append(simple_modules_path)
    for module_file in glob.glob(simple_modules_path + "*.py"):
        modules_to_load.append(os.path.basename(module_file)[:-3])

    modules_instances = []

    for module in modules_to_load:
        _mod = import_module(module)
        _cls = getattr(_mod,module.upper())
        modules_instances.append(_cls)

    for _mod_inst in modules_instances:
        if request.method == _mod_inst.REQUEST_METHOD_SUPPORTED:
            _mod_obj = _mod_inst(request)
            result = _mod_obj.process()
            
                
    
    return HttpResponse(response)