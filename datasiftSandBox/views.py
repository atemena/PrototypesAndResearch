from django.shortcuts import render
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def csdlTranslator(query):
	return query

# Create your views here.
def index(request):
	context={'streams': []}
	url = 'https://api.datasift.com/push/get'
	headers = {'Authorization': 'macdrewzy:c90dd8159a1e070a507689089cb46727'}
	res = requests.get(url, headers=headers)
	#import pdb; pdb.set_trace();
	context['streams'] = res.json().get('subscriptions')
	return render(request, 'datasiftSandBox/index.html', context)
#lists = requests.POST('https://api.datasift.com/v1/push/stop', headers = headers, json={'id':96f5f91a43e384690d742782d17615ea})

#s3_params = {'bucket': 'streams.shareroot.co','directory': 'data','acl': 'private','auth': {    'access_key': 'AKIAJYDTQ3GM5TMGYYRQ',    'secret_key': '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'},'delivery_frequency': 0,'max_size': 10485760,'file_prefix': 'DataSift'}

#header = {'Host': 'streams.shareroot.co.s3.amazon.aws.com', 'Date': 'JULY 6, 2015', 'Authorization':}

@csrf_exempt
def createStream(request):
	query = _queryBuilder(request.POST['query'])
	url = 'https://api.datasift.com/v1/compile' #'Connection': 'Keep-Alive',
	headers = {'Authorization': 'macdrewzy:c90dd8159a1e070a507689089cb46727'}
	req=requests.post(url, headers=headers, data={'csdl': query})
	import pdb; pdb.set_trace();
	if req.status_code == 200:
		#TODO: get directory, frequency, prefix?
		output_params = {	
			'bucket': 'streams.shareroot.co',
			'directory': request.POST['brandId'],
			'acl': 'private',
			'auth': {
				'access_key': 'AKIAJYDTQ3GM5TMGYYRQ', 
				'secret_key': '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'}, #4+z4RUBVi1Zn/VCfbhqhUp77txYrdzgvg6e6+aPF   4%2Bz4RUBVi1Zn%2FVCfbhqhUp77txYrdzgvg6e6%2BaPF
			'delivery_frequency': 60,
			'encryption': 'AES256',
			'max_size': 10485760,
			'file_prefix': "",
			'region': 'us-east-1',
			'compression': 'none'
			}
		res=requests.post('https://api.datasift.com/v1/push/create', headers=headers, json={'name': request.POST['brandId'] + '-' + request.POST['query'], 'hash': req.json().get('hash'), 'output_type': 's3', 'output_params': json.dumps(output_params)})
		print res.text
		print res.headers
		print req.json().get('hash')
		#TODO:make sure stream was created
		context = {'createdStatus': res.json(), 'streams': getStreams(), 'status_code': 200}
	else:
		return req.status_code
	return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def getStreams():
	url = 'https://api.datasift.com/push/get'
	headers = {'Authorization': 'macdrewzy:c90dd8159a1e070a507689089cb46727'}
	res = requests.get(url, headers=headers)
	return res.json()

@csrf_exempt
def stopStream(request):
	url = 'https://api.datasift.com/v1/push/stop'
	headers = {'Authorization': 'macdrewzy:c90dd8159a1e070a507689089cb46727'}
	res = requests.put(url, headers=headers, json={'id':request.POST['streamId']})
	context = {'deletedStatus': res.json(), 'streams': getStreams(), 'status_code': 200}
	return HttpResponse(json.dumps(context), content_type="application/json")

def _queryBuilder(query):
	query = query.split(",")
	csdl_query = ""
	for word in query:
		word = word.strip()
		csdl_query = csdl_query + 'tag "' + word + '" {interaction.content contains "'+word+'" } '
	first = True
	csdl_query = csdl_query + 'return {'
	for word in query:
		word = word.strip()
		if first:
			first = False
			csdl_query = csdl_query + 'interaction.content contains "' + word +'"'
		else:
			csdl_query = csdl_query + 'OR interaction.content contains "' + word +'"'
	csdl_query = csdl_query + '}'
	return csdl_query
