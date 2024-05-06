from typing import Any
from django.db import models
from django.conf import settings
from .events import Event
from django.core.mail import send_mail

STATUS_CHOICES = [
    ('not_sent', 'Not Sent'),
    ('opened', 'Opened'),
    ('sent', 'Sent'),
    ('attending', 'Attending'),
    ('not_attending', 'Not Attending'),
]
    
class Guest(models.Model):

    @staticmethod
    def get_pretty_status(status: str) -> str:
        for choice in STATUS_CHOICES:
            if choice[0] == status:
                return choice[1]
        return status
    
    @staticmethod
    def get_status_color(status: str) -> str:
        if status == 'not_sent' or status == 'Not Sent':
            return 'grey'
        elif status == 'sent' or status == 'Sent':
            return 'blue'
        elif status == 'opened' or status == 'Opened':
            return 'yellow'
        elif status == 'attending' or status == 'Attending':
            return 'green'
        elif status == 'not_attending' or status == 'Not Attending':
            return 'red'
        

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
    
    def getJSON(self):
        import json
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'event': self.event.id
        })
    
    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
        }

    def get_row(self):
        options = ''
        for status in STATUS_CHOICES:
            options += f'<option value="{status[0]}" {"selected" if self.status == status[0] else ""}>{status[1]}</option>'

        return [f'<input type="hidden" value="{self.pk}" name="guest_id">',
                f'<input type="hidden" value="{self.pk}" name="guest_id">' + 
                f'<input type="text" value="{self.name}" name="name">',
                f'<input type="text" value="{self.email}" name="email">',
                f'<input type="text" value="{self.phone}" name="phone">',
                f'<select name="status">' +
                    options +
                f'</select>', 
                f'<button id="resend_{self.pk}" style="margin: 0px" class="home-button button" onclick="scream({self.pk})">Resend</button>'
                ]
    
    def send_invitation(self):
        subject = "You're Invited! 🎉🎉🎉"
        message = f"""Dear {self.name},

        {self.event.host} has sent you an invitation to {self.event.title}!
        <br>
        <a href="http://localhost:8000/invite/{self.hash}"> Click Here to Review & Reply </a>"""
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
