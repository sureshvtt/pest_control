from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index(request):
	response = {}

	if 'login_error' in request.GET and request.GET['login_error']:
		response.update({'login_error':True})

	return render(request, "login.html", response)

def login(request):
	response = {}

	if request.method == 'GET':
		response.update({'next':request.GET.get('next', '')})
		return render(request, "login.html", response)

	print request.GET
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')

	user = authenticate(username=username,password=password)
	if user is not None and user.is_active:
		auth_login(request, user)
		
		if user.userprofile and user.userprofile.get_user_type_display() in ['Admin']:

			if 'next' in request.POST and request.POST['next']:
				return HttpResponseRedirect(request.POST['next'])

			return HttpResponseRedirect(reverse('userprofile-dashboard'))

		return HttpResponseRedirect('/?login_error=true')


	return HttpResponseRedirect('/?login_error=true')

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect(reverse('index'))
