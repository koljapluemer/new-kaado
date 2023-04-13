from django.shortcuts import render, redirect


def unpoly_cards_new(request):
    return render(request, 'unpoly/cards/new.html')