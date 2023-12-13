from django.shortcuts import render,redirect
from .forms import FranchisesModelForm,FranchisesForm
# Create your views here.

from django.http import HttpResponse
from .models import Franchises,UserInfo
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random


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
        message = f"HI {username},Your email id {email},has been successfully registered with us."
        data = send_mail("Registration Confirmation",message,'gsanjeevreddy91@gmail.com',[email],fail_silently=False)
        # import pdb;pdb.set_trace()
        print(data)
        messages.success(request,'User Registered!')
    return render(request,'iplapp/register_user.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        # 1st Way - Internal way
        # user_data = authenticate(username=username,password=password) # This is just for checking the credentials thats it..
        # print(user_data)
        # if user_data:
        #     login(request,user_data)
        #     messages.success(request,f"{user_data} logged in")
        #     return redirect('list_franchesis')
        # else:
        #     messages.warning(request,'Invalid credentials')

        # 2nd Way - Custom Way
        user_data = User.objects.filter(username=username)
        print(user_data)
        if user_data:
            if user_data[0].check_password(password):
                login(request,user_data[0])
                messages.warning(request,f"{user_data[0]} logged in")
                return redirect('list_franchesis')
            else:
                messages.warning(request,"username and password doensot match!")
        else:
            messages.warning(request,'Username not exist')
    return render(request,'iplapp/login.html')

def logout_user(request):
    user_data = request.user
    logout(request)
    messages.success(request,f'{user_data} logged out !')
    return redirect('login_user')

def forgot_email(request):
    if request.method == "POST":
        email = request.POST['email']
        user_data = User.objects.filter(email=email)
        if user_data:
            otp = random.randint(100000,999999)
            user_info = user_data[0]
            user_info_data = UserInfo.objects.get(user_data=user_info)
            user_info_data.otp = otp
            user_info_data.save()
            message = f"Use this OTP {otp} for changing the password."
            send_mail("Forgot OTP",message,"gsanjeevreddy91@gmail.com",[email],fail_silently=False)
            messages.success(request,"OTP has been sent to email id successfully")
            return redirect('verify_otp',user_info_data.id)
        else:
            messages.warning(request,"Invalid email , please check whether account exist.")
    return render(request,'iplapp/forgot_email.html')

def verify_otp(request,id):
    if request.method == "POST":
        otp = request.POST['otp']
        user_info = UserInfo.objects.get(id=id)
        print(user_info.otp == int(otp))
        print(type(otp))
        print(type(user_info.otp))
        if user_info.otp == int(otp):
            messages.success(request,'OTP verification successful')
            return redirect('password_change',id)
        else:
            messages.warning(request,"OTP mismatched, Please check the OTP and try again.")

    return render(request,'iplapp/verify_otp.html')

def password_change(request,id):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user_info = UserInfo.objects.get(id=id)
            user_id = user_info.user_data.id
            user_data = User.objects.get(id=user_id)
            user_data.set_password(password)
            user_data.save()
            messages.success(request,"Password Updated Successfully, please login")
            return redirect('login_user')
        else:
            messages.warning(request,"Password and Confirm Password Mismatched")
    return render(request,'iplapp/password_change.html')