from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect('queue')
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')

def sandbox(request):
    return render(request, 'pages/sandbox.html')