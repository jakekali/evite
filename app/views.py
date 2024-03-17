from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout

def home(request):
    return render(request, 'index.html', {'loggedIn':  request.user.is_authenticated})

def login_view(request):
    return render(request, 'login.html', {'loggedIn':  request.user.is_authenticated})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')