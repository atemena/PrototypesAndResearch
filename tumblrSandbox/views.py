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


viableSources=[
'Twitter for iPhone',
'Twitter for iPad',
'Twitter for Windows Phone',
'Twitter for Android',
'Twitter for Android Tablets',
'iOS'
]

tumblr = OAuth1Service(
	    name='tumblr',
	    consumer_key='zLZDEzKfKaxtlMeFnG1dXrZ4jlo1pFZuDZRLQGR7izKBHB7DeJ',
	    consumer_secret='c05OzghD6IBkKtD0Vekg2ucAK0q5dwgafhzbzlRs2kf4tn0sCq',
	    request_token_url='http://www.tumblr.com/oauth/request_token',
	    access_token_url='http://www.tumblr.com/oauth/access_token',
	    authorize_url='http://www.tumblr.com/oauth/authorize')

twitter = OAuth1Service(
       name='example',
       consumer_key='H7oEtDyZMPEMxX0RuElUfGNKE',
       consumer_secret='Wc1JGtvLqblv3Um7yv5CVv04mDHlSGkVO1LUQcYBdenvDVUtnD',
       request_token_url='https://api.twitter.com/oauth/request_token',
       access_token_url='https://api.twitter.com/oauth/access_token',
       authorize_url='https://api.twitter.com/oauth/authorize',
       base_url='https://api.twitter.com/1.1/')

instagram = OAuth2Service(
       name='example',
       client_id='3cc0c367787843d4a97d8c59cfc9b208',
       client_secret='6fddfb45317f4e319dd8e66414e6f359',
       access_token_url='https://api.instagram.com/oauth/access_token',
       authorize_url='https://api.instagram.com/oauth/authorize/',
       base_url='https://api.instagram.com/')

#notes on refreshing tokens
# instagram will give error_type=OAuthAccessTokenError if expired will need to reauth if expired

def index(request):
	return render(request, 'tumblrSandbox/index.html')

def indexNew(request):
	return render(request, 'tumblrSandbox/indexNew.html')

def authen(request):
	network = request.GET.get('network')
	if network == 'tumblr':
		request.session['blog_name'] =  request.GET.get('search')
		#if 'tumblr_oauth_token' in request.session.keys() and 'tumblr_oauth_token_secret' in request.session.keys() and 'tumblr_session' in request.session.keys():
			#return getSessionTumblr(request)			
		request_token, request_token_secret = tumblr.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':request.build_absolute_uri('/tumblrSandbox/getSessionTumblr')})
		authorize_url = tumblr.get_authorize_url(request_token)
		request.session['tumblr_oauth_token'] = request_token
		request.session['tumblr_oauth_token_secret'] = request_token_secret

	elif network == 'twitter':
		request.session['twitter_search'] =  request.GET.get('search')
		request.session['twitter_mediatype'] =  request.GET.get('mediatype')
		if 'twitter_oauth_token' in request.session.keys() and 'twitter_oauth_token_secret' in request.session.keys() and 'twitter_session' in request.session.keys():
			return getSessionTwitter(request)
		else:
			request_token, request_token_secret = twitter.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':request.build_absolute_uri('/tumblrSandbox/getSessionTwitter')})
			authorize_url = twitter.get_authorize_url(request_token)
			request.session['twitter_oauth_token'] = request_token
			request.session['twitter_oauth_token_secret'] = request_token_secret

	elif network == 'instagram':
		request.session['instagram_search'] =  request.GET.get('search')
		#if 'oauth_token' in request.session.keys() and 'oauth_token_secret' in request.session.keys() and 'session' in request.session.keys():
		#	return getSessionInstagram(request)
		#else:
		params = {'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagram'),
	          'response_type': 'code',
	          'client_id': '3cc0c367787843d4a97d8c59cfc9b208',
	          'scope': 'likes comments'}
		authorize_url = instagram.get_authorize_url(**params)
	return redirect(authorize_url)

def authenNew(request):
	network = request.GET.get('network')
	if network == 'tumblr':
		request.session['blog_name'] =  request.GET.get('search')
		if 'tumblr_oauth_token' in request.session.keys() and 'tumblr_oauth_token_secret' in request.session.keys() and 'tumblr_session' in request.session.keys():
			return getSessionTumblr(request)			
		request_token, request_token_secret = tumblr.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':request.build_absolute_uri('/tumblrSandbox/getSessionTumblrNew')})
		authorize_url = tumblr.get_authorize_url(request_token)
		request.session['tumblr_oauth_token'] = request_token
		request.session['tumblr_oauth_token_secret'] = request_token_secret

	elif network == 'twitter':
		request.session['twitter_search'] =  request.GET.get('search')
		request.session['twitter_mediatype'] =  request.GET.get('mediatype')
		if 'twitter_oauth_token' in request.session.keys() and 'twitter_oauth_token_secret' in request.session.keys() and 'twitter_session' in request.session.keys():
			return getSessionTwitterNew(request)
		else:
			request_token, request_token_secret = twitter.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':request.build_absolute_uri('/tumblrSandbox/getSessionTwitterNew')})
			authorize_url = twitter.get_authorize_url(request_token)
			request.session['twitter_oauth_token'] = request_token
			request.session['twitter_oauth_token_secret'] = request_token_secret

	elif network == 'instagram':
		request.session['instagram_search'] =  request.GET.get('search')
		#if 'oauth_token' in request.session.keys() and 'oauth_token_secret' in request.session.keys() and 'session' in request.session.keys():
		#	return getSessionInstagram(request)
		#else:
		params = {'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagramNew'),
	          'response_type': 'code',
	          'client_id': '3cc0c367787843d4a97d8c59cfc9b208',
	          'scope': 'likes comments'}
		authorize_url = instagram.get_authorize_url(**params)
	return redirect(authorize_url)

def getSnapshot(request):
	#check if authorized
	if 'twitter_session' not in request.session.keys():
		request.session['twitter_session'] = twitter.get_auth_session(request.session['twitter_oauth_token'], request.session['twitter_oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	
	#Twitter
	search = request.GET.get('search') or 'shareroot'
	mediatype = request.GET.get('mediatype') or 'images'
	min_id = request.GET.get('min') or '0'
	search_query = {'q':search + ' -RT filter:' + mediatype + " lang:en", 'count': '33'}
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)

	#get twitter pics
	context = {}
	search_results = json.loads(search_results.text)
	tweets = []
	for tweet in search_results['statuses']:
		if request.session['twitter_mediatype'] == 'images' and tweet['user']['verified'] == False:
			if 'media' in tweet['entities'].keys():
				if len(tweet['entities']['media']) > 0:
					media_url = tweet['entities']['media'][0]['media_url_https']
			else:
				media_url = ""
			if len(tweet['entities']['urls']) > 0:
				url = tweet['entities']['urls'][0]['url']
			tweets.append({'text': tweet['text'], 'url': media_url, 'id': tweet['id'], 'screen_name': tweet['user']['screen_name'], 'date_created': tweet['created_at'] }) #hashtags retweet_count id
		elif request.session['twitter_mediatype'] == 'news':
			tweets.append({'text': tweet['text']})
		#get posted date as well
	context['tweets'] = tweets
	if 'localhost:9000' not in sys.argv:
		if 'instagram_session' not in request.session.keys() :
			data = {'code': request.session['code'],
			        'grant_type': 'authorization_code',
			        'redirect_uri': 'http://10.0.1.11:8000/tumblrSandbox/getSessionInstagram'}
			request.session['instagram_session'] = instagram.get_auth_session(data=data, decoder=json.loads)

		#Instagram photos +request.GET.get('tag')+
		media = requests.get("https://api.instagram.com/v1/tags/"+urllib.quote(urllib.unquote(search).replace(" ", ""))+"/media/recent", params={'client_id': "3cc0c367787843d4a97d8c59cfc9b208", 'min_id': min_id, 'count':'100'})
		#Instagram tags
		tags = request.session['instagram_session'].get('https://api.instagram.com/v1/tags/search', params={'format': 'json','q':request.GET.get('search'), 'access_token':request.session['instagram_session'].access_token})
		try:
			media = json.loads(media.text)
	 	except ValueError, e:
	 		media = {}
		posts = []
		if 'data' in media.keys():
			for post in media['data']:
				cap = 'No caption'
				if 'caption' in post.keys():
					if post['caption'] is not None:
						cap = post['caption']['text']
				datetime.datetime.fromtimestamp(float(post['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
				posts.append({'tags': post['tags'], 'id': post['id'], 'link':post['link'], 'likes':post['likes']['count'], 'url': post['images']['standard_resolution']['url'], 'username': post['user']['username'], 'date_created': post['created_time'] ,'caption': cap }) 
		context['posts']= posts # 'nextLink': nextLink
		if 'pagination' in media.keys():
			if 'next_max_tag_id' in media['pagination'].keys():
				context['next_max_tag_id'] = media['pagination']['next_max_tag_id']
		#get insta tags
		tags = tags.json()
		tag_info = []
		if 'data' in tags.keys():
			for tag in tags['data']:
				tag_info.append({'media_count': tag['media_count'], 'name': tag['name'], 'url': 'https://api.instagram.com/v1/tags/'+tag['name']+'/media/recent?client_id=3cc0c367787843d4a97d8c59cfc9b208'})
			context['tags_info']=tag_info
		context['search'] = search
	else:
		context['posts'] = []
		context['next_max_tag_id'] = 0
		context['search'] = []
	return render(request, 'tumblrSandbox/getSnapshot.html', context)

def getSnapshotNew(request):
	#check if authorized
	if 'twitter_session' not in request.session.keys():
		request.session['twitter_session'] = twitter.get_auth_session(request.session['twitter_oauth_token'], request.session['twitter_oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	
	#Make all api calls:
	#Twitter
	search = request.GET.get('search') or 'shareroot'
	mediatype = request.GET.get('mediatype') or 'images'
	min_id = request.GET.get('min') or '0'
	search_query = {'q':search + ' -RT filter:' + mediatype + " lang:en"}
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)
	context = {}
	search_results = json.loads(search_results.text)
	tweets = []
	for tweet in search_results['statuses']:
		if request.session['twitter_mediatype'] == 'images' and tweet['user']['verified'] == False:
			if 'media' in tweet['entities'].keys():
				if len(tweet['entities']['media']) > 0:
					media_url = tweet['entities']['media'][0]['media_url_https']
			else:
				media_url = ""
			if len(tweet['entities']['urls']) > 0:
				url = tweet['entities']['urls'][0]['url']
			print tweet['source'].split('>')[1].split('>')[0]
			if tweet['source'].split('>')[1].split('<')[0] in viableSources:
				tweets.append({'text': tweet['text'], 'url': media_url, 'id': tweet['id'], 'screen_name': tweet['user']['screen_name'], 'date_created': tweet['created_at'], 'source': tweet['source'] }) #hashtags retweet_count id
		elif request.session['twitter_mediatype'] == 'news':
			tweets.append({'text': tweet['text']})
	context['tweets'] = tweets
	#filter here by checking source
	
	#instagram
	if 'localhost:9000' not in sys.argv:
		if 'instagram_session' not in request.session.keys():
			data = {'code': request.session['code'],
			        'grant_type': 'authorization_code',
			        'redirect_uri': 'http://10.0.1.11:8000/tumblrSandbox/getSessionInstagram'}
			request.session['instagram_session'] = instagram.get_auth_session(data=data, decoder=json.loads)
		media = requests.get("https://api.instagram.com/v1/tags/"+urllib.quote(urllib.unquote(search).replace(" ", ""))+"/media/recent", params={'client_id': "3cc0c367787843d4a97d8c59cfc9b208", 'min_id': min_id})
		tags = request.session['instagram_session'].get('https://api.instagram.com/v1/tags/search', params={'format': 'json','q':request.GET.get('search'), 'access_token':request.session['instagram_session'].access_token})
		try:
			media = json.loads(media.text)
	 	except ValueError, e:
	 		media = {}
		posts = []
		#nextLink = media['pagination']['next_url']

		cap = 'No caption'
		if 'data' in media.keys():
			for post in media['data']:
				if 'caption' in post.keys():
					if post['caption'] is not None:
						cap = post['caption']['text']
				datetime.datetime.fromtimestamp(float(post['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
				posts.append({'tags': post['tags'], 'id': post['id'], 'link':post['link'], 'likes':post['likes']['count'], 'url': post['images']['standard_resolution']['url'], 'username': post['user']['username'], 'date_created': post['created_time'] ,'caption': cap }) 
		context['posts']= posts # 'nextLink': nextLink
		#context['next_max_tag_id'] = media['pagination']['next_max_tag_id']
		#get insta tags
		tags = tags.json()
		tag_info = []
		if 'data' in tags.keys():
			for tag in tags['data']:
				tag_info.append({'media_count': tag['media_count'], 'name': tag['name'], 'url': 'https://api.instagram.com/v1/tags/'+tag['name']+'/media/recent?client_id=3cc0c367787843d4a97d8c59cfc9b208'})
			context['tags_info']=tag_info
		context['search'] = search
	else:
		context['posts'] = []
		context['next_max_tag_id'] = 0
		context['search'] = []
	return render(request, 'tumblrSandbox/getSnapshotNew.html', context)


@csrf_exempt
def getSessionTumblr(request):
	#check if user already has verified token if not do:
	blog_name = request.session['blog_name'] or 'lampsdotcom'
	if 'tumblr_session' not in request.session.keys():
		request.session['tumblr_session'] = tumblr.get_auth_session(request.session['tumblr_oauth_token'], request.session['tumblr_oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	#else:
		#
	options = {'type': 'photo', 'source': 'http://img2.wikia.nocookie.net/__cb20120427202836/gameofthrones/images/7/78/House_Stark_sigil.jpg'}
	post = request.session['tumblr_session'].post('http://api.tumblr.com/v2/blog/'+blog_name+'/post', data=options)
	options = {'base-hostname': blog_name+'.tumblr.com'}
	followers = request.session['tumblr_session'].get('http://api.tumblr.com/v2/blog/'+blog_name+'.tumblr.com/followers', data=options)
	post_options = {'base-hostname': blog_name+'.tumblr.com', 'reblog_info': 'true', 'notes_info': 'true'}
	posts = request.session['tumblr_session'].get('http://api.tumblr.com/v2/blog/'+blog_name+'.tumblr.com/posts?api_key=zLZDEzKfKaxtlMeFnG1dXrZ4jlo1pFZuDZRLQGR7izKBHB7DeJ', params=post_options)
	post_options2 = {'base-hostname': blog_name+'.tumblr.com', 'reblog_info': 'true', 'notes_info': 'true', 'offset': 20}
	posts2 = request.session['tumblr_session'].get('http://api.tumblr.com/v2/blog/'+blog_name+'.tumblr.com/posts?api_key=zLZDEzKfKaxtlMeFnG1dXrZ4jlo1pFZuDZRLQGR7izKBHB7DeJ', params=post_options2)
	post_options3 = {'base-hostname': blog_name+'.tumblr.com', 'reblog_info': 'true', 'notes_info': 'true', 'offset': 40}
	posts3 = request.session['tumblr_session'].get('http://api.tumblr.com/v2/blog/'+blog_name+'.tumblr.com/posts?api_key=zLZDEzKfKaxtlMeFnG1dXrZ4jlo1pFZuDZRLQGR7izKBHB7DeJ', params=post_options3)
	
	info_options = {'base-hostname': blog_name+'.tumblr.com'}
	info = request.session['tumblr_session'].get('http://api.tumblr.com/v2/blog/'+blog_name+'.tumblr.com/info?api_key=zLZDEzKfKaxtlMeFnG1dXrZ4jlo1pFZuDZRLQGR7izKBHB7DeJ', data=options)
	context = { 'posts':json.loads(posts.text),'posts2':json.loads(posts2.text),'posts3':json.loads(posts3.text),  }
	post_info = []
	posts = context['posts']['response']['posts'] + context['posts2']['response']['posts'] + context['posts3']['response']['posts']
	for post in posts:
		reblogs = 0
		likes = 0
		id = post['id']
		#answers = 0
		#posted = False
		#src = ''
		#if 'photos' in post:
		#	src = post['photos'][0]['original_size']['url']
		if 'notes' in post:
			for note in post['notes']:
				if note['type'] == "reblog":
					reblogs = reblogs +1
				if note['type'] =="like":
					likes = likes + 1
				#if note['type'] == "answer":
				#	answers = answers + 1
				#if note['type'] == "posted":
				#	posted = True
		post_info.append({'reblogs': reblogs, 'likes': likes, 'id': id}) #'answers': answers, 'posted': posted, 'src': src
	context2 = {'followers':json.loads(followers.text), 'posts':post_info, 'info':json.loads(info.text)}
	#postsReblogs = get from posts
	#postsLikes = get from posts
	return render(request, 'tumblrSandbox/getSession.html', context2)
	#return HttpResponse(status=201)

@csrf_exempt
def getSessionTwitter(request):
	if 'twitter_session' not in request.session.keys():
		request.session['twitter_session'] = twitter.get_auth_session(request.session['twitter_oauth_token'], request.session['twitter_oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	#else:
		#should already be authenticated
	search_query = {'q':' -RT filter:' + request.session['twitter_mediatype'] + " lang:en", "geocode": '33.677903,-117.840679,0.8mi', 'count':100, 'result_type': 'recent'} #filter:' + request.session['twitter_mediatype'] + "
	#requester('tweets_twitter', request.session['twitter_session'], search_query)
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)

	search_results = json.loads(search_results.text)
	tweets = []
	print search_results['statuses']
	for tweet in search_results['statuses']:
		if request.session['twitter_mediatype'] == 'images':
			if 'media' in tweet['entities'].keys():
				if len(tweet['entities']['media']) > 0:
					media_url = tweet['entities']['media'][0]['media_url_https']
			else:
				media_url = ""
			if len(tweet['entities']['urls']) > 0:
				url = tweet['entities']['urls'][0]['url']
			tweets.append({'text': tweet['text'], 'url': media_url, 'id_str': tweet['user']['id_str'], 'screen_name': tweet['user']['screen_name']  }) #hashtags retweet_count id
			print tweet
		elif request.session['twitter_mediatype'] == 'news':
			tweets.append({'text': tweet['text']})
	context = {'tweets': tweets}
	return render(request, 'tumblrSandbox/getSessionTwitter.html', context)

@csrf_exempt
def getSessionTwitterNew(request):
	if 'twitter_session' not in request.session.keys():
		request.session['twitter_session'] = twitter.get_auth_session(request.session['twitter_oauth_token'], request.session['twitter_oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	#else:
		#should already be authenticated
	search_query = {'q':request.session['twitter_search'] + ' -RT filter:' + request.session['twitter_mediatype'] + " lang:en"}
	#requester('tweets_twitter', request.session['twitter_session'], search_query)
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)
	search_results = json.loads(search_results.text)
	tweets = []
	for tweet in search_results['statuses']:
		if request.session['twitter_mediatype'] == 'images':
			if 'media' in tweet['entities'].keys():
				if len(tweet['entities']['media']) > 0:
					media_url = tweet['entities']['media'][0]['media_url_https']
			else:
				media_url = ""
			if len(tweet['entities']['urls']) > 0:
				url = tweet['entities']['urls'][0]['url']
			tweets.append({'text': tweet['text'], 'url': media_url, 'id_str': tweet['user']['id_str'], 'screen_name': tweet['user']['screen_name']  }) #hashtags retweet_count id
		elif request.session['twitter_mediatype'] == 'news':
			tweets.append({'text': tweet['text']})
	context = {'tweets': tweets, 'access_token': request.session['twitter_session'].access_token}
	return render(request, 'tumblrSandbox/getSessionTwitter.html', context)

def postToTwitter(request):
	options = {'status': 'Post Succesful'}
	post = request.session['session'].post('https://api.twitter.com/1.1/statuses/update.json', data=options)
	tweet_info = []
	user_info = request.session['session'].get('https://api.twitter.com/1.1/account/verify_credentials.json', params={})
	user_info_json = json.loads(user_info.text)
	user_timeline = request.session['session'].get('https://api.twitter.com/1.1/statuses/user_timeline.json', params={'screen_name': user_info_json['screen_name'] })
	user_timeline = json.loads(user_timeline.text)
	for tweet in user_timeline: 
		tweet_info.append({'retweets': tweet['retweet_count'], 'favorites': tweet['favorite_count'], 'text':tweet['text']})
	context={'user_info_followers': user_info_json['followers_count'], 'user_info_friends': user_info_json['friends_count'],'user_info_statuses': user_info_json['statuses_count'], 'user_timeline':user_timeline, 'tweet_info': tweet_info }
	return render(request, 'tumblrSandbox/getSessionTwitter.html', context)

def mentionUser(request):
	#status = request.session['session'].post("https://api.twitter.com/1.1/direct_messages/new.json", data={'screen_name': 'andrewthreethou', 'text': request.GET.get('text')})
	options = {'status': request.GET.get('text')}
	post = request.session['session'].post('https://api.twitter.com/1.1/statuses/update.json', data=options)
	#import pdb; pdb.set_trace(); #	
	status = json.loads(post.text)
	context = {'status': status}
	return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def getSessionInstagram(request):
	data = {'code': request.GET['code'],
	        'grant_type': 'authorization_code',
	        'redirect_uri':  request.build_absolute_uri('/tumblrSandbox/getSessionInstagram') }
	session = instagram.get_auth_session(data=data, decoder=json.loads)
	request.session['code'] = request.GET['code']
	request.session['instagram_session'] = session
	
	#tags = session.get('https://api.instagram.com/v1/tags/search', params={'format': 'json','q':request.session['instagram_search'], 'access_token':session.access_token})
	#''''' for likes vvvvvvv''''''
	#tags = session.get('https://api.instagram.com/v1/users/self/media/liked', params={'max_like_id': 1150014038812429291, 'access_token':session.access_token})
	#''''''''' for users vvvvv'''''''
	print session.access_token
	tags = session.get('https://api.instagram.com/v1/users/' + request.session['instagram_search'] + '/media/recent', params={'format': 'json', 'access_token':session.access_token})
	#tags = session.get('https://api.instagram.com/v1/media/' + request.session['instagram_search'], params={'format': 'json', 'access_token':session.access_token})
	print tags
	tags = tags.json()
	tag_info = []
	print tags['data']
	for tag in tags['data']:
		tag_info.append({'media_count': tag['media_count'], 'name': tag['name'], 'url': 'https://api.instagram.com/v1/tags/'+tag['name']+'/media/recent?client_id=3cc0c367787843d4a97d8c59cfc9b208'})
	context = {'tag_info': tag_info}
	return render(request, 'tumblrSandbox/getSessionInstagram.html', context)

	#data = {'code': request.GET['code'],
	#        'grant_type': 'authorization_code',	
	#        'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagram')}
	#session = instagram.get_auth_session(data=data, decoder=json.loads)
	#request.session['code'] = request.GET['code']
	#request.session['instagram_session'] = session

	
	#context = {'loc_info': loc_info, 'image_info': image_info}
	#return render(request, 'tumblrSandbox/searchLocations.html', context)

@csrf_exempt
def getSessionInstagramNew(request):
	data = {'code': request.GET['code'],
	        'grant_type': 'authorization_code',	
	        'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagram')}
	session = instagram.get_auth_session(data=data, decoder=json.loads)
	request.session['code'] = request.GET['code']
	request.session['instagram_session'] = session
	tags = session.get('https://api.instagram.com/v1/tags/search', params={'format': 'json','q':request.session['instagram_search'], 'access_token':session.access_token})
	
	tags = tags.json()
	tag_info = []
	#import pdb; pdb.set_trace();
	for tag in tags['data']:
		tag_info.append({'media_count': tag['media_count'], 'name': tag['name'], 'url': 'https://api.instagram.com/v1/tags/'+tag['name']+'/media/recent?client_id=3cc0c367787843d4a97d8c59cfc9b208'})
	context = {'tag_info': tag_info}
	return render(request, 'tumblrSandbox/getSessionInstagramNew.html', context)


def getImagesByTag(request):
	media = requests.get("https://api.instagram.com/v1/tags/"+request.GET.get('tag')+"/media/recent", params={'client_id': "3cc0c367787843d4a97d8c59cfc9b208", 'count':33})
	media = json.loads(media.text)
	posts = []
	#nextLink = media['pagination']['next_url']

	import pdb; pdb.set_trace();
	for post in media['data']:
		if 'caption' in post.keys():
			cap = post['caption']['text']
		else:
			cap = 'No caption'
		posts.append({'tags': post['tags'],  'link':post['link'], 'likes':post['likes']['count'], 'url': post['images']['standard_resolution']['url'], 'username': post['user']['username'], 'caption': cap }) 
	context = {'posts': posts,} # 'nextLink': nextLink
	return HttpResponse(json.dumps(context), content_type="application/json")

def getImagesByTagNew(request):
	#twitter
	search_query = {'q':request.GET.get('search') + ' -RT filter:images lang:en', 'max_id': request.GET.get('max_id_twi'), 'count': '33'}#
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)
	search_results = json.loads(search_results.text)
	tweets = []
	if 'statuses' in search_results.keys():
		for tweet in search_results['statuses']:
			if request.session['twitter_mediatype'] == 'images' and tweet['user']['verified'] == False:
				if 'media' in tweet['entities'].keys():
					if len(tweet['entities']['media']) > 0:
						media_url = tweet['entities']['media'][0]['media_url_https']
				else:
					media_url = ""
				if len(tweet['entities']['urls']) > 0:
					url = tweet['entities']['urls'][0]['url']
				tweets.append({'text': tweet['text'], 'url': media_url, 'id': tweet['id'], 'screen_name': tweet['user']['screen_name'], 'date_created': tweet['created_at'] }) #hashtags retweet_count id
			elif request.session['twitter_mediatype'] == 'news':
				tweets.append({'text': tweet['text']})
		#get posted date as well
	#context['tweets'] = tweets
	#instagram
	media = requests.get("https://api.instagram.com/v1/tags/"+request.GET.get('search')+"/media/recent", params={'client_id': "3cc0c367787843d4a97d8c59cfc9b208", 'max_tag_id': request.GET.get('max_id_in'), 'count': '45'})
	media = json.loads(media.text)
	posts = []
	#nextLink = media['pagination']['next_url']
	if 'data' in media.keys():
		for post in media['data']:
			cap = 'No caption'
			if 'caption' in post.keys():
				if post['caption'] is not None:
					cap = post['caption']['text']
			posts.append({'tags': post['tags'],'id': post['id'], 'link':post['link'], 'likes':post['likes']['count'], 'url': post['images']['standard_resolution']['url'], 'username': post['user']['username'], 'date_created': post['created_time'] ,'caption': cap }) 
	next_max_tag_id = 0
	if 'pagination' in media.keys():
		if 'next_max_tag_id' in media['pagination'].keys():
			next_max_tag_id = media['pagination']['next_max_tag_id']
	context = {'posts': posts, 'tweets': tweets, 'next_max_tag_id': next_max_tag_id } # 'nextLink': nextLink
	return HttpResponse(json.dumps(context), content_type="application/json")


def commentIG(request):
	options = {'access_token': request.session['token'], 'text':request.GET.get('text')}
	status = request.session['session'].post('https://api.instagram.com/v1/media/'+request.GET.get('media_id')+'/comments', data=options)
	return HttpResponse(json.dumps(status.text), content_type="application/json")

def editOrDeletePost(request):
	#check if user already has verified token if not do:
	post_id = request.POST.get('postID')
	action = request.POST.get('action')
	request.session['blog_url'] =  request.GET.get('blog')
	if not request.session['session']:
		if not request.session['oauth_token'] or not request.session['oauth_token_secret']:
			return redirect(authen)
		request.session['session'] = tumblr.get_auth_session(request.session['oauth_token'], request.session['oauth_token_secret'], data={'oauth_verifier':request.GET.get('oauth_verifier')})
	if action == 'edit':
		options = {'id':post_id, 'date':request.POST.get('date')}
	if action == 'delete':
		options = {'id':post_id}
	r = request.session['session'].post('http://api.tumblr.com/v2/blog/'+request.session['blog_url']+'/post/' + action, data=options)
	return HttpResponse(status=201)

def getPictures(platform, session, options):
	endpoints={
		#'tumblr': 'https://api.tumblr.com/v2/blog/{base-hostname}/posts'+[/type]+'?api_key='+{key},
		'instagram': 'https://api.instagram.com/v1/tags/snow/media/recent?access_token=ACCESS-TOKEN', 
		'twitter': 'https://api.twitter.com/1.1/search/tweets.json', 
	}
	data = session.get(endpoints[platform], params = options)
	return handlePictures(data, platform)

def handlePictures(data, platform):
	data = json.loads(data.text)
	image = ''
	if platform == "twitter": 
		image = Image(
			favorites= data['favorite_count'],
			text= data['text'],
			link= data['link'],
			image_url= data['entities']['media'][0]['media_url_https'],
			social_network= 'twitter',
			username= 'required',
			retweets= data['retweet_count'],
			tags= data['hashtags'] 
		)
	elif platform == 'instagram':
		image = Image(
			favorites= data['likes']['count'],
			text= data['caption']['text'] or 'no caption',
			link= data['link'],
			image_url= data['images']['standard_resolution']['url'],
			social_network= 'instagram',
			username= data['user']['username'],
			tags= data['tags']
		)
	return image

def postUpdateDelete(platformAction, session, options):
	endpoints = {
	'post_twitter': 'https://api.twitter.com/1.1/statuses/update.json', #id etc 
	'delete_tweet_twitter': 'https://api.twitter.com/1.1/statuses/destroy/'+id+'.json',

	'post_tumblr':'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post', #RESPONSE 201
	'edit_tumblr': 'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post/edit', # RESPONSE 200
	'delete_tumblr': 'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post/delete', #RESPONSE 200

	'comment_instagram': 'https://api.instagram.com/v1/media/'+media_id+'/comments', #code 200
	'delete_instagram': 'https://api.instagram.com/v1/media/'+media_id+'/comments' #code 200
	}
	data = session.get(endpoints[platformAction], params = options)
	return handlePostResponse(data, platformAction)

def handlePostResponse(data, platformAction):
	if platformAction.endsWith('_twitter'):
		return responseCode
	if platformAction.endsWith('_tumblr'):
		return responseCode
	if platformAction.endsWith('_instagram'):		
		return responseCode
	pass

def misc(platform, session, options):
	endpoints= {
		'mentions_twitter': 'https://api.twitter.com/1.1/statuses/mentions_timeline.json',  
		'user_tweets_twitter': 'https://api.twitter.com/1.1/statuses/user_timeline.json',
		'direct_message_twitter': 'https://api.twitter.com/1.1/direct_messages/new.json',
		'tags_instagram': 'https://api.instagram.com/v1/tags/search?q=snowy&access_token=ACCESS-TOKEN',
		#'media_tumblr': 'https://api.tumblr.com/v2/blog/{base-hostname}/posts'+[/type]+'?api_key='+{key},
	}
	data = session.get(endpoints[platformAction], params = options)
	return handleDataResponse(data, platformAction)

def handleDataResponse(data, platformAction):
	if platformAction.endsWith('_twitter'):
		return tweets
	elif platformAction.endsWith('_instagram'):
		return tags
	elif platformAction.endsWith('_tumblr'):
		return media
	pass

def requester(requestKeyword, session, options):
	toEndpoint = {
	'post_twitter': 'https://api.twitter.com/1.1/statuses/update.json', #id etc 
	'delete_tweet_twitter': 'https://api.twitter.com/1.1/statuses/destroy/3.json', #+id instead of 3

	#'post_tumblr':'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post', #RESPONSE 201
	#'edit_tumblr': 'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post/edit', # RESPONSE 200
	#'delete_tumblr': 'https://api.tumblr.com/v2/blog/'+ base_hostname+'/post/delete', #RESPONSE 200

	#'comment_instagram': 'https://api.instagram.com/v1/media/'+media_id+'/comments', #code 200
	#'delete_instagram': 'https://api.instagram.com/v1/media/'+media_id+'/comments' #code 200
	}
	if requestKeyword != 'post_twitter' or requestKeyword != 'comment_instagram':
		data = session.get(toEndpoint[requestKeyword], params = options)
		#import pdb; pdb.set_trace();
	else:
		data = session.post(toEndpoint[requestKeyword], data = options)
		#import pdb; pdb.set_trace();
	return dataToModel(data, requestKeyword)

def givePermission(request):
	platform = request.GET.get('platform')
	if platform == 'in':
		request.session['instagram_search'] =  request.GET.get('search')
		#if 'oauth_token' in request.session.keys() and 'oauth_token_secret' in request.session.keys() and 'session' in request.session.keys():
		#	return givePermission(request)
		#else:
		params = {'redirect_uri': 'http://127.0.0.1:8000/tumblrSandbox/getSessionInstagram',
	          'response_type': 'code',
	          'client_id': '3cc0c367787843d4a97d8c59cfc9b208',
	          'scope': 'likes comments'}
		authorize_url = instagram.get_authorize_url(**params)
	elif platform == 'twi':
		request.session['twitter_search'] =  request.GET.get('search')
		request.session['twitter_mediatype'] =  request.GET.get('mediatype')
		if 'twitter_oauth_token' in request.session.keys() and 'twitter_oauth_token_secret' in request.session.keys() and 'twitter_session' in request.session.keys():
			return givePermission(request)
		else:
			request_token, request_token_secret = twitter.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':'10.0.1.11/tumblrSandbox/getSessionTwitter'})
			authorize_url = twitter.get_authorize_url(request_token)
			request.session['twitter_oauth_token'] = request_token
			request.session['twitter_oauth_token_secret'] = request_token_secret
	return redirect(authorize_url)

def authenAPI(request):

	request.session['twitter_search'] =  'starbucks'
	request.session['twitter_mediatype'] =  'images'
	request.session['instagram_search'] =  'starbucks'

	request_token, request_token_secret = twitter.get_request_token(method='POST', key_token='oauth_token', key_token_secret='oauth_token_secret', data={'oauth_callback':request.build_absolute_uri('/tumblrSandbox/getSessionTwitter')})
	authorize_url_twi = twitter.get_authorize_url(request_token)
	request.session['twitter_oauth_token'] = request_token
	request.session['twitter_oauth_token_secret'] = request_token_secret


	params = {'redirect_uri': request.build_absolute_uri('/tumblrSandbox/getSessionInstagram'),
          'response_type': 'code',
          'client_id': '3cc0c367787843d4a97d8c59cfc9b208',
          'scope': 'likes comments'}
	authorize_url_in = instagram.get_authorize_url(**params)
	context = {'authorize_url_in':authorize_url_in, 'authorize_url_twi':authorize_url_twi}
	return HttpResponse(json.dumps(context), content_type="application/json")

def getImagesAPI(request):
	#twitter
	search_query = {'q':request.GET.get('search', 'starbucks') + ' -RT filter:images lang:en', 'count': 33}
	max_id = request.GET.get('max_id_twi', -1)
	if max_id != -1: 
		search_query['max_id'] = max_id
	search_results = request.session['twitter_session'].get('https://api.twitter.com/1.1/search/tweets.json', params=search_query)
	tweets = []
	try:
		search_results = json.loads(search_results.text)
		if 'statuses' in search_results.keys():
			for tweet in search_results['statuses']:
				if request.session['twitter_mediatype'] == 'images' and tweet['user']['verified'] == False:
					if 'media' in tweet['entities'].keys():
						if len(tweet['entities']['media']) > 0:
							media_url = tweet['entities']['media'][0]['media_url_https'].split('/')[4]
					else:
						media_url = ""
					if len(media_url) > 0:
						# 'date_created': tweet['created_at']
						#url = 'http://twitter.com/'+tweet['user']['id_str']+'/status/'+tweet['id_str']
						tweets.append({
							'source': 2,
							'body': tweet['text'],  
							'sourceUid': tweet['id_str'],
							'extra':{ 
								'username': tweet['user']['screen_name'],
								'hash': tweet['id_str'],
								'imgHash': media_url, #get hash
								'likes':tweet['favorite_count'],
								'retweet':tweet['retweet_count']
							}
						})
					#elif request.session['twitter_mediatype'] == 'news':
						#tweets.append({'text': tweet['text']})
	except ValueError:
   	 	pass
	else:
		pass

	#instagram
	params={'client_id': "3cc0c367787843d4a97d8c59cfc9b208", 'count': 33}
	max_id=request.GET.get('max_id_in')
	if max_id != -1: 
		search_query['max_tag_id'] = max_id
	media = requests.get("https://api.instagram.com/v1/tags/"+urllib.quote(urllib.unquote(request.GET.get('search', 'starbucks')).replace(" ", ""))+"/media/recent", params=params)
	posts = []
	next_max_tag_id = 0
	try:
		media = json.loads(media.text)
		if 'data' in media.keys():
			for post in media['data']:
				cap = 'No caption'
				if 'caption' in post.keys():
					if post['caption'] is not None:
						cap = post['caption']['text']
					#'tags': post['tags'],  'date_created': post['created_time']
				posts.append({
					'source': 4, 
					'sourceUid': post['id'],
					'body': cap, 
					'extra':{ 
						'username': post['user']['username'],
						'hash':post['link'].split('/')[4], 
						'imgHash': post['images']['standard_resolution']['url'].split('/')[5], 
						'likes':post['likes']['count'], 
						'comments': post['comments']['count']
					}
				}) 
		next_max_tag_id = 0
		if 'pagination' in media.keys():
			if 'next_max_tag_id' in media['pagination'].keys():
				next_max_tag_id = media['pagination']['next_max_tag_id']
	except ValueError:
   	 	pass
	else:
		pass
	if len(tweets) > 0:
		new_max_id_twi = tweets[-1]['sourceUid']
	else:
		new_max_id_twi = 0
	next_url = request.build_absolute_uri('/tumblrSandbox/getImagesAPI')+'/?search=' + urllib.quote(urllib.unquote(request.GET.get('search', 'graham')).replace(" ", "")) + '&max_id_twi=' + new_max_id_twi +'&max_id_in=' + str(next_max_tag_id)
	context = posts + tweets # 'next_url': next_url }
	response = HttpResponse(json.dumps(context), content_type="application/json")
	response.__setitem__('next_url', next_url)
	return response
		
	#authorize
	#check for in or twi
	#link has to contain username
	#get all from database with same user name
	#enable user to give permission

def shDemo(request):
	return render(request, 'tumblrSandbox/shDemo.html')

def getInstaPics(request):
	params = {'redirect_uri': 'http://127.0.0.1:8000/tumblrSandbox/getInstaPicsResults',
          'response_type': 'code',
          'client_id': '3cc0c367787843d4a97d8c59cfc9b208',
          'scope': 'likes comments'}
	authorize_url = instagram.get_authorize_url(**params)
	return redirect(authorize_url)

@csrf_exempt
def getInstaPicsResults(request):
	data = {'code': request.GET['code'],
	        'grant_type': 'authorization_code',	
	        'redirect_uri': 'http://127.0.0.1:8000/tumblrSandbox/getInstaPicsResults'}
	session = instagram.get_auth_session(data=data, decoder=json.loads)
	request.session['code'] = request.GET['code']
	request.session['instagram_session'] = session
	
	photos = session.get('https://api.instagram.com/v1/users/self/media/recent', params={'access_token':session.access_token})
	
	photos = photos.json()
	photo_info = []
	for photo in photos['data']:
		#if 'caption' in photo.keys():
			#cap = photo['caption']['text']
		#else:
			#cap = 'No caption' , 'caption': cap
		photo_info.append({'tags': photo['tags'],  'link':photo['link'], 'likes':photo['likes']['count'], 'url': photo['images']['standard_resolution']['url'], 'username': photo['user']['username'] }) 
	context = {'photos': photo_info, 'code': '#' + request.GET['code'], 'session': session} # 'nextLink': nextLink
	
	return render(request, 'tumblrSandbox/myPhotos.html', context)

'''
	#twitter
	#tweet_info.append({'retweets': tweet['retweet_count'], 'favorites': tweet['favorite_count'], 'text':tweet['text']}) #need link to tweet and username
	twitterModel= {
		'favorites': json['favorite_count'],
		'text': json['text'],
		'link': 'required',
		'image_url': json['entities']['media'][0]['media_url_https'],
		'social_network': 'twitter',
		'username': 'required',
		'retweets': json['retweet_count'],
		'tags': json['hashtags'] 
		}#returns an array that still needs to br proccessed

	#instagram	#posts.append({'tags': post['tags'], 'link':post['link'], 'likes':post['likes']['count'], 'url': post['images']['standard_resolution']['url'], 'username': post['user']['username'], 'caption': cap }) 
	instagramToModel = {
		'favorites': json['likes']['count'],
		'text': json['caption']['text'] or 'no caption',
		'link': json['link'],
		'image_url': json['images']['standard_resolution']['url'],
		'social_network': 'instagram',
		'username': json['user']['username'],
		'retweets': 'optionaltwitter',
		'tags': json['tags'], 
		}
	important or possibly useful endpoints:
	Twitter:

	Search for tweets:
	https://api.twitter.com/1.1/search/tweets.json
	Get last mentions:
	https://api.twitter.com/1.1/statuses/mentions_timeline.json
	Post a tweet:
	https://api.twitter.com/1.1/statuses/update.json

	Instagram:
	Get latest media with a certain tag:
	https://api.instagram.com/v1/tags/snow/media/recent?access_token=ACCESS-TOKEN
	Search for tags:
	https://api.instagram.com/v1/tags/search?q=snowy&access_token=ACCESS-TOKEN
	Comment:
    https://api.instagram.com/v1/media/{media-id}/comments 'text=This+is+my+comment'

	twitter to model dictionary:
	favorites = likes
	status = text
	url = link
	media_url = image_url
	social_network = twitter
	username = username
	retweets = retweets
	hashtags = tags

	instragram to model dictionary:
	likes = likes
	caption = text
	url = link



	model:
	favorites/likes = required
	text/caption = required
	link = required
	image_url = required
	social_network = required
	username = required
	retweets = optional twitter
	tags = optional 


	"hashtags": [
          {
            "text": "FreeBandNames",
def getQueue():
	queue = request.session['session'].post('http://api.tumblr.com/v2/blog/'+request.session['blog_url']+'/posts/queue', '')
	import pdb; pdb.set_trace();
	return queue.json()
'''

