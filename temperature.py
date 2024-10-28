from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorDeviceClass , SensorEntity
from homeassistant.const import UnitOfTemperature

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

        """set extra parametrs"""
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

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
        """Return sensor id"""
        return self._id
    
    @property
    def get_pin(self):
        """return sensor out pin"""
        return self._pin

    async def set_new_state(self, state) -> None:
        """Fetch new state data for the sensor."""

        _LOGGER.debug("New temperature state, id: %s , out pin: %s, state: %s" , self._id , self._pin , state)
        
        self._state = state
        self.async_write_ha_state()