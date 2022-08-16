
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from hashid_field import BigHashidField
# Create your models here.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import hashers

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
    uni_name = models.CharField(max_length=50,null=False)
    uni_id = models.IntegerField(primary_key=True,editable=True) #Later make editable False
    comes_under = models.CharField(max_length=100)
    objects = UniversityManager()
    
    def __str__(self):
        return str(self.uni_name)

class CollegeManager(BaseUserManager):

    def create_college(self, college_name, uni_name,college_email, uni_level_id,password=None):
        
        university = University.objects.get(uni_name = uni_name.lower().replace(" ", ''))
        college_id = int(str(university.uni_id) + str(uni_level_id))
        password = "college@"+hashers.make_password(str(college_id))[:6]
        college_user = User.objects.create(
            username  = college_id,
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
        )
        college.save(using=self._db)
        return college
class College(models.Model):
    
    college_id = models.IntegerField(primary_key=True)
    college_email =  models.EmailField(
        verbose_name="email_id",
        max_length=255,
        unique=True,
        null=False
    )
    college_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="college_user")
    college_name = models.CharField(max_length=50,null=False)
    college_type = models.CharField(max_length=20,null=False)
    university = models.ForeignKey(University,on_delete=models.CASCADE,related_name="university")
    uni_level_id = models.IntegerField(null=False)
    aicte_approved = models.BooleanField(default=False) 
    objects = CollegeManager()

    def __str__(self):
        return str(self.college_name)
    

class StudentManager(models.Manager):
    
    def create_student(self,college_id,grno,admission_date,student_ext_id=None):
        
        college = College.objects.get(college_id=college_id)
        grno = "".join([str(ord(x)%9) for x in grno])
        student_current_id = int(str(college.college_id)+str(grno)+str(admission_date.year))
        
        if student_ext_id:
            
            try:
                
                student = self.get(student_ext_id=student_ext_id)
                student_ext_id = student.student_ext_id.id
                
                while student.student_next_id:
                    student = self.get(student_current_id=student.student_next_id)
                    
                new_student = self.create(
                    student_current_id = student_current_id,
                    student_prev_id =  student.student_current_id,
                    student_ext_id = student_ext_id,
                    student_college=college,
                    student_admission_date = admission_date
                )
                
                new_student.save(using=self._db)
                student.student_next_id=student_current_id
                student.save(using=self._db)
                return new_student
             
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist("Student Doesn't exist")
            
        else:
            print(student_current_id)
            student = self.create(
                student_current_id = student_current_id,
                student_ext_id = student_current_id,
                student_college =college,
                student_grno = grno,
                student_admission_date = admission_date
            )
            
            student.save(using=self._db)
            return student
            
            
   
class Student(models.Model):
    salt = '*eyw$h8tutdvd6$m&za-x(1)s$7)-me58%g2p29l(^5#7a7mw1'  #Please don't change the salt
    
    student_current_id = models.BigIntegerField(primary_key=True)
    student_prev_id = models.BigIntegerField(default=None,null=True)
    student_next_id = models.BigIntegerField(default=None,null=True)
    
    student_ext_id =  BigHashidField(
        salt="student_student_id_"+salt,
        allow_int_lookup=True,
        enable_hashid_object=True,
    )
    
    student_college =  models.ForeignKey(College,on_delete=models.CASCADE)
    student_grno = models.CharField(max_length=20)
    student_admission_date = models.DateField()
    
    objects =  StudentManager()
    