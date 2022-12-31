


from .views_scripts.helpful import *
from .views_scripts.additional import *


from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from strategy.Volume import *
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
        brokerr = request.POST['broker']

        if brokerr == "angel":
            angelapi = request.POST['api']
            angelid = request.POST['client']
            angelpassword = request.POST['pass']

            myuser = User1.objects.get(username=current_user)

            # make_object_alpaca(alpacaapi,alpacasecret,uri,myuser.username)

            myuser.angel_api_keys = angelapi
            myuser.angel_client_id = angelid
            myuser.angel_password = angelpassword
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
            # with open("shop/strategy/data_strategy1.json", "w") as f:
            #     # Write the data to the file as JSON
            #     json.dump(data, f)

            start_class(data)
            # t = threading.Thread(target=start_class,args=[data])
            # t.setDaemon(True)
            # t.start()


    return Response(data)
