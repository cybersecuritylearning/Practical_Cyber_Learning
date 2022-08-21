from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path("hello/", views.hello, name="hello_page"),
]