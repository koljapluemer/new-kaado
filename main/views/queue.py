from django.utils import timezone
from ..models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from supermemo2 import SMTwo

@login_required(login_url='/accounts/login/')
def queue(request):
    if request.method == 'POST':
        card = Card.objects.get(id=request.POST['card-id'])
        type = card.type
        # Habit
        if type == 'habit':
            if 'not-today' in request.POST:
                # set due date to tomorrow
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                # add 10 minutes to due date
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'done' in request.POST:
                if card.interval_unit == 'd':
                    card.due_at = timezone.now() + timedelta(days=card.interval)
                elif card.interval_unit == 'h':
                    card.due_at = timezone.now() + timedelta(hours=card.interval)
        # Self Check-In
        elif type == 'check':
            # set due date to now + interval
            # check if unit is d or h
            if card.interval_unit == 'd':
                card.due_at = timezone.now() + timedelta(days=card.interval)
            elif card.interval_unit == 'h':
                card.due_at = timezone.now() + timedelta(hours=card.interval)
        # Miscellaneous
        elif type == 'misc':
            if 'show-next' in request.POST:
                card.due_at = timezone.now() + timedelta(days=7)
            elif 'cool-thanks' in request.POST:
                card.due_at = timezone.now() + timedelta(days=1)
        # article
        elif type == 'article':
            if 'not-today' in request.POST:
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'made-some-progress' in request.POST:
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'finished' in request.POST:
                card.type = 'misc'
                card.due_at = timezone.now() + timedelta(days=1)
        # book
        elif type == 'book':
            if 'not-today' in request.POST:
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'done' in request.POST:
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'finished' in request.POST:
                card.type = 'misc'
                card.due_at = timezone.now() + timedelta(days=1)

        # learn
        elif type == 'learn':
            if '0' in request.POST:
                response = 0
            elif '1' in request.POST:
                response = 1
            elif '2' in request.POST:
                response = 2
            elif '3' in request.POST:
                response = 3
            elif '4' in request.POST:
                response = 4
            elif '5' in request.POST:
                response = 5
            # API: review = SMTwo(review.easiness, review.interval, review.repetitions).review(4, "2021-3-14")
            review = SMTwo(card.ease, card.interval, card.repetitions).review(response)
            card.ease = review.easiness
            card.interval = review.interval
            card.repetitions = review.repetitions
            # this ignores the actually calculated due date, but that doesn't matter
            # since it's coarse and terrible SM2 anyways
            card.due_at = timezone.now() + timedelta(days=review.interval)

        card.save()
    # get a random card from user that is due
    profile = request.user.profile
    new_card = Card.objects.filter(profile=profile, due_at__lt=timezone.now(), occurrences__gt=0, is_active=True
                                   ).order_by('?').first()

    return render(request, 'pages/queue.html', {'card': new_card})

@login_required(login_url='/accounts/login/')
def stats(request):
    profile = request.user.profile
    due_cards_count = Card.objects.filter(profile=profile, due_at__lt=timezone.now(), is_active=True).count()
    return render(request, 'pages/stats.html', {'due_cards_count': due_cards_count})