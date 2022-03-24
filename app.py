from flask import Flask, request, render_template
from dotenv import load_dotenv
#import stripe
from os import getenv
import json, requests, time, csv
import pandas as pd


from datetime import datetime
from function import actualizar_csv, fractals

from urls import urls

app = Flask(__name__)


symbol = "BNBUSDT"
number = 2


@app.route("/")
def index():
        return render_template('index.html')



@app.route("/webhook", methods=["POST"])
def webhook():
    #Receiving the data
    data = json.loads(request.data)
    passhprase = data['passhprase']

    """
    if passhprase == "VOL-Long":
        actualizar_csv(symbol, number)

        df = pd.read_csv('token.csv')
        low = df['low'].values[-2]

        data_send = {
            "passhprase":"VOL-Long",
            "value":low
        }

        for url in urls:
            url_use = url[1]
            r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})

        return{
            "passhprase": passhprase
        }

    if passhprase == "VOL-Short":
        actualizar_csv(symbol, number)

        df = pd.read_csv('token.csv')
        high = df['high'].values[-2]

        data_send = {
            "passhprase":"VOL-Short",
            "value":high
        }

        for url in urls:
            url_use = url[1]
            r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})

        return{
            "passhprase": passhprase
        }
    """

    if passhprase == "check":
        #Actualizamos CSV
        actualizar_csv(symbol, number)

        df = pd.read_csv('token.csv')
        short = df['short'].values[-2]
        middle = df['middle'].values[-2]
        long = df['long'].values[-2]

        close = df['close'].values[-2]


        # Recoger última EMA
        list_emas = pd.read_csv('emas.csv')

        last_ema = list_emas['ema'].values[-1]

        fractals()
        print("fractales chequeados")

        #### Verde - Amarilla - Roja (Long)
        while True:
            if (short > middle) & (middle > long):
                
                if last_ema == "long":
                    fractals()
                    print("fractales chequeados")

                    break

                else:
                    #Recoger bull_fractal
                    fractals_long = pd.read_csv('fr_long.csv')
                    fractal_long = fractals_long['value'].values[-1]

                    data_send = {
                        "passhprase": "LONG",
                        "close": close,
                        "fractal_long":fractal_long
                    }

                    for url in urls:
                        url_use = url[1]
                        r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})

                    print("abierto long")

                    ema = "long"

                    miDato = [ema]
                    miArchivo = open('emas.csv', 'a+')
                    writer = csv.writer(miArchivo)
                    writer.writerow(miDato)
                    miArchivo.close()    

                    time.sleep(2)

                    fractals()
                    print("fractales chequeados")

                    break


            if (long > middle) & (middle > short):

                if last_ema == "short":
                    fractals()
                    print("fractales chequeados")

                    break

                else:
                    fractals_short = pd.read_csv('fr_short.csv')
                    fractal_short = fractals_short['value'].values[-1]

                    data_send = {
                        "passhprase": "SHORT",
                        "close": close,
                        "fractal_short":fractal_short
                    }

                    for url in urls:
                        url_use = url[1]
                        r = requests.post(url_use, data=json.dumps(data_send), headers={'Content-Type': 'application/json'})

                    print("abierto short")
                    
                    ema = "short"

                    miDato = [ema]
                    miArchivo = open('emas.csv', 'a+')
                    writer = csv.writer(miArchivo)
                    writer.writerow(miDato)
                    miArchivo.close()    

                    time.sleep(2)

                    fractals()
                    print("fractales chequeados")


                    break

            ##if ((short > long) & (long > middle)) or ((middle > short) & (short > long)) or ((long > short) & (short > middle)) or((middle > long) & (long > short)):
            else:

                if last_ema == "cruce":
                    fractals()
                    print("fractales chequeados")

                    break

                else:
                    ema = "cruce"

                    miDato = [ema]
                    miArchivo = open('emas.csv', 'a+')
                    writer = csv.writer(miArchivo)
                    writer.writerow(miDato)
                    miArchivo.close()    

                    time.sleep(2)

                    fractals()
                    print("fractales chequeados")

                    break
                
            

        return{
            "passhprase": passhprase
        }



    

if __name__ == '__main__':
    #load_dotenv()
    app.run(debug=True)
