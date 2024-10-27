import serial
from homeassistant.components.light import LightEntity , ColorMode
from homeassistant.core import HomeAssistant

from .outputs import Outputs
from .pwm import PWM

DOMAIN = "gryf_smart"

lights = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global lights

    lights_config = discovery_info or []

    for light in lights_config:
        name = light.get("name")
        light_id = light.get("id")
        pin = light.get("pin")
        lights.append(Outputs(hass, name, light_id, pin))

    name = "Gryf RST"
    light_id = 0
    pin = 0
    lights.append(Outputs(hass, name, light_id, pin))
    pwm = (PWM(hass , "pwm" , 4 , 1))

    lights.append(pwm)
    
    async_add_entities(lights)

    pwm = (PWM(hass , "pwm" , 1 , 1))

async def new_light_command(parsed_states):
    """Obsługa zmiany stanu sensora."""
    if lights:
            for i in range(len(lights) - 1):
                if str(lights[i].get_id) == parsed_states[0]:
                    pin = lights[i].get_pin
                    await change_light_state(i, parsed_states[pin])
                    

async def change_light_state(light_index, state):
    """Zmiana stanu światła na podstawie danych."""
    entity_id = f"light.{lights[light_index]._name.lower().replace(' ', '_')}"
    if state == "1":
        lights[light_index].set_on()
    elif state == "0":
        lights[light_index].set_off()
    
    lights[light_index].async_write_ha_state()

