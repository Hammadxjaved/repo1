"""seniorproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from donor_app import views

urlpatterns = [ 
path('', views.d_index,name= 'homepage'), 
path('_appoint', views.appoint,name= 'appointment'),
path('_show_req', views.d_show_req,name= 'blood_req'),
# path('_appoint_form', views.d_appoint_form,name= 'appointment'),
path('_signup', views.d_signup,name= 'signup'),
path('_login', views.d_login,name= 'login'),
path('_logout', views.d_logout,name= 'logout'),
path('_appointments', views.d_appoint,name= 'Appoint'),
path('_update', views.d_update,name= 'update'),
path('_h_page', views.d_h_page,name= 'hosp'),


]
