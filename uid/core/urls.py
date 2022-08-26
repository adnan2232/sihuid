from django.urls import path
from .views import *

urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login"),
    path("aictelogin",aicte_login,name="aicte_login"),
    path("upload_students_data", upload_students_data, name = "upload_students_data"),
    path("view_college_data", aicte_view_college_data, name = "aicte_view_college_data"),
    path("view_student_data", aicte_view_students_data, name = "aicte_view_students_data"),
    path("logout", user_logout, name = "user_logout"),
    path('individual_student_data/<int:adhar_no>',student_data,name="student_data"),
    path("logout", user_logout, name = "user_logout"),
    path("college_view_students_data",view_students_data,name="college_view_students_data"),
    path("college_dashboard",college_dashboard,name="college_dashboard"),
    path("upload_data",upload_college,name="upload_college"),
    path("student_register",studentRegister,name="student_register"),
    path("student_login",studentLogin,name="student_login"),
    path("student_profile",student_profile,name="student_profile"),
    path("student_college_data",student_college_data, name="student_college_data"),
    path("edit_data", edit_data, name = "edit_data"),
    path("college_data", college_data, name = "college_data"),
    ]