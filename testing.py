# from smartapi import SmartConnect
# import pyotp
# obj=SmartConnect(api_key="7QRXAUNi")
# print(pyotp.TOTP("NYE52I73HJUB73CBB2EJ4LZEPU").now())


# data = obj.generateSession("P81389","8788",pyotp.TOTP("NYE52I73HJUB73CBB2EJ4LZEPU").now())
# print(data)
# refreshToken= data['data']['refreshToken']
# obj.ltpData("NSE",'INFY-EQ' ,)['data']['ltp']


i=0
stocks=['A','b','C']

for i in range(len(stocks)):
    
    if i==1:
        del stocks[i]

    print(stocks,i)