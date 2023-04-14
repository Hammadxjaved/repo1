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
from patient_app import views
 
urlpatterns = [
path('', views.p_index,name= 'homepage'),
path('_signup', views.p_signup,name= 'signup'), 
path('_login', views.p_login,name= 'login'),
path('_update', views.p_update,name= 'update'),
path('_make_req', views.p_make_req,name= 'make_req'),
path('_req', views.p_req,name= 'req'),
path('_logout', views.p_logout,name= 'logout'),

]
