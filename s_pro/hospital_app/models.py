
from django.db import models
from django.contrib.auth.models import *
 

# Create your models here.
class hospital_address(models.Model):
    hopital_id =  models.CharField(max_length=40, primary_key=True)
    state = models.CharField(max_length=40) 
    city = models.CharField(max_length=40) 
    address = models.CharField(max_length=100) 
    landmark = models.CharField(max_length=40, null=True) 


class blood_quantity(models.Model):
    hopital_id =  models.CharField(max_length=40,primary_key=True)
    bg_O_pos = models.IntegerField()
    bg_O_neg = models.IntegerField()
    bg_B_pos = models.IntegerField()
    bg_B_neg = models.IntegerField()
    bg_A_pos = models.IntegerField()
    bg_A_neg = models.IntegerField()
    bg_AB_pos = models.IntegerField()
    bg_AB_neg = models.IntegerField()
    last_updated = models.DateField(null=True)


class hospital_details(models.Model):
    id_no = models.CharField(max_length=40,primary_key=True)
    # id_no = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40) 
    email = models.EmailField(max_length=40)
    location = models.ForeignKey(hospital_address,on_delete=models.CASCADE,default='-1')
    contact_no1 = models.CharField(max_length=12)
    contact_no2 = models.CharField(max_length=13, null=True, blank=True)
    blood_quant = models.ForeignKey(blood_quantity,on_delete=models.CASCADE,default='-1')

