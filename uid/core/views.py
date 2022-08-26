from operator import index
from unittest import result
from urllib import response
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from .models import College, Student
import datetime
import csv
import json
from core.models import User
import pandas as pd

from .filters import CollegeFilter

# Create your views here.
def homepage(request):
    context = {
        "homepage":"HELLO",
        "error":[]
    }
    return render(request,"index.html",context=context)

def aicte_login(request):
    if request.method == "POST":
        
        data = request.POST.dict()
        username = data["aicte_username"]
        password = data["aicte_password"]
        user = authenticate(request,username=str(username),password=str(password))
        if user is not None:
            login(request,user)
            # print("success")
            return redirect(aicte_toggle)
        else:
            context = {"errors":["Username or Password Incorrect"]}
            return render(request,"aicte_login.html",context=context)
        
    else:
        context = {"errors":[]}
        return render(request,"aicte_login.html",context=context)
        

def college_login(request):
    if request.method == "POST":
        
        data = request.POST.dict()
        username = data["college_username"]
        password = data["college_password"]
        user = authenticate(request,username=str(username),password=str(password))
        if user is not None:
            login(request,user)
            print("success")
            return redirect(college_dashboard)
            # return redirect(upload_students_data)
        else:
            context = {"errors":["Username or Password Incorrect"]}
            return render(request,"college_login.html",context=context)
        
    else:
        context = {"errors":[]}
        return render(request,"college_login.html",context=context)
    

def user_logout(request):
    logout(request)
    return redirect(homepage)

def view_students_data(request):

    print(request.user.college_user)

    result = request.user.college_user.student_set.all()
    # print(result)
    return render(request, "students_data.html", context = {"student_data": result})


def upload_students_data(request):
    
    if request.method  == "POST":
        
        student_data = pd.read_csv(request.FILES["student_data"])
        data = student_data.values.tolist()
        for x in data:
            # print(x[0])
            # print(x[1])
            # print(x[2])
            # print(x[3])
            try:
                student = Student.objects.get(
                    student_current_id = str(request.user.college_user.college_id)+str(x[2])+str(datetime.datetime.strptime(x[3], '%d-%m-%Y'))
                )
                
                if student.student_gender != x[0]:
                    pass
            except:
                Student.objects.create_student(student_name = x[0], college_id = request.user, grno = x[2], admission_date =  datetime.datetime.strptime(x[3], '%d-%m-%Y'), student_ext_id = x[1])
    
        return view_students_data(request)
        
    else:
        return render(request,"upload_students_data.html",context = {})
        

def aicte_view_college_data(request):

    result = College.objects.all()

    myFilter = CollegeFilter(request.GET, queryset=result)
    result = myFilter.qs

    return render(request, "college_data.html", context = {"college_data": result, "myFilter":myFilter})


def aicte_view_students_data(request):

    result = Student.objects.all()
    print(result)
    return render(request, "aicte_view_students_data.html", context = {"students_data": result})

def student_data(request,adhar_no):
    
    student_data = Student.objects.filter(student_ext_id = adhar_no)
    return render(request,"individ_student_data.html",context={"student_data":student_data})

def aicte_toggle(request):
    
    try:
        
        if request.user.aicte_user:
            return render(request,"aicte_toggle.html")
    except:
        return redirect(".")
    
    
def college_dashboard(request):
    return render(request,"clg_dashboard.html")


def upload_college(request):
    
    if request.method == "POST":
        college_data = pd.read_csv(request.FILES["college_data"])
        data = college_data.values.tolist()
        for x in data:
            # print(x[0])
            # print(x[1])
            # print(x[2])
            # print(x[3])
            College.objects.create_college(
                college_name=x[0],
                uni_name=x[3],
                college_email=x[2],
                uni_level_id=x[4],
                college_type=x[1]
            )
        return redirect(aicte_view_college_data)
    else:
        return render(request,"upload_college.html")
        

    