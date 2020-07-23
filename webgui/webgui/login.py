from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators import csrf

import time

from .__init__ import tokenData

def renderPage(request,login_dict):
	return render(request,'login.html',login_dict)

def Login(request):
	timeoutFlag,timeoutResponse = tokenData().cookieTimeout(request)
	if timeoutFlag:
		return timeoutResponse
	if request.method == 'GET':
		return renderPage(request,{'err' : ''})
	elif request.method == 'POST':
		if 'index' in request.POST:
			return HttpResponseRedirect('/')
		token = request.POST['token']
		if not token:
			return renderPage(request,{'err' : 'Token 为空'})
		Data = tokenData()
		if Data.chkToken(token):
			response = HttpResponseRedirect('/panel')
			response.set_cookie('token',token)
			response.set_cookie('time',str(time.time()))
			return response
		else:
			return renderPage(request,{'err' : 'Token 不存在'})