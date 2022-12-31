from models import *
from datetime import datetime,time
from pytz import timezone
import ast
import pandas as pd

def start_class_PPM(json_data):
    strategy=run_PPM(json_data)
    strategy.trigger_PPM()


class run_PPM():

    def __init__(self,json_data):
        self.json_data=json_data
        self.tokens={}
        self.tokens=self.calculate_tokens()

    def calculate_tokens(self):
        df = pd.read_csv('shop/strategy/scripts.csv')

        for i in range(len(df)):

                if self.json_data["stocks"]+'-EQ' == df['symbol'][i]:
                    self.token[str(df['symbol'][i])] = str(df['token'][i])


    def close_position(self,data):

        users_opened_positions=positions_userwise.objects.filter(strategy_name=data.strategy_name,status="OPEN",symbol=data.symbol,side=data.side)

        for i in range(len(users_opened_positions)):
            users_opened_positions[i].status="CLOSED"
            users_opened_positions[i].price_out=float(self.json_data['trigger_price'])
            users_opened_positions[i].current_price=float(self.json_data['trigger_price'])
            users_opened_positions[i].time_out=datetime.now(timezone="Asia/Kolkata")
            users_opened_positions[i].save()

        data.price_out=float(self.json_data['trigger_price'])
        data.current_price=float(self.json_data['trigger_price'])
        data.time_out=datetime.now(timezone="Asia/Kolkata")
        data.status="CLOSED"
        data.save()


    def _updated_market_order(self):



        if self.json_data["triggered_type"]()=="sell":
            order_type="sell"
            opened_positions=positions.objects.filter(strategy_name="PPM",status="OPEN")

            for j in range(len(opened_positions)):
                if self.json_data["stocks"]==opened_positions[j].symbol:
                    if opened_positions[j].side=="sell":
                        return "NA"


                    else:
                        self.close_position(opened_positions[j])
                        return "NA"




        elif self.json_data["triggered_type"]()=="buy":
            order_type="buy"
            opened_positions=positions.objects.filter(strategy_name="PPM",status="OPEN")

            for j in range(len(opened_positions)):
                if self.json_data["stocks"]==opened_positions[j].symbol:
                    if opened_positions[j].side=="buy":
                        return "NA"


                    else:
                        self.close_position(opened_positions[j])
                        return "NA"


        

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
            user_symbols = ast.literal_eval(subs[i].symbols)
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
                    user_position.save()




    def trigger_PPM(self):
        self._updated_market_order()


    # def update_ltp(self):
    #     opened_positions = positions.objects.filter(strategy_name="PPM", status="OPEN")

    #     for i in range(len(opened_positions)):
    #         opened_positions[i].current_price=self.obj.ltpData("NSE",opened_positions[i].symbol+'-EQ' ,opened_positions[i].token)['data']['ltp']
    #         opened_positions[i].save()

