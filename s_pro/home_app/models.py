from django.db import models

# Create your models here.
from django.contrib.auth.models import *
from hospital_app.models import *
from donor_app.models import *
from patient_app.models import *



# Create your models here.
class appointment_scheduled(models.Model):
    date_scheduled = models.DateTimeField(null=True)
    date_of_appointment = models.DateField()
    donor_id = models.ForeignKey(donor_details,on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital_details,on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)


class blood_request(models.Model):
    
    date_of_request = models.DateField()
    patient_id = models.ForeignKey(patient_details,on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=30) #if listed hospital then hospital id else name of hospital
    hospital_add = models.CharField(max_length=100,null=True) #if listed hospital then hospital id else name of hospital
    quantity = models.IntegerField(null=True)
    recieved = models.BooleanField(default=False)
    date_of_response = models.DateField(null=True)
    donor_id = models.ForeignKey(donor_details,on_delete=models.CASCADE, null=True)

class blood_request_response(models.Model): 
    donor_id = models.ForeignKey(donor_details,on_delete=models.CASCADE, null=True)
    patient_id = models.ForeignKey(patient_details,on_delete=models.CASCADE, null=True)
    req_id =  models.ForeignKey(blood_request,on_delete=models.CASCADE, null=True)
    




