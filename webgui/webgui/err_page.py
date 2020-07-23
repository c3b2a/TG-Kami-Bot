from django.shortcuts import render,HttpResponseRedirect

def page_404(request):
	return render(request,'404.html')
	
def page_500(request):
	return render(request,'500.html')