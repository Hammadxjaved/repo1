from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.contrib import messages

from hospital_app.models import *


# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')

def check(request):
    user = User.objects.all()
    return render(request,'check.html',{"user":user})


import random
def pwd(request):
    if request.method=='POST':
        id=request.POST.get('username')
        request.session['username'] = id
        
        user = User.objects.get(username=id)

        otp = random.randint(100000,999999)
        try:
            send_mail(
            'Otp to reset password',
            f'Your Otp is {otp}',
            'hammadj684@gmail.com',
            [f'{user.email}'],
            fail_silently=False,
            )
        except:
            content = "<html><head><style>body { font-size: 20px; }</style></head><body><br><br><br><h1>This Service is Temporarily Unavailable</h1></body></html>"
            return HttpResponse(content)
        
        return render(request,'pwd_otp.html',{"user":user, "otp":otp})
    users = User.objects.all()
    return render(request,'pwd_forgot.html',{"users":users})


def r_pwd(request):
    if request.method=='POST':
        pass1=request.POST.get('pass1')
        if 'username' in request.session:
            id =  request.session['username'] 
        else:
            return redirect('/password_reset')
        user = User.objects.get(username=id)
        user.set_password(pass1)
        user.save()
        del request.session['username'] 
        messages.success(request, 'Password reset Successful')
        return redirect('/')

    return render(request,'pwd_reset.html')

def h_search(request):
    if request.method=='POST':
        city=request.POST.get('city')

        hosp_detail = hospital_details.objects.filter(location__city = city)
        #location__city will refer to city field with is in table connectd by feild location with foreign key
        return render(request,'h_search.html',{"hospd":hosp_detail})



  
