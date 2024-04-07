#Libraries
import board
import Adafruit_DHT as adafruit
from time import sleep

#Set sensor
DHT = adafruit.DHT22(board.D4)

def get_dht_data():
    # Print the values to the serial port
    temperature_c = DHT.temperature
    temperature_f = temperature_c * (9 / 5) + 32
    humidity = DHT.humidity
    print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))
    return temperature_c, humidity






