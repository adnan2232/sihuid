
from contextlib import nullcontext
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from hashid_field import BigHashidField
# Create your models here.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import hashers
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime,date
class User(AbstractUser):
    pass

class UniversityManager(models.Manager):
    
    def create_university(self,uni_name,uni_type,uni_id,comes_under):
      
        university = self.create(
            uni_name = uni_name.lower().replace(" ",""),
            uni_type=uni_type,
            uni_id=uni_id,
            comes_under=comes_under
        )
        return university

class University(models.Model):
    uni_type = models.CharField(max_length=100)
    uni_name = models.CharField(max_length=100,null=False)
    uni_id = models.IntegerField(primary_key=True,editable=True) #Later make editable False
    comes_under = models.CharField(max_length=100)
    objects = UniversityManager()
    
    def __str__(self):
        return str(self.uni_name)

class CollegeManager(BaseUserManager):

    def create_college(self, college_name, uni_name,college_email, uni_level_id,college_type, aicte_approved="No",password=None):
        
        university = University.objects.get(uni_name = uni_name.lower().replace(" ", ''))
        college_id = str(university.uni_id) + str(uni_level_id)
        password = "college@"+hashers.make_password(str(college_id))[-7:]
        college_user = User.objects.create_user(
            username  = college_id+college_name,
            email=college_email,
            password=password,
            is_staff=False,
        )
        college_user.save()
        college = self.create(
            college_name = college_name.lower().replace(" ", ""),
            college_email=college_email,
            university = university,
            uni_level_id = uni_level_id,
            college_id = college_id,
            college_user=college_user,
            college_type=college_type
        )
        college.save(using=self._db)
        
        send_mail(
            subject="Your ID and Password for AICTE login is",
            message=f"College id: {college_id} and College Password: {password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[college_email]
        )
        return college,password
class College(models.Model):
    
    college_id = models.CharField(primary_key=True,max_length=100)
    college_email =  models.EmailField(
        verbose_name="email_id",
        max_length=255,
        unique=True,
        null=False
    )
    college_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="college_user")
    college_name = models.CharField(max_length=100,null=False)
    college_type = models.CharField(max_length=100,null=False)
    university = models.ForeignKey(University,on_delete=models.CASCADE,related_name="university")
    uni_level_id = models.IntegerField(null=False)
    aicte_approved = models.BooleanField(default=False) 
    objects = CollegeManager()

    def __str__(self):
        return str(self.college_name)
    

class StudentManager(models.Manager):
    
    def create_student(self,adhar_id,password,name,dob,city,state,zipcode,mobile_number,email):
        
        user = User.objects.create_user(
            username = adhar_id,
            password=password
        )
        try:
            student= self.create(
                adhar_id=adhar_id,
                user=user,
                name=name,
                dob=dob,
                city=city,
                state=state,
                zipcode=zipcode,
                mobile_number=mobile_number,
                email=email,
            )
            student.save()
        except:
            user.delete()
        return student
            
        
        
        
        
                 
class Student(models.Model):
    
    adhar_id = models.BigIntegerField(primary_key=True,null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length=100,null=False)
    dob = models.DateField(null=False)
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,null="")
    zipcode = models.IntegerField(default=0)
    mobile_number = models.CharField(max_length=14,null=False)
    email = models.EmailField(default="")
    
    def __str__(self):
        return (self.name)
    objects = StudentManager()
    


class StudentCollegeDataManager(models.Model):
    
    def create_student_college_data(self,student,college,date_of_admission,semester,branch,depart,gr_no):
        stud_data_uid = str(college.college_id)+str(gr_no)+str(date_of_admission)+str(date.today())
        data = StudentCollegeData.objects.create(
            stud_data_uid =stud_data_uid,
            student=student,
            college=college,
            date_of_admission=date_of_admission,
            semester=semester,
            branch=branch,
            depart=depart,
            gr_no=gr_no
        )
        data.save()
        return data
        

class StudentCollegeData(models.Model):
    
    
    STATUS_CHOICES = [
        ("pen","PENDING"),
        ("app","APPROVED"),
        ("rej","REJECTED")
    ]
    stud_data_uid = models.CharField(max_length=100)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    college = models.ForeignKey(College,on_delete=models.SET_NULL,null=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=3,default="pen")
    date_of_issue = models.DateField(auto_now_add=True,editable=False)
    date_of_admission = models.DateField()
    semester = models.IntegerField()
    branch = models.CharField(max_length=50)
    depart = models.CharField(max_length=50)
    gr_no = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return str(self.stud_data_uid)

class AICTEManager(BaseUserManager):
    
    def create_aicte_user(self, aicte_username, aicte_email, password):
        
        aicte_user = User.objects.create_superuser(
            username = aicte_username, 
            email = aicte_email, 
            password = password
            )
        
        aicte_user.save()

        aicte = self.create(
            aicte_username = aicte_username,
            aicte_email = aicte_email,
            password = password,
            aicte_user = aicte_user
        )
        aicte.save(using = self._db)
        return aicte

class AICTE(models.Model):


    aicte_username = models.CharField(max_length=50, null=False)
    aicte_email = models.EmailField(
        verbose_name="email_id",
        max_length=255,
        unique=True,
        null=False
    )
    password = models.CharField(max_length = 50, null = False, blank = False)
    
    aicte_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aicte_user')

    objects = AICTEManager()

    def __str__(self):
        return (self.aicte_username)
