from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.permissions import Permissions
from django_htmx.http import HttpResponseClientRedirect, retarget
import base64


backgrounds = [
    { "name": "ocean",
    "url": "https://images.unsplash.com/photo-1682687982468-4584ff11f88a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "forest",
    "url": "https://plus.unsplash.com/premium_photo-1675355675451-d49606cb8e4a?q=80&w=2664&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "mountain",
        "url": "https://plus.unsplash.com/premium_photo-1673254928968-b6513f32d43b?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "turtle",
        "url": "https://images.unsplash.com/photo-1707343848873-d6a834b5f9b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "easter hot cross buns with chocolate eggs on a wooden table jesus food coffee cup",
        "url": "https://plus.unsplash.com/premium_photo-1710267557925-4c05618b8caf?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "ocean",
    "url": "https://images.unsplash.com/photo-1682687982468-4584ff11f88a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "forest",
    "url": "https://plus.unsplash.com/premium_photo-1675355675451-d49606cb8e4a?q=80&w=2664&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "mountain",
        "url": "https://plus.unsplash.com/premium_photo-1673254928968-b6513f32d43b?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "turtle",
        "url": "https://images.unsplash.com/photo-1707343848873-d6a834b5f9b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    },
    { "name": "easter hot cross buns with chocolate eggs on a wooden table jesus food coffee cup",
        "url": "https://plus.unsplash.com/premium_photo-1710267557925-4c05618b8caf?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    }
    
    ]



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

        # TODO: Add event to database, and return event_id
        print(files)
        print(request.POST.get('event_name'))
        print(request.POST.get('host_name'))
        print(request.POST.get('date_time'))
        print(request.POST.get('description'))
        print(request.POST.get('location'))

        event_id = 1234

        out = render(request, 'newEvent/background_selection.html', {'loggedIn':  request.user.is_authenticated,
                                                                    'backgrounds' : backgrounds,
                                                                    'event_id': event_id})
        return retarget(out, '#background_selection')

    

    else:
        # TODO add background images via database instead of this import
        return render(request, 'newEvent/index.html', {'loggedIn':  request.user.is_authenticated, 'backgrounds': backgrounds})
    
def selectBackground(request):
    if request.htmx:
        for key in request.POST:
            print(key)
            print(request.POST[key])

def eventPreview(request):
    return render(request, 'inviteView/animation.html', {'loggedIn':  request.user.is_authenticated})