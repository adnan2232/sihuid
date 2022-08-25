from django import views
from django.urls import path
from .views import homepage, college_login, aicte_view_college_data, upload_college, upload_students_data, aicte_view_students_data, aicte_login, user_logout,aicte_toggle,student_data, view_students_data, college_dashboard
 
urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login"),
    path("aictelogin",aicte_login,name="aicte_login"),
    path("upload_students_data", upload_students_data, name = "upload_students_data"),
    path("view_college_data", aicte_view_college_data, name = "aicte_view_college_data"),
    path("view_student_data", aicte_view_students_data, name = "aicte_view_students_data"),
    path("logout", user_logout, name = "user_logout"),
    path('individual_student_data/<int:adhar_no>',student_data,name="student_data"),
    path("aicte_toggle",aicte_toggle,name="aicte_toggle"),
    path("logout", user_logout, name = "user_logout"),
    path("college_view_students_data",view_students_data,name="college_view_students_data"),
    path("college_dasboard",college_dashboard,name="college_dashboard"),
    path("upload_data",upload_college,name="upload_college")
    ]