from os import lseek
from importlib import import_module
import glob,os,sys
from flask import Flask
from flask import request
from flask import make_response


app = Flask(__name__)

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class User:
    id = "7989b708b5320d57108631ff9f151c2fdabbc481208fd713e545475283b8df44"


@app.route("/",methods=['GET', 'POST'])
def runner():
    simple_modules_path = PARENT_DIR + "/Workshop/scripts/"
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
            return make_response(400)

    response = make_response(data['Data'],200)
    return response
    


if __name__=='__main__':
    app.run("0.0.0.0",8000)