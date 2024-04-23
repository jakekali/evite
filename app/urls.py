from django.urls import path, include
from . import views
from .views import event_views
from .views import index


urlpatterns = [
    path('', index.index, name='index'),
    path('myEvents/', event_views.myEvents, name='myEvents'),
    path('createEvent/', event_views.createEvent, name='createEvent'),
    path('createEvent/background/', event_views.selectBackground, name='selectBackground'),
    path('createEvent/preview/<int:event_id>/', event_views.eventPreview, name='eventPreview'),
    path('createEvent/guests/<int:event_id>/', event_views.guestPage, name='addGuests'),

    path('editGuests/', event_views.editGuests, name='editGuests'),
    path('editGuests/<str:hash>', event_views.editGuests, name='editGuests'),


    path('invite/event_id/<int:event_id>/', event_views.get_animation, name='invite'),
    
]