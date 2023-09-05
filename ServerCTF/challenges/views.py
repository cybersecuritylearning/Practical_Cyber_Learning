from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import HttpResponse
from . import models
from accounts import models as accounts_models

# Create your views here.

class PassInsideView() :
	name = ''
	challenge_id = ''
	category = ''
	description = ''
	hint = ''
	points = ''
	file = ''
	flag = ''
	author = ''

	def __init__(self, name, challenge_id, category, description, hint, points, file, flag, author) :
		self.name = name
		self.challenge_id = challenge_id
		self.category = category
		self.description = description
		self.hint = hint
		self.points = points
		self.file = file
		self.flag = flag
		self.author = author

def assignID(a) :
	return a.lower().replace(' ','_')

@login_required()
def index(request) :
	challenge = models.Challenges.objects.order_by("points")
	challenge_info_basic_object = []
	challenge_info_cve_object = []
	
	for c in challenge :
		if c.category == 'Basic' :
			b = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.hint, c.points, c.file, c.flag, c.author)
			challenge_info_basic_object.append(b)
		elif c.category == 'CVEs' :
			cve = PassInsideView(c.name, assignID(c.name), c.category, c.description, c.hint, c.points, c.file, c.flag, c.author)
			challenge_info_cve_object.append(cve)

	solved_challenges_by_user = []
	try :
		fc = models.ChallengesSolvedBy.objects.filter(user_name=request.user)
		for f in fc :
			solved_challenges_by_user.append(f.challenge_id)
	except :
		pass

	return render(request, 'challenges.html',{'data_basic':challenge_info_basic_object,
		'data_cve':challenge_info_cve_object})

@login_required()
def flagsubmit(request) :
	if request.method == 'POST' :
		flag_submit = ''
		flag_submit_id = ''
		x = ''
		for k in request.POST :
			if k == 'submit' :
				continue
			if k == 'csrfmiddlewaretoken' :
				continue
			else :
				x = k
		flag_submit = request.POST[x]
		flag_submit_id = x[:-5]
	flag = models.Challenges.objects.get(challenge_id=flag_submit_id).flag
	points = models.Challenges.objects.get(challenge_id=flag_submit_id).points
	if flag == flag_submit and not request.user.is_superuser :
		fr = models.ChallengesSolvedBy(challenge_id=flag_submit_id, user_name=request.user, points=points)
		try :
			fc = models.ChallengesSolvedBy.objects.filter(user_name=request.user)
			obs = []
			for k in fc :
				obs.append(k.challenge_id)
			if flag_submit_id in obs :
				response = '<div id="flag_already"><p>ALREADY SUBMITTED</p></div>'
			else :
				fr.save()
				initial_points = accounts_models.Users.objects.get(username=request.user).points
				updated_points = initial_points + points
				accounts_models.Users.objects.filter(username=request.user).update(points=updated_points)
				response = '<div id="flag_correct"><p>CORRECT</p></div>'
		except :
			fr.save()
			initial_points = accounts_models.Users.objects.get(username=request.user).points
			updated_points = initial_points + points
			accounts_models.Users.objects.filter(username=request.user).update(points=updated_points)
			response = '<div id="flag_correct"><p>CORRECT</p></div>'
	elif request.user.is_superuser :
		response = '<div id="flag_already"><p>Correct, But not added to scoreboard</p></div>'
	else :
		response = '<div id="flag_incorrect"><p>INCORRECT</p></div>'
	return HttpResponse(response)

@login_required()
def addchallenges(request) :
	
	if request.user.is_superuser :
		if request.method == 'POST' :
			success = 0
			form = forms.AddChallengeForm(request.POST, request.FILES)
			if form.is_valid() :
				success = 1
				print(request.FILES)
				if request.FILES :
					i = models.Challenges(file=request.FILES['file'], 
						name=request.POST['name'], 
						category=request.POST['category'], 
						description=request.POST['description'], 
						hint=request.POST['hint'], 
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'], 
						author=request.POST['author'])
					i.save()
				else :
					i = models.Challenges( 
						name=request.POST['name'], 
						category=request.POST['category'], 
						description=request.POST['description'], 
						hint=request.POST['hint'], 
						points=request.POST['points'],
						challenge_id=assignID(request.POST['name']),
						flag=request.POST['flag'], 
						author=request.POST['author'])
					i.save()
				return render(request, 'addchallenges.html', {'form':form,'success':success})
		else :
			form = forms.AddChallengeForm()

		return render(request, 'addchallenges.html', {'form':form})
	
	else :
		return redirect("/")