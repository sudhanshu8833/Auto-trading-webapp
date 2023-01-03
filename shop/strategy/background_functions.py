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

    for i in range(len(df)):
        print(i)

        if '-EQ' in df['symbol'][i] and 'NSE' in df['exch_seg'][i]:
            df1.loc[len(df1.index)] = df.loc[i] 
        else:
            continue


    df1.to_csv("scripts.csv")


if __name__=="__main__":
    this_scripts()