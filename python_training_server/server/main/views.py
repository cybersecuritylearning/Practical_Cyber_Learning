from importlib import import_module
import glob,os,sys
import re
from datetime import datetime
from hashlib import sha256
import json, random

from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import UserToken, Learning_Modules
from .forms import NewUserForm
from .core.Messages import MESSAGES 
from .core.utils import dec_number_from_name, inc_number_from_name, init_userToken
from .core.utils import CVEsAndServers
from .core.connections import Connection

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Create your views here.

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:login_page")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main:hello_page')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})

def hello(request):
    
    try:
        User = UserToken.objects.filter(User=request.user)[0]
    except IndexError as e:
        User=init_userToken(request)
    except TypeError as e:
        return redirect("main:login_page")

    button_v = "Start"
    url = "/home/learn"
    message = f"""
            Welcome {User.User.username} to Cyber Security Python Hands On Course
            Your key is {User.UserId} and you have to include it in your requests as
            Usert:<key> header
            """
   
    if len(User.Passed_modules):
        button_v = "Continue"
    else:
        User.Current_Level = "TRAIN-01-01"
        User.save()   
    data = {
        "Button_display":button_v,
        "redirect":url,
        "Message":message,
        "api_key_here":User.UserId

    }
    
    return render(request = request,
                  template_name='main/home.html',
                  context=data)

def learn(request):
    flag = None
    if request.method == "POST":
        try:
            flag = request.POST['Flag']
            if len(flag) != 64:
                return None
            
            user = UserToken.objects.filter(Hash_check=flag)[0]
            if not user:
                return HttpResponse(
                        json.dumps({'fail':"This is not the correct flag!"}),
                        content_type="application/json"
                    ) 
            
            user.Hash_check = ''
            user.save()

            level_a = user.Current_Level
            Lrmodules = Learning_Modules.objects.all()
            
            for module in Lrmodules.iterator():
                if module.Module_name not in user.Passed_modules:
                    current_level = module.Module_name
                    user.Current_Level = current_level
                    user.save()
                    
                    response_data = {}

                    if "TRAIN_CVE" in module.Module_type:
                        server_ip = CVEsAndServers.get_server(module.CVE_number)
                        connection = Connection('/Users/catalinfilip/.ssh/linode',server_ip,'root')

                        port = connection.get_available_port()
                        response_data["instance"]=""

                    response_data['quest'] = module.Module_message
                    response_data['tips'] = module.Module_tips
                    
                    
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    ) 

        except (KeyError,IndexError):
            return HttpResponse(
                        json.dumps({'fail':"Flag is not right, Try Harder!"}),
                        content_type="application/json"
                    ) 

    
    
    User = UserToken.objects.filter(User=request.user)[0]
    current_level = User.Current_Level
    
    __current_level_model = Learning_Modules.objects.filter(Module_name=current_level)[0]

    return render(request = request,
                template_name='main/quest.html',
                context={"message":__current_level_model.Module_message,
                        "tip":__current_level_model.Module_tips,
                        "api_key_here":User.UserId}
            )

@csrf_exempt
def run_simple_python(request):
    
    
    simple_modules_path = PARENT_DIR + "/modules/run_simple_python/"
    cve_modules_path = PARENT_DIR + "/modules/cves_modules/"
    modules_paths = [simple_modules_path,cve_modules_path]

    modules_to_load = []
    try:
        __user_id = request.META['HTTP_USERT']
    except KeyError:
        return HttpResponse("User key not set, please set UserT header",status=[401])
    
    try:
        User = UserToken.objects.filter(UserId=__user_id)[0]
    except:
        return HttpResponse(MESSAGES.NOT_REGISTERED)

    sys.path.append(simple_modules_path)

    for path in modules_paths:
        for module_file in glob.glob(path + "*.py"):
            modules_to_load.append(os.path.basename(module_file)[:-3])

    modules_instances = []
    #TO DO, here we should do something
    for module in modules_to_load:
        try:
            _mod = import_module(module)
            _cls = getattr(_mod,module.upper())
        except Exception as e:
            log_data.log_debug(e)
            
        if _cls.TRAIN_ID == User.Current_Level:
            try:
                data = _cls(request).process(User)
            except Exception as e:
                print(str(e))

    return HttpResponse(data['Data'])

def register(request):
    if request.method =="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            now = datetime.now()
            user_token = sha256(str(now.microsecond).encode()).hexdigest()
            user_obj = User.objects.get(username=form.cleaned_data.get("username"))
            try:
                User_data = UserToken()
                User_data.User = user
                User_data.Score = 0 
                User_data.UserId = user_token
                User_data.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"New account created: {username}")
            except Exception as e:
                print(str(e))
                return HttpResponse(MESSAGES.REGISTER_ERROR)
            return redirect("main:hello_page")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request=request, 
                template_name="main/register.html",
                context={"form":form})



def move(request):
    """Module which handles modules movement"""
    user = UserToken.objects.filter(User=request.user)[0]
    current_level = user.Current_Level

    try:
        if request.GET['pos'] == "prev":
            level_decrement = dec_number_from_name(current_level)
            module = Learning_Modules.objects.filter(Module_name=level_decrement)[0]
        
        if request.GET['pos'] == "next":
            level_increment = inc_number_from_name(current_level)

            if not user.User.is_superuser:
                currently_undone_level = inc_number_from_name(user.Passed_modules[-1])

                if level_increment not in user.Passed_modules:
                    if (level_increment !=currently_undone_level):
                        return  HttpResponse(
                            "Level not found!"
                        )

            module = Learning_Modules.objects.filter(Module_name=level_increment)[0]
        

        current_level = module.Module_name
        user.Current_Level = current_level
        user.save()
        
        response_data = {"instance":""}
        
        if "TRAIN_CVE" in module.Module_type:
                        server_ip = CVEsAndServers.get_server(module.CVE_number)
                        connection = Connection('/Users/catalinfilip/.ssh/linode',server_ip,'root')
                        connection.make_connection()
                        port = connection.get_available_port()
                        response_data["instance"]=f"{server_ip}:{port}"
        
        response_data['quest'] = module.Module_message
        response_data['tips'] = module.Module_tips
        
        if current_level in user.Passed_modules:
            response_data['done'] = MESSAGES.SOLVED
        else:
            response_data['done'] = ''
        
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        ) 

    except Exception as e:
        return HttpResponse(
            "Level not found!"
        ) 
