from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

from django.contrib import messages
from home_app.models import *
from donor_app.models import *
from patient_app.models import *
from hospital_app.models import *

# Create your views here.


@login_required(login_url='/admin_user_login')
def a_index(request):
    donors = donor_details.objects.all()
    hospitals = patient_details.objects.all()
    patients = hospital_details.objects.all()
    context = {
        "donors":donors,
        "hosps":hospitals,
        "patients":patients
    }
    return render(request,'index_admin.html',context)



@login_required(login_url='/admin_user_login')
def a_d_del(request):
    if "d_id" in request.session:
        id_no = request.session["d_id"]
        User.objects.get(username = id_no).delete()
        donor_address.objects.get(donor_id = id_no).delete()
        donor_health.objects.get(id_no = id_no).delete()
        messages.success(request, 'Donor Removed Successfully')
        return redirect("/admin_user")
    return redirect("/admin_user")


@login_required(login_url='/admin_user_login')
def a_d_page(request):
    if request.method == "POST":
        id_no = request.POST.get("id_no")
        request.session["d_id"] = id_no
        user = donor_details.objects.get(id_no=id_no)
        app = appointment_scheduled.objects.filter(donor_id=id_no)
        req = blood_request.objects.filter(donor_id=id_no)
        return render(request,'a_d_page.html',{"d":user, "app":app , "r2":req})
    return redirect("/admin_user")



@login_required(login_url='/admin_user_login')
def a_h_page(request):
    if request.method == "POST":
        id_no = request.POST.get("id_no")
        request.session["h_id"] = id_no
        user = hospital_details.objects.get(id_no=id_no)
        app = appointment_scheduled.objects.filter(hospital_id=id_no)
        
        return render(request,'a_d_page.html',{"h":user, "app":app})
    return redirect("/admin_user")

@login_required(login_url='/admin_user_login')
def a_h_del(request):
    if "h_id" in request.session:
        id_no = request.session["h_id"]
        User.objects.get(username = id_no).delete()
        blood_quantity.objects.get(donor_id = id_no).delete()
        hospital_address.objects.get(id_no = id_no).delete()
        messages.success(request, 'Hospital Removed Successfully')
        return redirect("/admin_user")
    return redirect("/admin_user")

@login_required(login_url='/admin_user_login')
def a_p_page(request):
    if request.method == "POST":
        id_no = request.POST.get("id_no")
        request.session["p_id"] = id_no
        user = patient_details.objects.get(id_no=id_no)
        req = blood_request.objects.filter(patient_id=id_no)
        return render(request,'a_d_page.html',{"p":user, "req":req})
    return redirect("/admin_user")

@login_required(login_url='/admin_user_login')
def a_p_del(request):
    if "p_id" in request.session:
        id_no = request.session["p_id"]
        User.objects.get(username = id_no).delete()
        patient_address.objects.get(donor_id = id_no).delete()
        messages.success(request, 'Patient Removed Successfully')
        return redirect("/admin_user")
    return redirect("/admin_user")


@login_required(login_url='/admin_user_login')
def a_show_req(request):
    return render(request,'a_show_req.html')

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
            messages.success(request, 'Username or Password is incorrect!!')

    return render (request,'login_admin.html')

def a_logout(request):
    del request.session['uname']
    logout(request)
    return redirect('/')

