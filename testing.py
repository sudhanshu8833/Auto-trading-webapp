# from smartapi import SmartConnect
# import pyotp
# obj=SmartConnect(api_key="7QRXAUNi")
# print(pyotp.TOTP("NYE52I73HJUB73CBB2EJ4LZEPU").now())


# data = obj.generateSession("P81389","8788",pyotp.TOTP("NYE52I73HJUB73CBB2EJ4LZEPU").now())
# print(data)
# refreshToken= data['data']['refreshToken']
# obj.ltpData("NSE",'INFY-EQ' ,)['data']['ltp']


logged_errors = set()



while True:

    try:
        print(hello)
    except Exception as e:
        
        if str(e) not in logged_errors:
            print("hello")
        logged_errors.add(str(e))

