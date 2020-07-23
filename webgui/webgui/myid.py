from django.shortcuts import render,HttpResponseRedirect

from .__init__ import tokenData

def showid(request):
	tokenCookie = request.COOKIES.get('token')
	if (not tokenCookie) or (not tokenData().chkToken(tokenCookie)):
		return HttpResponseRedirect('/login')
	timeoutFlag,timeoutResponse = tokenData().cookieTimeout(request)
	if timeoutFlag:
		return timeoutResponse
	return render(request,'myid.html',{'identity' : tokenData().getIdentity(tokenCookie).replace('-',' ')})