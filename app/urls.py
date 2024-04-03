from django.urls import path
from . import views
from .views import event_views
from .views import index


urlpatterns = [
    path('', index.index, name='index'),
    path('myEvents/', event_views.myEvents, name='myEvents'),
    path('createEvent/', event_views.createEvent, name='createEvent'),
    path('createEvent/background/', event_views.selectBackground, name='createEvent'),
    path('createEvent/preview/', event_views.eventPreview, name='createEvent'),


    # path('upload_card/', event_views.upload_card, name='upload_card'),
]