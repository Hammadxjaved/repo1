from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, date
from home_app.models import appointment_scheduled

from django.core.mail import send_mail

from hospital_app.models import *


def in_my_group(user):
    return user.groups.filter(name='Hospital_Group').exists()
# Create your views here.


# @login_required(login_url='/hospital_login')

@user_passes_test(in_my_group, login_url='/hospital_login')
def h_index(request):
    if request.method == 'POST':
        h_uname = request.session['uname']
        d_id = request.POST.get('d_id')
        email = request.POST.get('d_email')
        id_no = request.POST.get('id_no')
        datetime_str = request.POST['date_scheduled']
        my_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        appoint = appointment_scheduled.objects.get(id=id_no)
        appoint.date_scheduled = my_datetime
        appoint.confirmed = True
        appoint.save()
        try:
            send_mail(
            'Your Appointment is confirmed',
            f'''Your Appointment for blood donation, Appointment ID: {id_no},
            is confirmed.
            Date Scheduled: {datetime_str}
            For more info login to the system
            ''',
            'hammadj684@gmail.com',
            [f'{email}'],
            fail_silently=False,
            )
        except:
            a = 1
        messages.success(request, 'Appointment confirmed successfully!!')
        return render(request, 'index_hospital.html')

    a = request.session['uname']
    if a[0] != 'H':
        logout(request)
        return redirect('/hospital_login')
    hosp = hospital_details.objects.get(id_no=a)
    return render(request, 'index_hospital.html',{"hosp":hosp})


# @user_passes_test(in_my_group,login_url='/hospital_login')
# @login_required(login_url='/hospital_login')
def h_page(request):
    if request.method == 'POST':
        id = request.POST.get('data')
        print(id)
        hosp = hospital_details.objects.get(id_no=id)
        return render(request, 'page_hospital.html', {"hosp": hosp})
    return render(request, 'page_hospital.html')


def h_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        if username[0] != 'H':
            return HttpResponse(f"Username or Password is incorrect!!!,{pass1},{username}")
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            request.session['uname'] = username
            return redirect('/hospital')
        else:
            messages.success(request, 'Username or Password is incorrect!!')

    return render(request, 'login_hospital.html')


def h_signup(request):
    if request.method == 'POST':
        # user
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # location
        add = request.POST.get('address')
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        st = request.POST.get('state')

        # details
        name = request.POST.get('name')
        phno1 = request.POST.get('phno1')
        phno2 = request.POST.get('phno2')

        # quantity
        Ap = request.POST.get('Ap')
        An = request.POST.get('An')
        Bp = request.POST.get('Bp')
        Bn = request.POST.get('Bn')
        ABp = request.POST.get('ABp')
        ABn = request.POST.get('ABn')
        Op = request.POST.get('Op')
        On = request.POST.get('On')

        user1 = User.objects.all()
        for i in user1:
            if i.username == uname:
                return HttpResponse("username already exist!!")

        if pass1 != pass2:
            return HttpResponse("Your password and confrim password are not Same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            group = Group.objects.get(name='Hospital_Group')
            group.user_set.add(my_user)
        quesry1 = hospital_address(
            hopital_id=uname, state=st, city=city, landmark=landmark, address=add)
        quesry1.save()

        query2 = blood_quantity(hopital_id=uname, bg_O_pos=Op, bg_O_neg=On, bg_B_pos=Bp, bg_B_neg=Bn,
                                bg_A_pos=Ap, bg_A_neg=An, bg_AB_pos=ABp, bg_AB_neg=ABn, last_updated=(date.today()))
        query2.save()

        query3 = hospital_details(id_no=uname, name=name, email=email, location=hospital_address.objects.get(
            hopital_id=uname), contact_no1=phno1, contact_no2=phno2, blood_quant=blood_quantity.objects.get(hopital_id=uname))
        query3.save()

        return redirect('/hospital_login')
    users = User.objects.all()
    return render(request, 'signup_hospital.html',{"users":users})


@user_passes_test(in_my_group, login_url='/hospital_login')
def h_update(request):
    if request.method == 'POST':
        # user
        email = request.POST.get('email')

        # details
        Ap = request.POST.get('Ap')
        An = request.POST.get('An')
        Bp = request.POST.get('Bp')
        Bn = request.POST.get('Bn')
        ABp = request.POST.get('ABp')
        ABn = request.POST.get('ABn')
        Op = request.POST.get('Op')
        On = request.POST.get('On')

        phno1 = request.POST.get('phno1')
        phno2 = request.POST.get('phno2')

        h_uname = request.session['uname']

        h_user = hospital_details.objects.get(id_no=h_uname)
        h_user.email = email
        h_user.contact_no1 = phno1
        h_user.contact_no2 = phno2
        quant = h_user.blood_quant
        quant.bg_O_pos = Op
        quant.bg_O_neg = On
        quant.bg_A_pos = Ap
        quant.bg_A_neg = An
        quant.bg_B_pos = Bp
        quant.bg_B_neg = Bn
        quant.bg_AB_pos = ABp
        quant.bg_AB_neg = ABn
        quant.last_updated = date.today()
        quant.save()

        h_user.save()
        messages.success(request, 'Your Profile is updated successfully')
        return redirect('/hospital')

    h_uname = request.session['uname']
    h_user = hospital_details.objects.get(id_no=h_uname)
    return render(request, "h_update.html", {"j": h_user})


@user_passes_test(in_my_group, login_url='/hospital_login')
def h_scheduled_appoint(request):
    h_uname = request.session['uname']
    appoint = appointment_scheduled.objects.filter(
        hospital_id=h_uname, confirmed=True)
    return render(request, "h_scheduled_appoint.html", {"app": appoint})


@user_passes_test(in_my_group, login_url='/hospital_login')
def h_appoint(request):
    if request.method == 'POST':
        h_uname = request.session['uname']
        d_id = request.POST.get('d_id')
        id = request.POST.get('id_no')
        appoint = appointment_scheduled.objects.get(id=id)
        return render(request, "h_appoint_page.html", {"hosp": appoint})

    h_uname = request.session['uname']
    appoint = appointment_scheduled.objects.filter(
        hospital_id=h_uname, confirmed=False)
    return render(request, "h_appoint.html", {"app": appoint})


@user_passes_test(in_my_group, login_url='/hospital_login')
def h_appoint_page(request):
    return HttpResponse("")


def h_logout(request):
    del request.session['uname']
    logout(request)
    return redirect('/hospital_login')
