from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.permissions import Permissions
from django_htmx.http import HttpResponseClientRedirect
import base64

def myEvents(request):
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect('/accounts/login/')
    
    # usersEvents = Event.objects.filter(owner=request.user)

    return render(request, 'manage/myEvents.html', {'loggedIn':  request.user.is_authenticated,
                                                    'events' : {'name1': 'Event 1', 
                                                                'name2': 'Event 2', 
                                                                'name3': 'Event 3',  
                                                                'name4': 'Event 4', 
                                                                'name5': 'Event 5' }
                                                    })

def createEvent(request):
    if request.htmx:
        files = (request.FILES)
        print(files)
        print(request.POST.get('event_name'))
        print(request.POST.get('host_name'))
        print(request.POST.get('date_time'))
        print(request.POST.get('description'))
        print(request.POST.get('location'))

        # TODO: Add event to database

    

    else:

        return render(request, 'newEvent/index.html', {'loggedIn':  request.user.is_authenticated})

