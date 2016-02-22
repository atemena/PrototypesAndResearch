from django.http import HttpResponse
from django.shortcuts import render
import urllib2
import json

def index(request):
	context = {}
	return render(request, 'instamap/index.html', context)

def getUserId(request):
	username = request.GET['username']
	j = urllib2.urlopen("https://api.instagram.com/v1/users/search?q=" + username + "&access_token=30986360.3cc0c36.9274076b88994cc882135cd2fe644c2d").read()
	d = json.loads(j)
	userId = d['data'][0]['id']
	content = {'userId': userId}
	return HttpResponse(json.dumps(content), content_type="application/json")