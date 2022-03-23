# Webhooker

Webhooker (enviador de señales), es un pequeño programa que se encargaba de hacer de "core" de una estrategia de trading para Binance Futuros, recibía cada hora una señal de TradingView(ya que al principio a parte de una señal cada hora mandaba ciertos valores con Trading View; el repositorio oficial con todos los commits no lo dejo público porque contiene Keys que no debo de compartir.

Ahora mismo, la actualización que haría sería en lugar de tener que fiarse del aviso de cada hora de trading view, usar una funcion como esta dentro de un bucle infinito.

```
def wait():
    time_now = datetime.utcnow()
    minute_now  = str(time_now.minute)
    second_now = int(time_now.second)

    hour = 60
    minute = 60

    minutes = hour - int(minute_now) -1
    seconds = minute - int(second_now)


    sleep = (minutes*60) + seconds

    print("El bot debe de esperar 1 hora")

    time.sleep(sleep)

```

¡ATENCIÓN! Esta estrategia no es recomendada para su uso ya que no es 100% viable.


