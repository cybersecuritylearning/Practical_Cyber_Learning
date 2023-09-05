from django.shortcuts import render
from accounts.models import Users
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def teams(request) :
	teams_list = Users.objects.all()
	return render(request, 'teams.html', {'teams_list':teams_list})