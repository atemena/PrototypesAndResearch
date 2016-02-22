from hashlib import sha512, sha1
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

@csrf_exempt
def index(request):
	context = {}
	context['user'] = request.GET['uid']
	#user = request.GET['uid']
	timestamp = request.GET['ts']
	token = request.GET['token']
	secret = 'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
	sha = sha512(user+timestamp+secret).hexdigest()
	#Double check user id
	#Get shareroot session from request.COOKIES
	context['timestamp'] = timestamp
	return render(request, 'hootsuite/index.html', context)

@csrf_exempt
def shaSign(request):
	content = {}
	user_id = request.GET['user_id']
	timestamp = request.GET['timestamp']
	url = request.GET['url']
	secret = 'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
	content['token'] = sha512(user_id+timestamp+url+secret).hexdigest()
	return HttpResponse(json.dumps(content), content_type="application/json")

