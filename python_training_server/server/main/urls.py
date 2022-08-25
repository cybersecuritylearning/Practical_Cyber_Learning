from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path("hello/", views.hello, name="hello_page"),
    path("simple/",views.run_simple_python, name="Simple_python_module")
]