from django.shortcuts import render, redirect

def github_callback(request):
    # print all properties of GET request
    for key, value in request.GET.items():
        print(key, value)
        print('\n-----\n')
    return redirect('index')