from django import forms
from . import models

category_list = [
	('Basic','Basic'),
	('CVEs','CVEs')
]

class AddChallengeForm(forms.ModelForm) :
	name = forms.CharField(max_length=250, label="Challenge Name *", widget=forms.TextInput(attrs={'placeholder':'Challenge Name','class':'form-control'}))
	category = forms.CharField(widget=forms.Select(choices=category_list, attrs={'class':'form-control'}), label="Challenge Category *")
	description = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder':'Challenge Description', 'class':'form-control','required':'true'}), label="Challenge Description *")
	hint = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder':'Challenge Hint', 'class':'form-control'}), label="Challenge Hint", required=False)
	points = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), label="Challenge Points *")
	file = forms.FileField(label="Challenge Files (if any)", required=False)
	flag = forms.CharField(max_length=500, label="Challenge Flag *", widget=forms.TextInput(attrs={'placeholder':'Challenge Flag','class':'form-control'}))
	author = forms.CharField(max_length=250, label="Challenge Author *", widget=forms.TextInput(attrs={'placeholder':'Challenge Author','class':'form-control'}))
	solved_by = forms.CharField(max_length=250, required=False)

	class Meta :
		model = models.Challenges
		fields = ["name","category","description","hint","points","file","flag","author"]