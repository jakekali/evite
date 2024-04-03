from django.contrib import admin

# Register your models here.
from .models.events import Event
from .models.guests import Guest
from .models.invitation import Invitation
from .models.backgrounds import Background



admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(Invitation)
admin.site.register(Background)
