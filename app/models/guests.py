from typing import Any
from django.db import models
from django.conf import settings
from .events import Event
from django.core.mail import send_mail

STATUS_CHOICES = [
    ('Not Sent', 'Not Sent'),
    ('Sent', 'Sent'),
    ('Opened', 'Opened'),
    ('Attending', 'Attending'),
    ('Not Attending', 'Not Attending'),
    ('Maybe', 'Maybe'),
    ('No Response', 'No Response')
]
    
class Guest(models.Model):

    def create_new_hash():
        import random
        import string
        not_unique = True
        while not_unique:
            new_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            if not Guest.objects.filter(hash=new_hash).exists():
                not_unique = False
        return new_hash
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField()

    phone = models.CharField(max_length=11, null=True, blank=True)      # is there better way? theres a phone number field pkg that exists if we want giggle
    status = models.CharField(null=False, default='Not Sent', max_length=20, choices=STATUS_CHOICES)
    hash = models.CharField(
        max_length=10,
        default=create_new_hash,
        unique=True,
        editable=False
    )

    def __str__(self):
        return f'{self.name} - {self.email} - {self.phone} - {self.status} - {self.event}'
    
    def send_invitation(self):
        subject = "You're Invited! 🎉🎉🎉"
        message = f"""Dear {self.name},

        {self.event.host} has sent you an invitation to {self.event.title}!
        <br>
        <a href="http://localhost:8000/invite/{self.event.id}/{self.id}"> Click Here to Review & Reply </a>"""
        sender = 'evite.ece464@gmail.com'

        send_mail(subject, message, sender, [self.email], html_message=message)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'email'], name='unique_guest'
            ),
            models.UniqueConstraint(
                fields=['event', 'phone'], name='unique_phone'
            )
        ]
