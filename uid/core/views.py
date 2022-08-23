from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
import json
from core.models import User
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
        
        