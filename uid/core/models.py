
import re
from django.db import models

# Create your models here.

class StateManager(models.Manager):
    
    def create_state(self,state_name):
        state_name = state_name.lower().replace(" ","")
        state = self.create(state_name=state_name)
        return state
class State(models.Model):
    
    state_name = models.CharField(max_length=30, null=False,editable=False)
    state_id = models.AutoField(primary_key=True)
    objects = StateManager()
    def __str__(self):
        return str(self.state_name)

class UniversityManager(models.Manager):
    
    def create_university(self,uni_name,state_name,state_level_id):
        state = State.objects.get(state_name=state_name.lower().replace(" ",""))
        uni_id = int(str(state.state_id)+str(state_level_id))   
        university = self.create(
            uni_name = uni_name.lower().replace(" ",""),
            state = state,
            state_level_id=state_level_id,
            uni_id=uni_id
        )
        return university
class University(models.Model):
    
    uni_name = models.CharField(max_length=50,null=False)
    state = models.ForeignKey(State,related_name="state",on_delete=models.DO_NOTHING,editable=False)
    state_level_id = models.IntegerField(null=False,editable=False)
    uni_id = models.IntegerField(primary_key=True,editable=False)
    objects = UniversityManager()
    
    def __str__(self):
        return str(self.uni_name)
    
class College(models.Model):
    
    college_name = models.CharField(max_length=50,null=False)
    college_type = models.CharField(max_length=20,null=False)
    university = models.ForeignKey(University,on_delete=models.DO_NOTHING) 
    uni_level_id=models.IntegerField(null=False)
    