from django.contrib import admin
from .models import University, College, User, Student
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(University)
admin.site.register(College)
admin.site.register(Student)