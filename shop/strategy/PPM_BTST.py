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


def start_class_PPM_BTST(json_data):

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

    def calculate_tokens(self):
        df = pd.read_csv('shop/strategy/scripts.csv')

        for i in range(len(df)):

            if self.json_data["stocks"]+'-EQ' ==df['symbol'][i]:
                self.token[str(df['symbol'][i])] = str(df['token'][i])

    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.admin_api_keys)
        self.obj.generateSession(admin.admin_client_id,admin.admin_password,pyotp.TOTP(admin.admin_token).now())

    def _updated_market_order(self):
        pos=positions.objects.filter(strategy_name="PPM BTST",status="OPEN",side=self.json_data['triggered type'],symbol=self.json_data['stocks'])

        if pos.exists():
            return "Already a position exists"
        
        else:
            position=positions(strategy_name="PPM BTST",
                        symbol=self.json_data["stocks"],
                        time_in=self.json_data['triggered_at'],
                        price_in=self.json_data["trigger_price"],
                        side=self.json_data['triggered_type'],
                        current_price=self.json_data["trigger_price"],
                        time_out=self.json_data['triggered_at'],
                        price_out=0,
                        status='OPEN',
                        token=self.token[self.json_data["stocks"]+'-EQ'],
                        pnl=0
                        )
            position.save()

            subs=subscriptions.objects.filter(strategy_name="PPM BTST",status="on")

            for i in range(len(subs)):
                user_symbols = subs[i].symbols.split(',')

                for j in range(len(user_symbols)):
                    if user_symbols[j]==self.json_data["stocks"]:
                        user_position=positions_userwise(username=subs[i].username,
                                                        strategy_name="PPM BTST",
                                                        symbol=self.json_data["stocks"],
                                                        time_in=self.json_data['triggered_at'],
                                                        price_in=self.json_data["trigger_price"],
                                                        side=self.json_data['triggered_type'],
                                                        current_price=self.json_data["trigger_price"],
                                                        time_out=self.json_data['triggered_at'],
                                                        price_out=0,
                                                        status='OPEN',
                                                        token=self.token[self.json_data["stocks"]+'-EQ'],
                                                        pnl=0,
                                                        quantity=int(subs[i].quanity)
                        )
                        self.create_real_orders(user_position,"OPEN")
                        user_position.save()
                        break

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
            logger.info(traceback.format_exc())

    def trigger_PPM(self):
        self._updated_market_order()

