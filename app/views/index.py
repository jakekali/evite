from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..models.events import Event
from ..models.guests import Guest, STATUS_CHOICES
import json
from django.db import models

def index(request):
    return render(request, 'index.html', {'loggedIn':  request.user.is_authenticated})

def updateRow(request):
    if request.user.is_authenticated:

        if request.POST['action'] == 'update_row':
            guest_id = request.POST['guest_id']
            guest = Guest.objects.get(pk=guest_id)
            if guest.event.owner == request.user:
                guest.name = request.POST['name']
                guest.email = request.POST['email']
                guest.phone = request.POST['phone']
                guest.status = request.POST['status']
                guest.save()

                response = json.dumps({
                    'success': True,
                    "guest" : guest.get_dict()
                })
                print(response)
                return  HttpResponse(response, content_type='application/json')
            else:
                response = json.dumps({
                    'success': False,
                    'message': f'You do not have permission to edit this guest list, {request.user.username}'
                })

                return HttpResponse(response, content_type='application/json')
        else:
            response = json.dumps({
                'success': False,
                'message': 'Invalid request'
            })
            return HttpResponse(response, content_type='application/json')
    else:
        response = json.dumps({
            'success': False,
            'message': 'You must be logged in to edit this guest list'
        })
        return HttpResponse(response, content_type='application/json')
    
def getTableData(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
   

        draw = int(request.POST.get('draw'))
        start = int(request.POST.get('start'))
        length = int(request.POST.get('length'))
        search_value = request.POST.get('search[value]') if request.POST.get('search[value]') != 0 else None
        # cols = ['pk', 'name', 'email', 'phone', 'status']
        # order_column = cols[int(request.POST.get('order[0][column]'))] if (request.POST.get('search[value]')) != 0 else None
        # order_direction = request.POST.get('order[0][dir]') if request.POST.get('search[value]') != 0 else None

        print("draw", draw, 
              "start", start, 
              "length", length, 
              "seach_val", search_value, )
            #   "order col", type(order_column), 
            #   "order dir", order_direction)

        guests = Guest.objects.filter(event=event)
        recordsTotal = guests.count()
        from django.db.models import Q
        
        filter_gu = Guest.objects.filter(event=event).filter(Q(name__icontains=search_value) | 
                      Q(email__icontains=search_value) | 
                      Q(phone__icontains=search_value) | 
                      Q(status__icontains=search_value)).order_by('pk')
        
        data = filter_gu[start:start+length]
        recordsFiltered = filter_gu.count()
        

        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': [guest.get_row() for guest in data]
        }

        import json
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponse('You must be logged in to view this page')
    
def getStats(request, event_id):
    if request.user.is_authenticated:
        if not Event.objects.filter(pk=event_id).exists():
            return HttpResponse('Event not found', status=404)
        
        if not Event.objects.get(pk=event_id).owner == request.user:
            return HttpResponse('You do not have permission to view this page', status=403)
    
        event = Event.objects.get(pk=event_id)
        counts = Guest.objects.values('status').filter(event=event).annotate(total_guests=models.Count('status'))
        total_guests = Guest.objects.filter(event=event).count()

        dicti = {}
        for count in counts:
            dicti[Guest.get_pretty_status(count['status'])] = (count['total_guests'], 100*count['total_guests']/total_guests, Guest.get_status_color(count['status']))

        if request.htmx:
            return render(request, 'editEvent/stats.html', {'dicti': dicti})
        else:
            return HttpResponse(json.dumps(dicti), content_type='application/json')

    else:
        return HttpResponse('You must be logged in to view this page')

    
