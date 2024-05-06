from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.backgrounds import Background
from ..models.invitation import Invitation
from ..models.guests import Guest, STATUS_CHOICES

from django_htmx.http import HttpResponseClientRedirect, retarget, HttpResponseClientRefresh
from django.core.mail import send_mass_mail, send_mail
import base64
import math
import os

import json


def myEvents(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login/')
    
    invitations = Invitation.objects.filter(event__owner=request.user)
    
    return render(request, 'manage/myEvents.html', {'loggedIn':  request.user.is_authenticated,
                                                    'invitations' : invitations })

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
    
def getInvitePage(request, hash):
    if request.htmx:
        guest = Guest.objects.get(hash=hash)

        if request.htmx.trigger == 'not_attending':
            guest.status = 'Not Attending'
            guest.save()

        if request.htmx.trigger == 'attending':
            guest.status = 'Attending'
            guest.save()

        return HttpResponseClientRedirect("/invite/" + hash)

    if hash is None:
        return HttpResponse("Event ID not provided")
    else:
        guest = Guest.objects.get(hash=hash)
        event = guest.event
        if guest.status == 'Not Sent' or guest.status == 'Sent':
            guest.status = 'Opened'
            guest.save()
        return render(request, 'inviteView/rsvp_page.html', {'loggedIn':  request.user.is_authenticated, 'event': event, 'guest' 
                                                          : guest})

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
    
    if event_id is None:
        return HttpResponse("Event ID not provided")
    else:
        event = Event.objects.get(pk=event_id)
        guests = Guest.objects.filter(event=event)

        return render(request, 'editEvent/guests1.html', {'loggedIn':  request.user.is_authenticated, 'event': event, 'guests': guests,
                                                         'STATUS_CHOICES': STATUS_CHOICES})

def editGuests(request, hash=None):
    import json
    data = json.loads(request.body)

    guest_id = int(data['guest_id'])
    name = data['name']
    email = data['email']
    phone = data['phone']
    status = data['status']

    # if the current user is the owner of the event, they can edit the guest list
    if request.user.is_authenticated:
        guest = Guest.objects.filter(id=guest_id)[0]
        if guest.event.owner == request.user:
            guest.name = name
            guest.email = email
            guest.phone = phone
            guest.status = status
            guest.save()

            data = {
                'message': 'Guest updated successfully',
                'guest_id': guest_id,
                'name': guest.name,
                'email': email,
                'phone': phone,
                'status': status
            }
            json_data = json.dumps(data)

            return HttpResponse(json_data, content_type='application/json')
        
        else:
            data = {
                'message': 'You do not have permission to edit this guest list'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'You must be logged in to edit this guest list'}), content_type='application/json')
    

def newGuest(request):

    if request.htmx:
        for key, value in request.POST.items():
            print(f'{key}: {value}')

        event_id = request.POST['event_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        # clean the phone number to remove any non numeric characters, and trim it to 11 characters
        phone = ''.join(filter(str.isdigit, phone))[:11]



        if request.user.is_authenticated:
            if request.user == Event.objects.get(pk=event_id).owner:

                Guest.objects.create(
                    event=Event.objects.get(pk=event_id),
                    name=name,
                    email=email,
                    phone=phone,
                    status='Sent'
                )

                return HttpResponseClientRefresh()

        


    import json
    data = json.loads(request.body)

    event_id = int(data['event_id'])
    name = data['name']
    email = data['email']
    phone = data['phone']
    status = data['status']

    if status == 'yes':
        rsvp = True
    elif status == 'no':
        rsvp = False
    else:
        rsvp = None

    # if the current user is the owner of the event, they can add a new guest
    if request.user.is_authenticated:
        event = Event.objects.filter(id=event_id)[0]
        if event.owner == request.user:
            guest = Guest.objects.create(
                event=event,
                name=name,
                email=email,
                phone=phone,
                status=status
            )

            data = {
                'message': 'Guest added successfully',
                'guest_id': guest.id,
                'name': guest.name,
                'email': guest.email,
                'phone': guest.phone,
                'status': guest.status,
                'hash'  : guest.hash,
            }

            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
        
        else:
            data = {
                'message': 'You do not have permission to add a guest to this event'
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'You must be logged in to add a guest to this event'}), content_type='application/json')




def sendAllInvitations(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_authenticated and event.owner == request.user:
        event.sendInvites()
        return HttpResponse(f"All emails have been sent!")
    else:
        return HttpResponse("You do not have permission to send invitations")


def sendOneInvitation(request, event_id, guest_id):
    event = Event.objects.get(pk=event_id)
    guest = Guest.objects.get(pk=guest_id, event=event)

    if request.user.is_authenticated:
        if event.owner == request.user:
            guest.send_invitation()
            data = {
                'message': 'Email sent to ' + guest.email
            }
        else:
            data = {
                'message': 'You do not have permission to send invitations'
            }

    if request.htmx:
        return HttpResponse(f'Sent!')
    
    return HttpResponse(json.dumps(data), content_type='application/json')


