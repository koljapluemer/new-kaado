from django.utils import timezone
from ..models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def queue(request):
    # get a random card from user that is due
    profile = request.user.profile
    new_card = Card.objects.filter(profile=profile, due_at__lt=timezone.now()).order_by('?').first()
    if new_card:
        print('found a random due card', new_card)
    else:
        print('no due cards')
        new_card = None

    return render(request, 'pages/queue.html', {'card': new_card})