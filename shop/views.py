
from .views_scripts.helpful import *
from .views_scripts.additional import *


from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .strategy.Volume import *
from .strategy.PPM import *
from .strategy.Volume_stoploss import *
# Create your views here.

from django.contrib.auth.decorators import login_required
from .models import User1

from django.conf import settings
import json
import threading





@login_required(login_url='/signup')
def key(request):
    current_user = request.user
    if request.method == "POST":

        angelapi = request.POST['api']
        angelid = request.POST['client']
        angelpassword = request.POST['pass']
        token = request.POST['token']

        myuser = User1.objects.get(username=current_user)



        myuser.angel_api_keys = angelapi
        myuser.angel_client_id = angelid
        myuser.angel_password = angelpassword
        myuser.angel_token = token
        myuser.save()
        messages.success(request, "Successfully Added/Changed Angel Keys")
        return redirect('index')

        messages.error(request, "some problem occured ..!!")
        return redirect('index')




@api_view(["POST","GET"]) #allowed methods
def webhook_alert(request):
    data=request.data

    if request.method == "POST":
        if "scan_name" in data:
            
            start_class_volume(data)
            # start_stoploss_for_volume()

        

        else:
            if "System" in data:
                if data["System"]=="PPM":
                    start_class_PPM(data)



    return Response(data)
