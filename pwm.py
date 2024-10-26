import serial
from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.core import HomeAssistant

class PWM(LightEntity):
    """Klasa reprezentująca światło."""

    def __init__(self, hass: HomeAssistant, name, light_id, pin):
        self.hass = hass
        self._name = name
        self._is_on = False
        self._id = light_id
        self._pin = pin
        self._attr_supported_color_modes = {ColorMode.ONOFF}
        self.serial_port = "/dev/ttyS0"
        self.baudrate = 115200
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        self._brightness = 0

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @property
    def extra_state_attributes(self):
        return {
            "id": self._id,
            "pin": self._pin,
            "brightness": self._brightness
        }

    def turn_on(self, **kwargs):
        """Włącza światło i ustawia jasność."""
        self._is_on = True
        self._brightness = 100
        self.update_pwm()  # Funkcja, która aktualizuje PWM

        command = f"AT+SetLED={self._id},{self._pin},{self._brightness}"
        self.send_command(command)

    def turn_off(self, **kwargs):
        """Wyłącza światło."""
        self._is_on = False
        self._brightness = 0  # Reset brightness when turning off
        self.update_pwm()

        command = f"AT+SetLED={self._id},{self._pin},{self._brightness}"
        self.send_command(command)

    def __del__(self):
        """Zamyka połączenie szeregowe."""
        if self.ser.is_open:
            self.ser.close()

    def send_command(self, command):
        """Wysyła komendę do urządzenia."""
        try:
            full_command = command + "\n\r"
            self.ser.write(full_command.encode('ascii'))
        except Exception as e:
            print(f"Error sending command: {e}")

    def update_pwm(self):
        """Aktualizuje sygnał PWM na podstawie stanu."""

        command = f"AT+SetLED={self._id},{self._pin},{self._brightness}"
        self.send_command(command)

