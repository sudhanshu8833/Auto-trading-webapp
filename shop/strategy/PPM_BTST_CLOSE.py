
import logging
from shop.models import *
import os
import traceback
from smartapi import SmartConnect
import pyotp


logger = logging.getLogger('dev_log')

def close_position_for_ppm_btst():
    try:
        strategy=PPM_BTST_CLOSE()
        strategy.PPM_BTST()
    except Exception:
        logger.info(traceback.format_exc())


class PPM_BTST_CLOSE():

    def __init__(self):
        self.login()


    def login(self):
        admin=admin_info.objects.get(username_main="admin")
        self.obj=SmartConnect(api_key=admin.admin_api_keys)
        self.obj.generateSession(admin.admin_client_id,admin.admin_password,pyotp.TOTP(admin.admin_token).now())



    def close_real_orders(self,data,type):

        try:

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


    def PPM_BTST(self):
        pos=positions_userwise.objects.filter(strategy_name="PPM BTST",status="OPEN")

        for i in range(len(pos)):
            stock_data=self.obj.ltpData("NSE",pos[i].symbol,pos[i].token)['data']

            self.close_real_orders(pos[i],pos[i].side)
            pos[i].status='CLOSED'
            pos[i].price_out=int(stock_data)
            pos[i].current_price=int(stock_data)
            pos[i].save()