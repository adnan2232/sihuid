from django import views
from django.urls import path
from .views import homepage, college_login, aicte_view_college_data, upload_students_data, aicte_view_students_data, aicte_login, user_logout
 
urlpatterns = [
    path("",homepage,name="homepage"),
    path("collegelogin",college_login,name="college_login"),
    path("aictelogin",aicte_login,name="aicte_login"),
    path("upload_students_data", upload_students_data, name = "upload_students_data"),
    path("view_college_data", aicte_view_college_data, name = "aicte_view_college_data"),
    path("view_student_data", aicte_view_students_data, name = "aicte_view_students_data"),
    path("logout", user_logout, name = "user_logout")
    ]