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


def shDemoRedirect(request):
	return render(request, 'tumblrSandbox/shDemoRedirect.html')