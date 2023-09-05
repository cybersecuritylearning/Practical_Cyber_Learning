from django.shortcuts import render
from accounts.models import Users
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def score(request) :
	teams_list = Users.objects.order_by("-points")
	return render(request, 'scoreboard.html', {'teams_list':teams_list})