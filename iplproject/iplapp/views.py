from django.shortcuts import render,redirect
from .forms import FranchisesModelForm
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
        # 1st Approach
        # name = request.POST['f_name']
        # nickname = request.POST['f_nickname']
        # f_started_year = request.POST['f_started_year']
        # no_of_trophies = request.POST['no_of_trophies']
        # logo = request.FILES['f_logo']
        # Franchises.objects.create(f_name=name,f_nickname=nickname,f_started_year=f_started_year,f_logo=logo,no_of_trophies=no_of_trophies)

        # 2nd Approach
        # data = request.POST
        # print(request.FILES)
        # new_record = {record:data[record] for record in data if record != 'csrfmiddlewaretoken'}
        # new_record['f_logo'] = request.FILES['f_logo']
        # import pdb;pdb.set_trace()
        # Franchises.objects.create(**new_record)

        # 3rd Approach
        data = request.POST
        print(request.FILES)
        new_record = {record:data[record] for record in data if record != 'csrfmiddlewaretoken'}
        new_record['f_logo'] = request.FILES['f_logo']
        franchesis_data = Franchises(**new_record)

        franchesis_data.save()

        return HttpResponse("Franchesis Added Successfully!")
    return render(request,'iplapp/register_franchesis.html')

def list_franchesis(request):
    data = Franchises.objects.all()
    return render(request,'iplapp/list_franchesis.html',{"data":data})

def update_franchesis(request,id):
    data = Franchises.objects.get(id=id)
    if request.method == "POST":
        # 1st Approach
        # data.f_name = request.POST['f_name']
        # data.f_nickname = request.POST['f_nickname']
        # data.f_started_year = request.POST['f_started_year']
        # data.no_of_trophies = request.POST['no_of_trophies']
        # data.save()

        # 2nd Approach
        filtered_data = Franchises.objects.filter(id=id)
        new_record = {record:request.POST[record] for record in request.POST if record != 'csrfmiddlewaretoken'}
        new_record['f_logo'] = request.FILES['f_logo']
        filtered_data.update(**new_record)
        # return HttpResponse("Franchesis Updated!")
        return redirect('list_franchesis')
    return render(request,'iplapp/update_franchesis.html',{'data':data})

def delete_franchesis(request,id):
    data = Franchises.objects.get(id=id)
    data.delete()
    return HttpResponse("Franchesis Deleted")


# Django Forms:
    # ModelForm
    # NormalForm.

def register_modelform(request):
    model_form = FranchisesModelForm(request.POST)
    return render(request,'iplapp/model_form.html',{'form':model_form})