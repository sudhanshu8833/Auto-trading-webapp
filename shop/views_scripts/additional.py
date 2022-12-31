
from django.contrib.auth.decorators import login_required
from shop.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.views import *
from django.core.mail import send_mail
from django.http import HttpResponse
from shop.helpful_scripts.object import *
from django.contrib.auth import authenticate,  login, logout



def about(request):
    return render(request, "shop/about.html")


def contact(request):
    if request.method == "POST":
        # print(request.POST)
        # bot.sendMessage(1039725953, str(request.POST['hello']))
        pass
    return render(request, "shop/contact.html")


def error(request):
    return render(request, "shop/error.html")



@login_required(login_url='/signup')
def add_api(request):
    current_user = request.user
    myuser = User1.objects.get(username=current_user)
    params = {'myuser': myuser}
    return render(request, "shop/add_api_credentials.html", params)