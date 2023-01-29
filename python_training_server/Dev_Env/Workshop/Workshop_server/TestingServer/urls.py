from django.urls import path
from . import views

app_name = "TestingServer"

urlpatterns = [
    path("simple/",views.runner, name="Simple_python_module")
]