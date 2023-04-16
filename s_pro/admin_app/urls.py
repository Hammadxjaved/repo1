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
from admin_app import views

urlpatterns = [
path('', views.a_index,name= 'homepage'),
path('_d_page', views.a_d_page,name= 'donorpage'),
path('_d_del', views.a_d_del,name= 'donordelete'),
path('_h_page', views.a_h_page,name= 'hosppage'),
path('_p_page', views.a_p_page,name= 'patientpage'),
path('_show_req', views.a_show_req,name= 'showreq'),
path('_login', views.a_login,name= 'login'),
path('_logout', views.a_logout,name= 'logout'),
]
