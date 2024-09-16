from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models

class RegisterForm(forms.ModelForm) :
	username = forms.CharField(max_length=250, label="User Name")
	email = forms.EmailField(max_length=250, label="Email", widget=forms.TextInput(attrs={'type':'email'}))
	password = forms.CharField(max_length=250, min_length=8, label="Password", widget=forms.TextInput(attrs={'type':'password'}))

	class Meta :
		model = models.Users
		fields = ["username","email"]

class LoginForm(AuthenticationForm) :
	username = forms.CharField(max_length=50, label="User Name")
	password = forms.CharField(max_length=250, min_length=8, label="Password", widget=forms.TextInput(attrs={'type':'password'}))

class UpdateTeamDetails(forms.ModelForm) :
	job = forms.CharField(max_length=250, label="Job", required=False)
	company = forms.CharField(max_length=250, label="Company", required=False)

	class Meta :
		model = models.Users
		fields = ["job","company"]