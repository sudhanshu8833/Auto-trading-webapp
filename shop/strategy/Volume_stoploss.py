from shop.models import *
from datetime import datetime,time
from django.forms.models import model_to_dict
import pyotp
from smartapi import SmartConnect

from pytz import timezone
import ast
import pandas as pd

import traceback
import logging
logger = logging.getLogger('dev_log')


def start_stoploss_for_volume():
    try:
        strategy=run_volume()
        strategy.main()
    except Exception:
        logger.info(traceback.format_exc())


class run_volume():

    def __init__(self):

        self.login()
        self.logged_error=[]
    
    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.admin_api_keys)
        self.obj.generateSession(admin.admin_client_id,admin.admin_password,pyotp.TOTP(admin.admin_token).now())


    def update_ltp(self):
        opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
        opened_positions1=positions.objects.filter(strategy_name="Volume Based Intraday",status="PARTIAL_CLOSE")
        opened_positions=opened_positions | opened_positions1
        
        for i in range(len(opened_positions)):
            ltp=self.obj.ltpData("NSE",opened_positions[i].symbol+'-EQ' ,opened_positions[i].token)['data']['ltp']
            opened_positions[i].current_price=ltp
            opened_positions[i].save()
            
            user_opened_positions=positions_userwise.objects.filter(strategy_name="Volume Based Intraday",status="OPEN",symbol=opened_positions[i].symbol)
            for j in range(len(user_opened_positions)):
                user_opened_positions[j].current_price=ltp
                user_opened_positions[j].save()

    def close_position(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)
        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="CLOSED"
            users_opened_positions[i].price_out=round(float(data.current_price),2)
            users_opened_positions[i].time_out=datetime.now(timezone("Asia/Kolkata"))
            users_opened_positions[i].pnl=data.pnl
            self.create_real_orders(users_opened_positions[i],"CLOSE",0,data)
            users_opened_positions[i].save()
            
        data.price_out=data.current_price
        data.time_out=datetime.now(timezone("Asia/Kolkata"))
        data.status="CLOSED"
        data.save()

    def partial_close(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)
        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="PARTIAL_CLOSE"

            self.create_real_orders(users_opened_positions[i],"PARTIAL_CLOSE",int(users_opened_positions[i].quantity)-int(users_opened_positions[i].quantity)/2,data)
            users_opened_positions[i].quantity/=2
            
            users_opened_positions[i].save()

        data.status="PARTIAL_CLOSE"
        data.strategy1_status="CLOSE"
        data.save()

    def check_updates(self):
        opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
        opened_positions1=positions.objects.filter(strategy_name="Volume Based Intraday",status="PARTIAL_CLOSE")
        opened_positions=opened_positions | opened_positions1

        for i in range(len(opened_positions)):
            
            if opened_positions[i].side=="buy":
                if opened_positions[i].current_price <= opened_positions[i].stoploss:
                    self.close_position(opened_positions[i])

                elif opened_positions[i].status=="OPEN" and opened_positions[i].current_price >= opened_positions[i].takeprofit_1:
                    self.partial_close(opened_positions[i])
                    opened_positions[i].status="PARTIAL_CLOSE"
                    opened_positions[i].save()

                elif (opened_positions[i].status=="PARTIAL_CLOSE" or opened_positions[i].status=="OPEN") and opened_positions[i].current_price >= opened_positions[i].takeprofit_2:
                    self.close_position(opened_positions[i])

            if opened_positions[i].side=="sell":
                if opened_positions[i].current_price >= opened_positions[i].stoploss:
                    self.close_position(opened_positions[i])

                elif opened_positions[i].status=="OPEN" and opened_positions[i].current_price <= opened_positions[i].takeprofit_1:
                    self.partial_close(opened_positions[i])

                elif (opened_positions[i].status=="PARTIAL_CLOSE" or opened_positions[i].status=="OPEN") and opened_positions[i].current_price <= opened_positions[i].takeprofit_2:
                    self.close_position(opened_positions[i])


    def create_real_orders(self,data,type,quantity,position_info):

        try:
            if type=="CLOSE" or type=="PARTIAL_CLOSE":
                if data.side=="buy":
                    data.side="sell"
                else:
                    data.side="buy"

            if type=="PARTIAL_CLOSE":
                data.quantity=quantity


            user=User1.objects.get(username=data.username)

            user_obj=SmartConnect(api_key=user.angel_api_keys)
            user_obj.generateSession(user.angel_client_id,user.angel_password,pyotp.TOTP(user.angel_token).now())

            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": str(data.symbol)+'-EQ',
                "symboltoken": str(data.token),
                "transactiontype": str((data.side).upper()),
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "quantity": str(int(data.quantity)),
            }


            orderId = user_obj.placeOrder(orderparams)\

            try:
                logger.info("The order id is: {}: {}: {}: {}".format(orderId,type, orderparams, model_to_dict(position_info)))
            except:
                logger.info("The order id is: {}: {}: {}".format(orderId,type, orderparams))
        except Exception:
            logger.info(traceback.format_exc())



    def main(self):
            logger.info("started")
            while True:

                if time(15, 20) <= datetime.now(timezone("Asia/Kolkata")).time():
                    opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
                    opened_positions1=positions.objects.filter(strategy_name="Volume Based Intraday",status="PARTIAL_CLOSE")
                    opened_positions=opened_positions| opened_positions1
                    for i in range(len(opened_positions)):
                        self.close_position(opened_positions[i])

                else:
                    self.update_ltp()
                    self.check_updates()


