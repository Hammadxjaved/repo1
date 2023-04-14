from django.contrib import admin
from hospital_app.models import *

# Register your models here.
admin.site.register(hospital_details)
admin.site.register(hospital_address)
admin.site.register(blood_quantity)

