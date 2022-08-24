from operator import index
from unittest import result
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
import json
from core.models import User
import pandas as pd

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
            return redirect("homepage")
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
            return redirect("homepage")
        else:
            context = {"errors":["Username or Password Incorrect"]}
            return render(request,"college_login.html",context=context)
        
    else:
        context = {"errors":[]}
        return render(request,"college_login.html",context=context)
    
    
def upload_students_data(request):
    
    if request.method  == "POST":
        student_data = pd.read_csv(request.FILES["student_data"],index_col="adhar_number")
        result = []
        for x in student_data.index:
            result.append(list(student_data.loc[x].values)+[x])
        
        return render(request,"students_data.html",context = {"student_data":result})
        
    
    else:
        return render(request,"upload_students_data.html",context = {})
        
        
        