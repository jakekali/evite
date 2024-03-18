from django.test import TestCase
from django.db.backends.sqlite3.base import IntegrityError
from django.utils import timezone
from .models.users import User
from .models.events import Event
from .models.permissions import Permissions


# Create your tests here.
# set settings var: export DJANGO_SETTINGS_MODULE=evite.settings

class EventPermTest(TestCase):
    def setUp(self):
        User.objects.create(username="etho", email="etho@gmail.com")
        User.objects.create(username="slab", email="slab@gmail.com")
        
        """Etho creates event"""
        Event.objects.create(title="minecraft", 
                             description="Wow so fun event yay",
                             location="YouTube",
                             date_time=timezone.now,
                             owner= User.objects.get(username="etho"),
                             host="Incredible Ethoslab wow")
        
        """ Etho gives Slab permissions to event """
        Permissions.objects.create(editor=User.objects.get(username="slab"),
                                   event= Event.objects.get(title="minecraft"))
    
    def testUniqueUser(self):
        with self.assertRaises(Exception) as raised:
            User.objects.create(username="slab", email="slab@gmail.com")
        self.assertEqual(IntegrityError, type(raised.exception))

    def testCreateEvent(self):
        event1 = Event.objects.get(title="minecraft") 
        self.assertEqual(event1.location, 'YouTube')

    def testPerms(self):
        perms1 = Permissions.objects.get()