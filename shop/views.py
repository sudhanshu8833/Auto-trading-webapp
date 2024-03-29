
from .views_scripts.helpful import *
from .views_scripts.additional import *
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .strategy.Volume import *
from .strategy.PPM import *
from .strategy.PPM_BTST import *
from .strategy.Volume_stoploss import *
# Create your views here.

from django.contrib.auth.decorators import login_required
from .models import User1

from django.conf import settings
import json
import threading


def start_thread(request):
    try:
        logger.info("testing about the cron")
        # start_stoploss_for_volume()
        t = threading.Thread(target=start_stoploss_for_volume, args=[])
        t.setDaemon(True)
        t.start()

        return HttpResponse("thread started")
    except Exception as e:
        logger.info(str(traceback.format_exc()))


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


    try:
        data=request.data
        url = request.get_full_path()

        # logger.info(str(url))
        logger.info(data)
        if request.method == "POST":
            if "scan_name" in data:
                
                start_class_volume(data)
                # start_stoploss_for_volume()



            else:
                if "System" in data:
                    if data["System"]=="PPM":
                        start_class_PPM(data)

                    if data['System']=="PPM BTST" and datetime.datetime.now().time().hour>=15:
                        start_class_PPM_BTST(data)


        return Response(data)

    except Exception:
        logger.info(traceback.format_exc())
        return Response(traceback.format_exc())
