from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.permissions import Permissions

def index(request):
    return render(request, 'index.html', {'loggedIn':  request.user.is_authenticated})
