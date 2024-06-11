from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError
import subprocess

# Данный файл-модуль является костылем для получения данных с датчика Xiaomi Mijia (LYWSD03MMC)
# char-write-req 0x0038 0100 для включения нотификации
# В будущем переход на более надежный DHT22

def restart_bluetooth_service():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'bluetooth'], check=True)
    except subprocess.CalledProcessError as e:
        pass


class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.temperature = 0
        self.humidity = 0
        self.battery_level = 0

    def handleNotification(self, cHandle, data):
        self.temperature = int.from_bytes(data[:2], byteorder='little', signed=False) / 100.0
        self.humidity = data[2]
        self.battery_level = int.from_bytes(data[3:], byteorder='little', signed=False) / 1000


Room_device_address = "A4:C1:38:95:D6:32"
Box_device_addres = "A4:C1:38:25:BB:92"

notification_delegate = NotificationDelegate()


def get_mi_sensor_data(timeout=10.0):
    device = None
    try:
        device = Peripheral()
        if device.addrType == None:
            device.connect(Box_device_addres)
        device.setDelegate(notification_delegate)
        if device.waitForNotifications(timeout):
            return notification_delegate.temperature, notification_delegate.humidity, notification_delegate.battery_level

    except BTLEDisconnectError as e:
        temperature = "🛑"
        humidity = "🛑"
        battery_level = "🛑"
        restart_bluetooth_service()
        return temperature, humidity, battery_level

    finally:
        if device:
            device.disconnect()


'''
temperature, humidity, battery_level = get_sensor_data()
print(f"Temperature: {temperature} 'C")
print(f"Humidity: {humidity} %")
print(f"Battery Level: {battery_level} m.volt")
'''
