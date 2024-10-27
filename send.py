import serial
from homeassistant.components.sensor import SensorEntity

from .const import BAUDRATE , GRYF_OUT_NAME

ser = None
sensorEntity = []

def setupPlatform(async_add_entities):
    global sensorEntity

    sensorEntity.append(SendSensor())

    async_add_entities(sensorEntity)

def setup_serial(port):
    global ser
    
    ser = serial.Serial(port, BAUDRATE, timeout=1)

def send_command(command):
    if ser: 
            try:
                full_command = command + "\r\n"
                ser.write(full_command.encode('utf-8'))
                sensorEntity[0].set_new_state(command)
            except Exception as e:
                print(f"Error sending command: {e}")

class SendSensor(SensorEntity):

    def __init__(self) -> None:
        self._state = None
        self._name = GRYF_OUT_NAME

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def get_id(self):
        return self._id
    
    @property
    def get_pin(self):
        return self._pin

    def set_new_state(self, state) -> None:
        self._state = state
        self.async_write_ha_state()