from django.db import models
from django.contrib.auth.models import *


# Create your models here.
class donor_address(models.Model):
    donor_id =  models.CharField(max_length=40, primary_key=True)
    state = models.CharField(max_length=40) 
    city = models.CharField(max_length=40) 
    address = models.CharField(max_length=100) 
    landmark = models.CharField(max_length=40, null=True) 

class donor_health(models.Model):
    id_no = models.CharField(max_length=40,primary_key=True)
    weight = models.IntegerField()  #50kg or more
    last_donation_date = models.DateField(null=True, blank=True)#last blood donation date
    hemoglobin_level = models.FloatField(null=True, blank=True) # minimum 13g/dl
    piercing = models.BooleanField(default=False) #tattoo or piercing in last 12 months
    diabetic = models.BooleanField(default=False) #if taking insulin then no
    disease = models.BooleanField(default=False) # infectious diseases, such as HIV, hepatitis B or C, syphilis, or malaria,heart disease or cancer or any type of blood related infection
    preg = models.BooleanField(default=False)#pregnency or child birth in last 1 year is ineligible

class donor_details(models.Model):
    id_no = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    location = models.ForeignKey(donor_address,on_delete=models.CASCADE,default='-1')
    contact_no1 = models.CharField(max_length=12)
    gender = models.CharField(max_length=10,null=True, blank=True)
    age = models.IntegerField() #18 to 65
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5)
    health = models.ForeignKey(donor_health,on_delete=models.CASCADE,default='-1')


    
    

