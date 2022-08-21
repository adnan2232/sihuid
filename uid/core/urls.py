from django import views
from django.urls import path
from .views import homepage,college_login
 
urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login")
]