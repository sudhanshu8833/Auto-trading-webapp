from smartapi import SmartConnect
import pyotp
obj=SmartConnect(api_key="cOuAdu1P")
print(pyotp.TOTP("E6A6M7TCCH2FMY5U3A23FUMXKU").now())


data = obj.generateSession("B400150","Pankaj@278",pyotp.TOTP("E6A6M7TCCH2FMY5U3A23FUMXKU").now())
refreshToken= data['data']['refreshToken']
obj.ltpData("NSE",'INFY-EQ' ,)['data']['ltp']
