from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from tumblrSandbox.models import *
from rauth import OAuth1Service, OAuth2Service
from django.shortcuts import redirect
import datetime
import json
import requests
#import pytumblr
import urllib
import sys



def searchLocations(request):
	data = {'code': request.GET['code'],
	        'grant_type': 'authorization_code',	
	        'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagram')}
	session = instagram.get_auth_session(data=data, decoder=json.loads)
	request.session['code'] = request.GET['code']
	request.session['instagram_session'] = session
	locations = session.get('https://api.instagram.com/v1/locations/search', params={'format': 'json','lat':'latitude', 'long':'longitude', 'access_token':session.access_token})
	
	locations = locations.json()
	loc_info = []
	#import pdb; pdb.set_trace();
	for loc in locations['data']:
		loc_info.append({'name': loc['name'], 'url': 'https://api.instagram.com/v1/locations/'+loc['id']+'/media/recent?access_token='+session.access_token})
	context = {'loc_info': loc_info}
	return render(request, 'tumblrSandbox/searchLocations.html', context)