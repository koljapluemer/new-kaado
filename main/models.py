from django import forms

from django.db import models
from django.contrib.auth.models import User


from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
class Tag(models.Model):
    name = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
CARD_TYPES = (
    ('Habit', 'habit'),
    ('Self Check-In', 'check'),
    ('Miscellaneous', 'misc'),
    ('Book', 'book'),
    ('Article', 'article'),
    ('Learning', 'learn'),
    ('Project', 'project'),
)

class Card(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    front = models.TextField()
    back = models.TextField(null=True)
    type = models.TextField(choices=CARD_TYPES)

    tags = models.ManyToManyField(Tag)

    is_active = models.BooleanField(default=True)
    is_priority = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)

    ease = models.FloatField(default=1)
    repetitions = models.IntegerField(default=0)
    occurrences = models.IntegerField(default=0)
    interval = models.IntegerField(default=0)
    interval_unit = models.CharField(max_length=1, default="d")
    due_at = models.DateTimeField(default=timezone.now)
