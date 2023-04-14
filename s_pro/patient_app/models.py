from django.db import models
from django.contrib.auth.models import *



# Create your models here.
class patient_address(models.Model):
    patient_id =  models.CharField(max_length=40, primary_key=True)
    state = models.CharField(max_length=40) 
    city = models.CharField(max_length=40) 
    address = models.CharField(max_length=100) 
    landmark = models.CharField(max_length=40, null=True) 

class patient_details(models.Model):
    id_no = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=40) 
    email = models.EmailField(max_length=40)
    location = models.ForeignKey(patient_address,on_delete=models.CASCADE)
    contact_no1 = models.CharField(max_length=12)
    gender = models.CharField(max_length=10,null=True, blank=True) 
    age = models.IntegerField()
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5)
