from django.shortcuts import render,redirect
from .forms import FranchisesModelForm,FranchisesForm
# Create your views here.

from django.http import HttpResponse
from .models import Franchises,UserInfo
from django.contrib import messages

from django.contrib.auth.models import User


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
    form = FranchisesModelForm()
    if request.method == "POST":
        form = FranchisesModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Franchesis Registered Successfully!')
            return redirect('list_franchesis')
    return render(request,'iplapp/model_form.html',{'form':form})

def register_form(request):
    form = FranchisesForm()
    if request.method == "POST":
        form = FranchisesForm(request.POST,request.FILES)
        if form.is_valid():
            # form.save()
            new_record = form.cleaned_data
            Franchises.objects.create(**new_record)
            return HttpResponse("Franchesis Registered!")
    return render(request,'iplapp/normal_form.html',{'form':form})

def RegisterUser(request):
    if request.method == "POST":
        email = request.POST['email']
        # import pdb;pdb.set_trace()
        username = email.split('@')[0]
        password = request.POST['password']
        mobile = request.POST['mobile']
        address = request.POST['address']
        confirm_pass = request.POST['confirm_pass']
        if password != confirm_pass:
            messages.warning(request,"Password and Confirm Password Mismatched!")
            return redirect('register_user')
        user = User.objects.create(username=username,email=email)
        user.set_password(password) # This is used for converting the raw text to encrypted password.
        # user.is_staff = True
        # user.is_superuser = True
        user.save()
        UserInfo.objects.create(user_data=user,mobile=mobile,address=address)
        messages.success(request,'User Registered!')
    return render(request,'iplapp/register_user.html')


def login_user(request):
    return render(request,'iplapp/login.html')