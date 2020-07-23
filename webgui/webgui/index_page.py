from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.views.decorators import csrf
import time,os

from .__init__ import tokenData

def index(request):
	return render(request,'index.html')