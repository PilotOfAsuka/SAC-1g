from bluepy.btle import Peripheral, DefaultDelegate, BTLEDisconnectError


class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.temperature = 0
        self.humidity = 0
        self.battery_level = 0


    def handleNotification(self, cHandle, data):
        self.temperature = str(int.from_bytes(data[:2], byteorder='little', signed=False) / 100.0)
        self.humidity = str(data[2])
        self.battery_level = str(int.from_bytes(data[3:], byteorder='little', signed=False))


device_address = "A4:C1:38:95:D6:32"

notification_delegate = NotificationDelegate()


def get_sensor_data(timeout=10.0):
    device = None
    try:
        device = Peripheral()
        if device.addrType == None:
            device.connect(device_address)
        device.setDelegate(notification_delegate)
        if device.waitForNotifications(timeout):
            return notification_delegate.temperature, notification_delegate.humidity, notification_delegate.battery_level

    except BTLEDisconnectError as e:
        temperature = "🛑"
        humidity = "🛑"
        battery_level = "🛑"
        return temperature, humidity, battery_level

    finally:
        if device:
            device.disconnect()


#  temperature, humidity, battery_level = get_sensor_data()

'''
print(f"Temperature: {temperature} 'C")
print(f"Humidity: {humidity} %")
print(f"Battery Level: {battery_level} m.volt")
'''
