import stripe

from ..models import *
from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.conf import settings as cfg

from lazysignup.utils import is_lazy_user


def settings(request):
    try:
        profile = request.user.profile
    except:
        return redirect('login')

    if not is_lazy_user(request.user):

        stripe.api_key = cfg.STRIPE_SECRET_KEY
        stripe_id = profile.stripeCustomerID
        stripe_customer = stripe.Customer.retrieve(stripe_id)
        stripe_email = stripe_customer.email
        subscription_status = stripe_customer.subscriptions.data[0].status

        context = {
            'stripe_email': stripe_email,
            'subscription_status': subscription_status,
        }

    else:
        context = {
        }
    return render(request, 'pages/settings.html', context)
