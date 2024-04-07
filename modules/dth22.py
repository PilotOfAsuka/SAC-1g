#Libraries
import RPi.GPIO as GPIO
import Adafruit_DHT as dht


# Set DATA pin
DHT = 23


def get_dht_data():
    try:
        GPIO.cleanup()
        h, t = dht.read_retry(dht.DHT22, DHT)
        return round(t, 1), round(h, 1)
    except TypeError:
        return 0, 0





