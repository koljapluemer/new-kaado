from django.shortcuts import render, redirect

def index(request):
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')