from django.urls import path
from . import views
from django.shortcuts import redirect



app_name = "main"


urlpatterns = [
    path('', lambda request: redirect('landing/', permanent=False)),
    path("landing/",views.landing,name="landing_page"),
    path("hello/", views.hello, name="hello_page"),
    path("simple",views.run_simple_python, name="Simple_python_module"),
    path("learn/",views.learn, name="Learn_page_for_users"),
    path("move/",views.move, name="Change_quest"),
    path("register/",views.register, name="Registration"),
    path("logout", views.logout_request, name="logout"),
    path("login",views.login_request,name="login_page"),
    path("docker/", views.docker, name="docker_start"),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("load_categ/",views.load_categ,name="load_categ"),
    path("contact",views.contact, name="contact")
]