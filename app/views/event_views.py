from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.permissions import Permissions
from ..models.backgrounds import Background
from ..models.invitation import Invitation
from django_htmx.http import HttpResponseClientRedirect, retarget
import base64


backgrounds = Background.objects.all()

# backgrounds_list = [
#     { "name": "ocean",
#     "url": "https://images.unsplash.com/photo-1682687982468-4584ff11f88a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "forest",
#     "url": "https://plus.unsplash.com/premium_photo-1675355675451-d49606cb8e4a?q=80&w=2664&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "mountain",
#         "url": "https://plus.unsplash.com/premium_photo-1673254928968-b6513f32d43b?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "turtle",
#         "url": "https://images.unsplash.com/photo-1707343848873-d6a834b5f9b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "easter hot cross buns with chocolate eggs on a wooden table jesus food coffee cup",
#         "url": "https://plus.unsplash.com/premium_photo-1710267557925-4c05618b8caf?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "ocean",
#     "url": "https://images.unsplash.com/photo-1682687982468-4584ff11f88a?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "forest",
#     "url": "https://plus.unsplash.com/premium_photo-1675355675451-d49606cb8e4a?q=80&w=2664&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "mountain",
#         "url": "https://plus.unsplash.com/premium_photo-1673254928968-b6513f32d43b?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "turtle",
#         "url": "https://images.unsplash.com/photo-1707343848873-d6a834b5f9b9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     },
#     { "name": "easter hot cross buns with chocolate eggs on a wooden table jesus food coffee cup",
#         "url": "https://plus.unsplash.com/premium_photo-1710267557925-4c05618b8caf?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
#     }
#     ]

# # add everything from ^ to database
# for bg_data in backgrounds_list:
#     background = Background(title_bg=bg_data["name"], pattern_bg=bg_data["url"])
#     background.save()

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
        print(request.user.username)

        event = Event.objects.create(
                title=request.POST.get('event_name'),
                description=request.POST.get('description'),
                location=request.POST.get('location'),
                date_time=request.POST.get('date_time'),
                owner=request.user,
                host=request.POST.get('host_name')
                )

        event_id = event.pk        

        # TODO: create inviation here with card
        invitation = Invitation.objects.create(event=event)
        card_photo = request.FILES.get('file')
        invitation.card.save(card_photo.name, card_photo)

        print(invitation.card)
        out = render(request, 'newEvent/background_selection.html', {'loggedIn':  request.user.is_authenticated,
                                                                    'backgrounds' : backgrounds,
                                                                    'event_id': event_id})
        return retarget(out, '#background_selection')



    else:
        # TODO add background images via database instead of this import
        ## check up ^
        return render(request, 'newEvent/index.html', {'loggedIn':  request.user.is_authenticated, 'backgrounds': backgrounds})
    
def selectBackground(request):
    if request.htmx:

        event_id = request.POST['event_id']
        selected_bg_id = request.POST['selected_image']

        print(selected_bg_id)
        selected_bg = Background.objects.get(id=selected_bg_id)
        event = Event.objects.get(pk=event_id)
        invitation = Invitation.objects.get(event=event)

        if request.user.is_authenticated:
            if event.owner == request.uAser:
                # TODO: Add card to inviation
                invitation.background = selected_bg
                invitation.save()
                print(invitation)
                print('sup')

            else: 
                return HttpResponseClientRedirect("/login")



def eventPreview(request):
    return render(request, 'inviteView/animation.html', {'loggedIn':  request.user.is_authenticated})


def getEvents(request):
     # TODO: return events that a user has, with their card images, dates, other things that go on the list of events
    if request.user.is_authenticated:
        if event.owner == request.user:
            owned_events = Event.objects.filter(owner=event.owner)
            print(events)
            # print('sup')

        else: 
            return HttpResponseClientRedirect("/login")


# def getGuests(request):
#     # TODO get all the guests for an event (request.POST[event_id])
    
# def setsRVSP(request):
#     #TODO 