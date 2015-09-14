from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
	context={}
	return render(request, 'gallery/index.html', context)
