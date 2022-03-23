import pandas as pd
import numpy as np

import csv
from dateutil.relativedelta import relativedelta
from datetime import datetime
import time, requests, json

from urls import urls

import csv
import math

from binance.enums import *
from binance.client import Client


api_key = "ZI8hWrGFfO5SjupxGngZPdX6qA2Hjx7nsVU7S6UwEmFbmSrcWNGMWbWSCSWA9zxW"
secret_key = "RG7MIqlBIX4d0S3xNVW5IMVxAetAmkpLHDrhU7j0MBvmQ1hJsPHSezJeOzz8duCT"

client = Client(api_key, secret_key, tld='com')

def round_decimals_down(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return np.floor(number)

    factor = 10 ** decimals
    return np.floor(number * factor) / factor



def start(symbol, number):
    # PRimero calcular los candlesticks
    df = pd.DataFrame(client.futures_historical_klines(symbol=symbol, interval="1h", start_str="2021-03-24", end_str=None))

    # crop unnecessary columns
    df = df.iloc[:, :6]
    # ascribe names to columns
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    # convert timestamp to date format and ensure ohlcv are all numeric
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col])
    df.head()

    #Calculate the Short/Fast Exponential Moving Average
    ShortEMA = df.close.ewm(span=4, adjust=False).mean() #AKA Fast moving average
    df['short'] = round_decimals_down(ShortEMA, number)
    #Calculate the Middle Exponential Moving Average
    MiddleEMA = df.close.ewm(span=9, adjust=False).mean() #AKA Middle-Slow moving average
    df['middle'] = round_decimals_down(MiddleEMA, number)
    #Calculate the Long/Slow Exponential Moving Average
    LongEMA = df.close.ewm(span=18, adjust=False).mean() #AKA Slow moving average
    df['long'] = round_decimals_down(LongEMA, number)

    periods = (-2, -1, 1, 2)


    df['bear_fractal']  = pd.Series(np.logical_and.reduce([
    df['high'] > df['high'].shift(period) for period in periods
    ]), index=df.index)

    df['bull_fractal']  = pd.Series(np.logical_and.reduce([
    df['low'] < df['low'].shift(period) for period in periods
    ]), index=df.index)

    n=1
    df = df.head(-n)

    df.to_csv('token.csv', index=False, encoding='utf-8')

# start("SRMUSDT", 4)


def actualizar_csv(symbol, number):
    while True:
        try:
            ##VALORES
            df1 = pd.read_csv('token.csv')
            # Eliminar última línea ya que no se va a cerrar con esos valores:
            n=24
            df1 = df1.head(-n)

            #Definir el tiempo de START
            #last_date = df1['date'].values[-1]
            df1.to_csv('token.csv', index = False, encoding='utf-8')

            last_date = df1['date'].values[-1]
            last_date_form = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')
            new_date = str(last_date_form + relativedelta(minutes=5))

            #PRimero calcular los candlesticks
            df = pd.DataFrame(client.futures_historical_klines(symbol=symbol, interval="1h", start_str=new_date, end_str=None))

            # Eliminar columnas innecesarias
            df = df.iloc[:, :6]
            # # ascribe names to columns
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            # Convertir el tiempo a fecha formateada y asegurar que sea un número
            df['date'] = pd.to_datetime(df['date'], unit='ms')
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col])
            df.head()

            # Merge de los datos viejos y los nuevos
            df = pd.concat([df1,df])

            #Calculate the Short/Fast Exponential Moving Average
            ShortEMA = df.close.ewm(span=4, adjust=False).mean() #AKA Fast moving average
            df['short'] = round_decimals_down(ShortEMA, number)
            #Calculate the Middle Exponential Moving Average
            MiddleEMA = df.close.ewm(span=9, adjust=False).mean() #AKA Middle-Slow moving average
            df['middle'] = round_decimals_down(MiddleEMA, number)
            #Calculate the Long/Slow Exponential Moving Average
            LongEMA = df.close.ewm(span=18, adjust=False).mean() #AKA Slow moving average
            df['long'] = round_decimals_down(LongEMA, number)
            #print(df1)
            #print(df)

            # Fractals
            periods = (-2, -1, 1, 2)

            df['bear_fractal']  = pd.Series(np.logical_and.reduce([
            df['high'] > df['high'].shift(period) for period in periods
            ]), index=df.index)

            df['bull_fractal']  = pd.Series(np.logical_and.reduce([
            df['low'] < df['low'].shift(period) for period in periods
            ]), index=df.index)


            # Actualizar el CSV con los nuevos valores recogidos
            df.to_csv('token.csv', index=False, encoding='utf-8')



            print("CSV Actualizado")

            break

        except Exception as e:
            print(e)
            time.sleep(10)
            actualizar_csv(symbol, number)
            break


def fractals():
    df = pd.read_csv('token.csv')

    #Cuantos lineas hay
    index = df.index
    number_of_rows = len(index)
    rows = int(number_of_rows)

    for n in range(0, rows):
        #Chequear últimos fractales
        fractals_long = pd.read_csv('fr_long.csv')
        fractals_short = pd.read_csv('fr_short.csv')
        last_fr_long = fractals_long['number'].values[-1]
        last_fr_short = fractals_short['number'].values[-1]

        #Bucle para contar a partir del numero del último FRactal
        #FR-Long
        if (n > last_fr_long):
            if df['bull_fractal'].values[n] == True:
                #Valores a mandar
                value_fr_long = df['low'].values[n]
                
                #Añadir a la bd
                FRLong = [value_fr_long,n]
                miFRLcsv = open('fr_long.csv', 'a+')
                writeFRL = csv.writer(miFRLcsv)
                writeFRL.writerow(FRLong)
                miFRLcsv.close()
                

                #Mandar señal
                data_send = {
                    "passhprase": "FR-Long",
                    "value":value_fr_long
                }

                for url in urls:
                    url_use = url[1]
                    r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})
                
                time.sleep(1)


        # FR-Short
        if (n > last_fr_short):
            if df['bear_fractal'].values[n] == True:
                #Valores a mandar
                value_fr_short = df['high'].values[n]

                #Añadir a la bd
                FRShort = [value_fr_short,n]
                miFRScsv = open('fr_short.csv', 'a+')
                writeFRS = csv.writer(miFRScsv)
                writeFRS.writerow(FRShort)
                miFRScsv.close()

                #Mandar señal
                data_send = {
                    "passhprase": "FR-Short",
                    "value":value_fr_short
                }

                for url in urls:
                    url_use = url[1]
                    r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})

                time.sleep(1)


