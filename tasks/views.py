from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.conf import settings
import requests

# Create your views here.
def index(request):
	tasks = Task.objects.all()

	form = TaskForm()

	print(request.method)
	if request.method == 'POST':
		form = TaskForm(request.POST)	
		url = ""			
		if 'button_netflix' in request.POST:
			url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&include_null_first_air_dates=false&language=en-US&page=1&sort_by=vote_average.desc&with_networks=213"		
		if 'button_AP' in request.POST:
			url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&include_null_first_air_dates=false&language=en-US&page=1&sort_by=vote_average.desc&with_networks=1024"
		if 'button_Apple' in request.POST:
			url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&include_null_first_air_dates=false&language=en-US&page=1&sort_by=vote_average.desc&with_networks=2552"
		token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZTFhNDFmNDg1YWI0MzEzM2IzNTZkYzBkNDM2MWFlZSIsIm5iZiI6MTc3MTMyMDY1OS45NDcsInN1YiI6IjY5OTQzNTUzMGMxNTFlY2M1ODZmNzI0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.gD0Ral8P2zMD-Z2NfEamcZBAua9DUZXj6Zp-i72BdQM"
		headers = {"Authorization": f"Bearer {token}",
			"accept": "application/json"}
		response = requests.get(url, headers=headers)
		data = response.json()
		dix_premiers_elements = data['results']
		i : int = 0
		for element in dix_premiers_elements:
			if not Task.objects.filter(title=element['name']).exists():
				Task.objects.create(title=element['name'])
				i += 1
				if i == 10:
					break		
	if form.is_valid():
		#adds to the database if valid
		form.save()
		return redirect('/')

	context= {'tasks':tasks,'form':form, 'VERSION':settings.VERSION}
	return render(request, 'tasks/list.html',context)

def updateTask(request,pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)

	if request.method == "POST":
		form = TaskForm(request.POST,instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')


	context = {'form':form}
	return render(request, 'tasks/update_task.html',context)

def deleteTask(request,pk):
	item = Task.objects.get(id=pk)

	if request.method == "POST":
		item.delete()
		return redirect('/')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)

def addNetflix(request):
	pass

def addAP(request):
	pass

def addApple(request):
	pass