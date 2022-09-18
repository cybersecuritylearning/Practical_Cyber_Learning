from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path("hello/", views.hello, name="hello_page"),
    path("simple/",views.run_simple_python, name="Simple_python_module"),
    path("get_token/",views.user_token, name="Simple_User_Token"),
    path("learn/",views.learn, name="Learn_page_for_users"),
    path("register/",views.register, name="Registration"),
    path("logout", views.logout_request, name="logout"),
    path("login",views.login_request,name="login_page")
]