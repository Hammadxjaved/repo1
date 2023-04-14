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
from hospital_app import views

urlpatterns = [
path('', views.h_index,name= 'homepage'),
path('_page', views.h_page,name= 'page'),
path('_update', views.h_update,name= 'update'),
path('_scheduled_appoints', views.h_scheduled_appoint,name= 'scheduled_apppointments'),
path('_appoints', views.h_appoint,name= 'apppointments'),
path('_appoints_page', views.h_appoint_page,name= 'apppointment page'),
path('_signup', views.h_signup,name= 'signup'),
path('_login', views.h_login,name= 'login'),
path('_logout', views.h_logout,name= 'logout'),
]