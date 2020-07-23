from django.shortcuts import render,HttpResponseRedirect
from django.views.decorators import csrf
import time

def Logout(request):
	response = render(request,'logout.html')
	response.delete_cookie('token')
	response.delete_cookie('editFormSelect')
	response.set_cookie('time',str(time.time()))
	return response