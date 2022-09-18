from django.shortcuts import render, redirect
from importlib import import_module
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from .models import UserToken
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
    username = request.user.username
    return render(request = request,
                  template_name='main/home.html',
                  context={"username":username})

def learn(request):
    
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

def user_token(request):
    now = datetime.now()
    user_token = sha256(str(now.microsecond).encode()).hexdigest()
    try:
        User_data = UserToken()
        User_data.UserId = user_token
        User_data.Score = 0
        User_data.Time_to_live = datetime.now()
        User_data.save()
    except:
        return HttpResponse(MESSAGES.REGISTER_ERROR)
    
    return HttpResponse(user_token)

def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("main:hello_page")

    form = UserCreationForm
    return render(request=request, 
                template_name="main/register.html",
                context={"form":form})