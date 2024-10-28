from homeassistant.components.number import NumberEntity

from .send import send_command

covers = []

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global covers

    cover_config = discovery_info or []

    for cover in cover_config:
        name = cover.get("name")
        cover_id = cover.get("id")
        pin = cover.get("pin")
        time = cover.get("time")
        covers.append(Pwm(name, cover_id, pin))

    async_add_entities(covers)

class Pwm(NumberEntity):
    def __init__(self, name, pwm_id , pin):
        self._attr_name = name
        self._attr_min_value = 0
        self._attr_max_value = 100
        self._attr_value = 0
        self._pin = pin
        self._id = pwm_id

    async def async_set_native_value(self, value: float) -> None:
        """Ustawia wartość PWM."""
        
        command = f"AT+SetLED={self._id},{self._pin},{int(value)}"
        send_command(command)

        self._attr_value = value
        self.schedule_update_ha_state()

    @property
    def native_value(self) -> float:
        """Zwraca aktualną wartość PWM."""
        return self._attr_value
