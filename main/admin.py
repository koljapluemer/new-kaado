# set up django admin dashboard

from .models import *
from django.contrib import admin

admin.site.register(Card)
admin.site.register(Tag)
admin.site.register(Profile)