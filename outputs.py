import serial
from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant

class Outputs(LightEntity):
    """Klasa reprezentująca światło."""

    def __init__(self, hass: HomeAssistant, name, light_id, pin):
        self.hass = hass
        self._name = name
        self._is_on = False
        self._brightness = 255
        self._id = light_id
        self._pin = pin
        self.serial_port = "/dev/ttyS0"
        self.baudrate = 115200
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def extra_state_attributes(self):
        return {
            "id": self._id,
            "pin": self._pin
        }

    @property
    def get_id(self):
        return self._id

    @property
    def get_pin(self):
        return self._pin

    def set_on(self):
        self._is_on = True

    def set_off(self):
        self._is_on = False

    def turn_on(self, **kwargs):
        """Włącza światło."""
        if self._pin > 0:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "1"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            self.send_command(command)

    def turn_off(self, **kwargs):
        """Wyłącza światło."""
        if self._pin > 0:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "2"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            self.send_command(command)

        async def async_toggle(self, **kwargs):
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "1"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            self.send_command(command)

    def send_command(self, command):
        """Wysyła komendę do urządzenia."""
        try:
            full_command = command + "\r"
            self.ser.write(full_command.encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")

    def __del__(self):
        """Zamyka połączenie szeregowe."""
        if self.ser.is_open:
            self.ser.close()
