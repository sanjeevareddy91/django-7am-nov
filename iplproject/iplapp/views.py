from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def welcome_message(request):
    return HttpResponse("<h1>Hello, Welcome to Django!</h1>")

def sample_page(request):
    return render(request,'iplapp/sample.html')

def register(request):
    print(request.POST)
    return render(request,'iplapp/register.html')