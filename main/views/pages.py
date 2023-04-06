from ..models import *
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta

# The landing page
def home(request):
    # if POST, print POST dict
    if request.method == 'POST':
        # get card from card-id 
        print('post dict: ', request.POST)
        card = Card.objects.get(id=request.POST['card-id'])
        type = card.template.type

        if type == 'Habit':
            if 'not-today' in request.POST:
                # set due date to tomorrow
                card.due = timezone.now() + timedelta(days=1)
                card.save()
            elif 'do-later' in request.POST:
                # add 10 minutes to due date
                card.due = timezone.now() + timedelta(minutes=10)
                card.save()
            elif 'done' in request.POST:
                # delete card
                card.delete()
        
        elif type == 'Self Check-In':
            # set due date to now + interval
            # check if unit is d or h
            if card.template.unit == 'd':
                card.due = timezone.now() + timedelta(days=card.template.every)
            elif card.template.unit == 'h':
                # add the every interval in hours
                card.due = timezone.now() + timedelta(hours=card.template.every)
            card.save()

        elif type == 'Miscellaneous':
            # if show-next +7 days, otherwise 1 day
            if 'show-next' in request.POST:
                card.due = timezone.now() + timedelta(days=7)
            else:
                card.due = timezone.now() + timedelta(days=1)
            card.save()

        elif type == 'Book':
            # not-today or done: +1 day; finished-book: delete
            if 'not-today' in request.POST:
                card.due = timezone.now() + timedelta(days=1)
                card.save()
            elif 'done' in request.POST:
                card.due = timezone.now() + timedelta(days=1)
                card.save()
            elif 'finished-book' in request.POST:
                card.delete()
            

        elif type == 'Article':
            # not-today or made-some-progress: +1 day; finished-article: delete
            # TODO: how could we handle a conversion to type misc?
            if 'not-today' in request.POST:
                card.due = timezone.now() + timedelta(days=1)
                print('made some progress')
            elif 'made-some-progress' in request.POST:
                card.due = timezone.now() + timedelta(days=1)
                card.save()
            elif 'finished-article' in request.POST:
                card.delete()

        elif type == 'Learning':
            print('Learning')

    # get a random card from user that is due
    profile = request.user.profile
    new_cards = Card.objects.filter(profile=profile, due__lte=timezone.now()).order_by('?')
    print('FOUND DUE CARDS', new_cards)
    if new_cards.count() > 0:
        print('found a random due card')
        new_card = new_cards.first()
    else:
        print('no due cards')
        new_card = None

    return render(request, 'pages/index.html', {'card': new_card})

def about(request):
    return render(request, 'pages/about.html')

def premium(request):
    return render(request, 'pages/premium.html')

# privacy and tos
def privacy(request):
    return render(request, 'pages/privacy.html')

def tos(request):
    return render(request, 'pages/tos.html')