from django import views
from django.urls import path
from .views import aicte_login, homepage,college_login
 
urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login"),
    path("aictelogin",aicte_login,name="aicte_login")
]