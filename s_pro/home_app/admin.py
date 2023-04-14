from django.contrib import admin
from home_app.models import *

# Register your models here.
admin.site.register(appointment_scheduled)
admin.site.register(blood_request)
admin.site.register(blood_request_response)