from homeassistant.components.cover import CoverEntity
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING
import serial

covers = []

async def new_rols_command(parsed_states):
    if covers:
        for i in range(len(covers)):
            if str(covers[i].get_id) == parsed_states[0]:
                covers[i].changeRolState(parsed_states)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info or []

    for cover in cover_config:
        name = cover.get("name")
        cover_id = cover.get("id")
        pin = cover.get("pin")
        time = cover.get("time")
        covers.append(Cover(hass, name, cover_id, pin, time))

    async_add_entities(covers)

class Cover(CoverEntity):
    def __init__(self, hass, name, cover_id, pin, time):
        """Inicjalizacja instancji cover"""
        self._name = name
        self._pin = pin
        self._id = cover_id
        self._state = STATE_CLOSED
        self._is_opening = False
        self._is_closing = False
        self._position = None 
        self._time = time
        self.serial_port = "/dev/ttyS0"
        self.baudrate = 115200
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)

    @property
    def name(self):
        """Nazwa urządzenia w Home Assistant"""
        return self._name

    @property
    def current_cover_position(self):
        """Aktualna pozycja osłony w procentach"""
        return self._position

    @property
    def is_opening(self):
        """Czy osłona się otwiera"""
        return self._is_opening

    @property
    def is_closing(self):
        """Czy osłona się zamyka"""
        return self._is_closing

    @property
    def get_id(self):
        return self._id

    @property
    def get_pin(self):
        return self._pin

    @property
    def is_closed(self):
        """Czy osłona jest zamknięta"""
        return self._state == STATE_CLOSED

    @property
    def device_class(self):
        """Typ osłony (np. żaluzje, brama)"""
        return 'window'

    async def changeRolState(parsed_states):
        if parsed_states[self._id] == "0" and self._is_opening:
            self._is_opening = False
            self._state = STATE_OPEN
            self.schedule_update_ha_state()

        if parsed_states[self._id] == "0" and self._is_closing:
            self._is_closing = False
            self._state = STATE_CLOSED
            self.schedule_update_ha_state()

            


    def open_cover(self, **kwargs):
        """Obsługuje otwieranie osłony"""
        self._is_opening = True
        self._is_closing = False
        self._state = STATE_OPENING

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 2
        t1 = self._time
        control = self._id + t1 + sum(states)

        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        self.send_command(command)
        self.schedule_update_ha_state()

    def close_cover(self, **kwargs):
        """Obsługuje zamykanie osłony"""
        self._is_opening = True
        self._is_closing = False
        self._state = STATE_CLOSING

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 1
        t1 = self._time
        control = self._id + t1 + sum(states)

        command = f"AT+SetRol={self._id},{t1},{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        self.send_command(command)
        self.schedule_update_ha_state()

    def stop_cover(self, **kwargs):
        self._is_opening = True
        self._is_closing = False
        self._state = None

        states = [0 , 0 , 0 , 0]
        states[self._pin - 1] = 3
        control = self._id + sum(states)

        command = f"AT+SetRol={self._id},0,{states[0]},{states[1]},{states[2]},{states[3]},{control}"
        self.send_command(command)
        self.schedule_update_ha_state()

    def set_cover_position(self, position, **kwargs):
        """Ustawia osłonę na określoną pozycję"""
        self._position = position
        # Tutaj dodaj logikę do ustawiania pozycji, jeśli urządzenie obsługuje ustawienie pozycji
        self.schedule_update_ha_state()

    @property
    def state(self):
        """Aktualny stan osłony"""
        return self._state

    def send_command(self, command):
        """Wysyła komendę do urządzenia."""
        try:
            full_command = command + "\r"
            self.ser.write(full_command.encode('utf-8'))
        except Exception as e:
            print(f"Error sending command: {e}")
