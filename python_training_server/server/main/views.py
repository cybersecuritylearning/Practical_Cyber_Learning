from django.shortcuts import render, redirect
from importlib import import_module
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import UserToken, Learning_Modules
from .forms import NewUserForm
from .core.Messages import MESSAGES 
from django.contrib import messages
import glob,os,sys
from datetime import datetime
from hashlib import sha256
import json

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
    
    User = UserToken.objects.filter(User=request.user)[0]
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
        "Message":message

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
                return None
            
            level_a = user.Current_Level
            Lrmodules = Learning_Modules.objects.all()
            
            for module in Lrmodules.iterator():
                if module.Module_name not in user.Passed_modules:
                    current_level = module.Module_name
                    user.Current_Level = current_level
                    user.save()
                    
                    response_data = {}
                    response_data['quest'] = module.Module_message
                    response_data['tips'] = module.Module_tips
                    
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    ) 

        except KeyError:
            return None
    
    
    User = UserToken.objects.filter(User=request.user)[0]
    current_level = User.Current_Level
    
    __current_level_model = Learning_Modules.objects.filter(Module_name=current_level)[0]

    return render(request = request,
                template_name='main/quest.html',
                context={"message":__current_level_model.Module_message,
                        "tip":__current_level_model.Module_tips,
                        "api_key_here":User.UserId}
            )

def run_simple_python(request):
    
    simple_modules_path = PARENT_DIR + "/modules/run_simple_python/"
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

    for module_file in glob.glob(simple_modules_path + "*.py"):
        modules_to_load.append(os.path.basename(module_file)[:-3])

    modules_instances = []

    for module in modules_to_load:
        _mod = import_module(module)
        _cls = getattr(_mod,module.upper())
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
