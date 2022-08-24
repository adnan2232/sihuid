from django import views
from django.urls import path
from .views import homepage,college_login, upload_students_data
 
urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login"), 
    path("upload_students_data", upload_students_data, name = "upload_students_data")
    ]