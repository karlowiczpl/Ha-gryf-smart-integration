from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS

import logging

_LOGGER = logging.getLogger(__name__)

class Temperature(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, name, button_id, pin) -> None:
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._id = button_id
        self._pin = pin

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def get_id(self):
        return self._id
    
    @property
    def get_pin(self):
        return self._pin

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return DEVICE_CLASS_TEMPERATURE

    async def set_new_state(self, state) -> None:
        """Fetch new state data for the sensor."""
        self._state = state
        self.async_write_ha_state()