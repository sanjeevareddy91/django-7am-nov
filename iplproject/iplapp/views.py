from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import FranchisesModelForm,FranchisesForm
# Create your views here.

from django.http import HttpResponse
from .models import Franchises,UserInfo,Schedule
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
from .fixture_generator import main
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView


from django.views.generic.edit import CreateView,UpdateView
from .serializers import *

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

def schedule(request):
    data = [row.f_nickname for row in Franchises.objects.all()]
    # import pdb;pdb.set_trace()
    schedule = main(data)
    final_schedule = []
    for ele in schedule:
        for ele1 in ele:
            final_schedule.append(ele1)
    for match in final_schedule:
        Schedule.objects.create(team1=match[0],team2=match[1])
    messages.success(request,'Schedule created')
    return render(request,'iplapp/schedule.html',{'matches':final_schedule})

# Class Based Views : Writing the views by using the concepts of OOPs.
    # Views
    # Generic Views

class MessageView(View):
    def get(self,request):
        return HttpResponse("<h1>Hello, Welcome to Django!</h1>")

class SampleFromView(View):
    def get(self,request):
        return render(request,'iplapp/register.html')

    def post(self,request):
        print(request.POST)
        email = request.POST['email']
        return HttpResponse(f"{email}")
    
class RegisterFranchesisView(View):
    def get(self,request):
        return render(request,'iplapp/register_franchesis.html')
    
    def post(self,request):
        data = request.POST
        print(request.FILES)
        new_record = {record:data[record] for record in data if record != 'csrfmiddlewaretoken'}
        new_record['f_logo'] = request.FILES['f_logo']
        franchesis_data = Franchises(**new_record)

        franchesis_data.save()
        messages.success(request,"Class based Register Franchesis Success")
        return redirect('list_franchesis')


class ListFranchesisView(ListView):
    def get(self,request):
        data = Franchises.objects.all()
        return render(request,'iplapp/list_franchesis.html',{"data":data})
    
class FranchesisGenericCreateView(CreateView):
    model = Franchises
    fields = "__all__"
    success_url = reverse_lazy('list_franchesis')

class FranchesisGenericDetailView(DetailView):
    model = Franchises

class FranchesisGenericUpdateView(UpdateView):
    model = Franchises
    fields = "__all__"
    success_url = reverse_lazy('list_franchesis')


# Django Rest Framework APIs

# RestAPIs are divided into 2 types:
    # Function Based Apis
    # Class Based Apis
        # APIView
        # GenericApis
        # Viewsets

from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view decorator is very important to convert normal function in function based api..

@api_view(['GET',"POST"])
def sample_api(request):
    if request.method == "GET":
        return Response({'message':"Sample Api"})
    else:
        data = request.data
        print(data)
        email1 = "sanjeev@gmail.com"
        password1 = "password"
        if data['email'] == email1 and data['password'] == password1:
            return Response({"success":True,"message":"Login Successful"})
        else:
            return Response({"success":False,"message":"Check the credentials"})

import json        
@api_view(['GET',"POST"])
def register_franchesis_api(request):
    if request.method == "GET":
        data = Franchises.objects.all()
        response_data = []
        for ele in data:
            dict1 = {
                'id':ele.id,
                "f_name":ele.f_name,
                "f_nickname":ele.f_nickname,
                "f_started_year":ele.f_started_year,
                "no_of_trophies":ele.no_of_trophies,

            }
            response_data.append(dict1)
        return Response({
            "success":True,
            "data":response_data,
            "count":len(response_data)
        })
    else:
        new_record = {ele:request.data[ele] for ele in request.data}
        # import pdb;pdb.set_trace()
        Franchises.objects.create(**new_record)
        new_record.pop('f_logo')
        return Response({"success":True,"message":"Franchesis Added","data":json.dumps(new_record)})
    
@api_view(['PUT','DELETE','GET'])
def update_delete_get_franchesis_api(request,id):

    if request.method == "GET":
        data = Franchises.objects.get(id=id)
        final_data = {
            'f_name':data.f_name,
            'f_nickname':data.f_nickname,
            'f_started_year':data.f_started_year,
            'no_of_trophies':data.no_of_trophies,
            'f_logo':data.f_logo.url
        }
        return Response({'success':True,'data':final_data})
    
    elif request.method == "PUT":
        # data = Franchises.objects.get(id=id)
        # data.f_name = request.data['f_name']
        # data.f_nickname = request.data['f_nickname']
        # data.f_started_year = request.data['f_started_year']
        # data.no_of_trophies = request.data['no_of_trophies']
        # data.save()
        # final_data = {
        #     'f_name':data.f_name,
        #     'f_nickname':data.f_nickname,
        #     'f_started_year':data.f_started_year,
        #     'no_of_trophies':data.no_of_trophies,
        #     'f_logo':data.f_logo.url
        # }

        # 2nd Approach
        data = Franchises.objects.filter(id=id)
        data.update(**request.data)
        return Response({'success':True,'data':request.data})
    
    elif request.method == "DELETE":
        data = Franchises.objects.get(id=id)
        data.delete()
        return Response({'success':True,'message':"Franchesis deleted"})



# GET  - list
# POST - post 
# GET - retrieve 1 record
# PUT - update
# DELETE - delete 
    

from .serializers import FranchisesModelSerializer
@api_view(['GET','POST'])
def serializer_register_franchesis_api(request):
    if request.method == "GET":
        data = Franchises.objects.all()
        # if it is get method just pass data as positional argument to serializer
        serializer = FranchisesModelSerializer(data,many=True)
        return Response({'success':True,"data":serializer.data})
    
    elif request.method == "POST":
        serializer = FranchisesModelSerializer(data=request.data)
        # if it is post method pass data as keyword argument to serializer
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'data':serializer.data})
        return Response({'success':True,"message":serializer.errors})
    

@api_view(['PUT','DELETE','GET'])
def update_delete_get_serializer_franchesis_api(request,id):

    if request.method == "GET":
        data = Franchises.objects.get(id=id)
        serializer = FranchisesModelSerializer(data)
        return Response({'success':True,'data':serializer.data})
    
    elif request.method == "PUT":
        info = Franchises.objects.get(id=id)
        serializer = FranchisesModelSerializer(info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,'data':request.data})
        else:
            return Response({'success':False,'message':serializer.errors})
    
    elif request.method == "DELETE":
        data = Franchises.objects.get(id=id)
        data.delete()
        return Response({'success':True,'message':"Franchesis deleted"})


from .serializers import FranchesisNormalSerializer

@api_view(['GET','POST'])
def normalserializer_register_franchesis_api(request):
    if request.method == "GET":
        data = Franchises.objects.all()
        # if it is get method just pass data as positional argument to serializer
        serializer = FranchesisNormalSerializer(data,many=True)
        return Response({'success':True,"data":serializer.data})
    
    elif request.method == "POST":
        serializer = FranchesisNormalSerializer(data=request.data)
        # if it is post method pass data as keyword argument to serializer
        if serializer.is_valid():
            # Franchises.objects.create(**serializer.data)
            return Response({'success':True,'data':serializer.data})
        return Response({'success':True,"message":serializer.errors})


# Class Based Api Views 
    # APIView
    # Generic Views
    # Viewsets
# Https status code:
    # 200,201,204,400,401,403,404,500,504,408

from rest_framework.views import APIView

class ClsSampleAPi(APIView):
    def get(self,request):
        return Response({'message':"Sample Api"})
    
    def post(self,request):
        data = request.data
        print(data)
        email1 = "sanjeev@gmail.com"
        password1 = "password"
        if data['email'] == email1 and data['password'] == password1:
            return Response({"success":True,"message":"Login Successful"})
        else:
            return Response({"success":False,"message":"Check the credentials"})

from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


jwt_token = openapi.Parameter('Authorization', in_=openapi.IN_QUERY, description='JWT Token',
                                type=openapi.TYPE_STRING)
class FranchesisAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        manual_parameters=[jwt_token],
        # query_serializer=CategorySerializer,
        # responses = {
        #     '200' : category_response,
        #     '400': 'Bad Request'
        # },        
        security=[],
        operation_id='List of categories',
        operation_description='This endpoint does some magic',
    )
    def get(self,request):
        data = Franchises.objects.all()
        serializer = FranchesisNormalSerializer(data,many=True)
        return Response({'success':True,"data":serializer.data})

    def post(self,request):
        serializer = FranchesisNormalSerializer(data=request.data)
        # if it is post method pass data as keyword argument to serializer
        if serializer.is_valid():
            Franchises.objects.create(**serializer.data)
            return Response({'success':True,'data':serializer.data})
        return Response({'success':True,"message":serializer.errors})


class FranchesisModifyAPIView(APIView):
    def get(self,request,id):
        data = Franchises.objects.get(id=id)
        serializer = FranchesisNormalSerializer(data)
        return Response({'success':True,"data":serializer.data})

    def put(self,request,id):
        serializer = FranchesisNormalSerializer(data=request.data)
        # if it is post method pass data as keyword argument to serializer
        if serializer.is_valid():
            fran_data = Franchises.objects.filter(id=id)
            fran_data.update(**serializer.data)
            return Response({'success':True,'data':serializer.data})
        return Response({'success':True,"message":serializer.errors})

    def delete(self,request,id):
        data = Franchises.objects.get(id=id)
        data.delete()
        return Response({'success':True,"message":"Franchesis Deleted"})


from rest_framework.authtoken.models import Token

class UserInfoApiViews(APIView):
    def post(self,request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            # import pdb;pdb.set_trace()
            username = data['email'].split('@')[0]
            print(username)
            user_data = User.objects.create(username=username,email = data['email'])
            user_data.set_password(data['password'])
            user_data.save()
            # Token for the Created User..
            created_token = Token.objects.create(user=user_data)
            UserInfo.objects.create(user_data=user_data,mobile=data['mobile'],address=data['address'])
            return Response({"Success":True,"Message":"User Added",'token':created_token.key})

# Generic ApiViews 
from rest_framework import generics

class FranchesisCreateAPiView(generics.CreateAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

    # def post(self,request):
    #     custom code

class FranchesisListAPiView(generics.ListAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer


class FranchesisRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

class FranchesisUpdateAPIView(generics.UpdateAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

class FranchesisDestroyAPIView(generics.DestroyAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

class FranchesisListCreateAPIView(generics.ListCreateAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

class FranchesisRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

# Viewsets

# get - list
# post - create 
# get - retrieve 
# put - update 
# delete - destroy
# patch - partial_update

from rest_framework import viewsets

class FranchesisModelViewset(viewsets.ModelViewSet):
    queryset = Franchises.objects.all() 
    serializer_class = FranchisesModelSerializer

