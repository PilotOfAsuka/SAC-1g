#Libraries
import Adafruit_DHT as dht
from time import sleep

#Set DATA pin
DHT = 4

def get_dht_data():
    h, t = dht.read_retry(dht.DHT22, DHT)
    return round(t, 1), round(h, 1)






