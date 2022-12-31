from models import *
from datetime import datetime,time

import pyotp
from smartapi import SmartConnect

from pytz import timezone
import ast
import pandas as pd

def start_stoploss_for_volume():
    strategy=run_volume()
    strategy.main()

class run_volume():

    def __init__(self):
        self.login()
    
    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.angel_api_keys)
        self.obj.generateSession(admin.angel_client_id,admin.angel_password,pyotp.TOTP(admin.angel_token).now())


    def update_ltp(self):
        opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")

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
            users_opened_positions[i].save()

        data.status="CLOSED"
        data.save()

    def partial_close(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)
        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="PARTIAL_CLOSE"
            users_opened_positions[i].quantity/=2
            users_opened_positions[i].save()

        data.status="PARTIAL_CLOSE"
        data.save()

    def check_updates(self):
        opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")

        for i in range(len(opened_positions)):
            
            if opened_positions[i].side=="buy":
                if opened_positions[i].current_price <= opened_positions[i].stoploss:
                    self.close_position(opened_positions[i])

                elif opened_positions[i].strategy1_status=="OPEN" and opened_positions[i].current_price >= opened_positions[i].takeprofit_1:
                    self.partial_close(opened_positions[i])

                elif (opened_positions[i].strategy1_status=="PARTIAL_CLOSE" or opened_positions[i].strategy1_status=="OPEN") and opened_positions[i].current_price >= opened_positions[i].takeprofit_2:
                    self.close_position(opened_positions[i])

            if opened_positions[i].side=="sell":
                if opened_positions[i].current_price >= opened_positions[i].stoploss:
                    self.close_position(opened_positions[i])

                elif opened_positions[i].strategy1_status=="OPEN" and opened_positions[i].current_price <= opened_positions[i].takeprofit_1:
                    self.partial_close(opened_positions[i])

                elif (opened_positions[i].strategy1_status=="PARTIAL_CLOSE" or opened_positions[i].strategy1_status=="OPEN") and opened_positions[i].current_price <= opened_positions[i].takeprofit_2:
                    self.close_position(opened_positions[i])


    def main(self):
        while True:
            
            if time(3, 20) <= datetime.now(timezone("Asia/Kolkata")).time():
                opened_positions=positions.objects.filter(strategy_name="Volume Based Intraday",status="OPEN")
                for i in range(len(opened_positions)):
                    self.close_position(opened_positions[i])

            else:
                self.update_ltp()
                self.check_updates()