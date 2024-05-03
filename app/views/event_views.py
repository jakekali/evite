from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.permissions import Permissions
from ..models.backgrounds import Background
from ..models.invitation import Invitation
from ..models.guests import Guest

from django_htmx.http import HttpResponseClientRedirect, retarget
import base64
import math

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
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    if request.htmx:
        event = Event.objects.create(
            title=request.POST.get('event_name'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            date_time=request.POST.get('date_time'),
            owner=request.user,
            host=request.POST.get('host_name')
        )

        invitation = Invitation.objects.create(event=event)
        card_photo = request.FILES.get('file')
        invitation.card.save(card_photo.name, card_photo)

        backgrounds = Background.objects.all()

        out =  render(request, 'newEvent/background_selection.html', {'loggedIn':  request.user.is_authenticated,
                                                                    'backgrounds' : backgrounds,
                                                                    'event_id': event.pk,})

        return retarget(out, '#background_selection')

    else:
        # TODO add background images via database instead of this import
        ## check up ^
        backgrounds = Background.objects.all()


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
            if event.owner == request.user:
                # TODO: Add card to inviation
                invitation.background = selected_bg
                invitation.save()
                return HttpResponseClientRedirect("/createEvent/preview/" + event_id + "/")

            else: 
                return HttpResponseClientRedirect("/login")
            
        else:
            return HttpResponseClientRedirect("/login")



def eventPreview(request, event_id=None):
    if event_id is None:
        return HttpResponse("Event ID not provided")
    else:
        event = Event.objects.get(pk=event_id)
        invitation = Invitation.objects.get(event=event)
        print(invitation.card.url)
        return render(request, 'newEvent/preview.html', {'loggedIn':  request.user.is_authenticated, 'event': event, 'invitation': invitation})

def get_animation(request, event_id):
    if event_id is None:
        return HttpResponse("Event ID not provided")
    else:
        event = Event.objects.get(pk=event_id)
        invitation = Invitation.objects.get(event=event)
        print(invitation.card.url)
        return render(request, 'inviteView/animation.html', {'loggedIn':  request.user.is_authenticated, 'event': event, 'invitation': invitation})

def getEvents(request):
     # TODO: return events that a user has, with their card images, dates, other things that go on the list of events
    if request.user.is_authenticated:
        if event.owner == request.user:
            owned_events = Event.objects.filter(owner=event.owner)
            print(events)
            # print('sup')

        else: 
            return HttpResponseClientRedirect("/login")

def guestPage(request, event_id=None):
    #e
    return render(request, 'editEvent/guests.html', {'loggedIn':  request.user.is_authenticated})

def editGuests(request, hash=None):
    import json
    data = json.loads(request.body)

    guest_id = int(data['guests_id'])
    full_name = data['full_name']
    email = data['email']
    phone = data['phone']
    status = data['status']

    # if the current user is the owner of the event, they can edit the guest list
    if request.user.is_authenticated:
        guest = Guest.objects.filter(id=guest_id)
        if guest.event.owner == request.user:
            guest.full_name = full_name
            guest.email = email
            guest.phone = phone
            guest.status = status
            guest.save()
            return HttpResponse("Guest updated")
        
        else:
            return HttpResponse("You do not have permission to edit this guest list")
    else:
        return HttpResponse("You must be logged in to edit a guest list")



    
            
    

def setsRVSP(request):
    #TODO 
    pass

