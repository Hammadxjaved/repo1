from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.


@login_required(login_url='/admin_user_login')
def a_index(request):
    return render(request,'index_admin.html')

def a_login(request):
    if 'uname' in request.session:
        a=request.session['uname']
        if a == "admin":
            return redirect('/admin_user')
        
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        if username[0]!='a':
            return HttpResponse ("Username or Password is incorrect!!!")
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            request.session['uname'] = username
            return redirect('/admin_user')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login_admin.html')

def a_logout(request):
    logout(request)
    return redirect('/admin_user_login')

