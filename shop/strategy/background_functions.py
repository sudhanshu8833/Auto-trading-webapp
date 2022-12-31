import requests
import pandas as pd

def this_scripts():

    url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    print(url)
    data=requests.get(url=url)
    print(url)
    data=data.json()
    df = pd.DataFrame(data)

    df1=df[:1]

    # for i in range(len(df)):
    #     print(i)

    #     if 'NIFTY' in df['symbol'][i][:6] and 'NFO' in df['exch_seg'][i]:
    #         df1.loc[len(df1.index)] = df.loc[i] 
    #     else:
    #         continue
    # print(df)

    df1.to_csv("shop/strategy/scripts.csv")