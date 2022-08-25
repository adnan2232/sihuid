
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from hashid_field import BigHashidField
# Create your models here.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import hashers
from django.core.mail import send_mail
from django.conf import settings
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
    
    def create_student(self, student_name, student_gender, college_id,grno,admission_date,student_ext_id,student_year,student_branch,student_department,student_cgpa):
        
        college = College.objects.get(college_id=college_id)
        student_current_id = str(college.college_id)+str(grno)+str(admission_date.year)
        
        try:
                
            student = self.get(student_ext_id=student_ext_id)
            student_ext_id = student.student_ext_id
                
            while student.student_next_id:
                student = self.get(student_current_id=student.student_next_id)
                    
            new_student = self.create(
                student_name = student_name,
                student_gender = student_gender,
                student_current_id = student_current_id,
                student_prev_id =  student.student_current_id,
                student_ext_id = student_ext_id,
                student_college=college,
                student_admission_date = admission_date,
                student_year=student_year,
                student_branch=student_branch,
                student_department=student_department,
                student_cgpa=student_cgpa
            )
                
            new_student.save(using=self._db)
            student.student_next_id=student_current_id
            student.save(using=self._db)
            return new_student
             
        except Exception:
            student = self.create(
                student_name = student_name,
                student_gender = student_gender,
                student_current_id = student_current_id,
                student_ext_id = student_ext_id,
                student_college =college,
                student_grno = grno,
                student_admission_date = admission_date,
                student_year=student_year,
                student_branch=student_branch,
                student_department=student_department,
                student_cgpa=student_cgpa
            )
            
            student.save(using=self._db)
            return student
                  
class Student(models.Model):
    
    student_current_id = models.CharField(primary_key=True, max_length=100)
    student_name = models.CharField(max_length=100)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    student_gender = models.CharField(max_length = 1, choices = GENDER_CHOICES)

    student_prev_id = models.CharField(default=None,null=True,max_length=100)
    student_next_id = models.CharField(default=None,null=True, max_length=100)
    
    student_ext_id =  models.BigIntegerField(null=False)
    
    student_college =  models.ForeignKey(College,on_delete=models.CASCADE)
    student_grno = models.CharField(max_length=20)
    student_admission_date = models.DateField()
    student_year = models.IntegerField()
    student_branch = models.CharField(max_length=100,default="")
    student_department = models.CharField(max_length=100,default="")
    student_cgpa = models.FloatField(default=0)
    
    class Meta:
        ordering = ["-student_admission_date"]
    objects =  StudentManager()

    def __str__(self):
        return (self.student_name)
    
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
