from django import forms

from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver

from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Tag(models.Model):
    name = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# TODO: fix this in backend and kick the redundant ones
CARD_TYPES = (
    ('Habit', 'habit'),
    ('Self Check-In', 'check'),
    ('Miscellaneous', 'misc'),
    ('Miscellaneous', 'other'),
    ('Miscellaneous', 'standard'),
    ('Book', 'book'),
    ('Book', 'readingList'),
    ('Article', 'article'),
    ('Article', 'articleList'),
    ('Learning', 'learn'),
    ('Project', 'project'),
)

class Card(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    front = models.TextField()
    back = models.TextField(null=True, blank=True)
    type = models.TextField(choices=CARD_TYPES)

    tags = models.ManyToManyField(Tag, blank=True)

    is_active = models.BooleanField(default=True)
    is_priority = models.BooleanField(default=False)
    is_started = models.BooleanField(default=False)

    ease = models.FloatField(default=1)
    repetitions = models.IntegerField(default=0)
    occurrences = models.IntegerField(default=0)
    interval = models.IntegerField(default=1)
    interval_unit = models.CharField(max_length=1, default="d")
    due_at = models.DateTimeField(default=timezone.now)
    old_id = models.TextField(null=True, blank=True)

    @property
    def human_readable_type(self):
        for choice in CARD_TYPES:
            if choice[1] == self.type:
                return choice[0]
            

class Log(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0)
    type = models.TextField(choices=CARD_TYPES, null=True, blank=True)
    old_id = models.TextField(null=True, blank=True)
    input_type = models.IntegerField(default=99, null=True, blank=True)
    skip_note = models.TextField(null=True, blank=True)
    card_front = models.TextField(null=True, blank=True)