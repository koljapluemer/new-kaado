from ..models import *
from django.shortcuts import render, redirect
import os
from django.conf import settings as settings_conf

from django.contrib.auth import (
    authenticate, get_user_model, password_validation, login
)
from lazysignup.utils import is_lazy_user



def profile(request):
    try:
        request.user.profile
    except:
        return redirect('login')

    user = request.user
    profile = user.profile

    return render(request, 'pages/profile.html')


def signup(request):

    stripe.api_key = settings_conf.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("SIGNUP STARTED")
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            voucher_code = request.POST.get('voucher')
            print("CODE", voucher_code)

            return redirect('/voucher')
    else:
        form = SignUpForm()

    return render(request, 'pages/signup.html', {'form': form})

def changeEmail(request):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('/profile')
    else:
        form = EmailChangeForm()
    return render(request, 'registration/email_change.html', {'form': form})

def deleteUser(request):
    stripe.api_key = settings_conf.STRIPE_SECRET_KEY
    user = request.user
    try:
        stripe.Customer.delete(user.profile.stripeCustomerID)
    except:
        print("Stripe customer already deleted/something went wrong")
    user.delete()

    return redirect('/')
