import datetime
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

from donor_app.models import *
from hospital_app.models import *
from home_app.models import *

from django.contrib import messages

def calculate_age(dob):
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def in_my_group(user):
    return user.groups.filter(name='Donor_group').exists()



# Create your views here.
# Index page
@user_passes_test(in_my_group,login_url='/donor_login')
def d_index(request):
    a=""
    if "uname" in request.session:
        a=request.session['uname']
    if a[0]!='D':
        logout(request)
        return redirect('/donor_login')
    
    # hospitals = hospital_details.objects.all()
    hosp_detail = hospital_details.objects.all()
    return render(request,'donor/index_donor.html',{"hospd":hosp_detail}) 


#Login page
def d_login(request):
    if 'uname' in request.session:
        a=request.session['uname']
        if a[0]=='D':
            return redirect('/donor')  
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            user1 = donor_details.objects.get(id_no=username)
            user1.age = calculate_age(user1.dob)
            user1.save()
            login(request,user)
            request.session['uname'] = username
            return redirect('/donor')
        else:
            messages.success(request, 'Username or Password is incorrect!!')
            

    return render (request,'donor/login_donor.html')



#Signup page
def d_signup(request):
    if request.method=='POST':
        # user
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        # location
        add=request.POST.get('address')
        city=request.POST.get('city')
        landmark=request.POST.get('landmark')
        st=request.POST.get('state')

        # details
        name=request.POST.get('name')
        phno=request.POST.get('phno')
        gender=request.POST.get('gender')
        bg = request.POST.get('bg')
        # age = request.POST.get('age')
        dob_str = request.POST.get('dob')
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        age = calculate_age(dob)

        #health
        weight=request.POST.get('weight')
        hemo = request.POST.get('hemo')
        lastdonation_str = request.POST.get('lastdonation')
        lastdonation = datetime.datetime.strptime(lastdonation_str, '%Y-%m-%d').date()
        piercing = request.POST.get('piercing')
        diabetic = request.POST.get('diabetic')
        disease = request.POST.get('disease')
        preg = request.POST.get('preg')




        if uname[0]!='D':
            return HttpResponse("Enter Username starting with 'D'!!")

        user1 = User.objects.all()
        for i  in user1:
            if i.username == uname:
                return HttpResponse("Username already exist!!")
                
        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            group = Group.objects.get(name='Donor_group')
            group.user_set.add(my_user)
        query1 = donor_address(donor_id = uname,state=st,city=city,landmark= landmark,address=add)
        query1.save()

        query2 = donor_health(id_no = uname,weight=weight,last_donation_date=lastdonation, hemoglobin_level= hemo)
        query2.save()
        if diabetic=="Yes":
            query2.diabetic = True
        else:
            query2.diabetic = False
        if disease=="Yes":
            query2.disease = True
        else:
            query2.disease = False
        if preg=="Yes":
            query2.preg = True
        else:
            query2.preg = False
        if piercing=="Yes":
            query2.piercing = True
        else:
            query2.piercing = False

        query2.save()        

        query3 = donor_details(id_no=uname,name=name,email=email,location=donor_address.objects.get(donor_id = uname),contact_no1=phno,gender=gender,age = age,dob=dob,blood_group=bg,health=donor_health.objects.get(id_no = uname))
        query3.save()
        messages.success(request, 'Signup successful')
        return redirect('/donor_login')
    users = User.objects.all()
    return render (request,'donor/signup_donor.html',{"users":users})



 
# Request appointment form page
@user_passes_test(in_my_group,login_url='/donor_login')
def appoint(request):
    if request.method=='POST':
        h_uname = request.session["hosp"]
        d_id = request.session['uname']
        today = datetime.date.today()
        
        q = appointment_scheduled(donor_id = donor_details.objects.get(id_no =d_id),hospital_id = hospital_details.objects.get(id_no =h_uname),date_of_appointment=today)
        q.save()
        messages.success(request, 'Your Appointment is Requested successfully')
        return redirect('/donor')


    h_uname = request.session["hosp"]
    id = request.session['uname']
    user1 = donor_details.objects.get(id_no = id)
    hosp1 = hospital_details.objects.get(id_no = h_uname)

    return render(request,"donor/d_appoint_form.html",{"i":user1,"hosp":hosp1})



# All requested Appointments
@user_passes_test(in_my_group,login_url='/donor_login')
def d_appoint(request):
    d_uname = request.session['uname']
    appoint = appointment_scheduled.objects.filter(donor_id=d_uname)
    return render(request,"donor/d_scheduled_appoint.html",{"app":appoint})


# @user_passes_test(in_my_group,login_url='/donor_login')
# def d_appoint_form(request):
#     if request.method=='POST':
#         d_uname = request.session['uname']
#         h_uname = request.POST.get('hosp1')
#         today = datetime.date.today()
#         q = appointment_scheduled(date_of_appointment=today,donor_id=donor_details.objects.get(id_no = d_uname),hospital_id=hospital_details.objects.get(id_no = h_uname))
#         q.save()


#Show blood requests
@user_passes_test(in_my_group,login_url='/donor_login')
def d_show_req(request): 
    if request.method=='POST':
        d_id = request.session['uname']
        data=request.POST.get('data') 
        if not blood_request_response.objects.filter(donor_id = d_id,req_id = blood_request.objects.get(id=data)).exists():
            p_id=request.POST.get('p_id')
            q = blood_request_response(patient_id = patient_details.objects.get(id_no = p_id),donor_id = donor_details.objects.get(id_no = d_id),req_id = blood_request.objects.get(id=data))
            q.save()
            messages.success(request, 'Your interest Registerd successfully\nGet to the hospital as soon as possible')
            return redirect('/donor')
    d_id = request.session['uname']
    if blood_request_response.objects.filter(donor_id=donor_details.objects.get(id_no = d_id)).exists():
        req2 = blood_request_response.objects.filter(donor_id=donor_details.objects.get(id_no = d_id))
    else:
        req2 = ""
    req1 = blood_request.objects.filter(recieved=False)
    return render(request,"donor/d_show_req.html",{"r":req1,"r2":req2})


#Update details
@user_passes_test(in_my_group,login_url='/donor_login')
def d_update(request):
    if request.method=='POST':
        # user
       
        email=request.POST.get('email')
        

        # location
        add=request.POST.get('address')
        city=request.POST.get('city')
        landmark=request.POST.get('landmark')
        st=request.POST.get('state')

        # details
        
        phno=request.POST.get('phno')
        

        #health
        weight=request.POST.get('weight')
        hemo = request.POST.get('hemo')
        lastdonation_str = request.POST.get('lastdonation')
        lastdonation = datetime.datetime.strptime(lastdonation_str, '%Y-%m-%d').date()
        piercing = request.POST.get('piercing')
        diabetic = request.POST.get('diabetic')
        disease = request.POST.get('disease')
        preg = request.POST.get('preg')

        d_uname = request.session['uname']
        d_user = donor_details.objects.get(id_no=d_uname)
        d_user.email = email
        d_user.contact_no1 = phno

        health = d_user.health
        loc = d_user.location
        loc.address = add
        loc.landmark = landmark
        loc.city = city 
        loc.state = st
        loc.save()

        health.weight = weight
        health.hemoglobin_level = hemo
        health.last_donation_date =  lastdonation

        
        if diabetic=="Yes":
            health.diabetic = True
        else:
            health.diabetic = False
        if disease=="Yes":
            health.disease = True
        else:
            health.disease = False
        if preg=="Yes":
            health.preg = True
        else:
            health.preg = False
        if piercing=="Yes":
            health.piercing = True
        else:
            health.piercing = False
        health.save()
        d_user.save()
        messages.success(request, 'Profile Updated Successfully!!')
        return redirect('/donor')
    d_uname = request.session['uname']
    d_user = donor_details.objects.get(id_no=d_uname)
    if d_user.gender == "female":
        g = True
    else:
        g=False
    return render(request,"donor/d_update.html",{"j":d_user, "g":g})


# Hospital Profile
@user_passes_test(in_my_group,login_url='/donor_login')
def d_h_page(request):
    if request.method=='POST':
        id=request.POST.get('data')
        request.session['hosp'] = id
        hosp = hospital_details.objects.get(id_no=id)
        return render(request,'page_hospital.html',{"hosp":hosp})
    return render(request,'page_hospital.html')



def d_logout(request):
    del request.session['uname']
    logout(request)
    return redirect('/')
