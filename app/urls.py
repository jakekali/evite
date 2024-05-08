from django.urls import path, include
from . import views
from .views import event_views
from .views import index

urlpatterns = [
    # path('', index.index, name='index'),
    path('', event_views.createEvent, name='index'),
    path('myEvents/', event_views.myEvents, name='myEvents'),
    path('createEvent/', event_views.createEvent, name='createEvent'),
    path('createEvent/background/', event_views.selectBackground, name='selectBackground'),
    path('createEvent/preview/<int:event_id>/', event_views.eventPreview, name='eventPreview'),
    path('createEvent/guests/<int:event_id>/', event_views.guestPage, name='addGuests'),

    path('editGuests/', event_views.editGuests, name='editGuests'),
    path('newGuest/', event_views.newGuest, name='newGuest'),
    path('editGuests/<str:hash>', event_views.editGuests, name='editGuests'),

    path('createEvent/guests/updateRow/', index.updateRow, name='updateRow'),
    path('createEvent/guests/table/<int:event_id>/', index.getTableData, name='deleteRow'),
    path('getStats/<int:event_id>/', index.getStats, name='getStats'),
    

    path('invite/event_id/<int:event_id>/', event_views.get_animation, name='preview-invite'),
    path('invite/<str:hash>/', event_views.getInvitePage, name='invite'),
    path('invite/<str:hash>/<int:isAttending>', event_views.getInvitePage, name='invite'),



    # send invitation(s)
    path('sendInvitation/<int:event_id>/<int:guest_id>/', event_views.sendOneInvitation, name='send-invitation'),  
    path('sendAllInvitations/<int:event_id>/', event_views.sendAllInvitations, name='send-all-invitations'),  
]