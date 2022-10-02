from django.shortcuts import render, redirect
from importlib import import_module
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import UserToken
from .forms import NewUserForm
from .core.Messages import MESSAGES 
from django.contrib import messages
import glob,os,sys
from datetime import datetime
from hashlib import sha256

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# Create your views here.

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:hello_page")

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
    url = "../learn"
    message = f"Welcome {User.User.username} to Cyber Security Python Hands On Course"
   
    if len(User.Passed_modules):
        button_v = "Continue"
        message = f"Welcome back <br>{User.User.username}</br>"
    else:
        User.Passed_modules.append("TRAIN-01-01")
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

    User = UserToken.objects.filter(User=request.user)[0]
    current_level = User.Current_Level
    
    return render(request = request,
                template_name='main/quest.html',
                context={"message":"Works"}
            )

def run_simple_python(request):
    
    simple_modules_path = PARENT_DIR + "/modules/run_simple_python/"
    modules_to_load = []
    
    user_token = request.META.get("HTTP_USERT")
    if not user_token:
        return HttpResponse(MESSAGES.TOKEN_NOT_PRESENT,status=403)

    User = UserToken.objects.filter(UserId=user_token)

    if not User:
        return HttpResponse(MESSAGES.NOT_REGISTERED)
    
    User_data = User.values()[0]

    sys.path.append(simple_modules_path)
    for module_file in glob.glob(simple_modules_path + "*.py"):
        modules_to_load.append(os.path.basename(module_file)[:-3])

    modules_instances = []

    for module in modules_to_load:
        _mod = import_module(module)
        _cls = getattr(_mod,module.upper())
        if _cls.TRAIN_ID not in User_data['Passed_modules']:
            modules_instances.append(_cls)

    for _mod_inst in modules_instances:
        if request.method == _mod_inst.REQUEST_METHOD_SUPPORTED:
            _mod_obj = _mod_inst(request)
            result = _mod_obj.process(User_data)
            response = result['Data']
                
    
    return HttpResponse(response)

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
            except Exception as e:
                print(str(e))
                return HttpResponse(MESSAGES.REGISTER_ERROR)
            return redirect("main:hello_page")

    form = NewUserForm
    return render(request=request, 
                template_name="main/register.html",
                context={"form":form})