from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
import serial
import time
from .send import send_command
from .const import LOCK_ON_ICON , LOCK_OFF_ICON , LIGHT_ON_ICON , LIGHT_OFF_ICON

switches = []

async def new_switch_command(parsed_states):
    if switches:
        for i in range(len(switches) - 1):
            if str(switches[i].get_id) == parsed_states[0]:
                pin = switches[i].get_pin
                await change_switch_state(i, parsed_states[pin])

async def change_switch_state(light_index, state):
    """Zmiana stanu światła na podstawie danych."""
    entity_id = f"light.{switches[light_index]._name.lower().replace(' ', '_')}"
    if state == "1":
        switches[light_index].state_on()
    elif state == "0":
        switches[light_index].state_off()
    
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
        switches.append(Switch(name, switch_id, pin , 0))

    for lock in lock_config:
        name = lock.get("name")
        switch_id = lock.get("id")
        pin = lock.get("pin")
        switches.append(Switch(name, switch_id, pin , 1))

    switches.append(Switch("Gryf Rst" , 0 , 0 , 2))

    async_add_entities(switches)

class Switch(SwitchEntity):
    def __init__(self, name, button_id, pin , tp):
        self._name = name
        self._is_on = False
        self._id = button_id  
        self._pin = pin
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
            return LOCK_ON_ICON if self._is_on else LOCK_OFF_ICON
        else: 
            return LIGHT_ON_ICON if self._is_on else LIGHT_OFF_ICON
    
    def state_on(self):
        self._is_on = True

    def state_off(self):
        self._is_on = False
    
    def turn_on(self, **kwargs):
        if self._type != 2:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "1"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            send_command(command)
        else:
            command = "AT+RST=0"
            send_command(command)
            self._is_on = True  

    def turn_off(self, **kwargs):
        if self._type != 2:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "2"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            send_command(command)
        else:
            command = "AT+RST=0"
            send_command(command)
            self._is_on = False

    async def async_toggle(self, **kwargs):
        if self._type != 2:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "3"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            send_command(command)
        else:
            command = "AT+RST=0"
            send_command(command)

    async def async_turn_on(self, **kwargs):
        if self._type != 2:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "1"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            send_command(command)
        else:
            command = "AT+RST=0"
            send_command(command)

    async def async_turn_off(self, **kwargs):
        if self._type != 2:
            states_list = ["0", "0", "0", "0", "0", "0"]
            states_list[self._pin - 1] = "2"
            command = f"AT+SetOut={self._id},{','.join(states_list)}"
            send_command(command)
        else:
            command = "AT+RST=0"
            send_command(command)

    @property
    def get_id(self):  
        return self._id

    @property
    def get_pin(self): 
        return self._pin
