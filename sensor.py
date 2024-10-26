from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EVENT_HOMEASSISTANT_STOP

from .button import Button
from .serial import SerialSensor

buttons = []

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

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global buttons

    buttons_config = discovery_info[0] or []
    port_config = discovery_info[1]

    for button in buttons_config:
        name = button.get("name")
        button_id = button.get("id")
        pin = button.get("pin")
        buttons.append(Button(hass, name, button_id, pin))
    
    async_add_entities(buttons)

    port = port_config
    sensor = SerialSensor(port)
    async_add_entities([sensor], True)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, sensor.stop_serial_read)
