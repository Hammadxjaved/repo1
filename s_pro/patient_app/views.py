import datetime
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

from django.contrib import messages


def calculate_age(dob):
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

from patient_app.models import *
from hospital_app.models import *
from home_app.models import *



def in_my_group(user):
    return user.groups.filter(name='Patient_group').exists()
# Create your views here.
@user_passes_test(in_my_group,login_url='/patient_login')
def p_index(request):
    a=request.session['uname']
    if a[0]!='P':
        logout(request)
        return redirect('/donor_login')
    hosp_detail = hospital_details.objects.all()
    return render(request,'index_patient.html',{"hospd":hosp_detail})

def p_login(request):
    if 'uname' in request.session:
        a=request.session['uname']
        if a[0]=='P':
            return redirect('/patient')  

    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        if username[0]!='P':
            return HttpResponse ("Username or Password is incorrect!!!")
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            user1 = patient_details.objects.get(id_no=username)
            user1.age = calculate_age(user1.dob)
            user1.save()
            login(request,user)
            request.session['uname'] = username
            return redirect('/patient')
        else:
            messages.success(request, 'Username or Password is incorrect!!')
            

    return render (request,'login_patient.html')

def p_signup(request):
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
        bg = request.POST.get('bg')
        gender = request.POST.get('gender')
        # age = request.POST.get('age')
        dob_str = request.POST.get('dob')
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
        age = calculate_age(dob)

        if uname[0]!='P':
            return HttpResponse("Enter Username starting with 'P'!!")

        user1 = User.objects.all()
        for i  in user1:
            if i.username == uname:
                return HttpResponse("username already exist!!")
                
        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            group = Group.objects.get(name='Patient_group')
            group.user_set.add(my_user)
        query1 = patient_address(patient_id = uname,state=st,city=city,landmark= landmark,address=add)
        query1.save()

        query2 = patient_details(id_no=uname,name=name,email=email,location=patient_address.objects.get(patient_id = uname),contact_no1=phno,age = age,gender=gender,dob=dob,blood_group=bg)
        query2.save()
        
        return redirect('/patient_login')
    users = User.objects.all()
    return render (request,'signup_patient.html',{"users":users})

@user_passes_test(in_my_group,login_url='/patient_login')
def p_update(request):
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

        p_uname = request.session['uname']
        p_user = patient_details.objects.get(id_no=p_uname)
        p_user.email = email
        p_user.contact_no1 = phno

        loc = p_user.location
        loc.address = add
        loc.landmark = landmark
        loc.city = city
        loc.state = st
        loc.save()
        p_user.save()
        messages.success(request, 'Your Profile is updated successfully')
        return redirect('/patient')
    p_uname = request.session['uname']
    p_user = patient_details.objects.get(id_no=p_uname)
    return render(request,"p_update.html",{"j":p_user})

@user_passes_test(in_my_group,login_url='/patient_login')
def p_req(request):
    if request.method == "POST":
        id_no = request.POST.get('data')
        d_id = request.POST.get('d_id')
        req1 = blood_request.objects.get(id=id_no)
        req1.recieved = True
        if d_id != "none":
            req1.donor_id = donor_details.objects.get(id_no=d_id)
        req1.date_of_response = datetime.date.today()
        req1.save()
        blood_request_response.objects.filter(patient_id = request.session["uname"]).delete()
        messages.success(request, 'Updated successfully')
        return redirect('/patient')

    req1 = blood_request.objects.filter(patient_id=request.session['uname'],recieved = False)
    if blood_request_response.objects.filter(patient_id=request.session['uname']).exists():
        req2 = blood_request_response.objects.filter(patient_id=request.session['uname'])
    else:
        req2 =""
    
    return render(request,"p_req.html",{"r":req1,"r2":req2})

@user_passes_test(in_my_group,login_url='/patient_login')
def p_make_req(request):
    if request.method == "POST":
        quan=request.POST.get('quan')
        hosp=request.POST.get('hosp')
        hospn=request.POST.get('hospn')
        if hospn!="":
            hosp = hospn
            hosp_add=request.POST.get('hosp_add')
        else:
            hoop1 = hospital_details.objects.get(id_no=hosp)
            hosp_add = hoop1.location.address +", near "+ hoop1.location.landmark +", "+ hoop1.location.city +", "+ hoop1.location.state
            hosp = hoop1.name

        today = datetime.date.today()
        uname = request.session['uname']
        if blood_request.objects.filter(patient_id=uname).exists():
            user = blood_request.objects.get(patient_id=uname)
            user.date_of_request=today
            user.hospital_name=hosp
            user.hospital_add=hosp_add
            user.quantity=quan
            user.recieved = False
            user.donor_id = None 
            user.date_of_response = None
            user.save()
        else:     
            query = blood_request(date_of_request=today,hospital_name=hosp,hospital_add=hosp_add,quantity=quan,patient_id=patient_details.objects.get(id_no = uname))
            query.save()
        messages.success(request, 'Your request is successful')
        return redirect('/patient')

    p_uname = request.session['uname']
    p_user = patient_details.objects.get(id_no=p_uname)
    hosp = hospital_details.objects.all()
    return render(request,"p_make_req.html",{"i":p_user,"j":hosp})



def p_logout(request):
    del request.session['uname']
    logout(request)
    return redirect('/patient_login')