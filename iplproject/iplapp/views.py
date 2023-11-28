from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Franchises

def welcome_message(request):
    return HttpResponse("<h1>Hello, Welcome to Django!</h1>")

def sample_page(request):
    return render(request,'iplapp/sample.html')

def register(request):
    print(request.POST)
    return render(request,'iplapp/register.html')


def register_franchesis(request):
    # print(request.POST)
    if request.method == "POST":
        print(request.FILES)
        name = request.POST['f_name']
        nickname = request.POST['f_nickname']
        started_year = request.POST['started_year']
        no_of_trophies = request.POST['no_of_trophies']
        logo = request.FILES['f_logo']
        Franchises.objects.create(f_name=name,f_nickname=nickname,f_started_year=started_year,f_logo=logo,no_of_trophies=no_of_trophies)
        return HttpResponse("Franchesis Added Successfully!")
    return render(request,'iplapp/register_franchesis.html')