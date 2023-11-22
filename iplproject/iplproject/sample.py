from django.http import HttpResponse

def welcome_message(request):
    return HttpResponse("<h1>Hello, Welcome to Django!</h1>")