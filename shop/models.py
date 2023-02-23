
from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.contrib.auth.models import User
import random
import string



class admin_info(models.Model):

    username_main=models.CharField(max_length=10,default="admin")
    admin_api_keys=models.CharField(max_length=10,default="NA")
    admin_client_id=models.CharField(max_length=100,default='NA')
    admin_password=models.CharField(max_length=100,default='NA')
    admin_token=models.CharField(max_length=100,default='NA')
    expirydate=models.CharField(max_length=100,default='DDMMMYY')



class User1(models.Model):

    username=models.CharField(max_length=50,default='NA')
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=25)
    phone=models.IntegerField(default='999')
    fullname=models.CharField(max_length=50,default='NA')

    # Angel api keys
    angel_api_keys=models.CharField(max_length=100,default='NA')
    angel_client_id=models.CharField(max_length=100,default='NA')
    angel_password=models.CharField(max_length=100,default='NA')
    angel_token=models.CharField(max_length=100,default='NA')

    profits=models.FloatField(default=0)
    Total_transaction=models.FloatField(default=0)
    Total_invested=models.FloatField(default=0)




class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()

class strategy(models.Model):
    strategy_name=models.CharField(max_length=30,default="NA")




class positions(models.Model):

    strategy_name=models.CharField(max_length=200,default='NA')
    symbol=models.CharField(max_length=20,default='NA')
    time_in=models.DateTimeField(auto_now_add = True)
    price_in=models.FloatField(default=0)
    side = models.CharField(max_length=20,default='NA')
    current_price=models.FloatField(default=0)
    time_out=models.DateTimeField(default=0)
    price_out=models.FloatField(default=0)
    status=models.CharField(max_length=20,default='NA') #OPEN, CLOSE
    token=models.CharField(max_length=20,default='NA')
    pnl=models.FloatField(default=0)
    
    stoploss=models.FloatField(default=0)
    takeprofit_1=models.FloatField(default=0)
    takeprofit_2=models.FloatField(default=0)
    strategy1_status=models.CharField(default="OPEN",max_length=100)

class positions_userwise(models.Model):

    username=models.CharField(max_length=20,default='NA')
    strategy_name=models.CharField(max_length=200,default='NA')
    symbol=models.CharField(max_length=20,default='NA')
    time_in=models.DateTimeField(auto_now_add = True)
    price_in=models.FloatField(default=0)
    side = models.CharField(max_length=20,default='NA')
    current_price=models.FloatField(default=0)
    time_out=models.DateTimeField(default=0)
    price_out=models.FloatField(default=0)
    status=models.CharField(max_length=20,default='NA')
    token=models.CharField(max_length=20,default='NA')
    quantity=models.IntegerField(default=1)
    pnl=models.FloatField(default=0)


class subscriptions(models.Model):

    username=models.CharField(max_length=20,default='NA')
    strategy_name=models.CharField(max_length=200,default='NA')
    symbols=models.CharField(max_length=2000,default='NA')
    status=models.CharField(max_length=20,default='off')
    quantity=models.IntegerField(default=1)



