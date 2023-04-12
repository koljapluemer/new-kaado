from django.utils import timezone
from ..models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.contrib import messages
import random
from django.contrib.sessions.models import Session

from supermemo2 import SMTwo


def set_random_card(request):
    # get a random card from user that is due
    user = request.user
    # check if 'project_shown_at' date is yesterday
    # if so, show project card
    # if not, show random card
    project_shown_at = request.session.get('project_shown_at', None)
    if project_shown_at is None or project_shown_at != timezone.now().date().isoformat():
        new_card = Card.objects.filter(user=user, type='project', is_active=True
                                       ).order_by('?').first()
        request.session['project_shown_at'] = timezone.now().date().isoformat()
    else:
        random_type = random.choice(
            ['productivity', 'misc', 'book', 'article', 'learn'])
        if random_type == 'productivity':
            # get a card thats either 'todo', 'habit', or 'check'
            new_card = Card.objects.filter(user=user, type__in=['todo', 'habit', 'check'], is_active=True, due_at__lte=timezone.now()
                                           ).order_by('?').first()
        elif random_type == 'book':
            number_of_started_books = Card.objects.filter(user=user, type='book', is_active=True, is_started=True
                                                          ).count()
            if number_of_started_books < 5:
                new_card = Card.objects.filter(user=user, type='book', is_active=True, is_started=False
                                               ).order_by('?').first()
                new_card.is_started = True
                new_card.save()
            else:
                new_card = Card.objects.filter(user=user, type='book', is_active=True, is_started=True, due_at__lte=timezone.now()
                                               ).order_by('?').first()
        else:
            new_card = Card.objects.filter(user=user, type=random_type, is_active=True, due_at__lte=timezone.now()
                                           ).order_by('?').first()

        if new_card is None:
            # try to get any card
            new_card = Card.objects.filter(user=user, is_active=True, due_at__lte=timezone.now()
                                           ).order_by('?').first()
            # TODO: handle case where there are no cards, and case where user has no cards yet
            # save new_card to session
    request.session['card'] = new_card.id
    return redirect('queue')


def handle_review(request):
    if request.method == 'POST':

        card = Card.objects.get(id=request.POST['card-id'])
        type = card.type
        give_message_reward = False
        review = Review(
            user = request.user,
            card = card
        )
        # Habit
        if type == 'habit':
            if 'not-today' in request.POST:
                review.review = 'not-today'
                # set due date to tomorrow
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                review.review = 'do-later'
                # add 10 minutes to due date
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'done' in request.POST:
                review.review = 'done'
                if card.interval_unit == 'd':
                    card.due_at = timezone.now() + timedelta(days=card.interval)
                elif card.interval_unit == 'h':
                    card.due_at = timezone.now() + timedelta(hours=card.interval)
                give_message_reward = True
        # Self Check-In
        elif type == 'check':
            review.review = 'check'
            # set due date to now + interval
            # check if unit is d or h
            if card.interval_unit == 'd':
                card.due_at = timezone.now() + timedelta(days=card.interval)
            elif card.interval_unit == 'h':
                card.due_at = timezone.now() + timedelta(hours=card.interval)
        # Todo 
        elif type == 'todo':
            if 'not-today' in request.POST:
                review.review = 'not-today'
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                review.review = 'do-later'
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'done' in request.POST:
                review.review = 'done'
                card.delete()
                give_message_reward = True
        # Miscellaneous
        elif type == 'misc':
            if 'show-next' in request.POST:
                review.review = 'show-next'
                card.due_at = timezone.now() + timedelta(days=7)
            elif 'cool-thanks' in request.POST:
                review.review = 'cool-thanks'
                card.due_at = timezone.now() + timedelta(days=1)
        # article
        elif type == 'article':
            if 'not-today' in request.POST:
                review.review = 'not-today'
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                review.review = 'do-later'
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'made-some-progress' in request.POST:
                review.review = 'made-some-progress'
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'finished' in request.POST:
                review.review = 'finished'
                card.type = 'misc'
                card.due_at = timezone.now() + timedelta(days=1)
                give_message_reward = True
        # book
        elif type == 'book':
            if 'not-today' in request.POST:
                review.review = 'not-today'
                card.due_at = timezone.now() + timedelta(days=1)
            elif 'do-later' in request.POST:
                review.review = 'do-later'
                card.due_at = timezone.now() + timedelta(minutes=10)
            elif 'done' in request.POST:
                review.review = 'done'
                card.due_at = timezone.now() + timedelta(days=1)
                give_message_reward = True
            elif 'finished' in request.POST:
                review.review = 'finished'
                card.type = 'misc'
                card.due_at = timezone.now() + timedelta(days=1)
                card.front += ' *(finished reading)*'
                give_message_reward = True
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
                give_message_reward = True

            review.review = str(response)            
            sm_review = SMTwo(card.ease, card.interval,
                           card.repetitions).review(response)
            card.ease = sm_review.easiness
            card.interval = sm_review.interval
            card.repetitions = sm_review.repetitions
            # this ignores the actually calculated due date, but that doesn't matter
            # since it's coarse and terrible SM2 anyways
            card.due_at = timezone.now() + timedelta(days=sm_review.interval)

        card.save()
        review.save()

        if give_message_reward:
            affirmations = [
                'Good job!',
                'Nice work.',
                'Keep it up!',
                'You got this.',
                'You\'re doing great!',
                'You\'re on a roll.',
                'You\'re a rockstar.',
                'Not bad...',
                'You\'re a beast.',
                'Impressive',
                'You\'re a legend.',
                'Well played.'
            ]
            messages.success(request, random.choice(affirmations))

    return redirect(set_random_card)


@login_required
def queue(request):
    # get card from session
    if 'card' in request.session:
        if not Card.objects.filter(id=request.session['card'], user=request.user, is_active=True):
            # return to url of name set_random_card
            return redirect(set_random_card)
    else:
        return redirect(set_random_card)

    card = Card.objects.get(
        id=request.session['card'], user=request.user, is_active=True)
    
    # get last 50 reviews
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')[:120]

    return render(request, 'pages/queue.html', {'card': card, 'reviews': reviews})


@login_required
def stats(request):
    user = request.user
    due_cards_count = Card.objects.filter(
        user=user, due_at__lt=timezone.now(), is_active=True).count()
    return render(request, 'pages/stats.html', {'due_cards_count': due_cards_count})
