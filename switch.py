from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
import serial

switches = []

async def new_switch_command(parsed_states):
    if switches:
        for i in range(len(switches)):
            if str(switches[i].get_id) == parsed_states[0]:
                pin = switches[i].get_pin
                await change_switch_state(i, parsed_states[pin])

async def change_switch_state(light_index, state):
    """Zmiana stanu światła na podstawie danych."""
    entity_id = f"light.{switches[light_index]._name.lower().replace(' ', '_')}"
    if state == "1":
        switches[light_index].turn_on()
    elif state == "0":
        switches[light_index].turn_off()
    
    switches[light_index].async_write_ha_state()

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global switches

    light_config = discovery_info[0] or []
    lock_config = discovery_info[1] or []
    port = discovery_info[2] or []

    for light in light_config:
        name = light.get("name")
        switch_id = light.get("id")
        pin = light.get("pin")
        switches.append(Switch(hass, name, switch_id, pin , 0 , port))

    for lock in lock_config:
        name = lock.get("name")
        switch_id = lock.get("id")
        pin = lock.get("pin")
        switches.append(Switch(hass, name, switch_id, pin , 1 , port))

    async_add_entities(switches)

class Switch(SwitchEntity):
    def __init__(self, hass: HomeAssistant, name, button_id, pin , tp , port):
        self._name = name
        self._is_on = False
        self._id = button_id  
        self._pin = pin
        self.serial_port = port
        self.baudrate = 115200
        self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        self._type = tp

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def icon(self):
        if self._type:
            return "mdi:lock" if self._is_on else "mdi:lock-open-variant"
        else: 
            return "mdi:lightbulb-on" if self._is_on else "mdi:lightbulb-off"

    def turn_on(self, **kwargs):
        states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = "1"
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        self.send_command(command)
        self._is_on = True  

    def turn_off(self, **kwargs):
        states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = "2"
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        self.send_command(command)
        self._is_on = False

    async def async_toggle(self, **kwargs):
        states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = "3"
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        self.send_command(command)

    def send_command(self, command):
        """Wysyła komendę do urządzenia."""
        if self.ser:  # Sprawdza, czy `self.ser` jest zdefiniowane
            try:
                full_command = command + "\r"
                self.ser.write(full_command.encode('ascii'))
            except Exception as e:
                print(f"Error sending command: {e}")
        else:
            print("Serial interface `ser` is not initialized.")

    async def async_turn_on(self, **kwargs):
        states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = "1"
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        self.send_command(command)

    async def async_turn_off(self, **kwargs):
        states_list = ["0", "0", "0", "0", "0", "0"]
        states_list[self._pin - 1] = "2"
        command = f"AT+SetOut={self._id},{','.join(states_list)}"
        self.send_command(command)

    @property
    def get_id(self):  # Dodano @property
        return self._id

    @property
    def get_pin(self):  # Dodano @property
        return self._pin
