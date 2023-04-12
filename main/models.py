from django import forms

from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver

from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class Tag(models.Model):
    name = models.TextField()
    # TODO: in production, make this not nullable
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    old_user_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
CARD_TYPES = (
    ('habit', 'Habit'),
    ('check', 'Self Check-In'),
    ('todo', 'To-Do'),
    ('misc', 'Miscellaneous'),
    ('book', 'Book'),
    ('article', 'Article'),
    ('learn', 'Learn Card'),
    ('project', 'Project'),
)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
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

    connected_cards = models.ManyToManyField("self", blank=True)
    parent_cards = models.ManyToManyField("self", blank=True)
    child_cards = models.ManyToManyField("self", blank=True)

    old_user_id = models.TextField(null=True, blank=True)

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=0, null=True, blank=True)
    type = models.TextField(choices=CARD_TYPES, null=True, blank=True)
    old_id = models.TextField(null=True, blank=True)
    input_type = models.IntegerField(null=True, blank=True)
    skip_note = models.TextField(null=True, blank=True)
    card_front = models.TextField(null=True, blank=True)

    old_user_id = models.TextField(null=True, blank=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def get_color(self):
        if self.review == 'not-today':
            return 'red'
        elif self.review == 'do-later':
            return 'yellow'
        elif self.review == 'done' or self.review == 'made-some-progress':
            return 'green-light'
        elif self.review == 'finished' or self.review == 'finished-book':
            return 'green-dark'
        elif self.review == '0':
            return 'blue-lightest'
        elif self.review == '1':
            return 'blue-lighter'
        elif self.review == '2':
            return 'blue-light'
        elif self.review == '3':
            return 'blue'
        elif self.review == '4':
            return 'blue-dark'
        elif self.review == '5':
            return 'blue-darker'
        else:
            return 'grey'
        