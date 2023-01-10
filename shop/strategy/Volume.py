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


def start_class_volume(json_data):
    try:
        strategy=run_volume(json_data)
        strategy.trigger_volume()
    except Exception:
        logger.info(traceback.format_exc())

class run_volume():

    def __init__(self,json_data):
        self.json_data=json_data
        self.token={}
        self.calculate_tokens()
        self.login()
        self.logged_error=set()

    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.admin_api_keys)
        self.obj.generateSession(admin.admin_client_id,admin.admin_password,pyotp.TOTP(admin.admin_token).now())



    def calculate_tokens(self):
        df = pd.read_csv('shop/strategy/scripts.csv')

        stocks=self.json_data["stocks"]
        stocks = stocks.split(',')

        for i in range(len(df)):
            for j in range(len(stocks)):
                print(i)
                if stocks[j]+'-EQ' ==df['symbol'][i]:
                    self.token[str(df['symbol'][i])] = str(df['token'][i])


    def close_position(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)

        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="CLOSED"
            self.create_real_orders(users_opened_positions[i],"CLOSE")
            users_opened_positions[i].save()

        data.status="CLOSED"
        data.save()


    def _updated_market_order(self):

        stocks=self.json_data["stocks"]
        stocks = stocks.split(',')

        trigger_prices=self.json_data["trigger_prices"]
        trigger_prices = trigger_prices.split(',')

        for i in range(len(stocks)):
            if '0pen_H!gh' in self.json_data.values():
                order_type="buy"
                opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
                # stock_list_open=opened_positions.values_list("symbol")
                
                for j in range(len(opened_positions)):
                    if stocks[i]==opened_positions[j].symbol:
                        if opened_positions[j].side=="sell":

                            self.close_position(opened_positions[j])
                            stocks[i]="-NA"
                            trigger_prices[i]="-NA"

                            break

                        else:
                            stocks[i]="-NA"
                            trigger_prices[i]="-NA"

                            break




            else:
                order_type="sell"
                opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
                # stock_list_open=opened_positions.values_list("symbol")
                
                for j in range(len(opened_positions)):
                    if stocks[i]==opened_positions[j].symbol:
                        if opened_positions[j].side=="buy":

                            self.close_position(opened_positions[j])
                            stocks[i]="-NA"
                            trigger_prices[i]="-NA"
                            break

                        else:
                            stocks[i]="-NA"
                            trigger_prices[i]="-NA"
                            break


        for i in range(len(stocks)):
            if (stocks[i]=="-NA"):
                continue
            stock_data=self.obj.ltpData("NSE",stocks[i]+'-EQ' ,self.token[stocks[i]+'-EQ'])['data']

            if order_type=="buy":
                stoploss=float(stock_data['low'])*(1-.0003)
                takeprofit_1=float(stock_data['ltp'])*(1+.0033)
                takeprofit_2=float(stock_data['ltp'])*(1+.0066)

            else:
                stoploss=float(stock_data['high'])*(1+.0003)
                takeprofit_1=float(stock_data['ltp'])*(1-.0033)
                takeprofit_2=float(stock_data['ltp'])*(1-.0066)

            position=positions(strategy_name="Volume Based Intraday",
                        symbol=stocks[i],
                        time_in=datetime.now(timezone("Asia/Kolkata")),
                        price_in=trigger_prices[i],
                        side=order_type,
                        current_price=stock_data['ltp'],
                        time_out=datetime.now(timezone("Asia/Kolkata")),
                        price_out=0,
                        status='OPEN',
                        token=self.token[user_symbols[j]+'-EQ'],
                        pnl=0,
                        stoploss=stoploss,
                        takeprofit_1=takeprofit_1,
                        takeprofit_2=takeprofit_2
                        )
            position.save()


        subs=subscriptions.objects.filter(strategy_name="Volume Based Intraday",status="on")

        for i in range(len(subs)):
            user_symbols = subs[i].symbols.split(',')

            for j in range(len(user_symbols)):
                if user_symbols[j] in stocks:
                    user_position=positions_userwise(username=subs[i].username,
                        strategy_name="Volume Based Intraday",
                        symbol=user_symbols[j],
                        time_in=datetime.now(timezone("Asia/Kolkata")),
                        price_in=trigger_prices[i],
                        side=order_type,
                        current_price=0,
                        quantity=subs[i].quantity,
                        time_out=datetime.now(timezone("Asia/Kolkata")),
                        price_out=0,
                        status='OPEN',
                        token=self.token[user_symbols[j]+'-EQ'],
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
            logger.info(traceback.format_exc())


    def trigger_volume(self):
        self._updated_market_order()

