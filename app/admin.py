from django.contrib import admin

# Register your models here.
from .models.events import Event
from .models.guests import Guest
from .models.invitation import Invitation


admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(Invitation)
