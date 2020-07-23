from django.shortcuts import HttpResponseRedirect

import time

def process(request):
	if 'login' in request.GET:
		return HttpResponseRedirect('/login')
	elif 'panel' in request.GET:
		return HttpResponseRedirect('/panel')
	elif 'index' in request.GET:
		return HttpResponseRedirect('/')
	elif 'logout' in request.GET:
		return HttpResponseRedirect('/logout')
	elif 'admin' in request.GET:
		return HttpResponseRedirect('/panel/admin')
	elif 'ban' in request.GET:
		return HttpResponseRedirect('/panel/ban')
	elif 'kami' in request.GET:
		return HttpResponseRedirect('/panel/kami')
	elif 'log' in request.GET:
		return HttpResponseRedirect('/panel/log')
	elif 'myid' in request.GET:
		return HttpResponseRedirect('/myid')
	else:
		return HttpResponseRedirect('/')