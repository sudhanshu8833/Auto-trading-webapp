
from django.contrib.auth.decorators import login_required
from shop.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.views import *
from django.core.mail import send_mail
from django.http import HttpResponse
from shop.helpful_scripts.object import *
from django.contrib.auth import authenticate,  login, logout
from django.conf import settings


def home(request):
    return render(request, "shop/home1.html")


@login_required(login_url='/signup')
def setting(request):
    current_user = request.user
    if request.method == "POST":
        fullname = request.POST['fullname']
        number = request.POST['number']
        ifsc = request.POST['ifsc']
        binanceapi = request.POST['binanceapi']
        binancesecret = request.POST['binancesecret']
        angelapi = request.POST['angelapi']
        angelusername = request.POST['angelusername']
        angelpassword = request.POST['angelpassword']
        myuser = User1.objects.get(username=current_user)
        myuser.fullname = fullname
        myuser.ifsc = ifsc
        myuser.account_num = number
        myuser.binance_API_keys = binanceapi
        myuser.binance_Secret_Keys = binancesecret
        myuser.angel_API_keys = angelapi
        myuser.angel_username = angelusername
        myuser.angel_password = angelpassword
        myuser.save()
        buy1 = None
        try:
            buy1 = BOT1.objects.get(email=current_user.email)
        except:
            pass
        if(buy1):
            buy1.binance_API_keys = binanceapi
            buy1.binance_Secret_Keys = binancesecret
            buy1.save()
        buy2 = None
        try:
            buy2 = BOT2.objects.get(email=current_user.email)
        except:
            pass
        if(buy2):
            buy2.binance_API_keys = binanceapi
            buy2.binance_Secret_Keys = binancesecret
            buy2.save()
        buy3 = None
        try:
            buy3 = BOT3.objects.get(email=current_user.email)
        except:
            pass
        if(buy3):
            buy3.angel_API_keys = angelapi
            buy3.angel_username = angelusername
            buy3.angel_password = angelpassword
        buy4 = None
        try:
            buy4 = BOT4.objects.get(email=current_user.email)
        except:
            pass
        if(buy4):
            buy4.angel_API_keys = angelapi
            buy4.angel_username = angelusername
            buy4.angel_password = angelpassword
        messages.success(request, "Your details added successfully!!")
        return redirect('index')
    myuser = User1.objects.get(username=current_user)
    params = {'myuser': myuser}
    return render(request, "shop/settings.html", params)





def terms(request):
    return render(request, "shop/terms.html")





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

        chars = string.ascii_letters
        size = 40

        user = User1(username=username,
                     email=email,
                     password=password,
                     phone=phone,
                     fullname='XYZ',
                     binance_API_keys='NONE',
                     binance_Secret_Keys='NONE', alpaca_api_keys="NONE",
                     alpaca_secret_keys="NONE",
                     alpaca_base_url="https://app.alpaca.markets", passphrase=random_string_generator(size, chars))

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
    current_user = request.user
    total = []
    # total2 = []
    Buy1 = tradingview_orders.objects.all().filter(username=current_user)
    for i in Buy1:
        total.append(i)
    # print(buy1)
    # params={'zipped':zipped}
    myuser = User1.objects.get(username=current_user)
    print(total)
    params = {'myuser': myuser, 'total': total}
    return render(request, "shop/index.html", params)


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
