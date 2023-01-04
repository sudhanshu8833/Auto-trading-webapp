

from django.contrib.auth.decorators import login_required
from shop.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.views import *
from django.core.mail import send_mail
from django.http import HttpResponse
# from shop.helpful_scripts.object import *
from django.contrib.auth import authenticate,  login, logout
from django.conf import settings
from pytz import timezone
from datetime import datetime,timedelta

import logging
import traceback
logger = logging.getLogger('dev_log')


def home(request):
    return render(request, "shop/home1.html")


@login_required(login_url='/signup')
def setting(request):

    current_user = request.user
    if request.method == "POST":

        subs=subscriptions.objects.filter(username=current_user)

        for i in range(len(subs)):
            if subs[i].strategy_name=="Volume Based Intraday":
                subs[i].symbols=request.POST.get("symbol_1")
                subs[i].quantity=int(request.POST.get("quantity_1"))
                subs[i].save()

            elif subs[i].strategy_name=="PPM":
                subs[i].symbols=request.POST.get("symbol_2")
                subs[i].quantity=int(request.POST.get("quantity_2"))
                subs[i].save()

            elif subs[i].strategy_name=="PPM BTST":
                subs[i].symbols=request.POST.get("symbol_3")
                subs[i].quantity=int(request.POST.get("quantity_3"))
                subs[i].save()

            elif subs[i].strategy_name=="strategy4":
                subs[i].symbols=request.POST.get("symbol_4")
                subs[i].quantity=int(request.POST.get("quantity_4"))
                subs[i].save()

            elif subs[i].strategy_name=="strategy5":
                subs[i].symbols=request.POST.get("symbol_5")
                subs[i].quantity=int(request.POST.get("quantity_5"))
                subs[i].save()

        messages.success(request, "Your details added successfully!!")
        return redirect('index')


    myuser = User1.objects.get(username=current_user)
    subs=subscriptions.objects.filter(username=current_user)
    params = {'myuser': myuser,"subs":subs}
    return render(request, "shop/settings.html", params)



def is_today(dt):
    today = datetime.now(timezone("Asia/Kolkata")).date()
    return dt.date() == today

def is_thisweek(dt):
    now = datetime.now(timezone("Asia/Kolkata"))
    seven_days_ago = now - timedelta(days=7)
    return dt > seven_days_ago

def is_this_year(dt):
    now = datetime.now(timezone("Asia/Kolkata"))
    return dt.year == now.year

def activate_bot(request,passphrase):
    current_user=request.user
    
    try:
        if passphrase=="Volume Based Intraday":
            record=subscriptions.objects.get(strategy_name=passphrase,username=current_user)
            if record.status=="off":
                record.status="on"
                record.save()

            else:
                record.status="off"
                record.save()

        if passphrase=="PPM":
            record=subscriptions.objects.get(strategy_name=passphrase,username=current_user)
            if record.status=="off":
                record.status="on"
                record.save()

            else:
                record.status="off"
                record.save()

        if passphrase=="PPM BTST":
            record=subscriptions.objects.get(strategy_name=passphrase,username=current_user)
            if record.status=="off":
                record.status="on"
                record.save()

            else:
                record.status="off"
                record.save()


        if passphrase=="strategy4":
            record=subscriptions.objects.get(strategy_name=passphrase,username=current_user)
            if record.status=="off":
                record.status="on"
                record.save()

            else:
                record.status="off"
                record.save()


        if passphrase=="strategy5":
            record=subscriptions.objects.get(strategy_name=passphrase,username=current_user)
            if record.status=="off":
                record.status="on"
                record.save()

            else:
                record.status="off"
                record.save()
    except Exception:
        logger.info(traceback.format_exc())


    return redirect('index')

def strategies(request):
    current_user=request.user
    strat=strategy.objects.all()
    param=[]
    for j in range(len(strat)):



        position=positions.objects.filter(strategy_name=strat[j].strategy_name)

        data={}
        overall_pnl=0
        today_pnl=0
        week_pnl=0
        year_pnl=0

        for i in range(len(position)):

            try:
                if position[i].side=="buy":
                    pnl=((position[i].current_price-position[i].price_in)/position[i].price_in)*100
                    position[i].pnl=round(pnl,2)
                    position[i].save()
                    overall_pnl+=pnl

                    if is_thisweek(position[i].time_in):
                        week_pnl+=pnl

                    if is_today(position[i].time_in):
                        today_pnl+=pnl

                    if is_this_year(position[i].time_in):
                        year_pnl+=pnl

                else:
                    pnl=((position[i].price_in-position[i].current_price)/position[i].current_price)*100
                    position[i].pnl=round(pnl,2)
                    position[i].save()
                    overall_pnl+=pnl

                    if is_today(position[i].time_in):
                        today_pnl+=pnl

                    if is_thisweek(position[i].time_in):
                        week_pnl+=pnl

                    if is_this_year(position[i].time_in):
                        year_pnl+=pnl

            except Exception:
                logger.info(traceback.format_exc())

        data['week_pnl']=round(week_pnl,2)
        data['year_pnl']=round(year_pnl,2)
        data['today_pnl']=round(today_pnl,2)
        data['overall_pnl']=round(overall_pnl,2)
        data['strategy_name']=strat[j].strategy_name

        data['positions']=position
        # param[strat[j].strategy_name]=data

        param.append(data)

    params={"param":param,"myuser":current_user}
    print(params)
    return render(request, "shop/strategy.html",params)



def personal(request):
    current_user=request.user



    position=positions_userwise.objects.filter(username=current_user)

    data={}
    overall_pnl=0
    today_pnl=0
    week_pnl=0
    year_pnl=0

    for i in range(len(position)):


        try:
            if position[i].side=="buy":
                pnl=((position[i].current_price-position[i].price_in)/position[i].price_in)*100
                position[i].pnl=round(pnl,2)
                position[i].save()
                overall_pnl+=pnl

                if is_thisweek(position[i].time_in):
                    week_pnl+=pnl

                if is_today(position[i].time_in):
                    today_pnl+=pnl

                if is_this_year(position[i].time_in):
                    year_pnl+=pnl

            else:
                pnl=((position[i].price_in-position[i].current_price)/position[i].current_price)*100
                position[i].pnl=round(pnl,2)
                position[i].save()
                overall_pnl+=pnl

                if is_today(position[i].time_in):
                    today_pnl+=pnl

                if is_thisweek(position[i].time_in):
                    week_pnl+=pnl

                if is_this_year(position[i].time_in):
                    year_pnl+=pnl
        except Exception:
            logger.info(traceback.format_exc())



    data['week_pnl']=round(week_pnl,2)
    data['year_pnl']=round(year_pnl,2)
    data['today_pnl']=round(today_pnl,2)
    data['overall_pnl']=round(overall_pnl,2)


    data['positions']=position




    param={"param":data,"myuser":current_user}
    print(param)
    return render(request, "shop/personal.html",param)



def signup(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('usr')
            usr = User.objects.get(username=get_user)
            usr2 = User1.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                usr2.is_active = True
                usr2.save()
                messages.success(
                    request, " Your Account has been successfully created")
                login(request, usr)
                return redirect('index')
            else:
                messages.warning(request, " You Entered wrong OTP !")
                return redirect(request, "shop/signup.html", {'otp': True, 'usr': usr})
        username = request.POST['username']
        email = request.POST['email']
        phone = 9999999999
        password = request.POST['pass1']
        print(password)
        if len(username) > 10:
            messages.error(
                request, " Your user name must be under 10 characters")
            return redirect('signup')
        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('signup')

        match = None
        try:
            match = User1.objects.get(email=email)
        except User1.DoesNotExist:
            pass
        if(match):
            messages.error(request, " This email is already registered !! ")
            return redirect('signup')
        match = None
        try:
            match = User1.objects.get(username=username)
        except User1.DoesNotExist:
            pass
        if(match):
            messages.error(request, " This username is already registered !! ")
            return redirect('signup')
        myuser = User.objects.create_user(username, email, password)
        myuser.is_active = False
        myuser.save()

#############################################################
        all_strategy=strategy.objects.all()

        for i in range(5):
            subs=subscriptions(username=username,strategy_name=all_strategy[i].strategy_name,quantity=0,
                status="off",
                symbols="[]"
            )
            subs.save()
#############################################################

        user = User1(username=username,
                     email=email,
                     password=password,
                     phone=phone,
                     fullname='XYZ'
                     )

        user.save()
        usr_otp = random.randint(100000, 999999)
        UserOTP.objects.create(user=myuser, otp=usr_otp)

        mess = f"Hello {username} \n\nYour OTP is {usr_otp} \n\nPlease Do not share it with anyone..!!\nIf you didn't requested to login, you can safely ignore this email..!!\n\nYou may be required to register with the Site. You agree to keep your password confidential and will be responsible for all use of your account and password. We reserve the right to remove, reclaim, or change a username you select if we determine, in our sole discretion, that such username is inappropriate, obscene, or otherwise objectionable. \n\nAlgo99\nDelhi Technological University \nDelhi, India \nalgo99.sudhanshu@gmail.com"
        send_mail(
            "Welcome to algo99 -Verify Your Email",
            mess,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        messages.success(request, "OTP is sent to your email..!!!")

        return render(request, "shop/signup.html", {'otp': True, 'usr': myuser})
    return render(request, "shop/signup.html")




def forgot(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('usr')
            get_pass = request.POST.get('password')
            usr = User.objects.get(username=get_user)
            usr2 = User1.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.password=get_pass
                usr.save()
                print(usr.password)
                usr2.password=get_pass
                usr2.save()
                messages.success(request, "Password Changed Successfully")
                return redirect("signup")
            messages.error(request, "Entered Wrong OTP")
            return redirect("signup")
        loginusername = request.POST['username']
        if not User.objects.filter(username=loginusername).exists():
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("signup")
        myuser = User.objects.get(username=loginusername)
        usr_otp = random.randint(100000, 999999)
        UserOTP.objects.create(user=myuser, otp=usr_otp)
        mess = f"Hello {loginusername} \n\nYour OTP is {usr_otp} \n\nPlease Do not share it with anyone..!!\nIf you didn't requested to change password, you can safely ignore this email..!!\n\nYou may be required to register with the Site. You agree to keep your password confidential and will be responsible for all use of your account and password. We reserve the right to remove, reclaim, or change a username you select if we determine, in our sole discretion, that such username is inappropriate, obscene, or otherwise objectionable. \n\nAlgo99\nDelhi Technological University \nDelhi, India \nalgo99.sudhanshu@gmail.com"
        send_mail(
            "Welcome to algo99 -Verify Your Email",
            mess,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            fail_silently=False
        )
        messages.success(request, "OTP is sent to your email..!!!")
        return render(request, "shop/forgot.html", {'otp': True, 'usr': myuser})
    return render(request, "shop/forgot.html")



@login_required(login_url='/signup')
def index(request):
    current_user =  request.user
    subs=subscriptions.objects.filter(username=current_user.username)

    return render(request, "shop/index.html", {"data":subs, "myuser":current_user})


def handleLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        print(request.user)
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('usr')
            usr = User.objects.get(username=get_user)
            usr2 = User1.objects.get(username=get_user)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                usr2.is_active = True
                usr2.save()
                login(request, usr)
                # messages.success(request, "Successfully Logged In")
                return redirect("index")
            else:
                messages.warning(request, " You Entered wrong OTP !")
                return redirect(request, "shop/login.html", {'otp': True, 'usr': usr})
        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        # user = authenticate(username=loginusername, password=loginpassword)
        if not User.objects.filter(username=loginusername).exists():
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("signup")
        elif not User.objects.get(username=loginusername).is_active:
            myuser = User.objects.get(username=loginusername)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=myuser, otp=usr_otp)

            mess = f"Hello {loginusername} \n\nYour OTP is {usr_otp} \n\nPlease Do not share it with anyone..!!\nIf you didn't requested to login, you can safely ignore this email..!!\n\nYou may be required to register with the Site. You agree to keep your password confidential and will be responsible for all use of your account and password. We reserve the right to remove, reclaim, or change a username you select if we determine, in our sole discretion, that such username is inappropriate, obscene, or otherwise objectionable. \n\nAlgo99\nDelhi Technological University \nDelhi, India \nalgo99.sudhanshu@gmail.com"
            send_mail(
                "Welcome to algo99 -Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [myuser.email],
                fail_silently=False
            )
            messages.success(request, "OTP is sent to your email..!!!")

            return render(request, "shop/login.html", {'otp': True, 'usr': myuser})
        else:
            user=authenticate(username= loginusername, password= loginpassword)
            if user is not None:
                login(request,user)
                return redirect("index")
            else:
                messages.error(request, "Invalid credentials! Please try again")
                return redirect("signup")
    return render(request, "shop/login.html")

def handleLogout(request):
    logout(request)
    return redirect('/')




def resendOTP(request):

    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)

            mess = f"Hello {get_usr} \n\nYour OTP is {usr_otp} \n\nPlease Do not share it with anyone..!!\nIf you didn't requested to login, you can safely ignore this email..!!\n\nYou may be required to register with the Site. You agree to keep your password confidential and will be responsible for all use of your account and password. We reserve the right to remove, reclaim, or change a username you select if we determine, in our sole discretion, that such username is inappropriate, obscene, or otherwise objectionable. \n\nAlgo99\nDelhi Technological University \nDelhi, India \nalgo99.sudhanshu@gmail.com"
            send_mail(
                "Welcome to algo99 -Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            
            print("hii")
            messages.success(request, "OTP is sent to your email..!!!")
            return HttpResponse("Resend")
    return HttpResponse("Can't Send")
