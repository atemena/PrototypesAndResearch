from django.shortcuts import render

def index(request):
	return render(request, 'ccpSandbox/index.html')

def newIndex(request):
	return render(request, 'ccpSandbox/newIndex.html')

def blank(request):
	return render(request, 'ccpSandbox/blank.html')

def svgTest(request):
	return render(request, 'ccpSandbox/svgTest.html')