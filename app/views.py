from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate

def index(request):
    return render(request, 'index.html', {'loggedIn':  request.user.is_authenticated})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'loggedIn':  request.user.is_authenticated})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a home page
            print("User is authenticated")
            return HttpResponseRedirect('/')
        else:
            print("User is not authenticated")
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'loggedIn':  request.user.is_authenticated})

def myEvents(request):
    return render(request, 'manage/myEvents.html', {'loggedIn':  request.user.is_authenticated,
                                                    'events' : {'name1': 'Event 1', 'name2': 'Event 2', 'name3': 'Event 3',  'name4': 'Event 4', 'name5': 'Event 5' }
                                                    })
# Create your views here