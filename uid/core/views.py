from multiprocessing import context
from django.shortcuts import render

# Create your views here.
def homepage(request):
    context = {
        "homepage":"HELLO",
    }
    return render(request,"index.html",context=context)