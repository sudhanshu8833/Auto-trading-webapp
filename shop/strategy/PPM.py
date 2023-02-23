from shop.models import *
from datetime import datetime,time
from pytz import timezone
import ast
import pandas as pd
import pyotp
from smartapi import SmartConnect

import traceback
import logging
logger = logging.getLogger('dev_log')


def start_class_PPM(json_data):

    try:
        strategy=run_PPM(json_data)
        strategy.trigger_PPM()


    except Exception:
        logger.info(traceback.format_exc())

class run_PPM():

    def __init__(self,json_data):

        self.json_data=json_data
        self.token={}
        self.calculate_tokens()
        self.login()

    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.admin_api_keys)
        self.obj.generateSession(admin.admin_client_id,admin.admin_password,pyotp.TOTP(admin.admin_token).now())



    def calculate_tokens(self):
        df = pd.read_csv('shop/strategy/scripts.csv')

        for i in range(len(df)):

            if self.json_data["stocks"]+'-EQ' ==df['symbol'][i]:
                self.token[str(df['symbol'][i])] = str(df['token'][i])



    def close_position(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)

        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="CLOSED"
            users_opened_positions[i].price_out=float(self.json_data['trigger_price'])
            users_opened_positions[i].current_price=float(self.json_data['trigger_price'])
            users_opened_positions[i].time_out=datetime.now(timezone("Asia/Kolkata"))
            self.create_real_orders(users_opened_positions[i],"CLOSE")
            users_opened_positions[i].save()

        data.price_out=float(self.json_data['trigger_price'])
        data.current_price=float(self.json_data['trigger_price'])
        data.time_out=datetime.now(timezone("Asia/Kolkata"))
        data.status="CLOSED"
        data.save()


    def _updated_market_order(self):

        if self.json_data["triggered_type"]=="sell":
            order_type="sell"
            opened_positions=positions.objects.filter(strategy_name="PPM",status="OPEN")

            for j in range(len(opened_positions)):
                if self.json_data["stocks"]==opened_positions[j].symbol:
                    if opened_positions[j].side=="sell":
                        return "NA"


                    else:
                        self.close_position(opened_positions[j])
                        




        elif self.json_data["triggered_type"]=="buy":
            order_type="buy"
            opened_positions=positions.objects.filter(strategy_name="PPM",status="OPEN")

            for j in range(len(opened_positions)):
                if self.json_data["stocks"]==opened_positions[j].symbol:
                    if opened_positions[j].side=="buy":
                        return "NA"


                    else:
                        self.close_position(opened_positions[j])
                        

        stock_data=self.obj.ltpData("NSE",self.json_data["stocks"]+'-EQ' ,self.token[self.json_data["stocks"]+'-EQ'])['data']

        position=positions(strategy_name="PPM",
                    symbol=self.json_data["stocks"],
                    time_in=self.json_data['triggered_at'],
                    price_in=self.json_data["trigger_price"],
                    side=order_type,
                    current_price=stock_data['ltp'],
                    time_out=self.json_data['triggered_at'],
                    price_out=0,
                    status='OPEN',
                    token=self.token[self.json_data["stocks"]+'-EQ'],
                    pnl=0
                    )
        position.save()


        subs=subscriptions.objects.filter(strategy_name="PPM",status="on")

        for i in range(len(subs)):
            user_symbols = subs[i].symbols.split(',')
            for j in range(len(user_symbols)):
                if user_symbols[j]==self.json_data["stocks"]:
                    user_position=positions_userwise(username=subs[i].username,
                                                    strategy_name="PPM",
                                                    symbol=self.json_data["stocks"],
                                                    time_in=self.json_data['triggered_at'],
                                                    price_in=self.json_data["trigger_price"],
                                                    side=order_type,
                                                    current_price=stock_data['ltp'],
                                                    time_out=self.json_data['triggered_at'],
                                                    price_out=0,
                                                    status='OPEN',
                                                    token=self.token[self.json_data["stocks"]+'-EQ'],
                                                    pnl=0
                    )
                    self.create_real_orders(user_position,"OPEN")
                    user_position.save()


    def create_real_orders(self,data,type):

        try:
            if type=="CLOSE":
                if data.side=="buy":
                    data.side="sell"
                else:
                    data.side="buy"

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

            orderId = user_obj.placeOrder(orderparams)
            logger.info("The order id is: {}".format(orderId))

        except Exception:
            # logger.info(traceback.format_exc())
            pass


    def trigger_PPM(self):
        self._updated_market_order()
