from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from .button import Button
from .serial import SerialSensor
from .temperature import Temperature
from .send import setupPlatform

buttons = []
temp = []

async def input_state_relaod(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0]:
                pin = buttons[i].get_pin
                await buttons[i].set_new_state(parsed_states[pin])

async def pl_state_reload(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0] and str(buttons[i].get_pin) == parsed_states[1]:
                await buttons[i].set_new_state(3)

async def ps_state_reload(parsed_states):
    if buttons:
        for i in range(len(buttons)):
            if str(buttons[i].get_id) == parsed_states[0] and str(buttons[i].get_pin) == parsed_states[1]:
                await buttons[i].set_new_state(2)

async def temp_reload(parsed_states):
    if temp:
        for i in range(len(temp)):
            if str(temp[i].get_id) == parsed_states[0] and str(temp[i].get_pin) == parsed_states[1]:
                result_str = f"{parsed_states[2]}.{parsed_states[3]}"

                await temp[i].set_new_state(result_str)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global buttons
    global temp

    buttons_config = discovery_info[0] or []
    port_config = discovery_info[1]
    temperature_config = discovery_info[2] or []

    for button in buttons_config:
        name = button.get("name")
        button_id = button.get("id")
        pin = button.get("pin")
        buttons.append(Button(hass, name, button_id, pin))

    for temperature in temperature_config:
        name = temperature.get("name")
        button_id = temperature.get("id")
        pin = temperature.get("pin")
        temp.append(Temperature(hass, name, button_id, pin))
    
    async_add_entities(buttons)
    async_add_entities(temp)

    port = port_config
    sensor = SerialSensor(port)
    async_add_entities([sensor], True)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, sensor.stop_serial_read)
    setupPlatform(async_add_entities)